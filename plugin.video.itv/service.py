import os,xbmc

cache = xbmc.translatePath(os.path.join('special://home', 'cache'))

for root, dirs, files in os.walk(cache):


                
    for f in files:
        try:os.unlink(os.path.join(root, f))
        except:pass
    for d in dirs:
        try:shutil.rmtree(os.path.join(root, d))
        except:pass
