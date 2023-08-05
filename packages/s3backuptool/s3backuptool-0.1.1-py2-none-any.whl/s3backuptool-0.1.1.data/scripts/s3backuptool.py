#!python
""" Backup local files and folders to S3 buckets
Author: Alexandru Ionica <alexandru@ionica.eu>
"""
import argparse
import logging
import ConfigParser
import os
import stat
import sys
import hashlib
import base64
import sqlite3
import re
import boto.s3.connection
import boto.s3.key
import math
import io
import struct
import datetime
import time
import shutil
import tempfile
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES


class Callback_progress(object):
    """ we use this class only to show progress of uploads """

    def __init__(self, filepath, args, part=0, total_parts=0):
        """
        :filepath  => full path and name of uploaded object
        :filesize  => size in bytes of uploaded object
        :chunksize => size of chunk when using multipart upload
        """
        self.filepath = filepath
        self.args = args
        # if multipart upload then prepare prompt showing which part is uploaded
        if total_parts > 0:
            self.part = part + 1
        self.total_parts = total_parts
        # when was the last bit sent
        self.last_send_time = time.time()
        self.bytes_sent_so_far = 0

    def __call__(self, complete, total):
        """ display progress report of file upload
        the parameters are mandatory to exist as this function is called by the set_contents_from_filename S3 library function and it needs to accept those

        complete => number of bytes that have been successfully transmitted to S3
        total    => size of the to be transmitted object
        """
        if not self.args.quiet and int(total) > 0:
            sys.stdout.write('\r')
            if self.total_parts > 0:
                mp_message = "(part %s of %s) " % (self.part, self.total_parts)
            else:
                mp_message = ''

            progress = (int(complete) * 100) / int(total)
            if time.time() - self.last_send_time > 0:
                upload_speed_per_sec = (complete - self.bytes_sent_so_far) / (time.time() - self.last_send_time)
            else:
                upload_speed_per_sec = 0
            if upload_speed_per_sec < 0:
                upload_speed_per_sec = 0
            self.last_send_time = time.time()
            self.bytes_sent_so_far = complete
            # print progress
            # safe filename = we remove ascii characters from output because it's such a huge headache to deal with them and this is just the upload progress.
            #   Actuall file names are always preserved
            # safe_filename = self.filepath.encode('ascii', 'ignore')
            safe_filename = self.filepath.encode('utf-8')
            sys.stdout.write(str(progress).rjust(3) + '%' + '   ' + sizeof_fmt(upload_speed_per_sec).rjust(9) + '/sec  ' + mp_message + safe_filename)
            sys.stdout.flush()
        else:
            return


# END OF Callback_progress class #

