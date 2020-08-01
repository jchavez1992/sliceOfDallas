from django.shortcuts import render
from .forms import CMDropdown

# Create your views here.
def index(request):
    # ToDo: have it check the API at this stage

    cmembers_dropdown = CMDropdown()

    context = {"cm_dropdown": cmembers_dropdown}

    http_return = render(request, "votingRecord/index.html", context)
    return http_return
