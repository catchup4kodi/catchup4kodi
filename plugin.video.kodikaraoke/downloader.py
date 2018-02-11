import xbmcgui,xbmc
import urllib
import time
import requests



def download(url, dest,s, dp = None):

    if not dp:
        dp = xbmcgui.DialogProgress()
        dp.create("Kodi Karaoke","",'Building Database Please Wait', ' ')
    dp.update(0)
    start=time.clock()
    r = s.get(url, stream=True)
    f = open(dest, 'wb')
    total_length = int(r.headers['Content-Length'])
    dl = 0

    for chunk in r.iter_content(1024):
        dl += len(chunk)
        DL=dl/1024
        f.write(chunk)
        done = int(50 * dl / total_length)
        
        currently_downloaded = (dl/1024)

        
        kbps_speed = DL//(time.clock() - start)
        
        if kbps_speed > 0: 
            eta = (total_length - currently_downloaded) / kbps_speed 
        else: 
            eta = 0
            
        mbs = '%.02f MB of %.02f MB' % (currently_downloaded, total_length/1024) 
        e = 'Speed: %s kb/s ' % kbps_speed 
        e += ' ETA: %02d:%02d' % divmod(eta/60/60, 60)
        dp.update(done, mbs, e)
    if dp.iscanceled(): 
        dp.close()
   
    f.close()