# noinspection PyBroadException
class BackedUpItem(object):
    """ Class which handles backing up and restoring items
    """

    def __init__(self, root, name, db_cursor, db_conn, file_type, s3_bucket_obj, s3_parent_folder_path, check_file_checksum, config_section, args,
                 encrypt=False, encrypt_password=None, restore_options=None, restore_metadata=None):
        """
        :root                  => parent folder (full path, example: /var/log/apache2)
        :name                  => name of file or directory
        :db_cursor             => db cursor object
        :file_type             => 'dir' or 'file'
        :s3_bucket_obj         => S3 bucket object to be used to perform operations like upload
        :s3_parent_folder_path => path within the S3 bucket which will be prepended to any uploads
        :check_file_checksum   => if to compute and compare the files MD5 checksum in order to decide if changes have happened
        :config_section        => configuration section where this item is processed from
        :args                  => argparse object containing parameters specified on the command line
        :encrypt               => if to perform file encryption
        :encrypt_password      => password to use for encrypting files (when performing file encryption)
        :restore_options       => dict containing options for performing a item restore.
        :restore_metadata      => dict containing metadata as obtained from S3 for an item which pends a restore.
        """
        self.root = root
        self.name = name
        self.filepath = os.path.join(self.root, self.name)
        self.db_cursor = db_cursor
        self.db_conn = db_conn
        self.file_type = file_type
        self.s3_bucket_obj = s3_bucket_obj
        self.s3_parent_folder_path = s3_parent_folder_path
        self.check_file_checksum = check_file_checksum
        self.encrypt = encrypt
        self.encrypt_password = encrypt_password
        self.file_md5_sum = ''
        self.file_md5_base64_digest = ''
        self.symlink_target = ''
        self.config_section = config_section
        self.args = args
        self.metadata = None

        if restore_options:
            self.overwrite = restore_options['overwrite']
            self.overwrite_permissions = restore_options['overwrite_permissions']
            self.restore_path = restore_options['restore_path']
            self.db_table_restore_files = restore_options['db_table_restore_files']
            if 'tmpdir_path' in restore_options:
                self.tmpdir_path = restore_options['tmpdir_path']
            else:
                self.tmpdir_path = None

        if restore_metadata:
            self.encrypt = restore_metadata['encrypted']
            self.uid = restore_metadata['uid']
            self.gid = restore_metadata['gid']
            self.mtime = restore_metadata['mtime']
            self.ctime = restore_metadata['ctime']
            self.perm_mode = restore_metadata['perm_mode']
            if self.file_type == 'symlink':
                self.symlink_target = restore_metadata['symlink_target']
            self.size = restore_metadata['size']
            if 'md5' in restore_metadata:
                self.remote_md5 = restore_metadata['md5']
            else:
                self.remote_md5 = None
            # absolute path of the object to restore = self.restore_path + self.filepath
            self.restore_fullpath = self.restore_path.rstrip('/') + unicode(os.sep, 'utf-8') + self.filepath.lstrip('/')
            # store the effective UID of the restore process . We use this to decide if we need to change file permissions
            self.restore_euid = os.geteuid()

    def calculate_md5checksum(self, filepath=None):
        """ calculates the md5 checksum and diges for a given file and saves it in the self.file_md5_sum/self.file_md5_base64_digest variables
            filepath => this variable makes sense to be used only when performing restores as then the self.filepath variable refers to the original path
                        the file had while the restore path may be different
        """

        if filepath is None:
            filepath = self.filepath
        # read blocksize bytes at a time
        blocksize = 65536
        hasher = hashlib.md5()
        with open(filepath.encode('utf-8'), 'rb') as afile:
            buf = afile.read(blocksize)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(blocksize)
        # afile.close()
        self.file_md5_sum = hasher.hexdigest()
        self.file_md5_base64_digest = base64.encodestring(hasher.digest())
        if self.file_md5_base64_digest[-1] == '\n':
            self.file_md5_base64_digest = self.file_md5_base64_digest[0:-1]

    def mark_item_restore_as_failed(self):
        """ marks item as failed to restore by updating the filed 'failed' in the restore_files_$timestamp table
        """
        try:
            self.db_cursor.execute("UPDATE %s SET failed='1' where filepath=?" % self.db_table_restore_files, (self.filepath,))
            self.db_conn.commit()
        except:
            logging.error("Failed to update db record for item %s which failed restore to %s", self.filepath, self.restore_fullpath)

    def mark_item_restore_as_successful(self):
        """ marks item as successfult restored by updating the filed 'restored' in the restore_files_$timestamp table
        """
        try:
            self.db_cursor.execute("UPDATE %s SET restored='1' where filepath=?" % self.db_table_restore_files, (self.filepath,))
            self.db_conn.commit()
        except:
            logging.error("Failed to update db record for item %s which was successfully restored to %s", self.filepath, self.restore_fullpath)

    def ensure_restore_path_exists_and_is_usable(self):
        """ ensures the full path to where the dir/file/symlink is saved exists and is usable. If the parent folder doesn't allow writes or execute then
            it adjusts it's permissions. Returns False if it encounters problems but overall the restore can continue (at least with other items to be restored)
        """
        parent_dir = self.restore_fullpath.rsplit(unicode(os.sep, 'utf-8'), 1)[0]
        if not os.path.isdir(parent_dir):
            if os.path.isfile(parent_dir):
                logging.error("%s is a file instead of a dir, some other process removed the dir and created a file instead. Aborting restore for %s",
                              parent_dir, self.restore_fullpath)
                return False
            else:
                if len(parent_dir) >= len(self.restore_path):
                    logging.info("parent folder %s doesn't exist. Proceeding to create it", parent_dir)
                    self.db_cursor.execute('SELECT perm_mode FROM %s WHERE filepath=?' % self.db_table_restore_files, (parent_dir,))
                    db_query_result_rows = self.db_cursor.fetchall()
                    try:
                        if len(db_query_result_rows) > 0:
                            perm_mode = db_query_result_rows[0]['perm_mode']
                            os.makedirs(parent_dir.encode('utf-8'), perm_mode)
                        else:
                            os.makedirs(parent_dir.encode('utf-8'))
                    except os.error:
                        logging.error("encountered error while creating path %s .Aborting restore for %s", parent_dir, self.restore_fullpath)
                        return False
                else:
                    logging.error("attempt to create folder %s outside of the restore path %s .Aborting restore for %s", parent_dir, self.restore_path,
                                  self.restore_fullpath)
                    return False
        # if we're running as root then we don't need to check or adjust write/execute permissions
        if self.restore_euid != 0:
            if not os.access(parent_dir, os.W_OK):
                if self.overwrite or self.overwrite_permissions:
                    logging.info("The path: %s is not writable. Adjusting permissions to add write rights", parent_dir)
                    if not self.adjust_file_permissions(parent_dir, perm_add='uw'):
                        logging.error("Encountered error while adding write permissions for %s. Aborting restore for %s", parent_dir, self.restore_fullpath)
                        return False
                else:
                    logging.error(
                        "%s is missing write permissions and you have chose (via the restore options) not to overwrite/adjust permissions. "
                        "Aborting restore for %s", parent_dir, self.restore_fullpath)
                    return False
            if not os.access(parent_dir, os.X_OK):
                if self.overwrite or self.overwrite_permissions:
                    logging.info(
                        "The path: %s can not be changed into (meaning it's a folder/directory on which you miss the execute permission). "
                        "Adjusting permissions to add execute rights", parent_dir)
                    if not self.adjust_file_permissions(parent_dir, perm_add='ux'):
                        logging.error("Encountered error while adding execute permissions for %s. Aborting restore for %s", parent_dir, self.restore_fullpath)
                        return False
                else:
                    logging.error(
                        "%s is missing execute(change dir) permissions and you have chose (via the restore options) not to overwrite/adjust permissions. "
                        "Aborting restore for %s", parent_dir, self.restore_fullpath)
                    return False
        # if we got here then everything worked as expected
        return True

    @staticmethod
    def adjust_file_permissions(filepath, perm_add=None, perm_absolute=None):
        """ adjust file/directory permissions. Returns True on success and False otherwise
        :filepath      => full path of the item to adjust
        :perm_add      => one of ['ur', 'uw', 'ux', 'gr', 'gw', 'gx', 'or', 'ow', 'ox'] . Adds the respective permission (read/write/execute) to the
                            user/group/others part of the permissions
        :perm_absolute => absolute permissions as reported by os.stat  to change the file/dir to
        """
        # allowed values for "perm_add" parameter
        perm_add_options = {'ur': stat.S_IRUSR,
                            'uw': stat.S_IWUSR,
                            'ux': stat.S_IXUSR,
                            'gr': stat.S_IRGRP,
                            'gw': stat.S_IWGRP,
                            'gx': stat.S_IXGRP,
                            'or': stat.S_IROTH,
                            'ow': stat.S_IWOTH,
                            'ox': stat.S_IXOTH, }
        if (perm_add is None and perm_absolute is None) or (perm_add and perm_absolute):
            logging.error(
                "You must call BackedUpItem.adjust_file_permissions() with either perm_add or perm_absolute parameters mentioned to a value different than "
                "None. Also you must not specify both parameters with values different to None. Exiting")
            sys.exit(1)
        if perm_add and perm_add not in perm_add_options.keys():
            logging.error(
                "You have called BackedUpItem.adjust_file_permissions() with an invalid value for parameter \"perm_add\". Allowed values are %s. Exiting",
                perm_add_options.keys())
            sys.exit(1)

        if perm_add:
            try:
                current_permissions = os.stat(filepath.encode('utf-8'))
            except os.error:
                logging.error("Error while reading current permissions for %s . Skipping permission adjustment for it", filepath)
                return False
            try:
                os.chmod(filepath.encode('utf-8'), current_permissions.st_mode | perm_add_options[perm_add])
            except os.error:
                logging.error("Error while adjusting mode permissions on %s", filepath)
                return False

        if perm_absolute:
            try:
                # perm_absolute is passed as a unicode string, so we need to convert it to octal
                os.chmod(filepath.encode('utf-8'), int(perm_absolute, 8))
            except os.error:
                logging.error("Error while adjusting mode permissions on %s", filepath)
                return False

        # if we reached this point then all went according to plan
        return True

    @staticmethod
    def adjust_file_ownership(filepath, uid=None, gid=None):
        """ adjust file/directory user and group owners. Returns True on success and False otherwise
        :filepath      => full path of the item to adjust
        :uid           => numeric user id to adjust to. If None then keep current user id
        :gid           => numerig group id to adjust to. If None then keep current user id
        """
        if uid is None and gid is None:
            logging.error("You must call BackedUpItem.adjust_file_ownership() with either uid= or gid= having a value different than None. Exiting")
            sys.exit(1)
        if uid is None:
            uid = -1
        else:
            uid = int(uid)
        if gid is None:
            gid = -1
        else:
            gid = int(gid)

        try:
            os.chown(filepath, uid, gid)
        except os.error:
            logging.error("Error while adjusting ownership permissons on %s to uid: %s and gid: %s .Values of -1 means leave unchanged", filepath, uid, gid)
            return False

        # if we reached this point then all went according to plan
        return True

    def examine_file_and_backup(self):
        """ examines the file and based on type of file decide action
        """

        insert_db_record = False
        update_db_record = False
        upload_file = False
        update_s3_metadata = False
        try:
            fileinfo = os.lstat(self.filepath.encode('utf-8'))
        except:
            logging.warning("%s could not read file properties. Skipping file", self.filepath)
            return
        if os.path.islink(self.filepath.encode('utf-8')):
            self.file_type = 'symlink'
            self.symlink_target = os.readlink(self.filepath.encode('utf-8'))
        elif not stat.S_ISREG(fileinfo.st_mode) and self.file_type != 'dir':
            logging.warning("%s this is not a regular file, a symlink or a folder so we will skip backing it up", self.filepath)
            return
        if self.file_type == 'file' and (not os.path.isfile(self.filepath.encode('utf-8')) or not os.access(self.filepath.encode('utf-8'), os.R_OK)):
            logging.warning("%s does no longer exist or can not be read. Skipping file", self.filepath)
            return
        # calculate MD5 sum only if the file is not a Symbolic Link
        if self.file_type == 'file' and self.check_file_checksum:
            self.calculate_md5checksum()
        # create dict with metadata for S3
        # we convert (only in the metadata) the filename to an 'ascii' string because otherwise we get exceptions from AWS S3 because ascii is
        #   mandatory for HTTP headers
        #   https://code.google.com/p/boto/issues/detail?id=300
        self.metadata = {'filepath': self.filepath,
                         'uid': fileinfo.st_uid,
                         'gid': fileinfo.st_gid,
                         'perm_mode': oct(fileinfo.st_mode),
                         'filetype': self.file_type,
                         'size': int(fileinfo.st_size),
                         'mtime': int(float(fileinfo.st_mtime)),
                         'ctime': int(float(fileinfo.st_ctime)),
                         'encrypted': self.encrypt,
                         }
        # if filename contains unicode chars then convert them to unicode escaped code points
        if unicode(self.filepath.encode('ascii', 'ignore'), 'utf-8') != self.filepath:
            self.metadata['filepath'] = self.filepath.encode('unicode_escape')
            self.metadata['filename_encoded'] = True
        else:
            self.metadata['filename_encoded'] = False

        if self.file_type == 'symlink':
            self.metadata['symlink_target'] = self.symlink_target
        db_tuple_entry = (self.filepath, fileinfo.st_uid, fileinfo.st_gid, oct(fileinfo.st_mode), self.file_md5_sum, self.file_type, int(fileinfo.st_size),
                          self.symlink_target, int(float(fileinfo.st_mtime)), int(float(fileinfo.st_ctime)), self.encrypt)
        self.db_cursor.execute('SELECT * FROM files WHERE filepath=?', (self.filepath,))
        # if the file isn't mentioned in the database then this is a new file
        file_db_query_result = self.db_cursor.fetchone()
        if not file_db_query_result:
            insert_db_record = True
            upload_file = True
            logging.info("%s backing up new %s", self.filepath, self.file_type)
        # file exists already in the database so let's see if it has changed in any way which needs a backup
        else:
            dbrecd_uid = file_db_query_result['uid']
            dbrecd_gid = file_db_query_result['gid']
            dbrecd_perm_mode = file_db_query_result['perm_mode']
            dbrecd_md5 = file_db_query_result['md5']
            dbrecd_filetype = file_db_query_result['filetype']
            dbrecd_size = int(file_db_query_result['size'])
            dbrecd_symlink_target = file_db_query_result['symlink_target']
            dbrecd_mtime = file_db_query_result['mtime']
            if self.file_type == 'file':
                # if we compute checksums and MD5 changed then upload
                if self.check_file_checksum and self.file_md5_sum != dbrecd_md5:
                    logging.info("%s needs uploading because md5sum has changed", self.filepath)
                    upload_file = True
                    update_db_record = True
                # if file mtime or size has changed then upload
                elif int(float(fileinfo.st_mtime)) != int(float(dbrecd_mtime)):
                    logging.info("%s needs uploading because mtime has changed", self.filepath)
                    upload_file = True
                    update_db_record = True
                elif int(fileinfo.st_size) != dbrecd_size:
                    logging.info("%s needs uploading because size has changed", self.filepath)
                    upload_file = True
                    update_db_record = True
                # if file type differs from what is recorded in the DB then upload and in case in the DB a "dir" type was stored then we also need to cleanup
                if self.file_type != dbrecd_filetype:
                    if dbrecd_filetype == 'symlink':
                        logging.info("%s 's type has changed from %s to %s. Uploading", self.filepath, self.file_type, dbrecd_filetype)
                        upload_file = True
                        update_db_record = True
                    elif dbrecd_filetype == 'dir':
                        logging.info("%s has changed it's type from: %s to: %s . Deleting remote content first and then updating local and remote metadata",
                                     self.filepath, dbrecd_filetype, self.file_type)
                        # remove remote dir and any contents in the dir
                        s3_multi_delete(self.s3_bucket_obj, self.s3_parent_folder_path, file_list=[self.s3_parent_folder_path + self.filepath + u'/'],
                                        remove_from_db=False, db_cursor=self.db_cursor, db_conn=self.db_conn, recurse=True)
                        update_db_record = True
                        update_s3_metadata = True
                    else:
                        logging.error("%s 's DB entry mentions it is of type %s while the allowed types are: file, symlink, dir. Is the DB inconsistent?",
                                      self.filepath, dbrecd_filetype)
                # file isn't changed but permissions have so let's update the local DB record and S3 file metadata(on AWS)
                elif str(fileinfo.st_uid) != dbrecd_uid or str(fileinfo.st_gid) != dbrecd_gid or str(oct(fileinfo.st_mode)) != dbrecd_perm_mode:
                    logging.info("%s had is's permissions change. Updating local and remote metadata", self.filepath)
                    update_db_record = True
                    update_s3_metadata = True
                # nothing has changed, move on
                else:
                    pass
            elif self.file_type == 'symlink':
                if dbrecd_filetype == 'symlink':
                    # file isn't changed but permissions/owner/target has so let's update the local DB record and S3 file metadata(on AWS)
                    if str(fileinfo.st_uid) != dbrecd_uid or str(fileinfo.st_gid) != dbrecd_gid or str(
                            oct(fileinfo.st_mode)) != dbrecd_perm_mode or self.symlink_target != dbrecd_symlink_target:
                        logging.info("%s is a symlink and has changed it's permissions or it's target. Updating local and remote metadata", self.filepath)
                        update_db_record = True
                        update_s3_metadata = True
                # if file type locally is a symlink but in the DB is marked as "file" then update the metadata entry in the local
                #   DB and S3 file metadata(on AWS)
                elif dbrecd_filetype == 'file':
                    logging.info("%s has changed it's type from: %s to: %s . Updating local and remote metadata", self.filepath, dbrecd_filetype,
                                 self.file_type)
                    update_db_record = True
                    update_s3_metadata = True
                # if file type locally is a symlink but in the DB is marked as "dir" (directory) then we need to  remove contents of the
                #   remote directory and then update the metadata entry in the local DB and S3 file metadata(on AWS)
                elif dbrecd_filetype == 'dir':
                    logging.info("%s has changed it's type from: %s to: %s . Deleting remote content first and then updating local and remote metadata",
                                 self.filepath, dbrecd_filetype, self.file_type)
                    # remove remote dir and any contents from the dir
                    s3_multi_delete(self.s3_bucket_obj, self.s3_parent_folder_path, file_list=[self.s3_parent_folder_path + self.filepath + u'/'],
                                    remove_from_db=False, recurse=True)
                    update_db_record = True
                    update_s3_metadata = True
                else:
                    logging.error("%s 's DB entry mentions the file is of type %s while the allowed types are: file, symlink, dir. Is the DB inconsistent?",
                                  self.filepath, dbrecd_filetype)
            elif self.file_type == 'dir':
                # if DB record matches then:
                if dbrecd_filetype == 'dir':
                    # test dir isn't changed but permissions have and if yes let's update the local DB record and S3 file metadata(on AWS)
                    if str(fileinfo.st_uid) != dbrecd_uid or str(fileinfo.st_gid) != dbrecd_gid or str(oct(fileinfo.st_mode)) != dbrecd_perm_mode:
                        logging.info("%s hasn't changed but it's permissions have. Updating local and remote metadata", self.filepath)
                        update_db_record = True
                        update_s3_metadata = True
                    # directory isn't changed, metadata is ok, nothing to do
                    else:
                        pass
                elif dbrecd_filetype == 'file' or dbrecd_filetype == 'symlink':
                    logging.info("%s has changed it's type from: %s to: %s . Updating local and remote metadata", self.filepath, dbrecd_filetype,
                                 self.file_type)
                    # first to delete the remote S3 "file" or "symlink" before putting in a "directory" on S3
                    s3_multi_delete(self.s3_bucket_obj, self.s3_parent_folder_path, file_list=[self.s3_parent_folder_path + self.filepath.rstrip('/')])
                    update_db_record = True
                    update_s3_metadata = True
                else:
                    logging.error("%s 's DB entry mentions it is of type %s while the allowed types are: file, symlink, dir. Is the DB inconsistent?",
                                  self.filepath, dbrecd_filetype)
        # depending on what we detected as changed, act
        if upload_file:
            # if we upload a file and we want to store checksums for later comparison then we need to calculate this and store it as Metadata (not ETag
            #   because that is not usable for multipart uploads)
            if self.file_type == 'file' and self.check_file_checksum:
                self.metadata['md5'] = self.file_md5_sum
            # if we enabled encryption then let's generate a key , salt and IV(initialization vector) to use in order to create an encryptor object. Key and
            #   salt MUST be 32 bytes each due to AES256
            if self.encrypt and self.file_type == 'file':
                key, salt = gen_key_and_salt(password=self.encrypt_password)
                # Initialization Vector needs to be 16 bytes when using AES
                iv = os.urandom(16)
                encryptor = AES.new(key, AES.MODE_CBC, iv)
            else:
                encryptor = None
                salt = None
                iv = None
            upload_result = self.upload_object_to_s3(encryptor=encryptor, salt=salt, iv=iv)
            # if upload was not successful, skip inserting in the db or updating the db
            if not upload_result:
                insert_db_record = False
                update_db_record = False
                update_s3_metadata = False
        # upload_file takes care of updating S3 metadata too so we want to run update_s3_metadata only if a file upload is not needed
        if update_s3_metadata and not upload_file:
            s3_key_obj = prepare_s3_key_obj(self.s3_bucket_obj, self.s3_parent_folder_path, self.filepath, self.file_type)
            update_metadata_result = update_s3_key_metadata(s3_key_obj, self.metadata, self.filepath, force_update=True)
            # if metadata update was not successful, skip inserting in the db or updating the db
            if not update_metadata_result:
                insert_db_record = False
                update_db_record = False
        # DB record insertion/update should go after the file upload in order to be sure the upload was successful, otherwise we should skip those steps
        if insert_db_record:
            try:
                self.db_cursor.execute('INSERT INTO files VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', db_tuple_entry)
            except sqlite3.IntegrityError:
                logging.error(
                    '%s already is mentioned in the database belonging to configuration section [%s]. Check that you don\'t have two instances of the '
                    'backup tool running. Skipping to next file', self.filepath, self.config_section)
                # skip to next file without uploading this one as the situation is unclear. As we can't use "continue" here because we are in a function and the
                # for loop is outside the function the we just set to False the variables which would trigger the update
                update_db_record = False
            self.db_conn.commit()
        if update_db_record:
            try:
                self.db_cursor.execute(
                    'UPDATE files SET filepath=?, uid=?, gid=?, perm_mode=?, md5=?, filetype=?, size=?, symlink_target=?, mtime=?, ctime=?, encrypted=? '
                    'where filepath=?', db_tuple_entry + (self.filepath,))
                self.db_conn.commit()
            except sqlite3.Error:
                logging.error("unexpected sql database error while updating record for %s", self.filepath)

    def examine_file_and_restore(self):
        """ restore from backup a file/dir/symlink 
        """
        logging.info("restoring %s: %s", self.file_type, self.restore_fullpath)
        # ensure parent folder permissions are sufficient so we can restore contained files/folders
        if not self.ensure_restore_path_exists_and_is_usable():
            self.mark_item_restore_as_failed()
            return False
        # check if we already have an existing item at the same path
        if os.path.lexists(self.restore_fullpath.encode('utf-8')):
            logging.info("Something already exists on disk having the same path %s as item to restore", self.restore_fullpath)
            existing_file_info = os.lstat(self.restore_fullpath.encode('utf-8'))
            if self.file_type == 'dir':
                # check if both the restored item and the exiting one on disk are of type DIR so we just need to at most adjust permissions
                if os.path.isdir(self.restore_fullpath.encode('utf-8')):
                    # if mode permissions don't match then adjust them
                    if oct(existing_file_info.st_mode).decode('utf-8') != self.perm_mode:
                        # if overwrite allowed then adjust permissions
                        if self.overwrite or self.overwrite_permissions:
                            logging.info('adjusting directory mode permissions for %s', self.restore_fullpath)
                            if not self.adjust_file_permissions(self.restore_fullpath, perm_absolute=self.perm_mode):
                                logging.error("Encountered error while restoring mode permissions for directory %s. Marking restore as failed for this item",
                                              self.restore_fullpath)
                                self.mark_item_restore_as_failed()
                                return False
                        # we're not allowed to overwrite permissions, so marking item restore as failed
                        else:
                            logging.error(
                                "Can not restore mode permissions for directory %s due to the fact that the user selected not to overwrite items or not to "
                                "overwrite permissions", self.restore_fullpath)
                            self.mark_item_restore_as_failed()
                            return False
                    # if ownership permissions don't match then adjust them
                    if int(self.uid) != existing_file_info.st_uid or int(self.gid) != existing_file_info.st_gid:
                        # if overwrite allowed then adjust permissions
                        if self.overwrite or self.overwrite_permissions:
                            logging.info('adjusting directory ownership rights for %s', self.restore_fullpath)
                            if not self.adjust_file_ownership(self.restore_fullpath, self.uid, self.gid):
                                logging.error("Encountered error while restoring ownership rights for directory %s. Marking restore as failed for this item",
                                              self.restore_fullpath)
                                self.mark_item_restore_as_failed()
                                return False
                        # we're not allowed to overwrite permissions, so marking item restore as failed
                        else:
                            logging.error(
                                "Can not restore ownership rights for directory %s due to the fact that the user selected not to overwrite items or not to "
                                "overwrite permissions", self.restore_fullpath)
                            self.mark_item_restore_as_failed()
                            return False
                    # if we made it here it means the folder on this is identical to the one to be restored when regarding permissions mode and owner/group
                    # print nice percent bar and file path to inform of the succesful restore/comparison
                    print '100%                  ' + self.restore_fullpath.encode('utf-8')
                # exiting item on disk is not a DIR while we want to restore a dir. Proceed to remove whatever exists and create a new dir
                else:
                    if self.overwrite:
                        logging.info("removing already existing item %s which is not a directory, creating directory and setting ownership and permissions",
                                     self.restore_fullpath)
                        try:
                            os.remove(self.restore_fullpath.encode('utf-8'))
                        except os.error:
                            logging.error(
                                "%s already exists but it's a different type then directory. Attempt to delete it failed. Marking restore as failed"
                                " for this item", self.restore_fullpath)
                            self.mark_item_restore_as_failed()
                            return False
                        # make directory
                        logging.info("Creating folder %s", self.restore_fullpath)
                        try:
                            # make dir, set mode permissions afterwards
                            os.mkdir(self.restore_fullpath.encode('utf-8'))
                        except os.error:
                            logging.error("Error while creating folder %s . Marking restore as failed for this item", self.restore_fullpath)
                            self.mark_item_restore_as_failed()
                            return False
                        # set ownership rights for newly created folder
                        if not self.adjust_file_ownership(self.restore_fullpath, self.uid, self.gid):
                            logging.error("Encountered error while setting ownership rights for directory %s. Marking restore as failed for this item",
                                          self.restore_fullpath)
                            self.mark_item_restore_as_failed()
                            return False
                        # set mode permissions for newly created folder
                        if not self.adjust_file_permissions(self.restore_fullpath, perm_absolute=self.perm_mode):
                            logging.error("Encountered error while setting mode permissions for directory %s. Marking restore as failed for this item",
                                          self.restore_fullpath)
                            self.mark_item_restore_as_failed()
                            return False
                    else:
                        logging.error(
                            "While restoring %s can't remove exiting non dir item at same path due to the fact that the user selected not to overwrite items",
                            self.restore_fullpath)
                        self.mark_item_restore_as_failed()
                        return False
                # if we made it this far then the restore was successful for this folder - we either found the folder existing and adjusted it's permissions
                # or we removed whatever existed and created the folder
                self.mark_item_restore_as_successful()
                # print nice percent bar and file path to inform of the succesful restore/comparison
                print '100%                  ' + self.restore_fullpath.encode('utf-8')
                logging.info("Successfuly restored directory %s", self.restore_fullpath)
                return True
            # we're restoring a file, and an item with the same path already exists on disk so lets see what we can do
            elif self.file_type == 'file':
                # check if both the restored item and the exiting one on disk are of type FILE. If so then we need to check if the content is the same
                #  and if overwrite was selected then check we can actually overwrite the file
                if os.path.isfile(self.restore_fullpath.encode('utf-8')):
                    # check if we have a symlink on disk (as os.path.isfile returns true for symlinks too)
                    if os.path.islink(self.restore_fullpath.encode('utf-8')):
                        if not self.overwrite:
                            # overwriting is not selected by the user so we'll have to mark the restore as failed
                            logging.error(
                                "Can not restore file %s as on disk we have a symlink with the same path and the user selected not to overwrite items",
                                self.restore_fullpath)
                            self.mark_item_restore_as_failed()
                            return False
                        # let's remove the symlink
                        else:
                            try:
                                os.remove(self.restore_fullpath.encode('utf-8'))
                            except OSError:
                                logging.error("Could not remove already existing on disk %s which is a symlink but we're restoring a regular file. "
                                              "Marking restore as failed for this item", self.restore_fullpath)
                                self.mark_item_restore_as_failed()
                                return False
                    # so on disk we have also a file with the same path
                    else:
                        # if we're not allowed to overwrite then we'll mark the item as failed to restore
                        if not self.overwrite:
                            logging.error(
                                "Can not restore file %s as on disk we have a file with the same path and the user selected not to overwrite items",
                                self.restore_fullpath)
                            self.mark_item_restore_as_failed()
                            return False
                        # we're allowed to overwrite files on disk
                        else:
                            if self.restore_file_from_s3():
                                self.mark_item_restore_as_successful()
                                logging.info("Successfuly restored file %s", self.restore_fullpath)
                                return True
                            else:
                                logging.error("Failed to restore file %s when downloading from S3. Marking restore as failed for this item.",
                                              self.restore_fullpath)
                                self.mark_item_restore_as_failed()
                                return False
                # it means we're restoring a file but on disk we have a directory (or something else then a symlink or regular file)
                elif os.path.isdir(self.restore_fullpath.encode('utf-8')):
                    # if we're not allowed to overwrite then we'll mark the item as failed to restore
                    if not self.overwrite:
                        logging.error(
                            "Can not restore file %s as on disk we have a directory with the same path and the user selected not to overwrite items",
                            self.restore_fullpath)
                        self.mark_item_restore_as_failed()
                        return False
                    # we're allowed to overwrite whatever is on disk so we're going to remove that thing
                    else:
                        try:
                            shutil.rmtree(self.restore_fullpath.encode('utf-8'))
                        except OSError:
                            logging.error("Could not remove already existing on disk %s which is a directory but we're restoring a regular file. "
                                          "Marking restore as failed for this item", self.restore_fullpath)
                            self.mark_item_restore_as_failed()
                            return False
                        else:
                            # restore file
                            if self.restore_file_from_s3():
                                self.mark_item_restore_as_successful()
                                logging.info("Successfuly restored file %s", self.restore_fullpath)
                                return True
                            else:
                                logging.error("Failed to restore file %s when downloading from S3. Marking restore as failed for this item.",
                                              self.restore_fullpath)
                                self.mark_item_restore_as_failed()
                                return False
                # whatever exists on this at the same path is not a file, symlink or dir. Let's attempt to remove it (if overwrite)
                else:
                    if self.overwrite:
                        try:
                            os.remove(self.restore_fullpath.encode('utf-8'))
                        except OSError:
                            logging.error("Could not remove already existing on disk %s which is not a symlink/regular-file/dir but we're restoring a regular"
                                          " file. Marking restore as failed for this item", self.restore_fullpath)
                            self.mark_item_restore_as_failed()
                            return False
                        else:
                            if self.restore_file_from_s3():
                                self.mark_item_restore_as_successful()
                                logging.info("Successfuly restored file %s", self.restore_fullpath)
                                return True
                            else:
                                logging.error("Failed to restore file %s when downloading from S3. Marking restore as failed for this item.",
                                              self.restore_fullpath)
                                self.mark_item_restore_as_failed()
                                return False
                    else:
                        logging.error("Could not remove already existing on disk %s which is not a symlink/regular-file/dir as the user selected not to "
                                      "overwrite items. Marking restore as failed for this item", self.restore_fullpath)
                        self.mark_item_restore_as_failed()
                        return False

            # we're restoring a symlink, and an item with the same path already exists on disk so lets see what we can do
            elif self.file_type == 'symlink':
                if self.overwrite:
                    if os.path.isfile(self.restore_fullpath.encode('utf-8')):
                        try:
                            os.remove(self.restore_fullpath.encode('utf-8'))
                        except OSError:
                            logging.error("Could not remove already existing on disk %s which is a file or symlink and we're restoring a symlink. "
                                          "Marking restore as failed for this item", self.restore_fullpath)
                            self.mark_item_restore_as_failed()
                            return False
                    else:
                        try:
                            shutil.rmtree(self.restore_fullpath.encode('utf-8'))
                        except OSError:
                            logging.error("Could not remove already existing on disk %s which is a directory but we're restoring a symlin file. "
                                          "Marking restore as failed for this item", self.restore_fullpath)
                            self.mark_item_restore_as_failed()
                            return False
                    # if we got here then we managed to remove whatever was at the same path so let's create the symlink
                    if self.restore_symlink_from_metadata():
                        logging.info("Successfuly restored symlink %s", self.restore_fullpath)
                        self.mark_item_restore_as_successful()
                        return True
                    else:
                        logging.error("Could not recreate %s symlink. Marking restore as failed for this item", self.restore_fullpath)
                        self.mark_item_restore_as_failed()
                        return False
                else:
                    logging.error("Could not remove already existing on disk %s which is not a symlink as the user selected not to "
                                  "overwrite items. Marking restore as failed for this item", self.restore_fullpath)
                    self.mark_item_restore_as_failed()
                    return False
            else:
                logging.error("Item %s is reported as of type %s which isn't either of dir/file/symlink. Marking restore as failed for this item",
                              self.restore_fullpath, self.file_type)
                self.mark_item_restore_as_failed()
                return False
        # an item with the same path and name doesn't already exist on disk, proceeding to restore it
        else:
            if self.file_type == 'dir':
                # make directory
                logging.info("Creating folder %s", self.restore_fullpath)
                try:
                    # make dir, set mode permissions afterwards
                    os.mkdir(self.restore_fullpath.encode('utf-8'))
                except os.error:
                    logging.error("Error while creating folder %s . Marking restore as failed for this item", self.restore_fullpath)
                    self.mark_item_restore_as_failed()
                    return False
                # set ownership rights for newly created folder
                if not self.adjust_file_ownership(self.restore_fullpath, self.uid, self.gid):
                    logging.error("Encountered error while setting ownership rights for directory %s . Marking restore as failed for this item",
                                  self.restore_fullpath)
                    self.mark_item_restore_as_failed()
                    return False
                # set mode permissions for newly created folder
                if not self.adjust_file_permissions(self.restore_fullpath, perm_absolute=self.perm_mode):
                    logging.error("Encountered error while setting mode permissions for directory %s . Marking restore as failed for this item",
                                  self.restore_fullpath)
                    self.mark_item_restore_as_failed()
                    return False
                # if we made it this far then the restore was successful for this folder
                self.mark_item_restore_as_successful()
                # print nice percent bar and file path to inform of the succesful restore/comparison
                print '100%                  ' + self.restore_fullpath.encode('utf-8')
                logging.info("Successfuly restored directory %s", self.restore_fullpath)
                return True

            elif self.file_type == 'file':
                if self.restore_file_from_s3():
                    self.mark_item_restore_as_successful()
                    logging.info("Successfuly restored file %s", self.restore_fullpath)
                    return True
                else:
                    logging.error("Failed to restore file %s when downloading from S3. Marking restore as failed for this item.", self.restore_fullpath)
                    self.mark_item_restore_as_failed()
                    return False
            elif self.file_type == 'symlink':
                # let's restore the symlink
                if self.restore_symlink_from_metadata():
                    logging.info("Successfuly restored symlink %s", self.restore_fullpath)
                    self.mark_item_restore_as_successful()
                    return True
                else:
                    logging.error("Could not recreate %s symlink. Marking restore as failed for this item", self.restore_fullpath)
                    self.mark_item_restore_as_failed()
                    return False
            else:
                logging.error("Item %s is reported as of type %s which isn't either of dir/file/symlink. Marking restore as failed for this item",
                              self.restore_fullpath, self.file_type)
                self.mark_item_restore_as_failed()
                return False
        # if we made it this far then something is wrong in the code as we should have succeeded or failed before reaching here.
        # Marking as a failure for this item
        logging.error(
            "No action was taken or incomplete process was followed for restore of %s due to some kind of workflow issue in code. Marking restore as failed"
            " for this item",
            self.restore_fullpath)
        self.mark_item_restore_as_failed()
        return False

    # noinspection PyUnreachableCode
    def ensure_restored_folder_permissions(self):

        """ ensure restored folder permissions are correctly set (during file restore it's possible we may adjust them in order to be able to restore files)
        """
        no_error_encountered = True
        parent_folder_permissions_adjusted = False
        if self.file_type != 'dir':
            logging.info("we're supposed to ensure the permissions of folder %s are correct but ensure_restored_folder_permissions() was called for an item "
                         "which is not a directory but a %s", self.restore_fullpath, self.file_type)
            return False
        logging.info("checking folder permissions for %s", self.restore_fullpath)
        existing_file_info = os.lstat(self.restore_fullpath.encode('utf-8'))
        # if mode permissions don't match then adjust them
        if oct(existing_file_info.st_mode).decode('utf-8') != self.perm_mode:
            # ensure parent folder permissions are sufficient so we can adjust permissions for contained folders
            if not self.ensure_restore_path_exists_and_is_usable():
                logging.error("could not adjust parent folder permissions in order to adjust permissions for already restored directory %s .",
                              self.restore_fullpath)
                no_error_encountered = False
            else:
                parent_folder_permissions_adjusted = True
            # even if the above failed we're try to restore permissions
            logging.info('adjusting directory mode permissions for %s', self.restore_fullpath)
            if not self.adjust_file_ownership(self.restore_fullpath, self.uid, self.gid):
                logging.error("could not adjust ownership permissions for already restored directory %s .", self.restore_fullpath)
                no_error_encountered = False
        # if ownership permissions don't match then adjust them
        if int(self.uid) != existing_file_info.st_uid or int(self.gid) != existing_file_info.st_gid:
            if not parent_folder_permissions_adjusted:
                # ensure parent folder permissions are sufficient so we can adjust permissions for contained folders
                if not self.ensure_restore_path_exists_and_is_usable():
                    logging.error("could not adjust parent folder permissions in order to adjust permissions for already restored directory %s .",
                                  self.restore_fullpath)
                    no_error_encountered = False
            logging.info('adjusting directory ownership rights for %s', self.restore_fullpath)
            if not self.adjust_file_permissions(self.restore_fullpath, perm_absolute=self.perm_mode):
                logging.error("Encountered error while setting mode permissions for directory %s . Marking restore as failed for this item",
                              self.restore_fullpath)
                no_error_encountered = False

        return no_error_encountered

    # noinspection PyUnreachableCode
    def restore_file_from_s3(self):
        """ fetches a file from S3 and saves it to disk. If encrypted then attempt to decrypt the file
            Returns True on Success or False otherwise
        """
        # check we have enough disk space to restore this file
        restore_to_dir = self.restore_fullpath.rsplit(unicode(os.sep, 'utf-8'), 1)[0]
        # get file system usage for the parent dir holding our to be restored file
        restore_to_dir_statvfs = os.statvfs(restore_to_dir.encode('utf-8'))
        if int(self.size) > int(restore_to_dir_statvfs.f_bsize * restore_to_dir_statvfs.f_bavail):
            logging.error("Not enough disk space available to save %s . File is %s bytes while space availabe is %s",
                          self.restore_fullpath, self.size, restore_to_dir_statvfs.f_bsize * restore_to_dir_statvfs.f_bavail)
            return False
        s3_key_obj = prepare_s3_key_obj(self.s3_bucket_obj, self.s3_parent_folder_path, self.filepath, self.file_type)
        # encrypyted files need extra work as we can't decrypt on the fly but first we have to save them on disk and then decrypt them
        if self.encrypt:
            # obtain tmp file name to be used for storing the downloaded file before we decrypt it
            tmpfile = self.generate_tmpfile_for_restore()
            if not tmpfile:
                # means we could not obtain a tmp file so we're bailing out
                return False
            # adjust Callback so it shows somehow this download is going to a different place
            download_progress = Callback_progress('(downloading) ' + self.restore_fullpath + '  (tmp saving to ' + tmpfile + ') ', self.args)
        else:
            download_progress = Callback_progress(self.restore_fullpath, self.args)
        if self.file_type != 'file':
            logging.error("attempted to download from S3 %s which isn't a file but a %s . Aborting download for this item",
                          self.restore_fullpath, self.file_type)
            return False
        # if destination exists then figure out if we can write to it, if not return False and abort restore for item
        #  we ensure in the calling function that if the path exists, it is the same type as the restored item.
        if os.path.lexists(self.restore_fullpath.encode('utf-8')):
            if not os.access(self.restore_fullpath.encode('utf-8'), os.W_OK):
                # attempt to adjust permissions, return restore function as failed if this operation fails
                if not self.adjust_file_permissions(self.restore_fullpath, perm_add='uw'):
                    logging.error("Encountered error while adding user write permissions for %s . Aborting restore for this item", self.restore_fullpath)
                    return False
                # if we still don't have write access then attempt to change group permissions
                if not os.access(self.restore_fullpath.encode('utf-8'), os.W_OK):
                    if not self.adjust_file_permissions(self.restore_fullpath, perm_add='gw'):
                        logging.error("Encountered error while adding group write permissions for %s . Aborting restore for this item", self.restore_fullpath)
                        return False
                    # if we still don't have write access then attempt to change other users permissions
                    if not os.access(self.restore_fullpath.encode('utf-8'), os.W_OK):
                        if not self.adjust_file_permissions(self.restore_fullpath, perm_add='ow'):
                            logging.error("Encountered error while adding write permissions for other users on %s . Aborting restore for this item",
                                          self.restore_fullpath)
                            return False
                        # if we still don't have write permissions then abort restore for this file.
                        if not os.access(self.restore_fullpath.encode('utf-8'), os.W_OK):
                            logging.error("Encountered error while adding write permissions for %s despite adding write rights for user, group and others. "
                                          "Aborting restore for this item", self.restore_fullpath)
                            return False
        # proceed to download S3 key
        if self.encrypt:
            # noinspection PyUnboundLocalVariable
            target_file = tmpfile
        else:
            target_file = self.restore_fullpath
        try:
            s3_key_obj.get_contents_to_filename(filename=target_file, cb=download_progress, num_cb=100)
        except boto.exception.S3ResponseError as exception:
            if not self.args.quiet:
                print ""
            logging.error("could not download from S3 item to be saved as %s . Received exception reason is: \"%s\" and the body of the error response is: %s"
                          % (target_file, exception.reason, exception.body))
            return False
        except boto.exception.S3PermissionsError as exception:
            if not self.args.quiet:
                print ""
            logging.error("S3 permission error when attempting to download item to be saved as %s . Received exception reason is: \"%s\"" %
                          (target_file, exception.reason))
            return False
        except:
            if not self.args.quiet:
                print ""
            logging.error("Unexpected error while downloading from S3 the item to be saved as %s . Error was %s" % (target_file, sys.exc_info()))
            return False
        # download was successful
        else:
            # if encrypted then attempt to decrypt
            if self.encrypt:
                # perform decryption
                if self.decrypt_file(in_filename=tmpfile, out_filename=self.restore_fullpath):
                    # if decryption was successful then remove the tmp file
                    try:
                        if os.path.exists(tmpfile):
                            os.remove(tmpfile)
                    except OSError:
                        logging.info("Error encountered while trying to remove tmp file %s which holds %s before it gets decrypted",
                                     tempfile_name, self.restore_fullpath)
                # decryption was not successful so let's remove the tmp file and return false from the whole function
                else:
                    try:
                        if os.path.exists(tmpfile):
                            os.remove(tmpfile)
                    except OSError:
                        logging.info("Error encountered while trying to remove tmp file %s which holds %s before it gets decrypted",
                                     tempfile_name, self.restore_fullpath)
                    return False
            if not self.args.quiet:
                print ""
            # once we finished the download, let's adjust permissions of the file so it matches what we have stored in metadata
            # set ownership rights for newly restored file
            if not self.adjust_file_ownership(self.restore_fullpath, self.uid, self.gid):
                logging.warning("Encountered error while restoring ownership rights for file %s", self.restore_fullpath)
            # set mode permissions for newly restored file
            if not self.adjust_file_permissions(self.restore_fullpath, perm_absolute=self.perm_mode):
                logging.warning("Encountered error while restoring mode permissions for file %s", self.restore_fullpath)
                # even if restoring permissions failed, we won't mark the item as failed to restore. A warning was issued to notify the user.
            # if we have a checksum available for the remote file then let's compare it with the one of the restored file
            if self.remote_md5:
                self.calculate_md5checksum(filepath=self.restore_fullpath)
                if self.remote_md5 != self.file_md5_sum:
                    if self.encrypt:
                        logging.error("Recorded MD5 checksum for %s does not match the one computed from the restored file. Given that this file was encrypted"
                                      ", then an incorrect password would lead to this. Please check your password and try again", self.restore_fullpath)
                    else:
                        logging.error("Recorded MD5 checksum for %s does not match the one computed from the restored file.", self.restore_fullpath)
                    # removed failed file
                    try:
                        if os.path.exists(self.restore_fullpath):
                            os.remove(self.restore_fullpath)
                    except OSError:
                        logging.info("Error encountered while trying to remove file %s which failed md5 comparison once it was restored", self.restore_fullpath)
                    return False
            return True
        # we should not have gotten here. Returning false and issuing error too.
        logging.error("Workflow error in BackedUpItem.restore_file_from_s3() method. This stage should not have been reached. Marking restore as failed for %s"
                      " . Reason for this is a bug in the code.", self.restore_fullpath)
        return False

    def restore_symlink_from_metadata(self):
        """ restores symlink from metadata.
            Returns True on Success or False otherwise
        """

        try:
            os.symlink(self.symlink_target.encode('utf-8'), self.restore_fullpath.encode('utf-8'))
        except OSError:
            return False
        else:
            print '100%                  ' + self.restore_fullpath.encode('utf-8')
            return True

    # noinspection PyTypeChecker,PyUnboundLocalVariable
    def upload_object_to_s3(self, encryptor=None, salt=None, iv=None, chunk_size=52428800):
        """ takes care of uploading an object to S3 and also of adding metadata
            returns True if the upload was successful, otherwise False

        encryptor             => encryptor obejct to use for encrypting files.
                                 If this has a value different to None then we need to encrypt the files.
        salt                  => cryptographic salt used to build the encryptor object.
                                 We need to store the salt in the encrypted file in order to be able to later decrypt it
        iv                    => Initialization Vector (iv) used to build the encryptor object.
                                 We need to store the IV in the encrypted file in order to be able to later decrypt it
        chunk_size            => files larger than chunk_size will use multipart upload. It is mandatory that NUMBER MUST BE DIVISIBLE WITH 16
                                 or otherwise encryption(if used) will fail. Defaults to 50 MiB
        """
        result = False
        s3_key_obj = prepare_s3_key_obj(self.s3_bucket_obj, self.s3_parent_folder_path, self.filepath, self.file_type)
        upload_progress = Callback_progress(self.filepath, self.args)
        if self.file_type == 'file':
            file_size = os.stat(self.filepath.encode('utf-8')).st_size
            try:
                # file smaller that 50 MiB get uploaded with only one call, others use multipart upload
                if file_size < chunk_size:
                    # metadata is set using this method for single call file uploads. Multipart uploads support having metadata
                    # specified with the initiate upload call
                    if not update_s3_key_metadata(s3_key_obj, self.metadata, self.filepath):
                        logging.error("S3 metadata add/update error for file %s . Moving on to next file" % self.filepath)
                        return False
                    # if we do encryption then encrypted files are stored in a temporary variable (so in memory)
                    if encryptor and salt and iv:
                        logging.info("%s is being encrypted" % self.filepath)
                        encrypted_file = self.encrypt_file(encryptor, salt, iv, file_part=0, chunksize=file_size)
                        logging.info("%s uploading" % self.filepath)
                        s3_key_obj.set_contents_from_file(encrypted_file, replace=True, cb=upload_progress)
                    # upload without doing encryption
                    else:
                        # if we have computed the MD5 then let's use it
                        if self.file_md5_sum != '' and self.file_md5_base64_digest != '':
                            s3_key_obj.set_contents_from_filename(self.filepath.encode('utf-8'), replace=True, cb=upload_progress,
                                                                  md5=(self.file_md5_sum, self.file_md5_base64_digest))
                        # if not then the Boto library will calculate it anyway but at least we don't calculate it twice
                        else:
                            s3_key_obj.set_contents_from_filename(self.filepath.encode('utf-8'), replace=True, cb=upload_progress)
                else:
                    # here we replace single file upload with multipart upload
                    # Create a multipart upload request
                    mp = self.s3_bucket_obj.initiate_multipart_upload(key_name=self.s3_parent_folder_path.encode('utf-8') + self.filepath.encode('utf-8'),
                                                                      metadata=self.metadata)

                    chunk_count = int(math.ceil(file_size / float(chunk_size)))

                    # Send the file parts to create a file-like object that points to a certain byte range within the original file.
                    # We set bytes to never exceed the original file size.
                    for i in range(chunk_count):
                        upload_progress = Callback_progress(self.filepath, self.args, part=i, total_parts=chunk_count)
                        offset = chunk_size * i
                        send_bytes = min(chunk_size, file_size - offset)
                        # if we do encryption then encrypted files are stored in a temporary variable (so in memory)
                        if encryptor and salt and iv:
                            logging.info("Encrypting part %s of the file, part size being %s out of total size of %s from offset %s" %
                                         (i + 1, sizeof_fmt(send_bytes), sizeof_fmt(file_size), offset))
                            encrypted_file = self.encrypt_file(encryptor, salt, iv, file_part=i, chunksize=send_bytes, offset=offset)
                            logging.info("Uploading part %s of the file, part size being %s out of total size of %s", i + 1, sizeof_fmt(send_bytes),
                                         sizeof_fmt(file_size))
                            mp.upload_part_from_file(fp=encrypted_file, part_num=i + 1, cb=upload_progress, num_cb=100)
                            # print "iv is %s and salt is %s and filesize is %s" %(iv.encode('hex'), salt.encode('hex'), file_size)
                        # upload without doing encryption
                        else:
                            logging.info("Uploading part %s of the file, part size being %s out of total size of %s", i + 1, sizeof_fmt(send_bytes),
                                         sizeof_fmt(file_size))
                            with open(self.filepath, 'rb') as fp:
                                fp.seek(offset)
                                mp.upload_part_from_file(fp=fp, part_num=i + 1, cb=upload_progress, size=send_bytes, num_cb=100)
                                # Finish the upload - without this call the space will be consumed on the S3 side but the object won't be accessible/viewable
                                # so it's critical this call is made
                                # !!! Add code to deal with upload failure for one of the chunks (possible cleanup or retry) - remember we're already
                                #  in a try statement
                    mp.complete_upload()
                    # !!! ETag is not the file's MD5 when using multipart upload so we need to save the md5 as a separate tag
                # finished upload of file (either single call upload or multiple call/chunk upload)
                result = True
            except boto.exception.S3ResponseError as exception:
                if not self.args.quiet:
                    print ""
                logging.error("could not upload to S3 file %s . Received exception reason is: \"%s\" and the body of the error response is: %s" % (
                    self.filepath, exception.reason, exception.body))
                if file_size >= 52428800:
                    mp.cancel_upload()
            except boto.exception.S3PermissionsError as exception:
                if not self.args.quiet:
                    print ""
                logging.error("S3 permission error for file %s . Received exception reason is: \"%s\"" % (self.filepath, exception.reason))
                if file_size >= 52428800:
                    mp.cancel_upload()
            except:
                if not self.args.quiet:
                    print ""
                logging.error("Unexpected error while uploading the file %s to S3: %s" % (self.filepath, sys.exc_info()))
                if file_size >= 52428800:
                    mp.cancel_upload()
            if not self.args.quiet:
                print ""
        if self.file_type == 'dir' or self.file_type == 'symlink':
            # mapping short names to long names, makes sense really only for translating "dir" to "directory" in error messages
            file_type_name = {'dir': 'directory', 'file': 'file', 'symlink': 'symlink'}
            # add metadata only (and an empty string for the body of the "file" as S3 doesn't really have a concept of a folder or of a symlink)
            try:
                if not update_s3_key_metadata(s3_key_obj, self.metadata, self.filepath):
                    logging.error("S3 metadata add/update error for %s: %s . Moving on to next file" % (file_type_name[self.file_type], self.filepath))
                    return False
                s3_key_obj.set_contents_from_string('', replace=True)
                result = True
            except boto.exception.S3ResponseError as exception:
                logging.error("could not add to S3 the %s entry for %s . Received exception reason is: \"%s\" and the body of the error response is: %s" %
                              (file_type_name[self.file_type], self.filepath, exception.reason, exception.body))
            except boto.exception.S3PermissionsError as exception:
                logging.error("S3 permission error for %s: entry for %s . Received exception reason is: \"%s\"" %
                              (file_type_name[self.file_type], self.filepath, exception.reason))
            except:
                logging.error("Unexpected error while adding the %s entry for %s to S3: %s" % (file_type_name[self.file_type], self.filepath, sys.exc_info()))

        return result

    def encrypt_file(self, encryptor, salt, iv, file_part=0, chunksize=52428800, offset=0):
        """ Encrypts part of a file or the whole file. The output is put in an object of type io.BytesIO (which emulates a file handle)

            encryptor    => object of type Crypto.Cipher.AES to use in order to encrypt.
                            We're expected the object to have been generated with AES.new(key, AES.MODE_CBC, iv)
            salt         => cryptographic salt used to build the encryptor object.
                            We need to store the salt in the encrypted file in order to be able to later decrypt it
            iv           => Initialization Vector (iv) used to build the encryptor object.
                            We need to store the IV in the encrypted file in order to be able to later decrypt it
            file_part    => which part of the file we encrypt. This makes sense because we upload large files in
                            split parts to AWS and AWS glues the result back from multiple parts
            chunksize    => How much of the file we want to encrypt during this run. Default is 50 MB.
                            MUST BE A NUMBER DIVISIBLE WITH 16 UNLESS THIS IS THE LAST PART OF THE FILE
            offset       => From which byte in the input file to start reading content for encryption. Defaults to 0.
                            This is used when encrypting a large file in multiple runs
        """
        filesize = os.path.getsize(self.filepath.encode('utf-8'))
        outfile = io.BytesIO()

        with open(self.filepath.encode('utf-8'), 'rb') as infile:
            # at the begining of the encrypted file write the filesize + IV + SALT + the the encrypted content of the orig file + any needed whitespace padding
            if file_part == 0:
                outfile.write(struct.pack('<Q', filesize))
                outfile.write(iv)
                outfile.write(salt)
            else:
                # seek to the file position where we need to start reading bytes
                infile.seek(offset)
            chunk = infile.read(chunksize)
            # pad the last part before encryption as AES can encrypt only block sizes of 16 Bytes. Padding will be removed when decrypting
            if len(chunk) % 16 != 0:
                chunk += ' ' * (16 - len(chunk) % 16)
            outfile.write(encryptor.encrypt(chunk))
        # rewind output file object so when its output is read, it will be read from the begining
        outfile.seek(0)
        return outfile

    def decrypt_file(self, in_filename, out_filename, chunksize=24 * 1024, check_size=True):
        """ Decrypts a file using AES (CBC mode) with the given password. The Salt and the IV will be extracted from the file itself.
            Returns False if any issue is encountered and otherwise it returns True

            in_filename  => name of the file to decrypt
            out_filename => name of the file where to write the decrypted content
            chunksize    => Sets the size of the chunk which the function uses to read and decrypt the file. Larger chunk sizes can be faster for some files
                            and machines. chunksize must be divisible by 16.
            check_size   => if to compare file size as stored in S3 metadata vs size stored in the file itself. A mismatch causes an abort of decryption

        """
        if self.encrypt_password is None:
            logging.error("You attempting to decrypt %s and save its contents to %s but you have not provided a password for "
                          "decryption", in_filename, out_filename)
            return False
        with open(in_filename, 'rb') as infile:
            origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
            if check_size:
                if int(origsize) != int(self.size):
                    logging.error("The file size stored in the S3 metadata is %s but the size stored in the file header is %s . Aborting decryption attempt",
                                  origsize, self.size)
                    return False
            # for AES iv must be 16 bytes long
            iv = infile.read(16)
            # we know for sure that the used salt was 32 bytes long
            salt = infile.read(32)
            key, out_salt = gen_key_and_salt(password=self.encrypt_password, salt=salt)
            decryptor = AES.new(key, AES.MODE_CBC, iv)
            # nice progress report
            decrypting_progress = Callback_progress('(decrypting)  ' + out_filename + ' ', self.args)
            print ""
            # amount of bytes processed
            decrypted_so_far = 0

            with open(out_filename, 'wb') as outfile:
                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    outfile.write(decryptor.decrypt(chunk))
                    # next two lines are for displaying progress only
                    decrypted_so_far += chunksize
                    decrypting_progress(complete=decrypted_so_far, total=origsize)
                outfile.truncate(origsize)
        return True

    def generate_tmpfile_for_restore(self):
        """ generates a name for a tmp file we can use for storing files before decrypting them. Returns the full path of the file.
            this functions does not handle deletion of the file once it's no longer needed
        """
        try:
            if self.tmpdir_path is None:
                tempfile_fd, tempfile_name = tempfile.mkstemp(prefix=self.name.encode('utf-8'), suffix='_ENCRYPTED')
            else:
                tempfile_fd, tempfile_name = tempfile.mkstemp(prefix=self.name.encode('utf-8'), suffix='_ENCRYPTED', dir=self.tmpdir_path)
            os.close(tempfile_fd)
        except OSError:
            logging.error("Could not generate a temporary file name to store the encrypted filed %s before we attempt it's decryption", self.restore_fullpath)
            return False
        else:
            # figure out if we have enough disk space for the file to be restored
            # (os.statvfs('/tmp').f_bsize * os.statvfs('/tmp').f_bavail)
            parent_tmp_dir = tempfile_name.rsplit(unicode(os.sep, 'utf-8'), 1)[0]
            # get file system usage for the parent dir holding our tmp file
            parent_tmp_dir_statvfs = os.statvfs(parent_tmp_dir.encode('utf-8'))
            if int(self.size) > int(parent_tmp_dir_statvfs.f_bsize * parent_tmp_dir_statvfs.f_bavail):
                logging.error("Not enough disk space available to temporarly store %s on %s before decrypting it", self.restore_fullpath, parent_tmp_dir)
                # remove tmp file
                try:
                    if os.path.exists(tempfile_name.encode('utf-8')):
                        os.remove(tempfile_name.encode('utf-8'))
                except OSError:
                    logging.info("Error encountered while trying to remove tmp file %s which was generated to hold %s before it gets decrypted",
                                 tempfile_name, self.restore_fullpath)
                return False
            return tempfile_name

