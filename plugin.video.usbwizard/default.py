import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,sys
import shutil
import urllib2,urllib
import re
import extract
import time


ADDON        =  xbmcaddon.Addon(id='plugin.video.usbwizard')
zip          =  ADDON.getSetting('zip')
dialog       =  xbmcgui.Dialog()
dp           =  xbmcgui.DialogProgress()
USERDATA     =  xbmc.translatePath(os.path.join('special://home/userdata',''))
ADDON_DATA   =  xbmc.translatePath(os.path.join(USERDATA,'addon_data'))
ADDONS       =  xbmc.translatePath(os.path.join('special://home','addons'))
GUI          =  xbmc.translatePath(os.path.join(USERDATA,'guisettings.xml'))
FAVS         =  xbmc.translatePath(os.path.join(USERDATA,'favourites.xml'))
SOURCE       =  xbmc.translatePath(os.path.join(USERDATA,'sources.xml'))
ADVANCED     =  xbmc.translatePath(os.path.join(USERDATA,'advancedsettings.xml'))
RSS          =  xbmc.translatePath(os.path.join(USERDATA,'RssFeeds.xml'))
KEYMAPS      =  xbmc.translatePath(os.path.join(USERDATA,'keymaps','keyboard.xml'))
USB          =  xbmc.translatePath(os.path.join(zip))
skin         =  xbmc.getSkinDir()
THEPACKAGE       =  xbmc.translatePath(os.path.join('special://home','addons','packages'))
THEHTML = xbmc.translatePath(os.path.join(ADDON.getAddonInfo('path'),'theemail.html'))


if zip=='' and ADDON.getSetting('email')=='':
    if dialog.yesno("USB BACKUP/RESTORE", "You Have Not Set Your Storage Path", 'Set The Storage Path Now ?',''):
        ADDON.openSettings()


def XfinityInstaller():
    path = os.path.join(xbmc.translatePath('special://home'),'userdata', 'sources.xml')
    if not os.path.exists(path):
        f = open(path, mode='w')
        f.write('<sources><files><source><name>.[COLOR blue]X[/COLOR]finity Installer</name><path pathversion="1">http://xunitytalk.me/xfinity</path></source></files></sources>')
        f.close()
        return
        
    f   = open(path, mode='r')
    str = f.read()
    f.close()
    if not'xunitytalk.me/xfinity' in str:
        if '</files>' in str:
            str = str.replace('</files>','<source><name>.[COLOR blue]X[/COLOR]finity Installer</name><path pathversion="1">http://xunitytalk.me/xfinity</path></source></files>')
            f = open(path, mode='w')
            f.write(str)
            f.close()
        else:
            str = str.replace('</sources>','<files><source><name>.[COLOR blue]X[/COLOR]finity Installer</name><path pathversion="1">http://xunitytalk.me/xfinity</path></source></files></sources>')
            f = open(path, mode='w')
            f.write(str)
            f.close()

    
def BACKUP():  
    if zip == '':
        dialog.ok('USB BACKUP/RESTORE','You have not set your ZIP Folder or Email\nPlease update the addon settings and try again.','','')
        ADDON.openSettings(sys.argv[0])
    to_backup = xbmc.translatePath(os.path.join('special://','home'))
    backup_zip = xbmc.translatePath(os.path.join(USB,'backup.zip'))
    DeletePackages()    
    import zipfile
    
    dp.create("USB BACKUP/RESTORE","Backing Up",'', 'Please Wait')
    zipobj = zipfile.ZipFile(backup_zip , 'w', zipfile.ZIP_DEFLATED)
    rootlen = len(to_backup)
    for_progress = []
    ITEM =[]
    for base, dirs, files in os.walk(to_backup):
        for file in files:
            ITEM.append(file)
    N_ITEM =len(ITEM)
    for base, dirs, files in os.walk(to_backup):
        for file in files:
            for_progress.append(file) 
            progress = len(for_progress) / float(N_ITEM) * 100  
            dp.update(int(progress),"Backing Up",'[COLOR yellow]%s[/COLOR]'%file, 'Please Wait')
            fn = os.path.join(base, file)
            if not 'temp' in dirs:
                if not 'plugin.video.usbwizard' in dirs:
                   import time
                   CUNT= '01/01/1980'
                   FILE_DATE=time.strftime('%d/%m/%Y', time.gmtime(os.path.getmtime(fn)))
                   if FILE_DATE > CUNT:
                       zipobj.write(fn, fn[rootlen:])  
    zipobj.close()
    dp.close()
    dialog.ok("USB BACKUP/RESTORE", "You Are Now Backed Up", '','')
    
      
