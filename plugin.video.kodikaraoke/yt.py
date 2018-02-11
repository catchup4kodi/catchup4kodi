import re
import urllib2
import urllib
import cgi
import HTMLParser

try: import simplejson as json
except ImportError: import json


def GetVideoInformation(id):
    #id = 'H7iQ4sAf0OE' #test for HLSVP
    #id = 'ofHlUJuw8Ak' #test for stereo

    video = None
    links = None

    try:    video, links = GetVideoInfo(id)
    except: pass

    return video, links


def GetVideoInfo(id):
    url  = 'http://www.youtube.com/watch?v=%s&safeSearch=none' % id
    html = FetchPage(url)

    video, links = Scrape(html)

    video["videoid"]   = id
    video['thumbnail'] = "http://i.ytimg.com/vi/%s/0.jpg" % video['videoid']
    video["title"]     = GetVideoTitle(html)

    if len(links) == 0:
        if 'hlsvp' in video:
            video['best'] = video['hlsvp']

    else:
        video['best'] = links[0][1]


    return video, links


def GetVideoTitle(html):
    try:    return re.compile('<meta name="title" content="(.+?)">').search(html).groups(1)[0]
    except: pass

    return 'YouTube Video'

    
def Scrape(html):
    stereo = [82, 83, 84, 85, 100, 101, 102]
    video  = {}
    links  = []

    flashvars = ExtractFlashVars(html)

    if not flashvars.has_key(u"url_encoded_fmt_stream_map"):
        return video, links

    if flashvars.has_key(u"ttsurl"):
        video[u"ttsurl"] = flashvars[u"ttsurl"]

    if flashvars.has_key(u"hlsvp"):                               
        video[u"hlsvp"] = flashvars[u"hlsvp"]    

    for url_desc in flashvars[u"url_encoded_fmt_stream_map"].split(u","):
        url_desc_map = cgi.parse_qs(url_desc)
        if not (url_desc_map.has_key(u"url") or url_desc_map.has_key(u"stream")):
            continue

        key = int(url_desc_map[u"itag"][0])
        url = u""
        if url_desc_map.has_key(u"url"):
            url = urllib.unquote(url_desc_map[u"url"][0])
        elif url_desc_map.has_key(u"conn") and url_desc_map.has_key(u"stream"):
            url = urllib.unquote(url_desc_map[u"conn"][0])
            if url.rfind("/") < len(url) -1:
                url = url + "/"
            url = url + urllib.unquote(url_desc_map[u"stream"][0])
        elif url_desc_map.has_key(u"stream") and not url_desc_map.has_key(u"conn"):
            url = urllib.unquote(url_desc_map[u"stream"][0])

        if url_desc_map.has_key(u"sig"):
            url = url + u"&signature=" + url_desc_map[u"sig"][0]
        elif url_desc_map.has_key(u"s"):
            sig = url_desc_map[u"s"][0]
            url = url + u"&signature=" + DecryptSignature(sig)

        if key not in stereo:
            links.append([key, url])

    #links.sort(reverse=True)
    return video, links


def DecryptSignature(s):
    ''' use decryption solution by Youtube-DL project '''
    if len(s) == 88:
        return s[48] + s[81:67:-1] + s[82] + s[66:62:-1] + s[85] + s[61:48:-1] + s[67] + s[47:12:-1] + s[3] + s[11:3:-1] + s[2] + s[12]
    elif len(s) == 87:
        return s[62] + s[82:62:-1] + s[83] + s[61:52:-1] + s[0] + s[51:2:-1]
    elif len(s) == 86:
        return s[2:63] + s[82] + s[64:82] + s[63]
    elif len(s) == 85:
        return s[76] + s[82:76:-1] + s[83] + s[75:60:-1] + s[0] + s[59:50:-1] + s[1] + s[49:2:-1]
    elif len(s) == 84:
        return s[83:36:-1] + s[2] + s[35:26:-1] + s[3] + s[25:3:-1] + s[26]
    elif len(s) == 83:
        return s[6] + s[3:6] + s[33] + s[7:24] + s[0] + s[25:33] + s[53] + s[34:53] + s[24] + s[54:]
    elif len(s) == 82:
        return s[36] + s[79:67:-1] + s[81] + s[66:40:-1] + s[33] + s[39:36:-1] + s[40] + s[35] + s[0] + s[67] + s[32:0:-1] + s[34]
    elif len(s) == 81:
        return s[6] + s[3:6] + s[33] + s[7:24] + s[0] + s[25:33] + s[2] + s[34:53] + s[24] + s[54:81]
    elif len(s) == 92:
        return s[25] + s[3:25] + s[0] + s[26:42] + s[79] + s[43:79] + s[91] + s[80:83];
    #else:
    #    print ('Unable to decrypt signature, key length %d not supported; retrying might work' % (len(s)))


def ExtractFlashVars(data):
    flashvars = {}
    found = False

    for line in data.split("\n"):
        if line.strip().find(";ytplayer.config = ") > 0:
            found = True
            p1 = line.find(";ytplayer.config = ") + len(";ytplayer.config = ") - 1
            p2 = line.rfind(";")
            if p1 <= 0 or p2 <= 0:
                continue
            data = line[p1 + 1:p2]
            break
    data = RemoveAdditionalEndingDelimiter(data)

    if found:
        data = json.loads(data)
        flashvars = data["args"]

    return flashvars


def FetchPage(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    req.add_header('Referer',    'http://www.youtube.com/')

    return urllib2.urlopen(req).read().decode("utf-8")


def replaceHTMLCodes(txt):
    # Fix missing ; in &#<number>;
    txt = re.sub("(&#[0-9]+)([^;^0-9]+)", "\\1;\\2", txt)

    txt = HTMLParser.HTMLParser().unescape(txt)
    txt = txt.replace("&amp;", "&")
    return txt


def RemoveAdditionalEndingDelimiter(data):
    pos = data.find("};")
    if pos != -1:
        data = data[:pos + 1]
    return data



