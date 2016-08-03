# -*- utf-8 -*-

import os
import os.path
import shutil
import win32wnet


def netcopy(host, source, dest_dir, username=None, password=None, move=False):
    """ Copies files or directories to a remote computer. """

    wnet_connect(host, username, password)

    dest_dir = covert_unc(host, dest_dir)

    # Pad a backslash to the destination directory if not provided.
    if not dest_dir[len(dest_dir) - 1] == '\\':
        dest_dir = ''.join([dest_dir, '\\'])

    # Create the destination dir if its not there.
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    else:
        # Create a directory anyway if file exists so as to raise an error.
        if not os.path.isdir(dest_dir):
            os.makedirs(dest_dir)

    if move:
        if os.path.isdir(source):
            shutil.copytree(source, dest_dir)
            shutil.rmtree(source)
        elif os.path.isfile(source):
            shutil.move(source, dest_dir)
        else:
            raise AssertionError, '%s is neither a file nor directory' % (source)
    else:
        if os.path.isdir(source):
            shutil.copytree(source, dest_dir)
        elif os.path.isfile(source):
            shutil.copy(source, dest_dir)
        else:
            raise AssertionError, '%s is neither a file nor directory' % (source)


def netdelete(host, path, username=None, password=None):
    """ Deletes files or directories on a remote computer. """

    wnet_connect(host, username, password)

    path = covert_unc(host, path)
    if os.path.exists(path):
        # Delete directory tree if object is a directory.
        if os.path.isfile(path):
            os.remove(path)
        else:
            shutil.rmtree(path)
    else:
        # Remove anyway if non-existent so as to raise an error.
        os.remove(path)


def netmove(host, source, dest_dir, username=None, password=None):
    return netcopy(host, source, dest_dir, username, password, True)


def covert_unc(host, path):
    """ Convert a file path on a host to a UNC path."""
    return ''.join(['\\\\', host, '\\', path.replace(':', '$')])


def wnet_connect(host, username, password):
    unc = ''.join(['\\\\', host])
    try:
        win32wnet.WNetAddConnection2(0, None, unc, None, username, password)
    except Exception, err:
        if isinstance(err, win32wnet.error):
            # Disconnect previous connections if detected, and reconnect.
            if err[0] == 1219:
                win32wnet.WNetCancelConnection2(unc, 0, 0)
                return wnet_connect(host, username, password)
        raise err


if __name__ == '__main__':
    # Copy "c:\documents" folder/file to "c:\transferred" on host "w0001".
    netcopy('w0001', 'c:\\documents', 'c:\\transferred')

    # Move with account credentials.
    netmove('w0001', 'c:\\documents', 'c:\\transferred', 'admin', 'adminpass')

    # Delete with another account.
    netdelete('w0001', 'c:\\transferred', 'testdom\\user1', 'user1pass')