def READ_ZIP(url):

    import zipfile
    
    z = zipfile.ZipFile(url, "r")
    for filename in z.namelist():
        if 'guisettings.xml' in filename:
            a = z.read(filename)
            r='<setting type="(.+?)" name="%s.(.+?)">(.+?)</setting>'% skin
            
            match=re.compile(r).findall(a)
            
            for type,string,setting in match:
                setting=setting.replace('&quot;','') .replace('&amp;','&') 
                xbmc.executebuiltin("Skin.Set%s(%s,%s)"%(type.title(),string,setting))  
                
        if 'favourites.xml' in filename:
            a = z.read(filename)
            f = open(FAVS, mode='w')
            f.write(a)
            f.close()  
			               
        if 'sources.xml' in filename:
            a = z.read(filename)
            f = open(SOURCE, mode='w')
            f.write(a)
            f.close()    
                         
        if 'advancedsettings.xml' in filename:
            a = z.read(filename)
            f = open(ADVANCED, mode='w')
            f.write(a)
            f.close()                 

        if 'RssFeeds.xml' in filename:
            a = z.read(filename)
            f = open(RSS, mode='w')
            f.write(a)
            f.close()                 
            
        if 'keyboard.xml' in filename:
            a = z.read(filename)
            f = open(KEYMAPS, mode='w')
            f.write(a)
            f.close()                 
              
def RESTORE():

    import time
    dialog = xbmcgui.Dialog()
    if zip == '' and ADDON.getSetting('email')=='':
        dialog.ok('USB BACKUP/RESTORE','You have not set your ZIP Folder.\nPlease update the addon settings and try again.','','')
        ADDON.openSettings(sys.argv[0])
        
    lib=xbmc.translatePath(os.path.join(zip,'backup.zip'))
    READ_ZIP(lib)
    dp.create("USB BACKUP/RESTORE","Checking ",'', 'Please Wait')
    HOME = xbmc.translatePath(os.path.join('special://','home'))
    
    dp.update(0,"", "Extracting Zip Please Wait")
    extract.all(lib,HOME,dp)
    time.sleep(1)
    XfinityInstaller()
    xbmc.executebuiltin('UpdateLocalAddons ')    
    xbmc.executebuiltin("UpdateAddonRepos")
    time.sleep(1)
    xbmc.executebuiltin('UnloadSkin()') 
    xbmc.executebuiltin('ReloadSkin()')
    Kodi17()
    dialog.ok("USB BACKUP/RESTORE", "PLEASE REBOOT YOUR BOX IF HOMESCREEN HAS NOT CHANGED", "","")
    xbmc.executebuiltin("LoadProfile(Master user)")
    

    
    
def CATEGORIES():
    addDir('Backup','url',1,'','Back Up Your Full System')
    addDir('Restore','url',5,'','Restore Your Full System')
    #addDir('Fix Repos Not Downloading Properly','url',1000,'','Restore Your Full System')
    if not ADDON.getSetting('email_pass_1')=='':
        addDir('Reset Email Pass','url',10,'','Reset Email Pass')


