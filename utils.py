from sher.models import Account, Service
from sher.services import twitter_service, youtube_service, facebook_service, flickr_service 

def get_auth_service(service="", account_user=""):
    """Responsible for returning an authenticated instance of the service for account user."""   
    assert service and account_user, "Need an account username and service name to work"
    
    service = service.lower()
    try:
        service_obj = Service.objects.get(name__iexact=service)
        account_obj = Account.objects.get(user__iexact=account_user, service=service_obj) 
        
        if service == "twitter":
            return twitter_service.authenticated(account_obj)
        if service == "facebook":
            return facebook_service.authenticated(account_obj)
        if service == "flickr": 
            return flickr_service.authenticated(account_obj)
        if service == "youtube": 
            return youtube_service.authenticated(account_obj)

    except Service.DoesNotExist:
        raise Service.DoesNotExist("This service does not exist.")
    except Account.DoesNotExist:
        raise Account.DoesNotExist("This account does not exist.")
    except Exception, e:
        raise e