# END OF CLASS
class RestoreItems(object):
    def __init__(self, root, s3_bucket_obj):
        """ constructor for RestoreItems class
            :root          => the top level folder in S3 Bucket we're using for backups. Under this folder are the actual files & folders we have backed up
            :s3_bucket_obj => S3 bucket object as returned by Boto
        """
        if root[-1] != '/':
            self.backup_root = root + '/'
        else:
            self.backup_root = root
        self.pwd = self.backup_root
        self.command = None
        self.command_arguments = None
        self.s3_bucket_obj = s3_bucket_obj
        self.items_to_restore = []

    def select_files_for_restore(self):
        """ main method of the class which basically is the Text User Interface for selection of what files/folders to restore """
        while True:
            user_input = raw_input('#:> ').strip().decode('utf-8')
            # separate actual command and arguments
            self.command = user_input.split(' ', 1)[0]
            # if we had arguments then let's check them
            if len(self.command) < len(user_input):
                self.command_arguments = user_input.split(' ', 1)[1]
            else:
                self.command_arguments = None
            if self.command == 'ls':
                self.command_ls()
            elif self.command == 'pwd':
                print '/' + self.pwd.encode('utf-8')
            elif self.command == 'cd':
                self.command_cd()
            elif self.command == 'select':
                self.command_select()
            elif self.command == 'show':
                self.command_show()
            elif self.command == '':
                continue
            elif self.command == 'help':
                self.show_help(detailed=True)
            elif self.command == 'unselect':
                self.command_unselect()
            elif self.command == 'finish':
                break
            else:
                self.show_help()

    def show_help(self, detailed=False):
        """ show help message for the interactive TUI
            :detailed => if True then show detailed help. By default it's False
        """
        if self.command is not None:
            print "No such command: %s" % self.command
        print "Allowed commands are: cd finish ls help pwd select show unselect"
        if detailed:
            print "All of the following commands work with data fetched from Amazon S3. This means that some commands will be slow if there are a lot of " \
                  "items in a particular directory on which you operate\n"
            print "cd       - change directory. This command makes sense only for backed up directories. Outside of those, S3 does not have the concept of a" \
                  "directory so you will not be able to navigate the rest of an S3 bucket (for example items uploaded with other tools)"
            print "ls       - display files and folders in the current directory. Ignores any passed arguments"
            print "help     - show help"
            print "pwd      - show path to current working directory. '/' represents the root of the S3 bucket where files are stored"
            print "select   - select files or folder for restore. If you select a folder then all of it's children are marked for restore"
            print "show     - show what items are marked for restore"
            print "unselect - remove a file or folder from the list of items marked for restore"
            print "finish   - commences restore with marked items"

    def command_ls(self):
        """ command to list folder contents according to what we have backed up in S3 """
        displayed_items = []
        if self.command_arguments:
            print "WARNING !!! arguments to the 'ls' command are ignored and current directory is always shown"
        print 'TYPE'.rjust(7), 'SIZE'.rjust(10) + ' ', 'CTIME'.rjust(19), ' NAME'
        for key in self.s3_bucket_obj.list(prefix=self.pwd, delimiter='/'):
            selected_key = self.s3_bucket_obj.get_key(key.name)
            remote_file_size = sizeof_fmt(selected_key.size)
            remote_file_type = selected_key.get_metadata('filetype')
            remote_ctime = selected_key.get_metadata('ctime')
            if selected_key is None:
                return
            short_name = key.name[len(self.pwd):]
            # if we're missing any of the following metadata fields then skip the item as it was uploaded with something else (not this tool)
            if remote_file_size is None or remote_file_type is None or remote_ctime is None:
                continue
            if len(short_name) == 0:
                short_name = '..'
            else:
                displayed_items.append(key.name)
            ctime = datetime.datetime.fromtimestamp(int(remote_ctime)).strftime('%Y-%m-%d %H:%M:%S')
            print remote_file_type.rjust(7), str(remote_file_size).rjust(10) + ' ', str(ctime).rjust(19), ' ' + short_name.encode('utf-8')

    def command_cd(self):
        """ method which changes current directory"""
        if self.pwd[-1] != '/':
            self.pwd += '/'
        if self.command_arguments:
            if self.command_arguments == '..':
                target_folder = self.pwd.rsplit('/', 2)[0] + '/'
            elif self.command_arguments[-1] != '/':
                # if argument begins with '/' then we have an absolute path typed in
                if self.command_arguments[:1] == '/':
                    target_folder = self.command_arguments[1:] + '/'
                else:
                    target_folder = self.pwd + self.command_arguments + '/'
            else:
                # if argument begins with '/' then we have an absolute path typed in
                if self.command_arguments[:1] == '/':
                    target_folder = self.command_arguments[1:]
                else:
                    target_folder = self.pwd + self.command_arguments
            # if we backup to the root level of the backup then there we can't check if a folder exists as there isn't an actual S3 key ending with '/'
            if target_folder == self.backup_root:
                self.pwd = target_folder
            elif len(self.backup_root) > len(target_folder):
                print "Can not CD to above %s due to the fact no files are backed up above this path for the configuration section you're restoring files for" \
                    % self.pwd.encode('utf-8')
            else:
                # check key exists before attempting CD
                if self.check_key_exists(name=target_folder):
                    self.pwd = target_folder
                else:
                    print 'No such folder: /%s' % target_folder
        else:
            # if no folder is specified then return to the self.backup_root path from which downward we have directory keys stored
            self.pwd = self.backup_root

    def command_select(self):
        """ method which adds an items to the list of items selected for restore
        """
        if self.pwd[-1] != '/':
            self.pwd += '/'
        if self.command_arguments:
            if self.command_arguments == '..':
                target_item = self.pwd.rsplit('/', 2)[0] + '/'
            else:
                # if argument begins with '/' then we have an absolute path typed in
                if self.command_arguments[:1] == '/':
                    target_item = self.command_arguments[1:]
                else:
                    target_item = self.pwd + self.command_arguments

            if len(self.backup_root) > len(target_item) and self.backup_root[:-1] != target_item:
                print "Can not select to above /%s due to the fact no files are backed up above this path for the configuration section you're restoring " \
                      "files for" % self.backup_root.encode('utf-8')
                return False
            elif target_item == self.backup_root or target_item == self.backup_root[:-1]:
                # no point to go testing if the path exists as it will fail due to the fact that we don't have a "folder" stored in S3 for the
                #   root of the backup
                if target_item[-1] != '/':
                    target_item += '/'
                self.add_to_restore_items(target_item)
                return True
            else:
                # check key exists before attempting to add it
                if not self.check_key_exists(name=target_item):
                    # check if the target is a folder as the check for it to be a file or symlink has failed
                    target_item += '/'
                    if not self.check_key_exists(name=target_item):
                        print "Can not add /%s to list of restorable items as an S3 item with the same path could not be validated" % target_item[:-1]
                        return False
                    else:
                        self.add_to_restore_items(target_item)
                        return True
                # validated and S3 key exists at that path so let's add it to the queue
                else:
                    self.add_to_restore_items(target_item)
                    return True
        else:
            print "You did not specify any path as an argument to the 'select' command"
            return False

    def command_show(self):
        """ show which files are selected for restore """
        if len(self.items_to_restore) > 0:
            print "items selected for restore are:"
            for item in self.items_to_restore:
                print '/' + item
        else:
            print "There are no items added to restore list"

    def command_unselect(self):
        """ remove an item from the list of items to restore """
        if self.command_arguments:
            for existing_item in list(self.items_to_restore):
                if existing_item == self.command_arguments[1:]:
                    self.items_to_restore.remove(self.command_arguments[1:])
                    return True
            # if we got here then we did not find any match in self.items_to_restore
            print "%s does not match any of the items selected for restore. Please use as arguments for 'unselect' only items shown in the output of the" \
                  " 'show' command" % self.command_arguments
            return False
        else:
            print "You did not specify any path as an argument to the 'unselect' command"
            return False

    def add_to_restore_items(self, item):
        """ add a validated item to the list of items to restore. First check if we already have a parent folder added or if we have children items added
            :item => item to add to the list. It's expected the validation took place outside this function
        """
        # check if item is already part of the list
        if item in self.items_to_restore:
            print "Item /%s was already selected" % item
            return False
        # walk the list of items selected for restore and check if we already have a parent path added or if the path to be added is a parent to existing added
        #  paths
        for added_item in list(self.items_to_restore):
            # check if we already have a parent folder added
            if added_item[-1] == '/':
                if item.startswith(added_item):
                    print "Parent folder /%s already added to restore list and it means all of it's content it going to be restored so there isn't a point to" \
                          "also add /%s to the list of restored items" % (added_item, item)
                    return False
            # if the item to add is a folder then check if it's the parent of existing items
            if item[-1] == '/':
                if added_item.startswith(item):
                    print "Adding /%s which is a parent folder of /%s so we're removing the latter from the restore list" % (item, added_item)
                    self.items_to_restore.remove(added_item)
        # if we made it so far, then add the item
        self.items_to_restore.append(item)
        return True

    def check_key_exists(self, name):
        """ checks if an S3 key exists. Returns True if it does, False otherwise.
            :name                  => name of the item we want to CD. This should be an absolute path in the S3 bucket. Folders need to end with
                                        '/' but it's up to the calling function to make the correct call
        """
        s3_key_obj = boto.s3.key.Key(self.s3_bucket_obj)
        s3_key_obj.key = name.encode('utf-8')
        if s3_key_obj.exists():
            return True
        else:
            return False

    def generate_restore_list(self):
        """
        Generator type function which for each S3 key returns a dict object with the file properties.
        This function is normaly used as input to populate the list of files selected for restore.
        """
        for item in self.items_to_restore:
            for key in self.s3_bucket_obj.list(prefix=item):
                selected_key = self.s3_bucket_obj.get_key(key.name)
                metadata = get_metadata_from_s3_key(selected_key, key.name, remove_extra_keys=False, keep_booleans=True)
                # if the key doesn't have the mandatory minimum fields then move on to the next key
                if metadata is None:
                    continue
                else:
                    yield metadata