def BACKUP_OPTION():
    if not zip == '': 
        addDir('FULL BACKUP','url',3,'','Back Up Your Full System')
        addDir('Backup Just Your Addons','addons',6,'','Back Up Your Addons')
        addDir('Backup Just Your Addon UserData','addon_data',6,'','Back Up Your Addon Userdata')  
        addDir('Backup Guisettings.xml',GUI,4,'','Back Up Your guisettings.xml')
        if os.path.exists(FAVS):
            addDir('Backup Favourites.xml',FAVS,4,'','Back Up Your favourites.xml')
        if os.path.exists(SOURCE):
            addDir('Backup Source.xml',SOURCE,4,'','Back Up Your sources.xml')
        if os.path.exists(ADVANCED):
            addDir('Backup Advancedsettings.xml',ADVANCED,4,'','Back Up Your advancedsettings.xml')
        if os.path.exists(KEYMAPS):
            addDir('Backup Advancedsettings.xml',KEYMAPS,4,'','Back Up Your keyboard.xml')
        if os.path.exists(RSS):
            addDir('Backup RssFeeds.xml',RSS,4,'','Back Up Your RssFeeds.xml')
    
    if not ADDON.getSetting('email')=='':   
        addDir('[COLOR green]Backup And Email Me My Addons[/COLOR]','addons.zip',9,'','Restore Your Addons')

        
    if not ADDON.getSetting('email')=='':   
        addDir('[COLOR orange]Backup And Email Me My UserData[/COLOR]','addon_data.zip',9,'','Restore Your Addon UserData')


def RESTORE_OPTION():
    if os.path.exists(os.path.join(USB,'backup.zip')):   
        addDir('FULL RESTORE','url',2,'','Back Up Your Full System')
        
    if os.path.exists(os.path.join(USB,'addons.zip')):   
        addDir('Restore Your Addons','addons',6,'','Restore Your Addons')

        
    if os.path.exists(os.path.join(USB,'addon_data.zip')):   
        addDir('Restore Your Addon UserData','addon_data',6,'','Restore Your Addon UserData')

    if not ADDON.getSetting('email')=='':   
        addDir('[COLOR green]Restore Your Addons Via Your Email[/COLOR]','addons.zip',8,'','Restore Your Addons')

        
    if not ADDON.getSetting('email')=='':   
        addDir('[COLOR orange]Restore Your UserData Via Your Email[/COLOR]','addon_data.zip',8,'','Restore Your Addon UserData') 

    if os.path.exists(os.path.join(USB,'guisettings.xml')):
        addDir('Restore Guisettings.xml',GUI,4,'','Restore Your guisettings.xml')
    
    if os.path.exists(os.path.join(USB,'favourites.xml')):
        addDir('Restore Favourites.xml',FAVS,4,'','Restore Your favourites.xml')
        
    if os.path.exists(os.path.join(USB,'sources.xml')):
        addDir('Restore Source.xml',SOURCE,4,'','Restore Your sources.xml')
        
    if os.path.exists(os.path.join(USB,'advancedsettings.xml')):
        addDir('Restore Advancedsettings.xml',ADVANCED,4,'','Restore Your advancedsettings.xml')        

    if os.path.exists(os.path.join(USB,'keyboard.xml')):
        addDir('Restore Advancedsettings.xml',KEYMAPS,4,'','Restore Your keyboard.xml')
        
    if os.path.exists(os.path.join(USB,'RssFeeds.xml')):
        addDir('Restore RssFeeds.xml',RSS,4,'','Restore Your RssFeeds.xml')    


