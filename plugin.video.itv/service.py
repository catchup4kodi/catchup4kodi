import os,xbmc

cache = xbmc.translatePath(os.path.join('special://temp'))

for root, dirs, files in os.walk(cache):


                
    for f in files:
        if 'cookies' in f:
            try:os.unlink(os.path.join(root, f))
            except:pass