# END Of Class

def prepare_s3_key_obj(s3_bucket_obj, s3_parent_folder_path, filepath, file_type):
    """ returns an S3 key object (boto.s3.key.Key) to be used in order to upload/download a file or update it's metadata. The purpose of having a function is
        to encapsulate the logic around the naming of S3 objects
    s3_bucket_obj         => S3 bucket object
    s3_parent_folder_path => S3 parent folder path under which we store all files
    filepath              => the fully qualified file name (as seen on the OS where it's being backed up from)
    file_type             => one of file / symlink / dir
    """
    s3_key_obj = boto.s3.key.Key(s3_bucket_obj)
    if file_type == 'file':
        s3_key_obj.key = s3_parent_folder_path.encode('utf-8') + filepath.encode('utf-8')
    # we store symlinks with an adjusted S3 key name just to be sure that anyone browsing an S3 bucket doesn't mistake a SYMLINK for a real file
    elif file_type == 'symlink':
        s3_key_obj.key = s3_parent_folder_path.encode('utf-8') + filepath.encode('utf-8') + u'.SYMLINK'.encode('utf-8')
    elif file_type == 'dir':
        # for some reason, the API expects folders to end with a '/'
        s3_key_obj.key = s3_parent_folder_path.encode('utf-8') + filepath.encode('utf-8') + u'/'.encode('utf-8')
    return s3_key_obj