def RESTORE_ZIP_FILE(name,url):

    
    if zip == '' and ADDON.getSetting('email')=='':
        dialog.ok('USB BACKUP/RESTORE','You have not set your ZIP Folder.\nPlease update the addon settings and try again.','','')
        ADDON.openSettings(sys.argv[0])
        
    if 'addons' in url:
        ZIPFILE = xbmc.translatePath(os.path.join(USB,'addons.zip'))
        DIR = ADDONS
        to_backup = ADDONS
        
        backup_zip = xbmc.translatePath(os.path.join(USB,'addons.zip'))
    else:
        ZIPFILE = xbmc.translatePath(os.path.join(USB,'addon_data.zip'))
        DIR = ADDON_DATA

        
    if 'Backup' in name:
        DeletePackages() 
        import zipfile
        import sys
        dp.create("USB BACKUP/RESTORE","Backing Up",'', 'Please Wait')
        zipobj = zipfile.ZipFile(ZIPFILE , 'w', zipfile.ZIP_DEFLATED)
        rootlen = len(DIR)
        for_progress = []
        ITEM =[]
        for base, dirs, files in os.walk(DIR):
            for file in files:
                ITEM.append(file)
        N_ITEM =len(ITEM)
        for base, dirs, files in os.walk(DIR):
            for file in files:
                for_progress.append(file) 
                progress = len(for_progress) / float(N_ITEM) * 100  
                dp.update(int(progress),"Backing Up",'[COLOR yellow]%s[/COLOR]'%file, 'Please Wait')
                fn = os.path.join(base, file)
                if not 'temp' in dirs:
                    if not 'plugin.video.usbwizard' in dirs:
                       import time
                       CUNT= '01/01/1980'
                       FILE_DATE=time.strftime('%d/%m/%Y', time.gmtime(os.path.getmtime(fn)))
                       if FILE_DATE > CUNT:
                           zipobj.write(fn, fn[rootlen:]) 
        zipobj.close()
        dp.close()
        dialog.ok("USB BACKUP/RESTORE", "You Are Now Backed Up", '','')   
    else:

        dp.create("USB BACKUP/RESTORE","Checking ",'', 'Please Wait')
        
        import time
        dp.update(0,"", "Extracting Zip Please Wait")
        extract.all(ZIPFILE,DIR,dp)
        
        time.sleep(1)
        XfinityInstaller()
        xbmc.executebuiltin('UpdateLocalAddons ')    
        xbmc.executebuiltin("UpdateAddonRepos")
        Kodi17()
        dialog.ok("USB BACKUP/RESTORE", "You Are Now Restored", '','')


def Kodi17():
    xbmc_version =  re.search('^(\d+)', xbmc.getInfoLabel( "System.BuildVersion" ))
    if xbmc_version:
        xbmc_version = int(xbmc_version.group(1))
    else:
        xbmc_version = 1
        
    if xbmc_version >= 16.9:
            dependencies = []
            
            import glob


            folder = xbmc.translatePath('special://home/addons/')

            for DEPEND in glob.glob(folder+'*.*'):
                try:dependencies.append(DEPEND.rsplit('\\', 1)[1])
                except:dependencies.append(DEPEND.rsplit('/', 1)[1])


            for THEPLUGIN in dependencies:
              
                query = '{"jsonrpc":"2.0", "method":"Addons.SetAddonEnabled","params":{"addonid":"%s","enabled":true}, "id":1}' % (THEPLUGIN)
             
                xbmc.executeJSONRPC(query)
        
            xbmc.executebuiltin('UpdateLocalAddons') 
            xbmc.executebuiltin("UpdateAddonRepos")
        
        

def RESTORE_BACKUP_XML(name,url,description):
    if 'Backup' in name:
        TO_READ   = open(url).read()
        TO_WRITE  = os.path.join(USB,description.split('Your ')[1])
        
        f = open(TO_WRITE, mode='w')
        f.write(TO_READ)
        f.close() 
         
    else:
    
        if 'guisettings.xml' in description:
            a = open(os.path.join(USB,description.split('Your ')[1])).read()
            
            r='<setting type="(.+?)" name="%s.(.+?)">(.+?)</setting>'% skin
            
            match=re.compile(r).findall(a)
            
            for type,string,setting in match:
                setting=setting.replace('&quot;','') .replace('&amp;','&') 
                xbmc.executebuiltin("Skin.Set%s(%s,%s)"%(type.title(),string,setting))  
        else:    
            TO_WRITE   = os.path.join(url)
            TO_READ  = open(os.path.join(USB,description.split('Your ')[1])).read()
            
            f = open(TO_WRITE, mode='w')
            f.write(TO_READ)
            f.close()  
    dialog.ok("USB BACKUP/RESTORE", "", 'All Done !','')


def DeletePackages():
    xbmc.log( '############################################################       DELETING PACKAGES             ###############################################################')
    packages_cache_path = xbmc.translatePath(os.path.join('special://home/addons/packages', ''))
 
    for root, dirs, files in os.walk(packages_cache_path):
        file_count = 0
        file_count += len(files)
        
    # Count files and give option to delete
        if file_count > 0:
                        
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))

                

def Numeric():
        dialog = xbmcgui.Dialog()
        keyboard=dialog.numeric(0, 'Secret 4 Digits')
        return keyboard   

