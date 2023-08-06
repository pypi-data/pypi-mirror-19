# --------------------------------------------------------------------------
# Copyright (c) 2016 Digital Sapphire
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the
# following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF
# ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR
# ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.
# --------------------------------------------------------------------------
from __future__ import unicode_literals
import gzip
import json
import logging
import os
import warnings

import appdirs
from dsdev_utils.app import FROZEN
from dsdev_utils.helpers import (EasyAccessDict as _EAD,
                                 gzip_decompress as _gzip_decompress,
                                 Version as _Version)
from dsdev_utils.logger import logging_formatter
from dsdev_utils.paths import app_cwd, ChDir as _ChDir
from dsdev_utils.system import get_system as _get_system
import ed25519
import six

from pyupdater import settings, __version__
from pyupdater.client.downloader import FileDownloader as _FD
from pyupdater.client.updates import AppUpdate, _get_highest_version, LibUpdate
from pyupdater.utils.config import Config as _Config


warnings.simplefilter('always', DeprecationWarning)


log = logging.getLogger(__name__)
log_path = os.path.join(app_cwd, 'pyu.log')
if os.path.exists(log_path):  # pragma: no cover
    ch = logging.FileHandler(os.path.join(app_cwd,
                             'pyu.log'))
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(logging_formatter)
    log.addHandler(ch)
log.debug('PyUpdater Version %s', __version__)