def update_s3_key_metadata(s3_key_obj, metadata, filepath, force_update=False):
    """ add or update metadata to an S3 Key. PLEASE TAKE INTO ACCOUNT METADATA DOESN'T GET SENT UNLESS YOU CALL A set_contents_from_*
        method or copy the key to somewhere else (over itself)
        Returns True if the upload was successful, otherwise False

    s3_key_obj   => S3 key object
    metadata     => dictionary containing metadata to add
    filepath     => used only for error messages in order to relate to which file raised the exception
    force_update => If to force a metadata update by copying the S3 object over itself via an special api call.
                    This makes sense only if you want to update metadata and you're not going to update the file too.
                    None the less this seems at least a crazy way of fixing this problem and hopefully Amazon will release an API call that
                    can change metadata without requiring a file contents update.
                    According to http://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectCOPY.html it is possible to copy a file over itself;
                    quote: "You cannot copy an object to itself unless the MetadataDirective header is specified and its value set to REPLACE."
    """
    result = False
    try:
        for key in metadata:
            s3_key_obj.set_metadata(key, metadata[key])
        # we get around the problem of metadata not being updated unless we upload also the file contents by copying the file over itself.
        if force_update:
            _ = s3_key_obj.copy(s3_key_obj.bucket.name, s3_key_obj.name, s3_key_obj.metadata, preserve_acl=True)
        result = True
    except boto.exception.S3ResponseError as exception:
        logging.error("could not add/update metadata to S3 file %s . Received exception reason is: \"%s\" and the body of the error response is: %s" %
                      (filepath, exception.reason, exception.body))
    except boto.exception.S3PermissionsError as exception:
        logging.error("permission error while adding/updating metadata to S3 for file %s . Received exception reason is: \"%s\"" % (filepath, exception.reason))
    except:
        logging.error("Unexpected error while adding/updating S3 metadata for file %s : %s" % (filepath, sys.exc_info()))
    return result


def gen_key_and_salt(password=None, salt=None):
    """ Generates a 256 bit key and optionally a Salt. The key will be used as the secret for file encryption.
        The function returns the key and the salt. The salt will be needed in order to generate the same key again (based from the salt + the password)

    password => the password to use in order to generate the key
    salt     => the salt to couple with the password in order to generate the key. If the salt is not specified then a new one is generated.
                YOU SHOULD NEVER SPECIFY THE SALT if you are generating a new key for encryption. It makes sense to specify the salt only when
                you want to obtain the key to be used for decryption
    """

    if password is None:
        logging.error("gen_key_and_salt() needs to be called with at least parameter 'password'")
        sys.exit(1)
    iterations = 5000
    if salt is None:
        salt = os.urandom(32)

    key = PBKDF2(password, salt, dkLen=32, count=iterations)

    return key, salt


def get_args():
    """ Get arguments from CLI """

    parser = argparse.ArgumentParser(description='Script which backs up data to S3')

    parser.add_argument('--debug', required=False, action="store_true", default=False, help='Show debug level messages')
    parser.add_argument('-q', '--quiet', required=False, action="store_true", default=False, help='Show only ERROR level messages')
    parser.add_argument('-v', '--verbose', required=False, action="store_true", default=False, help='Show verbose level messages')
    parser.add_argument('-c', '--config', required=True, action="store", default=None, help='Path to configuration file')
    parser.add_argument('command', action="store", choices=['backup', 'initdb', 'list_remote', 'restore', 'stats', 'syncdb_remote', 'update_s3_metadata'],
                        help='Command to run')

    arguments = parser.parse_args()

    # if a config file was mentioned, test if it exists and it's readable
    if arguments.config is not None:
        if not os.path.isfile(arguments.config) or not os.access(arguments.config, os.R_OK):
            logging.error("config file %s is missing or is unreadable. Exiting", arguments.config)
            sys.exit(1)
    return arguments


def validate_configfile_key(config_file_object, config_section, key_name, allowed_in_default=True):
    """ validate that the section of the config file contains the tested key and it's not an empty string 

        config_file_object => object of type ConfigParser.SafeConfigParser
        config_section     => config file section to examine
        key_name           => config key to validate
        allowed_in_default => if the key can exist in the [DEFAULT] section too. By default this parameter is set to True
    """

    if allowed_in_default:
        default_msg = '(or in section [DEFAULT]) '
    else:
        default_msg = ''
        # check that the key is not specified in the [DEFAULT] section
        try:
            config_file_object.get('DEFAULT', key_name)
        except ConfigParser.NoOptionError:
            # we're are totally OK with not having the option in the [DEFAULT] and getting this exception here
            pass
        else:
            logging.error(
                "config file has the key \"%s\" defined in the [DEFAULT] section. This is not allowed as \"%s\" should be mentioned only in custom sections."
                " Exiting", key_name, key_name)
            sys.exit(1)
    try:
        key_value = config_file_object.get(config_section, key_name)
    except ConfigParser.NoOptionError:
        logging.error("config file does not have in section [%s] %sthe '%s' key defined. Exiting", config_section, default_msg, key_name)
        sys.exit(1)

    if key_value == "":
        logging.error("config file has in section [%s] %sthe '%s' key defined but it has no value. Exiting", config_section, default_msg, key_name)
        sys.exit(1)


def validate_and_return_config_file(file_path):
    """ check that the config file contains the mandatory minimum values 

        file_path => check given file (this should be a full path)
    """

    # dictionary to store default values (in case they are not mentioned in the config file)
    config_file_defaults = {
    }
    config = ConfigParser.SafeConfigParser(config_file_defaults, allow_no_value=False)
    try:
        config.read(file_path)
    except ConfigParser.ParsingError:
        logging.error("could not parse config file %s . Exiting. Actual exception message follows:\n %s", file_path, sys.exc_info()[1])
        sys.exit(1)

    if len(config.sections()) == 0:
        logging.error("config file %s does not have any sections defined. Exiting", file_path)
        sys.exit(1)

    # check that config section names contain only letters, numbers, underscore and dash
    for config_section in config.sections():
        if not re.match("^[a-zA-Z0-9_-]+$", config_section):
            logging.error("config file %s has section name [%s] which contains more than lower/upper case letters, numbers, underscore and dash. Exiting",
                          file_path, config_section)
            sys.exit(1)

    # validate individual mandatory keys are defined
    for config_section in config.sections():
        validate_configfile_key(config, config_section, 'path', allowed_in_default=False)
        validate_configfile_key(config, config_section, 'db_location')
        validate_configfile_key(config, config_section, 'aws_access_key_id')
        validate_configfile_key(config, config_section, 'aws_secret_access_key')
        validate_configfile_key(config, config_section, 's3_bucket')

    return config


# noinspection PyUnboundLocalVariable
def get_config_value(config, config_section, key, default=False, default_value=None, val_type='str', allowed_in_default_section=True):
    """ fetch a value from the config and optionally, if missing then return a default value

    config                     => ConfigParser type object (https://docs.python.org/2/library/configparser.html)
    config_section             => Configuration file section to search for the option in . Unless allowed_in_default_section = False then the [DEFAULT]
                                    section is examined too if the option is not found in the given section
    key                        => key to fetch the value for
    default                    => If to use the content of the default_value variable. If not specified then an error is returned and the program is
                                    terminated if a key is missing
    default_value              => default value to use if the key is not found in the config file
    val_type                   => the value of the key needs to be converted to either int / float / boolean / str .Default is str.
                                    This parameter is ignored if default_value=None
    allowed_in_default_section => if it is allowed to have the key mentioned in the [DEFAULT] section of the config file
    """

    if default and not allowed_in_default_section:
        logging.error('function get_config_value() can\'t be called with "default" being True and allowed_in_default_section=False')
        sys.exit(1)
    # if we have a default value supplied and we can skip validating the key exists in the config. Else let's validate the key exists
    if not default:
        validate_configfile_key(config, config_section, key, allowed_in_default=allowed_in_default_section)
    try:
        if val_type == 'str':
            value = str(config.get(config_section, key))
        elif val_type == 'int':
            value = config.getint(config_section, key)
        elif val_type == 'float':
            value = config.getfloat(config_section, key)
        elif val_type == 'boolean':
            value = config.getboolean(config_section, key)
        else:
            logging.error(
                "value of type \"%s\" specified for key \"%s\" is not of type int / float / boolean / str . Please call get_config_value() "
                "with correct parameters", val_type, key)
            sys.exit(1)
    except ConfigParser.NoOptionError:
        if default:
            if default_value is None:
                value = None
            elif val_type == 'str':
                value = str(default_value)
            elif val_type == 'int':
                value = int(default_value)
            elif val_type == 'float':
                value = float(default_value)
            elif val_type == 'boolean':
                if default_value.lower() in ['true', '1', 't', 'y', 'yes']:
                    value = True
                else:
                    value = False
        else:
            logging.error("key \"%s\" is not specified in the config file, but is required", key)
            sys.exit(1)
    return value


def init_sqlite_db(dbpath):
    """ initialize a sqlite database to hold file information 
        dbpath => full file path of the database
    """

    if os.path.isfile(dbpath):
        logging.error("Database file %s already exists. Ignoring attempt to initialize database contents from scratch", dbpath)
        return

    logging.info("creating database %s to hold file information", dbpath)

    conn = sqlite3.connect(dbpath)
    c = conn.cursor()

    # Create table
    c.execute(
        'CREATE TABLE files(filepath text, uid text, gid text, perm_mode text, md5 text, filetype text, size text, symlink_target text, mtime text, '
        'ctime text, encrypted text , PRIMARY KEY(filepath))')

    # Save (commit) the changes
    conn.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()


def create_restore_tables(db_cursor, db_conn, restore_time):
    """ create tables where to save the name of the files being restored and also a table noting the settings used for a restore
        so we can resume the restore at a later time.
    Returns the name of the table holding the file restore progress followed by the name of the table holding the restore settings

    :db_cursor    => database cursor type object
    :db_conn      => database connection type object
    :restore_time => unix timestamp when restore was initiated
    """

    logging.info("creating database tables to hold restore progress for restore started at %s",
                 datetime.datetime.fromtimestamp(restore_time).strftime('%Y-%m-%d %H:%M:%S'))
    # Create table to hold progress information - DBAPi doesn't support parameter substitution for table names, hence the use of python string substitution
    #   "filepath" in the created restore_files_$unix-timestamp table refers to the original path+name of the file and not to the place where it got restored
    db_cursor.execute(
        "CREATE TABLE restore_files_%s(filepath text, uid text, gid text, perm_mode text, md5 text, filetype text, size text, symlink_target text, mtime text, "
        "ctime text, encrypted text, restored text, failed text, PRIMARY KEY(filepath))" % (str(restore_time)))

    # Create table to hold restore parameters (needed when we want to resume a restore)
    db_cursor.execute("CREATE TABLE restore_settings_%s(setting text, value text, PRIMARY KEY(setting))" % (str(restore_time)))
    # commit above two statements
    db_conn.commit()

    return u'restore_files_' + str(restore_time).decode('utf-8'), u'restore_settings_' + str(restore_time).decode('utf-8')


def add_restore_settings_to_restore_session_table(db_cursor, db_conn, restore_options):
    """

    :db_cursor       => database cursor type object
    :db_conn         => database connection type object
    :restore_options => dict containing settings to add to the database
    """
    table = restore_options['db_table_restore_settings']
    for key in restore_options:
        #  keys we don't want to save as settings
        if key in ['db_table_restore_settings', 'db_table_restore_files']:
            continue
        db_cursor.execute('INSERT INTO %s (setting, value) VALUES (?, ?)' % table, (key, restore_options[key]))
    db_conn.commit()