def EmailPass():
    search_entered = ''
    keyboard = xbmc.Keyboard(search_entered, 'Please Enter Email Password')
    keyboard.setHiddenInput(True)
    keyboard.doModal()
    if keyboard.isConfirmed():
        return keyboard.getText()

  


    
def DecryptPass():
    import os, pyaes,hashlib
    key = hashlib.md5(Numeric()).hexdigest()[:16]
    aes = pyaes.AESModeOfOperationCTR (key)
    decrypted = aes.decrypt(ADDON.getSetting('email_pass_1'))
    return decrypted


def EncryptPass(password):
    import os, pyaes,hashlib
    key = hashlib.md5(Numeric()).hexdigest()[:16]
    aes = pyaes.AESModeOfOperationCTR (key)
    encrypted = aes.encrypt (password)
    ADDON.setSetting('email_pass_1',encrypted)


def ResetPass():   
    ADDON.setSetting('email_pass_1','')
    dialog.ok('USB BACKUP/RESTORE','Pass Reset','','')


    
####################################### EMAILING ##################################################
###################################################################################################
            

def getMessage():
    a='''Seems you are using gmail and havent enabled insecure apps on your google account\n\nSimply Log into your acount online once logged in visit:\n\n[COLOR royalblue]https://www.google.com/settings/security/lesssecureapps[/COLOR]\n\nAnd "Turn On" Access for less secure apps\n\n\nThen This Emailer Will Work :)\n\nThanks\nTeam [COLOR royalblue]X[/COLOR]unity[COLOR royalblue]T[/COLOR]alk'''
    return a


