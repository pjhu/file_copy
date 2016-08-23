# -*- uft-8 -*-
import os
import os.path
import shutil
import sys
import time
import win32wnet

def netcopy(ip):
    try:
        wnet_connect(ip, 'micros', 'support')

        dst_dir = ''.join(['\\\\', ip, '\\c$\\opt'])
        if os.path.isdir(dst_dir):
            shutil.rmtree(dst_dir)
        #copytree dst_dir will be atuo created, if directory exist, copytree will failed
        shutil.copytree('C:\\script\\copydonet\\Filebeat\\', ''.join(['\\\\', ip, '\\c$\\opt\\Filebeat']))
        check_files_ok(ip)
    except:
        with open("C:\\script\\copydonet\\already.txt", "a") as handle:
            handle.write(ip + "success\n")

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

def check_files_ok(ip):
    flag = True
    for root, dirs, files in os.walk('C:\\script\\copydonet\\Filebeat', topdown=False):
        for name in files:
            dst_name = ''.join(['\\\\', ip, '\\c$\\opt\\Filebeat\\', name])
            if os.path.isfile(dst_name):
                if os.path.getsize(os.path.join(root, name)) != os.path.getsize(dst_name):
                    flag = False
            else:
                flag = False
    if flag:
        with open("C:\\script\\copydonet\\already.txt", "a") as handle:
            handle.write(ip + "success\n")
    else:
        with open("C:\\script\\copydonet\\already.txt", "a") as handle:
            handle.write(ip + "false\n")


if __name__ == '__main__':
    print time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    with open("C:\\script\\copydonet\\deploy\\1.txt") as handle:
        iplist = handle.read().splitlines()
    for ip in iplist:
        netcopy(ip)
    print time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    print 'Done'