# noinspection PyUnboundLocalVariable
def check_and_resume_previous_restore(db_cursor, db_conn):
    """ check if a previous restore exists and offer to resume. If resume is selected then returns a dict containing at lease the name of the table
        holding the file restore progress followed by the name of the table holding the restore settings; If not previous restore exists then the keys
        for the table names have value None
    
    :db_cursor      => database cursor type object
    :db_conn        => database connection type object
    """
    found_restores = []
    restore_options = {}
    for row in db_cursor.execute('SELECT * FROM sqlite_master WHERE type="table" AND name LIKE "restore_files_%"'):
        found_restores.append(row['name'])
    if len(found_restores) > 0:
        print "Previous restore attempts have been found. If you wish to resume such an attempt then enter it's number, otherwise input 'n'"
        counter = 1
        for restore in found_restores:
            restore_time = int(restore.rsplit('_', 1)[1])
            # figure out if restore list has been completely generated
            db_cursor.execute("SELECT value FROM restore_settings_%s WHERE setting='restore_list_generated'" % str(restore_time))
            db_query_result = db_cursor.fetchone()
            if db_query_result['value'] == '1':
                # restore list is generated so let's figure out how many files have been restored
                db_cursor.execute("SELECT count(*) AS result FROM restore_files_%s where restored='1' and failed='0'" % str(restore_time))
                db_query_result = db_cursor.fetchone()
                num_restore_files = db_query_result['result']
                db_cursor.execute("SELECT count(*) AS result FROM restore_files_%s" % str(restore_time))
                db_query_result = db_cursor.fetchone()
                num_total_files_scheduled_for_restore = db_query_result['result']
                db_cursor.execute("SELECT count(*) AS result FROM restore_files_%s where failed='1'" % str(restore_time))
                db_query_result = db_cursor.fetchone()
                num_total_files_failed = db_query_result['result']
                restore_message = "with %s items restored and %s items failed to restore out of %s items selected for restore" % \
                                  (num_restore_files, num_total_files_failed, num_total_files_scheduled_for_restore)
            else:
                restore_message = 'with selected files list to be generated'
            restore_datetime = datetime.datetime.fromtimestamp(restore_time).strftime('%Y-%m-%d %H:%M:%S')
            print str(counter).rjust(3) + '.', 'restore started at:', restore_datetime, restore_message
            counter += 1
        while True:
            answer = raw_input("Please select an option or input 'n' to start a new backup restore: ")
            if answer.lower() not in ['n', 'no'] and answer not in [str(x) for x in range(1, len(found_restores) + 1)]:
                print "Please input a valid option"
            else:
                break
        if answer.lower() not in ['n', 'no']:
            restore_options['db_table_restore_settings'] = u'restore_settings_' + found_restores[int(answer) - 1].rsplit('_', 1)[1]
            restore_options['db_table_restore_files'] = found_restores[int(answer) - 1]
            # add to dict remaining options
            for row in db_cursor.execute("SELECT * FROM %s" % restore_options['db_table_restore_settings']):
                # SQLite stores booleans as numbers in a "text" field so we need to convert them here
                if row['setting'] in ['overwrite', 'overwrite_permissions', 'restore_list_generated']:
                    if row['value'] == '1':
                        restore_options[row['setting']] = True
                    else:
                        restore_options[row['setting']] = False
                else:
                    restore_options[row['setting']] = row['value']
            # ask user if he wants to also restore items marked as failed
            if num_total_files_failed > 0:
                while True:
                    answer = raw_input("Do you wish to attempt to also restore the items which failed to restore during a previous run ?\nY/N: ")
                    if answer.lower() not in ['y', 'yes', 'n', 'no']:
                        print "Please input one of: Y, y, yes, N, n, no"
                    else:
                        break
                if answer.lower() in ['y', 'yes']:
                    # remove the failed flag from the db for each of the items having one
                    try:
                        db_cursor.execute("UPDATE %s SET failed='0' where failed='1'" % (restore_options['db_table_restore_files']))
                        db_conn.commit()
                    except sqlite3.Error:
                        logging.error("unexpected sql database error while updating restore items table in order to mark previous failed items as to be "
                                      "retried. Exiting")
                        sys.exit(1)
        # user selected he wants a new restore to commence
        else:
            restore_options['db_table_restore_settings'] = None
            restore_options['db_table_restore_files'] = None
            # check if the user wants to delete the previous deletes
            while True:
                answer = raw_input("Do you wish to delete the previous restore sessions ?\nY/N: ")
                if answer.lower() not in ['y', 'yes', 'n', 'no']:
                    print "Please input one of: Y, y, yes, N, n, no"
                else:
                    break
            if answer.lower() in ['y', 'yes']:
                # delete previous restore sessions
                for restore in found_restores:
                    restore_time = restore.rsplit('_', 1)[1]
                    delete_previous_restore(db_cursor, db_conn, restore_time)
    else:
        restore_options['db_table_restore_settings'] = None
        restore_options['db_table_restore_files'] = None

    return restore_options


def delete_previous_restore(db_cursor, db_conn, restore_time):
    """ delete a previous restore session

    :db_cursor    => database cursor type object
    :db_conn      => database connection type object
    :restore_time => unix timestamp appended to the database tables
    """
    try:
        db_cursor.execute("DROP TABLE %s" % ('restore_settings_' + restore_time))
        db_cursor.execute("DROP TABLE %s" % ('restore_files_' + restore_time))
        db_conn.commit()
    except:
        logging.warning(
            "Error while deleting database tables restore_settings_%s and restore_files_%s which held a previous backup resture session for resume purposes",
            restore_time, restore_time)


def enable_sqlite3_regex_function(expr, item):
    """ regular expression function to be used in SQLITE when mentioning the sql parameter REGEXP. Without this we can't use REGEXP matching in sqlite """

    reg = re.compile(expr)
    return reg.search(item) is not None


def sqlite3_sort_by_number_of_ossep(item):
    """ sort the results based on the number of os.sep() contained in a column. Returns an integer showing the number of occurences
    :item => item on which to perform the counting of os.sep()
    """
    return item.count(unicode(os.sep, 'utf-8'))


def return_db_connection(dbpath):
    """ return a SQL lite database connection object (cursor object) which can be used in statements like cursor.execute('SQL CMD')

        dbpath => full file path of the database
    """

    if not os.path.isfile(dbpath) or not os.access(dbpath, os.R_OK):
        logging.error(
            "Database file %s is missing or is unreadable. Call the script with \"initdb\" in order to initialize the DB if this is the first run. Exiting",
            dbpath)
        sys.exit(1)

    conn = sqlite3.connect(dbpath)
    # needed in order to be able to use REGEXP with SQLITE in Pythob
    conn.create_function("REGEXP", 2, enable_sqlite3_regex_function)
    # needed for sorting based on number of os.sep() contained in a column
    conn.create_function("COUNT_NUM_SEPARATORS", 1, sqlite3_sort_by_number_of_ossep)
    # needed so we can also reference results of SELECT by column title (and not only by numeric index)
    conn.row_factory = sqlite3.Row

    return conn


def return_db_cursor(db_conn):
    """ given a db_connection object, returns a db_cursor object 
    :db_conn => db_conn object
    """
    cursor = db_conn.cursor()
    return cursor


def get_s3_bucket_obj(aws_access_key_id, aws_secret_access_key, s3_bucket_name, is_secure=True):
    """ return an s3 bucket object on which to perform operations like uploading files or listing/downloading 
    aws_access_key_id     => AWS Access Key id
    aws_secret_access_key => AWS Secret Key
    s3_bucket_name        => name of the bucket to perform operations on. The AWS access key id & and secret mentioned above should
                                have read/write access on this bucket
    is_secure             => boolean describing if to use HTTPS for all operations. Reccomended to be True

    The function returns an S3 bucket object
    """

    # obtain S3 connection object
    s3_conn = boto.s3.connection.S3Connection(aws_access_key_id, aws_secret_access_key, is_secure=is_secure)
    s3_bucket_obj = s3_conn.lookup(s3_bucket_name)
    if s3_bucket_obj is None:
        logging.error("Bucket: %s does not exist or your S3 credentials don't have access to it", s3_bucket_name)
        sys.exit(1)
    return s3_bucket_obj


def sizeof_fmt(num, suffix='B'):
    """ return size in human readable form 
        
    num    => value to process
    suffix => append this string to any output
    """

    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Yi', suffix)


def dblist_of_files_in_folder(db_cursor, folder):
    """ return the list of files and directories currently located in folder as it was recorded in the database 

    db_cursor =>
    folder    => folder to return the list for

    returns a dictionary having as key the file/folder name and the value the type: dir/file/symlink , all being contained in "folder"
    """

    file_list = {}
    regex = u'^' + folder + unicode(os.sep, 'utf-8') + u'[^/]*$'
    for row in db_cursor.execute('SELECT filepath, filetype FROM files WHERE filepath REGEXP ?', (regex,)):
        file_list[row['filepath'][len(folder + os.sep):]] = row['filetype']
    return file_list


def s3_multi_delete(s3_bucket_obj, s3_parent_folder_path, file_list, remove_from_db=False, db_cursor=None, db_conn=None, recurse=False):
    """ deletes with one call multiple S3 files. Returns True on success of all operations or False if at least one delete did not succeed

    s3_bucket_obj         => Boto object describing the bucket where we will upload. This means we already have successfuly established a connection to S3
    s3_parent_folder_path => folder within the bucket which is the "root" of the filesystem where files are stored
    file_list             => list of items, each item being full filepath of the object to delete (path as seen on the local OS where the file used to exist)
    remove_from_db        => if after successful S3 deletion to also remove the DB record for the file
    db_cursor             => db_cursor to be used if remove_from_db=True
    db_conn               => db_conn object, needed as db_cursor
    recurse               => if for directories to check if also directory contents is in "file_list" variable and if not then to append it.
                                By default this is False
    """

    return_result = True
    result = None
    # if Recurse == True then check that we are also removing all "directory" contents
    if recurse:
        recurse_file_list = []
        for item in file_list:
            if len(item) > 1 and item[-1:] == '/':
                for key in s3_bucket_obj.list(prefix=item):
                    remote_file_name = key.name
                    if remote_file_name not in file_list:
                        recurse_file_list.append(remote_file_name)
                        logging.info("S3 file %s still exists while parent folder %s is being deleted so we're marking it too for deletion", remote_file_name,
                                     s3_parent_folder_path.rstrip('/') + u'/' + item)
                        # we don't want to process more then 400 items for deletion at a time
                        if len(recurse_file_list) > 399:
                            s3_multi_delete(s3_bucket_obj, s3_parent_folder_path, file_list=recurse_file_list, remove_from_db=True, db_cursor=db_cursor,
                                            db_conn=db_conn, recurse=False)
                            recurse_file_list = []
        if len(recurse_file_list) > 0:
            s3_multi_delete(s3_bucket_obj, s3_parent_folder_path, file_list=recurse_file_list, remove_from_db=True, db_cursor=db_cursor, db_conn=db_conn,
                            recurse=False)
    logging.info('processing batch S3 deletion for %s file(s): %s', len(file_list), ", ".join(file_list))
    try:
        result = s3_bucket_obj.delete_keys(keys=file_list)
    except boto.exception.S3ResponseError as exception:
        logging.error("could not delete from S3 the items %s . Received exception reason is: \"%s\" and the body of the error response is: %s" %
                      (file_list, exception.reason, exception.body))
    except boto.exception.S3PermissionsError as exception:
        logging.error("S3 permission error while deleting the items %s . Received exception reason is: \"%s\"" % (file_list, exception.reason))
    except:
        logging.error("Unexpected error while deleting from S3 the items %s: %s" % (file_list, sys.exc_info()))
    if result and len(result.deleted) > 0:
        for deleted_item in result.deleted:
            # run command to delete from DB the successfully S3 deleted file - http://boto.cloudhackers.com/en/latest/ref/s3.html#boto.s3.multidelete.Deleted
            if remove_from_db:
                delete_file_entry_from_db(db_cursor, db_conn, deleted_item.key[len(s3_parent_folder_path):])
    if len(result.errors) > 0:
        return_result = False
        # for failed_item in result.errors:
        # do stuff with files which did not get deleted from S3 - http://boto.cloudhackers.com/en/latest/ref/s3.html#boto.s3.multidelete.Error
        # !!! TO DO !!!!
        #    pass
    return return_result


def delete_file_entry_from_db(db_cursor, db_conn, filepath):
    """ deletes a file entry from the database

    db_cursor => db_cursor type object to perform the SQL operations on
    db_conn   => db_conn type object, needed for .commit() of SQL operations
    filepath  => name of file to delete, example: /usr/local/a/file . We strip the '/' if it exists as the last character on the right side of the string
    """
    logging.info("Deleting database entry for file/dir: %s", filepath)
    try:
        db_cursor.execute('DELETE FROM files WHERE filepath=?', (filepath.rstrip('/'),))
        db_conn.commit()
    except sqlite3.Error:
        logging.error("unexpected sql database error while deleting record for %s", filepath)


def check_restore_path(restore_path):
    """ checks if a given path can be used to save restored files. Returns True if path is usable, otherwise False
    
    restore_path - path to test (if it's a folder and if we have write permissions to add items to it)
    """
    if not os.path.isdir(restore_path):
        logging.error("The path: %s is not a folder/directory. Please specify a folder/directory", restore_path)
        return False
    if not os.access(restore_path, os.R_OK):
        logging.error("The path: %s is not readable, meaning you can not list folder/directory contents", restore_path)
        return False
    # if restore path is / (root of the filesystem) then we don't need to check write rights
    if not os.access(restore_path, os.W_OK) and restore_path != '/':
        logging.error("The path: %s is not writable", restore_path)
        return False
    if not os.access(restore_path, os.X_OK):
        logging.error("The path: %s can not be changed into (meaning it's a folder/directory on which you miss the execute permission)", restore_path)
        return False
    return True


def clear_uncomplete_multipart_uploads(s3_bucket_obj, s3_parent_folder_path):
    """ Shows and cleans which S3 multipart uploads never completed and that is storage which still gets billed by AWS
    s3_bucket_obj         => S3 bucket type Object
    s3_parent_folder_path => Folder under the S3 hierarchy where we store backup up items
    """
    for multipart_upload in s3_bucket_obj.list_multipart_uploads():
        key_name = multipart_upload.key_name
        if re.match('^' + s3_parent_folder_path.rstrip('/') + '/', multipart_upload.key_name):
            logging.warning("Found incomplete multipart upload: %s . Proceeding to remove it", multipart_upload.key_name)
            try:
                multipart_upload.cancel_upload()
            except boto.exception.S3PermissionsError as exception:
                logging.error(
                    "S3 permission error while cancelling failed multipart upload %s . Received exception reason is: \"%s\"" % (key_name, exception.reason))
            except:
                logging.error("Unexpected error while cancelling failed multipart upload %s : %s" % (key_name, sys.exc_info()))


def return_db_stats(db_cursor, config_section):
    """ Give status report about backed up files, according to the information we have in the database 
    db_cursor      => db_cursor type object which will be used to perform the SQL operations
    config_section => name of the configuration section for which we're giving statistics
    """

    total_num_files = 0
    db_cursor.execute('SELECT count(*) AS result FROM files')
    db_query_result = db_cursor.fetchone()
    print "-" * 80
    if db_query_result:
        print "In configuration section %s there are %s backed up items out of which:" % (config_section, db_query_result['result'])
    db_cursor.execute('SELECT count(filetype) AS result FROM files WHERE filetype = "dir"')
    db_query_result = db_cursor.fetchone()
    if db_query_result:
        print "        %s directories/folders" % (db_query_result['result'])
    db_cursor.execute('SELECT count(filetype) AS result FROM files WHERE filetype = "file"')
    db_query_result = db_cursor.fetchone()
    if db_query_result:
        print "        %s files" % (db_query_result['result'])
        total_num_files = db_query_result['result']
    db_cursor.execute('SELECT count(filetype) AS result FROM files WHERE filetype = "symlink"')
    db_query_result = db_cursor.fetchone()
    if db_query_result:
        print "        %s symlinks" % (db_query_result['result'])

    db_cursor.execute('SELECT total(size) AS result FROM files')
    db_query_result = db_cursor.fetchone()
    if db_query_result:
        print "Total size of backed up files is %s" % (sizeof_fmt(int(db_query_result['result'])))
        if total_num_files > 0:
            print "Which means an average of %s per file" % (sizeof_fmt(int(db_query_result['result']) / total_num_files))
            db_cursor.execute('SELECT min(mtime) AS result FROM files')
            db_query_result = db_cursor.fetchone()
            oldest_file = int(float(db_query_result['result']))
            db_cursor.execute('SELECT max(mtime) AS result FROM files')
            db_query_result = db_cursor.fetchone()
            newest_file = int(float(db_query_result['result']))
            print "Oldest file (mtime) is from %s and newest from %s" % (datetime.datetime.fromtimestamp(oldest_file).strftime('%Y-%m-%d %H:%M:%S'),
                                                                         datetime.datetime.fromtimestamp(newest_file).strftime('%Y-%m-%d %H:%M:%S'))


def fetch_and_compare_metadata_key(selected_key, key_name, meta_field, metadata):
    """ fetches a metadata key, checks if the result is not null and if true then adds the key value to the dictionary  metadata.
        Returns the selected_key object and the metadata dictionary
    selected_key => S3 object repesenting a selected key (s3_bucket_obj.get_key(key.name))
    key.name     => name of the key to fetch. We use this when outputting error messages
    meta_field   => name of metadata field to fetch
    metadata     => dictionary where to store the fetched metadata value as long as the value exists
    """
    try:
        meta_field_val = selected_key.get_metadata(meta_field)
        if meta_field_val:
            # fields are fetched or converted by boto to unicode so no point to attempt this (as it will error out anyway)
            metadata[meta_field] = meta_field_val
    except:
        logging.warning("Encountered error while trying to fetch metadata field \"%s\" for key %s  .Skipping this file", meta_field,
                        key_name)
        return False, False
    return selected_key, metadata