class Client(object):
    """Used to check for updates & returns an updateobject if there
    is an update.

    ######Kwargs:

    obj (instance): config object

    refresh (bool): True - Refresh update manifest on object initialization.
    False - Don't refresh update manifest on object initialization

    progress_hooks (list): List of callbacks

    ######Returns:

    (obj): AppUpdate or LibUpdate

    """
    def __init__(self, obj=None, refresh=False,
                 progress_hooks=None, test=False):
        # String: Name of binary to update
        self.name = None

        # String: Version of the binary to update
        self.version = None

        # String: Update manifest as json string - set in _get_update_manifest
        self.json_data = None

        # Boolean: Version file verification
        self.verified = False

        # Boolean: Json being loaded to dict
        self.ready = False

        # LIst: Progress hooks to be called
        self.progress_hooks = []
        if progress_hooks is not None:
            assert isinstance(progress_hooks, list) is True
            self.progress_hooks += progress_hooks

        # Client config obj with settings to find & verify updates
        if obj is not None:
            self.init_app(obj, refresh, test)

    def init_app(self, obj, refresh=False, test=False):
        """Sets up client with config values from obj

        ######Args:

        obj (instance): config object

        ######Kwargs:

        refresh (bool) Meaning: True - Refresh update manifest on object
        initialization. False - Don't refresh update manifest on object
        initialization

        """

        # A super dict used to save config info & be dot accessed
        config = _Config()
        config.from_object(obj)

        # Boolean: If executing frozen
        self.FROZEN = FROZEN

        # Grabbing config information
        update_urls = config.get('UPDATE_URLS', [])

        # List of URL to check for update data
        self.update_urls = self._sanatize_update_url(update_urls)

        # Name of the running application
        self.app_name = config.get('APP_NAME', 'PyUpdater')

        # Name of the app author
        self.company_name = config.get('COMPANY_NAME', 'Digital Sapphire')

        # Used in testing to force use of the mac archive
        if test:
            # Making platform deterministic for tests.
            self.data_dir = obj.DATA_DIR
            self.platform = 'mac'
        else:  # pragma: no cover
            # Getting platform specific user data directory
            self.data_dir = appdirs.user_data_dir(self.app_name,
                                                  self.company_name)

            # Used when parsing the update manifest
            self.platform = _get_system()

        # Folder to house update archives
        self.update_folder = os.path.join(self.data_dir,
                                          settings.UPDATE_FOLDER)

        # The root public key to verify the app signing private key
        self.root_key = config.get('PUBLIC_KEY', '')

        # We'll get the app_key later in _get_signing_key
        # That's if we verify the keys manifest
        self.app_key = None

        # Used to disable TLS cert verification
        self.verify = config.get('VERIFY_SERVER_CERT', True)

        # Max number of download retries
        self.max_download_retries = config.get('MAX_DOWNLOAD_RETRIES')

        # The name of the version file to download
        self.version_file = settings.VERSION_FILE_FILENAME

        # The name of the key file to download
        self.key_file = settings.KEY_FILE_FILENAME

        # Creating data & update directories
        self._setup()

        if refresh is True:
            self.refresh()

    def refresh(self):
        "Will download and verify the version manifest."
        self._get_signing_key()
        self._get_update_manifest()

    def update_check(self, name, version, channel='stable', strict=True):
        """Checks for available updates

        ######Args:

        name (str): Name of file to update

        version (str): Current version number of file to update

        channel (str): Release channel

        ######Returns:

        (updateobject) Meanings:

        AppUpdate - Used to update current binary

        LibUpdate - Used to update external assets

        None - No Updates available
        """
        return self._update_check(name, version, channel, strict)

    def _update_check(self, name, version, channel, strict):
        valid_channels = ['alpha', 'beta', 'stable']
        if channel not in valid_channels:
            log.debug('Invalid channel. May need to check spelling')
            channel = 'stable'
        self.name = name

        # Version object used for comparison
        version = _Version(version)
        self.version = str(version)

        # Will be set to true if we are updating the currently
        # running app and not an app's asset
        app = False

        if self.ready is False:
            # No json data is loaded.
            # User may need to call refresh
            log.debug('No update manifest found')
            return None

        # Checking if version file is verified before
        # processing data contained in the version file.
        # This was done by self._get_update_manifest
        if self.verified is False:
            log.debug('Failed version file verification')
            return None

        # If we are an app we will need restart functionality, so we'll
        # user AppUpdate instead of LibUpdate
        if self.FROZEN is True and self.name == self.app_name:
            app = True

        log.debug('Checking for %s updates...', name)
        latest = _get_highest_version(name, self.platform,
                                      channel, self.easy_data, strict)
        if latest is None:
            # If None is returned _get_highest_version could
            # not find the supplied name in the version file
            log.debug('Could not find the latest version')
            return None

        # Change str to version object for easy comparison
        latest = _Version(latest)
        log.debug('Current version: %s', str(version))
        log.debug('Latest version: %s', str(latest))

        update_needed = latest > version
        log.debug('Update Needed: %s', update_needed)
        if latest <= version:
            log.debug('%s already updated to the latest version', name)
            return None

        # Config data to initialize update object
        data = {
            'strict': strict,
            'update_urls': self.update_urls,
            'name': self.name,
            'version': self.version,
            'easy_data': self.easy_data,
            'json_data': self.json_data,
            'data_dir': self.data_dir,
            'platform': self.platform,
            'channel': channel,
            'app_name': self.app_name,
            'verify': self.verify,
            'max_download_retries': self.max_download_retries,
            'progress_hooks': list(set(self.progress_hooks)),
            }

        # Return update object with which handles downloading,
        # extracting updates
        if app is True:
            # AppUpdate objects also has methods to restart
            # the app with the new version
            return AppUpdate(data)
        else:
            return LibUpdate(data)

    def add_progress_hook(self, cb):
        """Add a download progress callback function to the list of progress
        hooks.

        total:  Total size of the file to download

        downloaded: The amount of bytes that have been downloaded so far.

        percent_complete: The percentage downloaded so far

        status: Status of download

        Args:

        cb (function): Function which takes a dict as its first argument
        """
        self.progress_hooks.append(cb)

    def _get_signing_key(self):
        key_data_str = self._download_key()
        if key_data_str is None:
            return

        key_data = json.loads(key_data_str.decode('utf-8'))
        pub_key = key_data['app_public']
        if six.PY3:
            if not isinstance(pub_key, bytes):
                pub_key = bytes(pub_key, encoding='utf-8')
        else:
            pub_key = str(pub_key)

        sig = key_data['signature']
        signing_key = ed25519.VerifyingKey(self.root_key, encoding='base64')

        try:
            signing_key.verify(sig, pub_key, encoding='base64')
        except Exception as err:
            log.debug('Key file not verified')
            log.debug(err, exc_info=True)
        else:
            log.debug('Key file verified')
            self.app_key = pub_key

    # Here we attempt to read the manifest from the filesystem
    # in case of no Internet connection. Useful when an update
    # needs to be installed without an network connection
    def _get_manifest_filesystem(self):
        data = None
        with _ChDir(self.data_dir):
            if not os.path.exists(self.version_file):
                log.debug('No version file on file system')
                return data
            else:
                log.debug('Found version file on file system')
                try:
                    with open(self.version_file, 'rb') as f:
                        data = f.read()
                    log.debug('Loaded version file from file system')
                except Exception as err:
                    # Whatever the error data is already set to None
                    log.debug('Failed to load version file from file '
                              'system')
                    log.debug(err, exc_info=True)
                # In case we don't have any data to pass
                # Catch the error here and just return None
                try:
                    decompressed_data = _gzip_decompress(data)
                except Exception as err:
                    decompressed_data = None

                return decompressed_data

    # Downloading the manifest. If successful also writes it to file-system
    def _download_manifest(self):
        log.debug('Downloading online version file')
        try:
            fd = _FD(self.version_file, self.update_urls,
                                verify=self.verify)
            data = fd.download_verify_return()
            try:
                decompressed_data = _gzip_decompress(data)
            except IOError:
                log.debug('Failed to decompress gzip file')
                # Will be caught down below.
                # Just logging the error
                raise
            log.debug('Version file download successful')
            # Writing version file to application data directory
            self._write_manifest_2_filesystem(decompressed_data)
            return decompressed_data
        except Exception as err:
            log.debug('Version file download failed')
            log.debug(err, exc_info=True)
            return None

    # Downloading the key file.
    def _download_key(self):
        log.debug('Downloading key file')
        try:
            fd = _FD(self.key_file, self.update_urls,
                                verify=self.verify)
            data = fd.download_verify_return()
            try:
                decompressed_data = _gzip_decompress(data)
            except IOError:
                log.debug('Failed to decompress gzip file')
                # Will be caught down below. Just logging the error
                raise
            log.debug('Key file download successful')
            # Writing version file to application data directory
            self._write_manifest_2_filesystem(decompressed_data)
            return decompressed_data
        except Exception as err:
            log.debug('Version file download failed')
            log.debug(err, exc_info=True)
            return None

    def _write_manifest_2_filesystem(self, data):
        with _ChDir(self.data_dir):
            log.debug('Writing version file to disk')
            with gzip.open(self.version_file, 'wb') as f:
                f.write(data)

    def _get_update_manifest(self):
        #  Downloads & Verifies version file signature.
        log.debug('Loading version file...')

        data = self._download_manifest()
        if data is None:
            # Get the last downloaded manifest
            data = self._get_manifest_filesystem()

        if data is not None:
            try:
                log.debug('Data type: %s', type(data))
                # If json fails to load self.ready will stay false
                # which will cause _update_check to exit early
                self.json_data = json.loads(data.decode('utf-8'))

                # Ready to check for updates.
                self.ready = True
            except ValueError as err:
                # Malformed json???
                log.debug('Json failed to load: ValueError')
                log.debug(err, exc_info=True)
            except Exception as err:
                # Catch all for debugging purposes.
                # If seeing this line come up a lot in debug logs
                # please open an issue on github or submit a pull request
                log.debug(err, exc_info=True)
        else:
            log.debug('Failed to download version file & no '
                      'version file on filesystem')
            self.json_data = {}

        # If verified we set self.verified to True.
        self._verify_sig(self.json_data)

        self.easy_data = _EAD(self.json_data)
        log.debug('Version Data:\n%s', str(self.easy_data))

    def _verify_sig(self, data):
        if self.app_key is None:
            log.debug('App key is None')
            return

        # Checking to see if there is a signature key in the version file.
        if 'signature' in data.keys():
            signature = data['signature']
            log.debug('Deleting signature from update data')
            del data['signature']

            # After removing the signatures we turn the json data back
            # into a string to use as data to verify the sig.
            update_data = json.dumps(data, sort_keys=True)

            pub_key = ed25519.VerifyingKey(self.app_key, encoding='base64')
            if six.PY3:
                if not isinstance(update_data, bytes):
                    update_data = bytes(update_data, encoding='utf-8')
            try:
                pub_key.verify(signature, update_data, encoding='base64')
            except Exception as err:
                log.debug('Version file not verified')
                log.debug(err, exc_info=True)
            else:
                log.debug('Version file verified')
                self.verified = True
        else:
            log.debug('Signature not in update data')

    def _setup(self):
        # Create required directories on end-users computer
        # to place verified update data
        # Very safe director maker :)
        log.debug('Setting up directories...')
        dirs = [self.data_dir, self.update_folder]
        for d in dirs:
            if not os.path.exists(d):
                log.debug('Creating directory: %s', d)
                os.makedirs(d)

    # Legacy code used when migrating from single urls to
    # A list of urls
    def _sanatize_update_url(self, urls):
        sanatized_urls = []
        # Adds trailing slash to end of url if not already provided.
        # Doing this so when requesting online resources we only
        # need to add the resouce name to the end of the request.
        for u in urls:
            if not u.endswith('/'):
                sanatized_urls.append(u + '/')
            else:
                sanatized_urls.append(u)
        # Removing duplicates
        return list(set(sanatized_urls))
