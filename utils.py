from sher.models import Account, Service
import simplejson
import urllib2
import urlparse

#service shoterning url, 
#is.gd fallback
def shorten_url(url):
       
    if 'flickr' in url:
        parsed_url = urlparse.urlsplit(url)
        photo_id = parsed_url.path.split('/')[3]
        
        if photo_id:
            base58_id = base58(photo_id)
            url =  'http://flic.kr/p/%s' % base58_id

    elif 'youtube' in url:
        parsed_url = urlparse.urlsplit(url)
        video_id = urlparse.parse_qs(parsed_url.query)['v'][0]
        
        if video_id:
            url = 'http://youtu.be/%s' % video_id

    else:
        api = "http://is.gd/create.php?format=json&url=%s" % url 
        try:
            json = simplejson.loads(urllib2.urlopen(api).read())
            url = json['shorturl']
        except:
            pass

    return url

def get_services_list(text):
    
    if text.find(',') != -1: #comma split 
        slist = text.split(',')
    else:
        slist = text.split() #by space

    return slist

def get_account(service_name):
    return Account.objects.get(service_name__iexact=service_name)

def get_services(services):
    
    mod = __import__('sher.services', fromlist=['*'])
    
    sdict = {}

    for s in services:
        s = s.lower()
        try:
            sdict[s] = getattr(mod, '%s_service' % s)
        except AttributeError:
            pass
    
    for name,service in sdict.items():
        sdict[name] = service.authenticated(get_account(name)) 

    return sdict #return service name: authenticated api instance

def base58(n):
    alphabet='123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'
    result = ''
    while n >= 58:                                                          
        div,mod = divmod(int(n),58)
        result = alphabet[mod] + result
        n = div
    result = alphabet[n] + result
    base_count=len(alphabet)
    return result