def sync_db_from_remote_metadata(s3_bucket_obj, s3_parent_folder_path, db_conn, db_cursor):
    """ fetches metadata from S3 and compares it with the local database. Any inconsistencies will be fixed by fully trusting what metadata we have store in S3
    
    s3_bucket_obj         => S3 bucket type Object
    s3_parent_folder_path => Folder under the S3 hierarchy where we store backup up items
    db_conn               => DB conn object (needed for commit() actions)
    db_cursor             => DB cursor type object upon which we perfom all SQL operations

    """
    db_field_list = ['filepath', 'uid', 'gid', 'perm_mode', 'md5', 'filetype', 'size', 'symlink_target', 'mtime', 'ctime', 'encrypted']
    for key in s3_bucket_obj.list(prefix=s3_parent_folder_path.rstrip('/')):
        selected_key = s3_bucket_obj.get_key(key.name)
        metadata = get_metadata_from_s3_key(selected_key, key.name)
        # if the key doesn't have the mandatory minimum fields then move on to the next key
        if metadata is None:
            continue
        # Now let's compare the metadata fields with what we have in the database
        db_cursor.execute('SELECT * FROM files WHERE filepath=?', (metadata['filepath'],))
        db_query_result = db_cursor.fetchone()
        if db_query_result is None:
            logging.info("File %s is not in the database. Adding record to database", metadata['filepath'])
            try:
                db_list_entry = []
                for field_value in db_field_list:
                    if field_value in metadata:
                        db_list_entry.append(metadata[field_value])
                    else:
                        db_list_entry.append('')
                    db_tuple_entry = tuple(db_list_entry)
                db_cursor.execute(
                    'INSERT INTO files (filepath,uid,gid,perm_mode,md5,filetype,size,symlink_target,mtime,ctime,encrypted) '
                    'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', db_tuple_entry)
                db_conn.commit()
            except sqlite3.IntegrityError:
                logging.warning(
                    '%s already is mentioned in the database. Check that you don\'t have two instances of the backup tool running. Skipping to next file',
                    metadata['filepath'])
                continue
        else:
            # We have a DB entry for the file, let's check if the entry from S3 matches what we have locally in the DB
            db_entry_needs_update = False
            for metadata_field in metadata:
                if metadata[metadata_field] != db_query_result[metadata_field]:
                    logging.info("%s has on S3 field \"%s\" with value \"%s\" while in the DB the value is \"%s\"", metadata['filepath'], metadata_field,
                                 metadata[metadata_field], db_query_result[metadata_field])
                    db_entry_needs_update = True
            if db_entry_needs_update:
                logging.info("%s updating DB entry", metadata['filepath'])
                try:
                    db_list_entry = []
                    for field_value in db_field_list:
                        if field_value in metadata:
                            db_list_entry.append(metadata[field_value])
                        else:
                            db_list_entry.append('')
                        db_tuple_entry = tuple(db_list_entry)
                    db_cursor.execute(
                        'UPDATE files SET filepath=?, uid=?, gid=?, perm_mode=?, md5=?, filetype=?, size=?, symlink_target=?, mtime=?, ctime=?, encrypted=? '
                        'where filepath=?', db_tuple_entry + (metadata['filepath'],))
                    db_conn.commit()
                except sqlite3.Error:
                    logging.error("unexpected sql database error while updating record for %s", metadata['filepath'])


# noinspection PyDefaultArgument
def get_metadata_from_db_row(row,
                             db_field_list=['filepath', 'uid', 'gid', 'perm_mode', 'md5', 'filetype', 'size', 'symlink_target', 'mtime', 'ctime', 'encrypted'],
                             encode_filepath=True):
    """
    create the metadata dict based on the values of a row from the 'files' table

    :row             => db row as returned by the db_cursor.execute(SELECT) generator
    :db_field_list   => list object containing the fields we want to examine
    :encode_filepath => defaults to True. If True then if the filepath field needs escaping of non ascii characters then proceed to do that
    """
    metadata = {}
    for db_field in db_field_list:
        metadata[db_field] = row[db_field]
    # because SQLite stores booleans as strings with value 0/1 and we keep True/False in the S3 metadata then we have to fix this in the metadata to upload
    if row['encrypted'] == '1':
        metadata['encrypted'] = True
    else:
        metadata['encrypted'] = False
    # 'symlink_target' metadata field makes sense only for symlinks
    if row['filetype'] != 'symlink':
        metadata.pop('symlink_target')
    # remove md5 field if md5 is empty in the DB
    if row['md5'] == '':
        metadata.pop('md5')
    metadata['filepath'] = row['filepath']
    # if filename contains unicode chars then convert them to unicode escaped code points
    if unicode(metadata['filepath'].encode('ascii', 'ignore'), 'utf-8') != metadata['filepath'] and encode_filepath:
        metadata['filepath'] = metadata['filepath'].encode('unicode_escape')
        metadata['filename_encoded'] = True
    else:
        metadata['filename_encoded'] = False

    return metadata


# noinspection PyDefaultArgument
def get_metadata_from_s3_key(selected_key, key_name,
                             metadata_to_fetch=['filepath', 'uid', 'gid', 'perm_mode', 'filetype', 'size', 'mtime', 'ctime', 'encrypted', 'filename_encoded'],
                             remove_extra_keys=True, keep_booleans=False):
    """ create the metadata dict based on the values of a S3 key. Returns the dict object if successful, otherwise returns None
    :selected_key      => S3 object repesenting a selected key (s3_bucket_obj.get_key(key_name))
    :key_name          => name of the key to fetch. We use this when outputting error messages
    :metadata_to_fetch => list object containing the metadata fields we want to examine. Some other fileds are also added based on returned values
    :remove_extra_keys => defaults to True. If to remove metadata keys like filename_encoded which don't exist in the database.
    :keep_booleans     => defaults to False. If to convert booleans to '0' / '1' strings as SQLite3 doesn't support booleans
    """
    metadata = {}
    for meta_field in metadata_to_fetch:
        selected_key, metadata = fetch_and_compare_metadata_key(selected_key, key_name, meta_field, metadata)
        if not selected_key:
            return None
    for meta_field in metadata_to_fetch:
        if meta_field not in metadata:
            logging.warning(
                "Key %s is missing metadata field \"%s\", which is a mandatory field. Ignoring key and moving one to the next one. "
                "Most likely this key was not uploaded to S3 using this tool", key_name, meta_field)
            return None
    if metadata['filetype'] == 'symlink':
        # fetch symlink target
        selected_key, metadata = fetch_and_compare_metadata_key(selected_key, key_name, 'symlink_target', metadata)
        if not selected_key:
            return None
    elif metadata['filetype'] == 'file':
        # fetch md5 value and encrypted status (in case it's set)
        selected_key, metadata = fetch_and_compare_metadata_key(selected_key, key_name, 'md5', metadata)
        if not selected_key:
            return None
    # SQLite stores booleans as '0' or '1' (both strings not integers)
    if 'encrypted' in metadata:
        if metadata['encrypted'].lower() == 'true':
            if keep_booleans:
                metadata['encrypted'] = True
            else:
                metadata['encrypted'] = '1'
        else:
            if keep_booleans:
                metadata['encrypted'] = False
            else:
                metadata['encrypted'] = '0'
    else:
        if keep_booleans:
            metadata['encrypted'] = False
        else:
            metadata['encrypted'] = '0'
    # if the filepath is encoded (meaning it contains Unicode characters outside ASCII and we had to escape those characters)
    #  then decode the value back to it's original form
    if 'filename_encoded' in metadata:
        if metadata['filename_encoded'].lower() == 'true':
            metadata['filename_encoded'] = True
            metadata['filepath'] = metadata['filepath'].decode('unicode_escape')
        else:
            metadata['filename_encoded'] = False
        # remove metadata key 'filename_encoded' to prevent errors further on where we expect same ammount of keys in both metadata and db rows
        if remove_extra_keys:
            del metadata['filename_encoded']
    return metadata


def force_update_s3_metadata(s3_bucket_obj, s3_parent_folder_path, db_cursor):
    """ forcefully updates metadata on all S3 objects contained in the database 
        The purpose of this function is to make it easier to update metadata when we're making changes in the code which rename metadata fields
        or add new fields and then we want to apply it to already made backups

    s3_bucket_obj         => S3 bucket type Object
    s3_parent_folder_path => Folder under the S3 hierarchy where we store backup up items
    db_cursor             => DB cursor type object upon which we perfom all SQL read operations
    """
    for row in db_cursor.execute('SELECT * FROM files'):
        metadata = get_metadata_from_db_row(row)
        s3_key_obj = prepare_s3_key_obj(s3_bucket_obj, s3_parent_folder_path, row['filepath'], row['filetype'])

        logging.info("updating S3 metadata for %s", s3_key_obj.name)
        if not update_s3_key_metadata(s3_key_obj, metadata, row['filepath'], force_update=True):
            logging.warning("S3 metadata add/update error for: %s . Moving on to next file", row['filepath'])
            return False


# noinspection PyUnboundLocalVariable
def get_restore_options(config_section, db_cursor, db_conn, restore_path=None):
    """
    ask the user for options regarding a restore. If a restore is desired then return dict object with options else return None

    :config_section => config section for which we are performing this restore
    :db_cursor      => database cursor type object
    :db_conn        => database connection type object
    :restore_path   => suggestion for restore path
    """
    restore_options = {}
    # when we started the restore (now)
    restore_time = int(time.time())
    while True:
        answer = raw_input("Do you wish to restore files from configuration section %s ?\nY/N: " % config_section)
        if answer.lower() not in ['y', 'yes', 'n', 'no']:
            print "Please input one of: Y, y, yes, N, n, no"
        else:
            break
    if answer.lower() in ['y', 'yes']:
        # commands to restore files
        restore_options = check_and_resume_previous_restore(db_cursor, db_conn)
        # if we didn't find an already existing restore to resume or we found one but the user chose not to resume then ask the user questions
        if not restore_options['db_table_restore_files'] and not restore_options['db_table_restore_settings']:
            while True:
                if restore_path:
                    answer = raw_input("Please enter the local path where you want to save restored files: [%s] " % restore_path) or restore_path
                else:
                    answer = raw_input("Please enter the local path where you want to save restored files: ")
                if check_restore_path(restore_path=answer.decode('utf-8')):
                    restore_options['restore_path'] = answer.decode('utf-8')
                    break
            while True:
                answer = raw_input("Do you wish to overwrite existing files located within the restore path %s ?\nY/N: " % (restore_options['restore_path']))
                if answer.lower() not in ['y', 'yes', 'n', 'no']:
                    print "Please input one of: Y, y, yes, N, n, no"
                else:
                    break
            if answer.lower() in ['y', 'yes']:
                restore_options['overwrite'] = True
                restore_options['overwrite_permissions'] = True
            else:
                restore_options['overwrite'] = False
                while True:
                    answer = raw_input(
                        "Do you wish to adjust permissions of already existing files and folders located within the restore path %s which are not "
                        "overwritten but still have a backed up version ?\nY/N: " % (restore_options['restore_path']))
                    if answer.lower() not in ['y', 'yes', 'n', 'no']:
                        print "Please input one of: Y, y, yes, N, n, no"
                    else:
                        break
                if answer.lower() in ['y', 'yes']:
                    restore_options['overwrite_permissions'] = True
                else:
                    restore_options['overwrite_permissions'] = False
            # ask for a folder where to save encrypted files before we decrypt them
            while True:
                answer = raw_input("Do you wish to specify a temporary dir to be used for decrypting files (in case you have encrypted files) ?. "
                                   "Otherwise the system's TMP dir will be used, if needed.\nY/N: ")
                if answer.lower() not in ['y', 'yes', 'n', 'no']:
                    print "Please input one of: Y, y, yes, N, n, no"
                else:
                    break
            if answer.lower() in ['y', 'yes']:
                while True:
                    answer = raw_input("Please enter a path where you want to temporary save downloaded files before they are decrypted: ")
                    if check_restore_path(restore_path=answer.decode('utf-8')):
                        restore_options['tmpdir_path'] = answer.decode('utf-8')
                        break
            # check if the "files" table has entries and if so then ask the user if he wants to restore based on the database entries.
            #   Otherwise restore using S3 metadata
            db_cursor.execute('SELECT count(*) AS result FROM files')
            db_query_result = db_cursor.fetchone()
            if db_query_result['result'] > 0:
                while True:
                    answer = raw_input(
                        "Do you wish to restore based on the list of ALL files recorded in the local database or use the remote S3 metadata or select files"
                        " from S3 ?\n Please enter 'db' or 's3' or 'select': ")
                    if answer.lower() not in ['db', 's3', 'select']:
                        print "Please input one of: 'db' or 's3' or 'select"
                    else:
                        break
                restore_options['file_list_source'] = answer.lower()
            else:
                while True:
                    answer = raw_input(
                        "Do you wish to restore based on the list of ALL files recorded in S3 metadata or select files from S3 ?\n"
                        "Please enter 's3' or 'select': ")
                    if answer.lower() not in ['s3', 'select']:
                        print "Please input one of: 's3' or 'select"
                    else:
                        break
                restore_options['file_list_source'] = answer.lower()
            restore_options['db_table_restore_files'], restore_options['db_table_restore_settings'] = create_restore_tables(db_cursor, db_conn, restore_time)
            # next variable marks if we have finished generating the list of files to restore and we have saved them to the DB
            restore_options['restore_list_generated'] = False
            add_restore_settings_to_restore_session_table(db_cursor, db_conn, restore_options)
    if len(restore_options) == 0:
        return None
    else:
        return restore_options


def generate_restore_list_from_db(db_cursor):
    """
    Generator type function which for each entry in the "files" table returns a dict object with the file properties.
    This function is normaly used as input to populate the list of files selected for restore.
    :db_cursor => database cursor type object
    """
    for row in db_cursor.execute('SELECT * FROM files'):
        metadata = get_metadata_from_db_row(row, encode_filepath=False)
        yield metadata


def generate_restore_list_from_s3(s3_bucket_obj, s3_parent_folder_path):
    """
    Generator type function which for each S3 key returns a dict object with the file properties.
    This function is normaly used as input to populate the list of files selected for restore.
    :s3_bucket_obj         => S3 bucket type Object
    :s3_parent_folder_path => Folder under the S3 hierarchy where we store backup up items
    """
    for key in s3_bucket_obj.list(prefix=s3_parent_folder_path.rstrip('/')):
        selected_key = s3_bucket_obj.get_key(key.name)
        metadata = get_metadata_from_s3_key(selected_key, key.name, remove_extra_keys=False, keep_booleans=True)
        # if the key doesn't have the mandatory minimum fields then move on to the next key
        if metadata is None:
            continue
        else:
            yield metadata


def check_return_item_to_restore_list(db_cursor, restore_file_table, file_type):
    """ check if we still have items in the restore_file_$unix-timestamp table which haven't been restored and are of type file_type.
        Return True if so, otherwise False
    :db_cursor          => database cursor type object
    :restore_file_table => restore_file_$unix-timestamp  named table holding the items selected for restore
    :file_type          => one of 'file', 'dir', 'symlink'
    """
    db_cursor.execute("SELECT count(*) AS result FROM %s WHERE filetype=? AND restored='0' AND failed='0'" % restore_file_table, (file_type,))
    db_query_result = db_cursor.fetchone()
    if db_query_result['result'] > 0:
        return True
    else:
        return False

def return_item_to_restore_list(db_cursor, restore_file_table, file_type, num_rows=1000):
    """ generator type function which returns a dict object with file properties for items of type file_type from table restore_file_table.
        Those properties will be used so the item is restored to disk
    :db_cursor          => database cursor type object
    :restore_file_table => restore_file_$unix-timestamp  named table holding the items selected for restore
    :file_type          => one of 'file', 'dir', 'symlink'
    :num_rows           => how many rows to select in one run. We store in memory the results due to the fact that if we have an ongoing SELECT statement
                            and any statement which changes a table weird stuff happens with SQLite3 databases
    """
    if file_type not in ['file', 'dir', 'symlink']:
        logging.error("please call return_item_to_restore_list() with the correct parameters. file_type is not one of 'file', 'dir', 'symlink' . Exiting")
        sys.exit(1)
    # if returning folders then we want to ensure we first return the top most folders and then their children
    if file_type == u'dir':
        db_cursor.execute(
            "SELECT * FROM %s WHERE filetype=? AND restored='0' AND failed='0' ORDER BY COUNT_NUM_SEPARATORS(filepath) ASC LIMIT ?" % restore_file_table,
            (file_type, num_rows))
    else:
        db_cursor.execute("SELECT * FROM %s WHERE filetype=? AND restored='0' AND failed='0' LIMIT ?" % restore_file_table, (file_type, num_rows))
    rows = db_cursor.fetchall()
    for row in rows:
        metadata = get_metadata_from_db_row(row, encode_filepath=False)
        yield metadata

def return_restored_item_list(db_cursor, restore_file_table, file_type):
    """ generator type function which returns a dict object with file properties for items of type file_type from table restore_file_table.
        Those properties will be used so the item is possibly compared to one already restored to disk in order to ensure permissions where correctly set
    :db_cursor          => database cursor type object
    :restore_file_table => restore_file_$unix-timestamp  named table holding the items selected for restore
    :file_type          => one of 'file', 'dir', 'symlink'
    """
    if file_type not in ['file', 'dir', 'symlink']:
        logging.error("please call return_restored_item_list() with the correct parameters. file_type is not one of 'file', 'dir', 'symlink' . Exiting")
        sys.exit(1)
    # if returning folders then we want to ensure we first return the top most folders and then their children
    if file_type == u'dir':
        db_cursor.execute(
            "SELECT * FROM %s WHERE filetype=? AND restored='1' AND failed='0' ORDER BY COUNT_NUM_SEPARATORS(filepath) ASC" % restore_file_table, (file_type,))
    else:
        db_cursor.execute("SELECT * FROM %s WHERE filetype=? AND restored='1' AND failed='0'" % restore_file_table, (file_type,))
    rows = db_cursor.fetchall()
    for row in rows:
        metadata = get_metadata_from_db_row(row, encode_filepath=False)
        yield metadata