def send_email(TOWHO,LOG):
    PASSWORD=EmailPass()
    import zipfile
    dp = xbmcgui.DialogProgress()
    dp.create("USB BACKUP/RESTORE",'Logging Into Your Email')
    dp.update(0)
    THESMTP ,THEPORT = Servers()
    
    #zf = zipfile.ZipFile(LOG)
    fromaddr=ADDON.getSetting('email')
    toaddr=fromaddr
    try:filename = LOG.rsplit('\\', 1)[1]
    except:filename = LOG.rsplit('/', 1)[1]
   
    import datetime
    TODAY=datetime.datetime.today().strftime('[%d-%m-%Y %H:%M]')
    from email import encoders
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEText import MIMEText
    from email.mime.base import MIMEBase
    fromaddr = '"Hi Message From Yourself" <%s>'% (fromaddr)
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Your "+filename +'  '+str(TODAY)
 
    body = open(THEHTML).read()

    content = MIMEText(body, 'html')
    msg.attach(content)
    part = MIMEBase('application', 'zip')
    part.set_payload(open(LOG,'rb').read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"'%filename)
    msg.attach(part)
    import smtplib
    server = smtplib.SMTP(str(THESMTP), int(THEPORT))
    dp.update(50, 'Attaching Your Email',filename)
    server.ehlo()
    server.starttls()
    server.ehlo()
    try:server.login(ADDON.getSetting('email').encode('UTF-8'),PASSWORD.encode('UTF-8'))
    except Exception as e:
        if 'gmail' in THESMTP:
            if '/answer/787' in str(e):
                e=getMessage()
        return showText('[COLOR red]ERROR !![/COLOR]',str(e).replace('\\n','[CR]'))
    text = msg.as_string()
    dp.update(75, 'Sending........',filename.replace('log','txt'))
    try:server.sendmail(fromaddr, toaddr, text)
    except Exception as e:
        if 'gmail' in THESMTP:
            if '/answer/787' in str(e):
                e=getMessage()
        return showText('[COLOR red]ERROR !![/COLOR]',str(e).replace('\\n','[CR]'))
    dp.close()
    Show_Dialog('Email Sent To','[COLOR green]'+toaddr+'[/COLOR]','Also Check Junk Folder')


def Servers():
    SERVER = ADDON.getSetting('server')
    APPENDED=[]
    server_list   =[('Gmail','smtp.gmail.com','587'),
                    ('Outlook/Hotmail','smtp-mail.outlook.com','587'),
                    ('Office365','smtp.office365.com','587'),
                    ('Yahoo Mail','smtp.mail.yahoo.com','465'),
                    ('Yahoo Mail Plus','smtp.mail.yahoo.co.uk','465'),
                    ('Yahoo Mail Deutschland','smtp.mail.yahoo.com','465'),
                    ('Yahoo Mail AU/NZ','smtp.mail.yahoo.au','465'),
                    ('AOL','smtp.att.yahoo.com','465'),
                    ('NTL @ntlworld','smtp.ntlworld.com','465'),
                    ('BT Connect','smtp.btconnect.com','25'),
                    ('O2 Deutschland','smtp.1and1.com','587'),
                    ('1&1 Deutschland','smtp.1und1.de','587'),
                    ('Verizon','smtp.zoho.com','465'),
                    ('Mail','smtp.mail.com','587'),
                    ('GMX','smtp.gmx.com','465'),
                    ('Custom',ADDON.getSetting('custom_server'),ADDON.getSetting('custom_port'))]
    
    for server , smtp ,port in server_list:
        if SERVER ==server:
            APPENDED.append([smtp ,port])
            
    return  APPENDED[0][0],APPENDED[0][1]



def EmailLog(url):
    if ADDON.getSetting('email')=='':
        Show_Dialog('','You Need To Enter Your Email Details','')
        ADDON.openSettings()   
    send_email(ADDON.getSetting('email'),url)


def showText(heading, text):
    id = 10147

    xbmc.executebuiltin('ActivateWindow(%d)' % id)
    xbmc.sleep(100)

    win = xbmcgui.Window(id)

    retry = 50
    while (retry > 0):
        try:
            xbmc.sleep(10)
            retry -= 1
            win.getControl(1).setLabel(heading)
            win.getControl(5).setText(text)
            return
        except:
            pass

def DownloadAttachment(THEFILE):
    import email
    import imaplib
    passwd = EmailPass()#.encode('UTF-8')
   
    dp.create("USB BACKUP/RESTORE","Login To Email ",'', 'Please Wait')
    userName = ADDON.getSetting('email').encode('UTF-8')

    THESMTP ,THEPORT = Servers()
    ATTACH=[]
    nameSelect=[]
    try:
        imapSession = imaplib.IMAP4_SSL(THESMTP.replace('smtp','imap'))
        typ, accountDetails = imapSession.login(userName, passwd)
        if typ != 'OK':
            return dialog.ok('USB BACKUP/RESTORE','Not able to sign in!','','')
            
            
        
        imapSession.select('INBOX')
        typ, data = imapSession.search(None, '(Subject "%s")' % THEFILE)
        if typ != 'OK':
            return dialog.ok('USB BACKUP/RESTORE','Error searching Inbox.','','')
            
        
        # Iterating over all emails
        dp.update(25, 'Searching Email For........','')
        for msgId in data[0].split():
            typ, messageParts = imapSession.fetch(msgId, '(RFC822)')
            if typ != 'OK':
                return dialog.ok('USB BACKUP/RESTORE','Error fetching mail.','','')
           
                

            emailBody = messageParts[0][1]
            mail = email.message_from_string(emailBody)
            for part in mail.walk():
                if part.get_content_maintype() == 'multipart':
                    # print part.as_string()
                    continue
                if part.get('Content-Disposition') is None:
                    # print part.as_string()
                    continue
                fileName = part.get_filename()
                msg=email.message_from_string(messageParts[0][1])
                THESUBJECT=msg["Subject"]  
                dp.update(50, 'Searching Email For........',fileName)
                if bool(fileName):
                    filePath = xbmc.translatePath(os.path.join('special://home','addons','packages',fileName))
                    
                    if THEFILE in fileName:
                        nameSelect.append(THESUBJECT.split('Your ')[1])
                        ATTACH.append(filePath)
                        dp.update(75, 'Searching Email For........',fileName)

                        
        nameSelect.append('[COLOR red]Cancel[/COLOR]')
        ATTACH.append('[COLOR red]Cancel[/COLOR]')
        dp.update(100, 'Found','')
        ATTACHR = [i for i in reversed(ATTACH)]
        nameSelectR = [i for i in reversed(nameSelect)]
        LOCATION = ATTACHR[xbmcgui.Dialog().select('Please Select File', nameSelectR)]
        if not 'Cancel' in LOCATION:
            fp = open(LOCATION, 'wb')
            fp.write(part.get_payload(decode=True))
            fp.close()
            
            imapSession.close()
            imapSession.logout()

            RESTORE_EMAIL_FILE(LOCATION)
        else:
            imapSession.close()
            imapSession.logout()
    except Exception as e:
        if 'gmail' in THESMTP:
            if '/answer/787' in str(e):
                e=getMessage()
        return showText('[COLOR red]ERROR !![/COLOR]',str(e).replace('\\n','[CR]'))
    


def BackupEmail(url):
    import os,zipfile,glob,os,re
    
    dp.create("USB BACKUP/RESTORE","Backing Up",'', 'Please Wait')
    TEMP=xbmc.translatePath(os.path.join(THEPACKAGE,'foremail'))
    if os.path.exists(TEMP)==False:
        os.makedirs(TEMP)
        
    if 'addons.zip' in url:
        ZIPFILE = xbmc.translatePath(os.path.join(TEMP,'addons.zip'))
        DIR = TEMP
        #to_backup = ADDONS
       
   
        

        dependencies=[]
        for DEPEND in glob.glob(os.path.join(ADDONS,'*.*')):
          
            if not '.zip' in DEPEND:
                if not 'script.icechannel' in DEPEND:
                    if not 'istream' in DEPEND:
                        if not 'plugin.video.nhlgcl' in DEPEND:
                            if not 'plugin.video.mlbtv' in DEPEND:
                                if not 'plugin.video.nba' in DEPEND:
                                    if not 'plugin.video.espn-player' in DEPEND:
                                        if not 'plugin.video.salts' in DEPEND:
                                            if not 'exodus' in DEPEND:
                                                try:dependencies.append(DEPEND.rsplit('\\', 1)[1])
                                                except:dependencies.append(DEPEND.rsplit('/', 1)[1])


        for THEPLUGIN in dependencies:
            if not 'icechannel' in THEPLUGIN or not 'istream' in THEPLUGIN:
                TEMPPATH=xbmc.translatePath(os.path.join(TEMP,THEPLUGIN))
                TEMPXML =xbmc.translatePath(os.path.join(TEMPPATH,'addon.xml'))
                if os.path.exists(TEMPPATH)==False:
                    os.makedirs(TEMPPATH)
                   
                a=open(xbmc.translatePath(os.path.join(ADDONS,THEPLUGIN,'addon.xml'))).read()
                if 'Team Kodi' in a:
                    try:
                        os.remove(TEMPPATH)
                    except:
                        shutil.rmtree(TEMPPATH)
                else:
                    if 'repository.' in THEPLUGIN:
                        f = open(TEMPXML, mode='w')
                        f.write(a)
                        f.close()
                        
                    else:
                        
                        r='id="%s".+?version.+?"(.+?)"' %THEPLUGIN
                        match=re.compile(r,re.DOTALL).findall(a)[0]
                       
                        f = open(TEMPXML, mode='w')
                        f.write(a.replace(match,'0.0.1'))
                        f.close()
            
        zipobj = zipfile.ZipFile(ZIPFILE , 'w', zipfile.ZIP_DEFLATED)
        rootlen = len(DIR)
        for_progress = []
        ITEM =[]
        for base, dirs, files in os.walk(DIR):
            for file in files:
                ITEM.append(file)
        N_ITEM =len(ITEM)
        for base, dirs, files in os.walk(DIR):
            for file in files:
                for_progress.append(file) 
                progress = len(for_progress) / float(N_ITEM) * 100  
                dp.update(int(progress),"Backing Up",'[COLOR yellow]%s[/COLOR]'%file, 'Please Wait')
                fn = os.path.join(base, file)
                if not 'temp' in dirs:
                    if not 'plugin.video.usbwizard' in dirs:
                        import time
                        CUNT= '01/01/1980'
                        FILE_DATE=time.strftime('%d/%m/%Y', time.gmtime(os.path.getmtime(fn)))
                        if FILE_DATE > CUNT:
                            zipobj.write(fn, fn[rootlen:]) 
    else:
        ZIPFILE = xbmc.translatePath(os.path.join(TEMP,'addon_data.zip'))
        DIR = ADDON_DATA
        

        

            
        zipobj = zipfile.ZipFile(ZIPFILE , 'w', zipfile.ZIP_DEFLATED)
        rootlen = len(DIR)
        for_progress = []
        ITEM =[]
        for base, dirs, files in os.walk(DIR):
            for file in files:
                ITEM.append(file)
        N_ITEM =len(ITEM)
        for base, dirs, files in os.walk(DIR):
            for file in files:
                for_progress.append(file) 
                progress = len(for_progress) / float(N_ITEM) * 100  
                dp.update(int(progress),"Backing Up",'[COLOR yellow]%s[/COLOR]'%file, 'Please Wait')
                fn = os.path.join(base, file)
                if not 'temp' in dirs:
                    if not 'plugin.video.usbwizard' in dirs:

                       if not '.js' in file:
                           if not 'guide' in fn:
                               if not 'exodus' in fn:
                                   if not 'salts' in fn:
                                       if not 'specto' in fn: 
                                           import time
                                           CUNT= '01/01/1980'
                                           FILE_DATE=time.strftime('%d/%m/%Y', time.gmtime(os.path.getmtime(fn)))
                                           if FILE_DATE > CUNT:
                                               zipobj.write(fn, fn[rootlen:]) 
    zipobj.close()
    dp.close()
    EmailLog(ZIPFILE)
    DeletePackages() 
    

def RESTORE_EMAIL_FILE(ZIPFILE):
    
    if 'addons.zip' in ZIPFILE:
        DIR = ADDONS
        to_backup = ADDONS

    else:
        DIR = ADDON_DATA

    dp.create("USB BACKUP/RESTORE","Checking ",'', 'Please Wait')
    
    import time
    dp.update(0,"", "Extracting Zip Please Wait")
    extract.all(ZIPFILE,DIR,dp)
    
    time.sleep(1)
    XfinityInstaller()
    xbmc.executebuiltin('UpdateLocalAddons ')    
    xbmc.executebuiltin("UpdateAddonRepos")
    Kodi17()
    dialog.ok("USB BACKUP/RESTORE", "You Are Now Restored", 'If New Updates Dont Come Through Reboot Kodi','A Couple Times & Manually Update Plugins')
    xbmc.executebuiltin('UpdateLocalAddons ')    
    xbmc.executebuiltin("UpdateAddonRepos")

####################################### EMAILING ##################################################
###################################################################################################

    
def Show_Dialog(line1,line2,line3):
    dialog = xbmcgui.Dialog()
    dialog.ok('USB BACKUP/RESTORE', line1,line2,line3)




    
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param

def addDir(name,url,mode,iconimage,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description} )
        if mode==5 or mode==1:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        else:
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
        

                      
               
params=get_params()
url=None
name=None
mode=None
iconimage=None
description=None


try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass

        

       
if mode==1:
        BACKUP_OPTION()
        
elif mode==2:
        xbmc.log("############   RESTORE  #################")
        RESTORE()    
           
elif mode==3:
        xbmc.log("############   BACKUP  #################")
        BACKUP()
              
elif mode==4:
        xbmc.log("############   RESTORE_BACKUP_XML #################")
        RESTORE_BACKUP_XML(name,url,description)

elif mode==5:
        xbmc.log("############   RESTORE_OPTION   #################")
        RESTORE_OPTION()

elif mode==6:
        xbmc.log("############   RESTORE_ZIP_FILE   #################")
        RESTORE_ZIP_FILE(name,url)
        
elif mode==7:        
    EmailLog(url)

elif mode==8:        
    DownloadAttachment(url)

elif mode==9:        
    BackupEmail(url)

elif mode==10:        
    ResetPass()
    
elif mode==1000:        
    DeletePackages()
    xbmc.executebuiltin("UpdateAddonRepos")
    
else:
     CATEGORIES()        
xbmcplugin.endOfDirectory(int(sys.argv[1]))

