from sher.models import Account, Service
import simplejson
import urllib2

#is.gd url shortening for flickr/youtube links
def shorten_url(url):
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
