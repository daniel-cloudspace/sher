from django.http import HttpResponseRedirect, HttpResponse, Http404
from sher.models import Account, Service
from django.shortcuts import render
import sher.settings as settings
from django.contrib import messages
from django.core.urlresolvers import reverse

def index(request, template="sher/index.html"):
    """
    Serves as a listing for supported services and a way to authorize the _current_
    application with them.
    """
    return render(request, template, {'services': Service.objects.all()})


