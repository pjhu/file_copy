# -*- uft-8 -*-
import os
import os.path
import shutil
import sys
import time
import datetime
import win32wnet
from multiprocessing import Pool

def netcopy(ip, num):
    wnet_connect(ip, 'micros', 'support')

    file_path = ''.join(['\\\\', ip, '\\d$\\MICROS\\Shiji\\KunlunMomSbuxCRM\\Logs\\archives\\SBUX.Loyalty.Service.', str(num), '.log'])
    
    file_date = time.strftime("%Y%m%d", time.localtime(os.path.getmtime(file_path)))

    dest_file = ''.join(['c:\\script\\logs\\msr\\', ip, '_msr_', file_date, '.log'])
    if os.path.isfile(file_path):
        shutil.copy(file_path,  dest_file)
        if os.path.getsize(file_path) == os.path.getsize(dest_file):
            print ip + " success"
        else:
            print ip + "fail"
    else:
        print ip + " file not exit"
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
    print time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    with open("c:\\script\\ip.txt") as handle:
        iplist = handle.read().splitlines()
    result = []
    pool = Pool(5)
    for ip in iplist:
        result.append(pool.apply_async(netcopy, (ip, 61)))
    pool.close()
    pool.join()

    print time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    #for res in result:
    #    with open("c:\\script\\crm_status.txt", 'a') as handle:
    #        handle.write(res.get() + '\n' )
    print 'Done'    
    
                
    
