# -*- uft-8 -*-
import os
import os.path
import shutil
import sys
import time
import datetime
import win32wnet
from multiprocessing import Pool
from shutil import ignore_patterns

def netcopy(ip, year, month, day):
    wnet_connect(ip, 'micros', 'support')
    
    shutil.copytree(''.join(['\\\\', ip, '\\d$\\svcnew\\logs\\']),  ''.join(['c:\\script\\logs\\svc\\',ip]), ignore=ignoreFiles(year, month, day))
    return ip

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

def ignoreFiles(year, month, day):
    def ignoreref(directory, filenames):
        return (f for f in filenames if datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(directory,f))) < datetime.datetime(year, month, day))
    return ignoreref
    

if __name__ == '__main__':
    with open("c:\\script\\ip.txt") as handle:
        iplist = handle.read().splitlines()
    result = []
    pool = Pool(5)
    for ip in iplist:
        result.append(pool.apply_async(netcopy, (ip, 2016, 7, 1)))
    pool.close()
    pool.join()

    #with open("c:\\script\\svc_status.txt", 'a') as handle:
    #    handle.write(ip + '\n' )
    print 'Done'    
    
                
    
