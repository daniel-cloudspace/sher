from sher.models import Account
import gdata.youtube.service
import twitter

def get_service(service):
    service = service.lower()
    account = Account.objects.filter(service__exact=service)[0]
    
    if service == 'twitter':
        #return authenticated twitter api instsance
        #if the account contains the correct informations else exception to authorize
        pass

    if service == 'youtube':
        #return authenticated youtube api instance
        #if account contains proper information else exception and prompt to authorize
        pass
        
        

