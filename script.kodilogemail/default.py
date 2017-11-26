import urllib,xbmcplugin,xbmcgui,xbmcaddon,xbmc,os

ADDON = xbmcaddon.Addon(id='script.kodilogemail')
dialog       =  xbmcgui.Dialog()
DIR=os.path.join(ADDON.getAddonInfo('profile'))
THEHTML = xbmc.translatePath(os.path.join(ADDON.getAddonInfo('path'),'theemail.html'))

def CATEGORIES():
    if ADDON.getSetting('email')=='':
        Show_Dialog('','You Need To Enter Your Email Details','')
        ADDON.openSettings()    
    addDir('Email Me My Log','ME',2,'','')            
    addDir('Email Someone Else My Log','',2,'','') 
    if not ADDON.getSetting('email_pass_1')=='':
        addDir('Reset Email Pass','url',10,'','Reset Email Pass')

def search_entered():
    favs = ADDON.getSetting('favs').split(',')
    keyboard = xbmc.Keyboard('', 'Email')
    keyboard.doModal()
    if keyboard.isConfirmed():
        search_entered = keyboard.getText()
    
    if not search_entered in favs:
        favs.append(search_entered)
        ADDON.setSetting('favs', ','.join(favs))
        
    return search_entered
            
def getOther():
    
    NAME=['[COLOR red]Cancel[/COLOR]','[COLOR green]New Email Address[/COLOR]']
    
    if ADDON.getSetting('favs') =='':
        return search_entered()

    favs = ADDON.getSetting('favs').split(',')
    for title in favs:
        if len(title)>1:
            NAME.append(title)
    EMAIL=NAME[xbmcgui.Dialog().select('Please Select Email', NAME)]
    if EMAIL =='[COLOR green]New Email Address[/COLOR]':
        return search_entered()
    else:
        return EMAIL


def getMessage():
    a='''Seems you are using gmail and havent enabled insecure apps on your google account\n\nSimply Log into your acount online once logged in visit:\n\n[COLOR royalblue]https://www.google.com/settings/security/lesssecureapps[/COLOR]\n\nAnd "Turn On" Access for less secure apps\n\n\nThen This Emailer Will Work :)\n\nThanks\nTeam [COLOR royalblue]X[/COLOR]unity[COLOR royalblue]T[/COLOR]alk'''
    return a


def send_email(TOWHO,LOG):
    PASSWORD=EmailPass()
    dp = xbmcgui.DialogProgress()
    dp.create(".Kodi Log Emailer",'Logging Into Your Email')
    dp.update(0)
    THESMTP ,THEPORT = Servers()
 
    fromaddr=ADDON.getSetting('email')
    if TOWHO =='ME':
        toaddr=fromaddr
    else:
        toaddr=getOther()

    if toaddr =='[COLOR red]Cancel[/COLOR]':
        Show_Dialog('No Email Sent','','Email Cancelled')
    else:    
        import datetime
        TODAY=datetime.datetime.today().strftime('[%d-%m-%Y %H:%M]')
        
        from email.MIMEMultipart import MIMEMultipart
        from email.MIMEText import MIMEText
        fromaddr = '"Hi Message From Yourself" <%s>'% (fromaddr)
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Your Kodi Log "+str(TODAY)
     
        body = open(THEHTML).read()

        content = MIMEText(body, 'html')
        msg.attach(content)
        
        try:filename = LOG.rsplit('\\', 1)[1]
        except:filename = LOG.rsplit('/', 1)[1]

        f = file(LOG)
        attachment = MIMEText(f.read())
        attachment.add_header('Content-Disposition', 'attachment', filename=filename.replace('log','txt'))           
        msg.attach(attachment)
        import smtplib
        server = smtplib.SMTP(str(THESMTP), int(THEPORT))
        dp.update(50, 'Attaching Your Email',filename.replace('log','txt'))
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
        server.sendmail(fromaddr, toaddr, text)
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


def EmailLog(TOWHO):
    nameSelect=[]
    logSelect=[]
    import glob
    folder = xbmc.translatePath('special://logpath')
    xbmc.log(folder)
    for file in glob.glob(folder+'/*.log'):
        try:nameSelect.append(file.rsplit('\\', 1)[1].upper())
        except:nameSelect.append(file.rsplit('/', 1)[1].upper())
        logSelect.append(file)
        
    LOG = logSelect[xbmcgui.Dialog().select('Please Select Log', nameSelect)]
    send_email(TOWHO,LOG)


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




def Show_Dialog(line1,line2,line3):
    dialog = xbmcgui.Dialog()
    dialog.ok('.Kodi Log Emailer', line1,line2,line3)


def Numeric():
        dialog = xbmcgui.Dialog()
        keyboard=dialog.numeric(0, 'Secret 4 Digits')
        return keyboard   

def EmailPass():
    if ADDON.getSetting('email_pass_1')=='':
        search_entered = ''
        keyboard = xbmc.Keyboard(search_entered, 'Please Enter Email Password')
        keyboard.setHiddenInput(True)
        keyboard.doModal()
        if keyboard.isConfirmed():
            THEPASS = keyboard.getText()
        if dialog.yesno("USB BACKUP/RESTORE", "Do you Want To Save Your Password ?", 'Its Fully AES Encrypted','Just Enter Secret 4 Digit Number'):
            
            EncryptPass(THEPASS)
            
        return THEPASS    
    else:
        return DecryptPass()

    
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
    dialog.ok('KodiLog Emailer','Pass Reset','','') 


    
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

def addDir(name,url,mode,iconimage,pagenum):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&pagenum="+urllib.quote_plus(pagenum)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name} )
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
        
        
 
     
params=get_params()
url=None
name=None
mode=None
iconimage=None
pagenum=None


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
        pagenum=urllib.unquote_plus(params["pagenum"])
except:
        pass



if mode==2:        
    EmailLog(url)

elif mode==10:        
    ResetPass()

elif mode == 5002:
    favs = ADDON.getSetting('favs').split(",")
    try:
        favs.remove(name)
        ADDON.setSetting('favs', ",".join(favs))
    except:pass
    xbmc.executebuiltin("XBMC.Container.Refresh()")

          
else:
    CATEGORIES()    
xbmcplugin.endOfDirectory(int(sys.argv[1]))
