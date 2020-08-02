from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse
from .models import AgendaItem, CouncilMember, Vote
from .forms import CMDropdown
from votingRecord import utils

# Create your views here.
def index(request):
    # ToDo: have it check the API at this stage
    updated = utils.API_changed()

    cmembers_dropdown = CMDropdown()

    context = {"cm_dropdown": cmembers_dropdown}

    http_return = render(request, "votingRecord/index.html", context)
    return http_return


def voting_table(request):
    if request.method == "POST":
        form = CMDropdown(request.POST)
        if form.is_valid():
            c_member = form.cleaned_data["cmembers"]

            v_record = Vote.objects.filter(voter=c_member)

            return render(request, "votingRecord/voting_table.html", {
                "vote_records": v_record,
                "council_member": c_member
            })
        else:
            return HttpResponseRedirect(reverse("tasks:index"))
    else:
        return HttpResponseRedirect(reverse("tasks:index"))


def bio(request, district):
    city_bio_url = f"https://dallascityhall.com/government/citycouncil/" \
                   f"district{district}/Pages/Biography.aspx"

    bio_title, bio_html = utils.find_bio(city_bio_url)

    http_return = render(request, "votingRecord/bio.html", {
        "bio_title": bio_title,
        "bio_contents": bio_html
    })

    return http_return


def agenda_text(request, agenda_id):
    yr = agenda_id[4:6]
    if int(yr) < 19:
        return HttpResponseNotFound('<h1>Only available for meetings in 2019'
                                    'and later</h1>')
    # ToDo need path to be relative
    calendar_page = f"/Users/jchavez/Documents/CS33/sliceOfDallas/DallasCityCouncilCalendar20{yr}.html"

    # ToDo: get from function link to agenda item text, and put link on page
    meeting_text = utils.meeting_text(calendar_page, agenda_id)

    http_return = render(request, "votingRecord/agenda_text.html", {
        "text": meeting_text,
        "agenda_id": agenda_id
    })

    return http_return


#def future_meeting(request):

#    agenda_list =