def build_restore_list(s3_bucket_obj, s3_parent_folder_path, db_conn, restore_options, path):
    """ build list of files to be restored and save them in the restore_files_$unix-timestamp db table. File names will be later read by another function
        from this table and files having restored=False will be processed for restore and then marked with restored=True
    :s3_bucket_obj         => S3 bucket type Object
    :s3_parent_folder_path => Folder under the S3 hierarchy where we store backup up items
    :db_conn               => database connection type object
    :restore_options       => dict containing amongst other the table names where the settings for the restore are saved and also the table where
                                restored files are recorded
    :path                  => local filesystem path where files are backed up from. We use this to consturct where files are probably saved on S3
    """
    db_cursor = return_db_cursor(db_conn)
    db_cursor.execute("SELECT value FROM %s WHERE setting='restore_list_generated'" % (restore_options['db_table_restore_settings']))
    db_query_result = db_cursor.fetchone()
    # if 'db_table_restore_settings' is 1 (True) then skip building as we already have this done
    if db_query_result['value'] == '1':
        return
    #
    if restore_options['file_list_source'] == 'db':
        # select to restore all files based on database
        restore_file_list = generate_restore_list_from_db(db_cursor)
    elif restore_options['file_list_source'] == 's3':
        # select to restore all files based on remote S3 metadata
        restore_file_list = generate_restore_list_from_s3(s3_bucket_obj, s3_parent_folder_path)
    elif restore_options['file_list_source'] == 'select':
        # select files to restore based on what the User decides to select while browsing data fetched from S3
        restore_root = s3_parent_folder_path + path
        if restore_root[-1] != '/':
            restore_root += '/'
        restore_items = RestoreItems(root=restore_root, s3_bucket_obj=s3_bucket_obj)
        restore_items.select_files_for_restore()
        restore_file_list = restore_items.generate_restore_list()
    else:
        logging.error("Restore source isn't 'db' or 's3' but instead is %s . Exiting", restore_options['file_list_source'])
        sys.exit(1)
    # get new db_cursor object. We can't reuse the db_cursor as it's used for generate_restore_list_from_db(which is a generator function)
    #   and re-use would break that
    print "Building list of items selected for restore"
    db_cursor2 = return_db_cursor(db_conn)
    for restore_file_metadata in restore_file_list:
        file_is_restorable = True
        for field in ['filepath', 'uid', 'gid', 'perm_mode', 'filetype', 'size', 'mtime', 'ctime', 'encrypted']:
            if field not in restore_file_metadata:
                logging.warning("File %s is missing metadata fields. Skipping restore for this file", restore_file_metadata['filepath'])
                file_is_restorable = False
            break
        if not file_is_restorable:
            continue
        # we need to add the following empty values if they don't exist already in the metadata as we're inserting it in the DB and we need all the fields
        #    to be present
        if 'symlink_target' not in restore_file_metadata:
            restore_file_metadata['symlink_target'] = ''
        if 'md5' not in restore_file_metadata:
            restore_file_metadata['md5'] = ''
        db_tuple_entry = (restore_file_metadata['filepath'], restore_file_metadata['uid'], restore_file_metadata['gid'], restore_file_metadata['perm_mode'],
                          restore_file_metadata['md5'], restore_file_metadata['filetype'], restore_file_metadata['size'],
                          restore_file_metadata['symlink_target'], restore_file_metadata['mtime'], restore_file_metadata['ctime'],
                          restore_file_metadata['encrypted'], False, False)
        try:
            logging.info("%s adding item to list of items selected for restore", restore_file_metadata['filepath'])
            db_cursor2.execute(
                "INSERT INTO %s (filepath,uid,gid,perm_mode,md5,filetype,size,symlink_target,mtime,ctime,encrypted,restored,failed) VALUES "
                "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)" % (restore_options['db_table_restore_files']), db_tuple_entry)
            # if we're building the restore list from S3 the we can commit after each INSERT as we don't have a read lock because
            #   of generate_restore_list_from_db()
            if restore_options['file_list_source'] == 's3':
                db_conn.commit()
        except sqlite3.IntegrityError:
            logging.debug("duplicate entry detected for %s most likely because you're resuming a restore session. The item should still be properly restored",
                          restore_file_metadata['filepath'])
        except sqlite3.Error:
            logging.warning("unexpected sql database error while adding restore record for %s . File will be ignored and skipped from restore",
                            restore_file_metadata['filepath'])
        db_conn.commit()
    # mark in the settings table that we have finished building the list of files to restore
    db_cursor2.execute("UPDATE %s SET value=? where setting IS 'restore_list_generated'" % (restore_options['db_table_restore_settings']), '1')
    # commit all of the above INSERT statements and also the UPDATE statement
    if restore_options['file_list_source'] == 'db':
        print "Commiting list of items selected for restore"
        db_conn.commit()


def main():
    """
    Main body of program
    """

    args = get_args()

    if args.debug:
        log_level = logging.DEBUG
    elif args.quiet:
        log_level = logging.ERROR
    elif args.verbose:
        log_level = logging.INFO
    else:
        log_level = logging.WARNING

    log_format = '%(levelname)s: %(message)s'
    logging.basicConfig(format=log_format, level=log_level)
    logging.debug('Debug messages enabled')
    logging.info('starting program')

    if args.config is not None:
        config = validate_and_return_config_file(args.config)
        for config_section in config.sections():
            logging.info("Processing config section: %s", config_section)
            dbpath = get_config_value(config, config_section, 'db_location') + os.sep + config_section + '.db'
            aws_access_key_id = get_config_value(config, config_section, 'aws_access_key_id')
            aws_secret_access_key = get_config_value(config, config_section, 'aws_secret_access_key')
            # config file key s3_parent_folder_path is optional and specifies where to store backup files in the S3 Bucket. If not specified,
            #   the config section name will be used.
            s3_parent_folder_path = get_config_value(config, config_section, 's3_parent_folder_path', default=True, default_value=config_section)
            # check_file_checksum - if to compute the MD5 checksum and us it for comparison when deciding if a file has changed compared to it's backup
            check_file_checksum = get_config_value(config, config_section, 'check_file_checksum', default=True, default_value='False', val_type='boolean')
            # if to remove from S3 and the database the files which have been deleted on the local filesystem
            delete_removed_files = get_config_value(config, config_section, 'delete_removed_files', default=True, default_value='True', val_type='boolean')
            # if to perform encryption of file contents (file names remain readable and un-obfuscated)
            encrypt = get_config_value(config, config_section, 'encrypt', default=True, default_value='False', val_type='boolean')
            if encrypt:
                encrypt_password = get_config_value(config, config_section, 'encrypt_password')
            else:
                encrypt_password = None
            # initialize SQL Database
            if args.command == 'initdb':
                init_sqlite_db(dbpath)
            # perform backup
            elif args.command == 'backup':
                path = get_config_value(config, config_section, 'path')
                # for now only one file is accepted for exclusion. TO DO - support multiple files for exclusion
                exclude_file = get_config_value(config, config_section, 'exclude_file', default=True, default_value=None)
                # obtain DB connection objects
                db_conn = return_db_connection(dbpath)
                db_cursor = return_db_cursor(db_conn)
                s3_bucket_name = get_config_value(config, config_section, 's3_bucket')
                # obtain S3 bucket object, upon which all other operations will be performed
                s3_bucket_obj = get_s3_bucket_obj(aws_access_key_id, aws_secret_access_key, s3_bucket_name)
                file_list_to_delete = []
                # walk the path described in the config section and process each file and directory under it
                # for root, dirs, files in os.walk(unicode(path, 'utf-8')):
                for root, dirs, files in os.walk(path):
                    # converting dir names and file names to unicode. If we call os.walk(u'string') at least on FreeBSD 9 we get errors from the OS
                    #   library as it uses ASCII by default
                    files_unicode = []
                    for name in files:
                        files_unicode.append(name.decode('utf-8'))
                    files = files_unicode
                    dirs_unicode = []
                    for name in dirs:
                        dirs_unicode.append(name.decode('utf-8'))
                    dirs = dirs_unicode
                    root = root.decode('utf-8')
                    for name in files:
                        # if file was marked for exclusion then skip it
                        if exclude_file is not None and os.path.join(path, exclude_file) == os.path.join(root, name):
                            logging.debug("%s is marked for exclusion from backup so we're skipping it", os.path.join(path, exclude_file))
                            continue
                        # otherwise process file
                        item_to_process = BackedUpItem(root, name, db_cursor, db_conn, 'file', s3_bucket_obj, s3_parent_folder_path, check_file_checksum,
                                                       config_section, args, encrypt, encrypt_password)
                        item_to_process.examine_file_and_backup()
                    for name in dirs:
                        item_to_process = BackedUpItem(root, name, db_cursor, db_conn, 'dir', s3_bucket_obj, s3_parent_folder_path, check_file_checksum,
                                                       config_section, args)
                        item_to_process.examine_file_and_backup()
                    # if to delete from remote locally deleted files / folders
                    if delete_removed_files:
                        # beware that this whole check below doesn't remove files from S3 (and their DB records)  where for example a local folder was
                        #   deleted and a file with the same name was created in place.
                        # we handle this situation in a different place  (in the examine_file_and_backup() function)
                        dblist_of_files = dblist_of_files_in_folder(db_cursor, root)
                        for file_in_db in dblist_of_files:
                            if file_in_db not in files and file_in_db not in dirs:
                                logging.info("%s has been locally deleted but still exists in DB. Marking for deletion", root + os.sep + file_in_db)
                                # if the file to delete is actually a folder then append a '/' at it's end as this is how we're "marking" folders in S3
                                if dblist_of_files[file_in_db] == 'dir':
                                    file_list_to_delete.append(s3_parent_folder_path + root + '/' + file_in_db + '/')
                                else:
                                    file_list_to_delete.append(s3_parent_folder_path + root + '/' + file_in_db)
                                # we don't want to do an API call with more then 400 files to be deleted at a time
                                if len(file_list_to_delete) > 399:
                                    s3_multi_delete(s3_bucket_obj, s3_parent_folder_path, file_list_to_delete, remove_from_db=True, db_cursor=db_cursor,
                                                    db_conn=db_conn, recurse=True)
                                    file_list_to_delete = []
                    # list and clean multipart uploads which never completed
                    clear_uncomplete_multipart_uploads(s3_bucket_obj, s3_parent_folder_path)
                # if we found files to delete and we didn't find more then 399, then let's remove the remaining ones
                if len(file_list_to_delete) > 0 and delete_removed_files:
                    s3_multi_delete(s3_bucket_obj, s3_parent_folder_path, file_list_to_delete, remove_from_db=True, db_cursor=db_cursor, db_conn=db_conn,
                                    recurse=True)
                # cleanup stuff like open DB
                db_conn.close()
            # list all files stored in S3
            elif args.command == 'list_remote':
                s3_bucket_name = get_config_value(config, config_section, 's3_bucket')
                logging.info("Listing all files backed up to S3 in %s/%s" % (s3_bucket_name, s3_parent_folder_path.rstrip('/')))
                print 'type'.rjust(7), 'size'.rjust(10), 'name'
                # obtain S3 bucket object, upon which all other operations will be performed
                s3_bucket_obj = get_s3_bucket_obj(aws_access_key_id, aws_secret_access_key, s3_bucket_name)
                for key in s3_bucket_obj.list(prefix=s3_parent_folder_path):
                    selected_key = s3_bucket_obj.get_key(key.name)
                    remote_file_size = sizeof_fmt(selected_key.size)
                    remote_file_type = selected_key.get_metadata('filetype')
                    # if we're missing any of the following metadata fields then mark the file as it was uploaded with something else (not this tool)
                    if remote_file_size is None or remote_file_type is None:
                        remote_file_size = 'ERROR'
                        remote_file_type = 'ERROR'
                    if remote_file_type == 'symlink':
                        remote_file_name = key.name.encode('utf-8')[:-8]
                    elif remote_file_type == 'ERROR':
                        remote_file_name = key.name.encode('utf-8') + '   <=== THIS OBJECT IS NOT MANAGED BY THIS TOOL'
                    else:
                        remote_file_name = key.name.encode('utf-8')
                    print remote_file_type.rjust(7), str(remote_file_size).rjust(10), remote_file_name
            elif args.command == 'restore':
                # the local path which is backed up. We use it as a suggestion for the restore path
                path = get_config_value(config, config_section, 'path')
                # obtain DB connection objects
                db_conn = return_db_connection(dbpath)
                db_cursor = return_db_cursor(db_conn)
                restore_options = get_restore_options(config_section, db_cursor, db_conn, path)
                # if restore_options is not None then the user wants a restore
                if restore_options:
                    # obtain S3 bucket object, upon which all other operations will be performed
                    s3_bucket_name = get_config_value(config, config_section, 's3_bucket')
                    s3_bucket_obj = get_s3_bucket_obj(aws_access_key_id, aws_secret_access_key, s3_bucket_name)
                    # build list of files which need to be restored and store it in the restore table
                    build_restore_list(s3_bucket_obj, s3_parent_folder_path, db_conn, restore_options, path=path)
                    # fetch items from the restore table
                    #   first restore folders
                    print "Creating directories to hold restored files"
                    while check_return_item_to_restore_list(db_cursor, restore_options['db_table_restore_files'], 'dir'):
                        for restore_file_properties in return_item_to_restore_list(db_cursor, restore_options['db_table_restore_files'], 'dir'):
                            # initialize restore object
                            root, name = restore_file_properties['filepath'].rsplit(os.sep, 1)
                            item_to_process = BackedUpItem(root, name, db_cursor, db_conn, restore_file_properties['filetype'], s3_bucket_obj,
                                                           s3_parent_folder_path, check_file_checksum, config_section, args, encrypt, encrypt_password,
                                                           restore_options, restore_metadata=restore_file_properties)
                            item_to_process.examine_file_and_restore()
                    # after folders restore files
                    print "Restoring files"
                    while check_return_item_to_restore_list(db_cursor, restore_options['db_table_restore_files'], 'file'):
                        for restore_file_properties in return_item_to_restore_list(db_cursor, restore_options['db_table_restore_files'], 'file'):
                            # initialize restore object
                            root, name = restore_file_properties['filepath'].rsplit(os.sep, 1)
                            item_to_process = BackedUpItem(root, name, db_cursor, db_conn, restore_file_properties['filetype'], s3_bucket_obj,
                                                           s3_parent_folder_path, check_file_checksum, config_section, args, encrypt, encrypt_password,
                                                           restore_options, restore_metadata=restore_file_properties)
                            item_to_process.examine_file_and_restore()
                    # restore symlinks
                    print "Restoring symlinks"
                    while check_return_item_to_restore_list(db_cursor, restore_options['db_table_restore_files'], 'symlink'):
                        for restore_file_properties in return_item_to_restore_list(db_cursor, restore_options['db_table_restore_files'], 'symlink'):
                            # initialize restore object
                            root, name = restore_file_properties['filepath'].rsplit(os.sep, 1)
                            item_to_process = BackedUpItem(root, name, db_cursor, db_conn, restore_file_properties['filetype'], s3_bucket_obj,
                                                           s3_parent_folder_path, check_file_checksum, config_section, args, encrypt, encrypt_password,
                                                           restore_options, restore_metadata=restore_file_properties)
                            item_to_process.examine_file_and_restore()

                    # do another run to adjust permissions on folders (during the restore
                    #   we may have adjusted folder permissions in order to be able to restore files). Start from the most long folder (counting number
                    #    of folders in the path) and work upwards
                    print "Doing another walk on the folder structure to ensure restored folders have correct permissions"
                    for restore_file_properties in return_restored_item_list(db_cursor, restore_options['db_table_restore_files'], 'dir'):
                        root, name = restore_file_properties['filepath'].rsplit(os.sep, 1)
                        item_to_process = BackedUpItem(root, name, db_cursor, db_conn, restore_file_properties['filetype'], s3_bucket_obj,
                                                       s3_parent_folder_path, check_file_checksum, config_section, args, encrypt, encrypt_password,
                                                       restore_options, restore_metadata=restore_file_properties)
                        item_to_process.ensure_restored_folder_permissions()
                # cleanup stuff like open DB
                db_conn.close()

            elif args.command == 'stats':
                # get DB cursor object
                db_conn = return_db_connection(dbpath)
                db_cursor = return_db_cursor(db_conn)
                return_db_stats(db_cursor, config_section)
            elif args.command == 'syncdb_remote':
                # get DB cursor object
                db_conn = return_db_connection(dbpath)
                db_cursor = return_db_cursor(db_conn)
                s3_bucket_name = get_config_value(config, config_section, 's3_bucket')
                # obtain S3 bucket object, upon which all other operations will be performed
                s3_bucket_obj = get_s3_bucket_obj(aws_access_key_id, aws_secret_access_key, s3_bucket_name)
                sync_db_from_remote_metadata(s3_bucket_obj, s3_parent_folder_path, db_conn, db_cursor)
            # the update_s3_metadata is mostly useful only when doing development work and changing metadata field names.
            elif args.command == 'update_s3_metadata':
                # get DB cursor object
                db_conn = return_db_connection(dbpath)
                db_cursor = return_db_cursor(db_conn)
                s3_bucket_name = get_config_value(config, config_section, 's3_bucket')
                # obtain S3 bucket object, upon which all other operations will be performed
                s3_bucket_obj = get_s3_bucket_obj(aws_access_key_id, aws_secret_access_key, s3_bucket_name)
                force_update_s3_metadata(s3_bucket_obj, s3_parent_folder_path, db_cursor)


# if we weren't called as a module, then run the main body of the program
if __name__ == "__main__":
    main()
