# -*- uft-8 -*-
import os
import os.path
import shutil
import sys
import time
import win32wnet
from multiprocessing import Pool

def netcopy(ip, day):
    wnet_connect(ip, 'micros', 'support')

    #shutil.copy(file_path,  dest_file)
    shutil.copy(''.join(['\\\\', ip, '\\d$\\svcnew\\logs\\', day, '.log']),  ''.join(['c:\\script\\logs\\svc\\', ip, '_',day, '.log']))
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

if __name__ == '__main__':
    with open("c:\\script\\ip.txt") as handle:
        iplist = handle.read().splitlines()
    result = []
    pool = Pool(5)
    for ip in iplist:
        result.append(pool.apply_async(netcopy, (ip, '20160727')))
    pool.close()
    pool.join()

    for res in result:
        with open("c:\\script\\svc_status.txt", 'a') as handle:
            handle.write(res.get() + '\n' )
    print 'Done'    
    
                
    
