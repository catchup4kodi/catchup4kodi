from md_request import open_url
import re,urllib


def googletag(url):

    
    quality = re.compile('itag=(\d*)').findall(url)
    quality += re.compile('=m(\d*)$').findall(url)
    try: quality = quality[0]
    except: return []

    if quality in ['37', '46', '137', '299', '96', '248', '303', '46']:
        return [{'quality': '1080P', 'url': url}]
    elif quality in ['22', '45', '84', '136', '298', '120', '95', '247', '302', '45', '102']:
        return [{'quality': '720P', 'url': url}]
    elif quality in ['35', '59', '44', '135', '244', '94']:
        return [{'quality': 'DVD', 'url': url}]
    elif quality in ['18', '34', '43', '82', '100', '101', '134', '243', '93']:
        return [{'quality': 'SD', 'url': url}]
    elif quality in ['5', '6', '36', '83', '133', '242', '92', '132']:
        return [{'quality': 'SD', 'url': url}]
    else:
        return []




def GLinks(doc):

    if '/securesc/' in doc:
        doc_id = doc.split('/*/')[1].split('?')[0]
        doc = 'https://docs.google.com/file/d/%s/view' %doc_id

    doc = doc.replace('drive.google.com', 'docs.google.com')
    doc = doc.replace('/preview','/view').replace('/edit','/view').replace('/download','/view')

    link = open_url(doc, verify=False, timeout=3)

    res = []
    url = []

    match = re.compile('itag\\\u003d.*?\\\u0026url\\\u003d(.*?)%3B').findall(link.content)

    for doc_url in match:
        doc_url = urllib.unquote(doc_url)
        doc_url = doc_url.replace('\\u003d','=').replace('\\u0026','&')
        
        try:
            doc_url = doc_url.split('url=')[2]
        except:pass

        for a in googletag(doc_url):

            cookie = link.cookies.get_dict()
            if 'DRIVE_STREAM' in cookie:
                cookie = urllib.quote('Cookie:DRIVE_STREAM=%s; NID=%s' %(cookie['DRIVE_STREAM'],cookie['NID']))
                g_url = a['url'] + '|' + cookie
            else:
                g_url = a['url']

            url.append(g_url)
            res.append(a['quality'])

    return zip(res, url)
