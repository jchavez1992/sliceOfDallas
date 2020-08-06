import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.urls import reverse
from django.views.decorators.cache import cache_page

from .models import AgendaItem, CouncilMember, Vote, User, Comment
from .forms import CMDropdown
from votingRecord import utils
from bs4 import BeautifulSoup


# Create your views here.
def index(request):
    updated = utils.API_changed()
    if updated:
        utils.csv_to_model()

    cmembers_dropdown = CMDropdown()

    context = {"cm_dropdown": cmembers_dropdown}

    http_return = render(request, "votingRecord/index.html", context)
    return http_return


def voting_table(request):
    cm_dropdown = CMDropdown()
    if request.method == "POST":
        form = CMDropdown(request.POST)
        c_member = form.data["cmembers"]  # If it comes from the bio, it won't validate
        if form.is_valid():
            c_member = form.cleaned_data["cmembers"]

        if type(c_member) is str:   # If it came from the bio, it will be an id
            c_member = CouncilMember.objects.get(id=c_member)

        v_record = Vote.objects.filter(voter=c_member)

        return render(request, "votingRecord/voting_table.html", {
                    "vote_records": v_record,
                    "council_member": c_member,
                    "cm_dropdown": cm_dropdown
        })
    else:
        return HttpResponseRedirect(reverse("votingRecord:index"))


@cache_page(864000)  # Cache for a day
def bio(request, council_member_id):

    council_member = CouncilMember.objects.get(id=council_member_id)
    bio_title, bio_html = utils.find_bio(council_member_id)

    http_return = render(request, "votingRecord/bio.html", {
        "bio_title": bio_title,
        "bio_contents": bio_html,
        "council_member": council_member
    })

    return http_return


@cache_page(864000)  # Cache for a day
def agenda_text(request, agenda_id):
    if agenda_id[0:3] == 'Leg':
        url = f"https://cityofdallas.legistar.com/{agenda_id}&FullText=1"
        meeting_text, _ = utils.meeting_text(url, 'future')
        agenda_id = ''
    else:
        yr = agenda_id[4:6]
        if int(yr) < 19:
            return HttpResponseNotFound('<h1>Only available for meetings in 2019'
                    ' and later</h1> <br> See <a href='
                    '"https://dallascityhall.com/government/Pages/Council-Agenda.aspx">'
                    'this page </a> for older agendas.'
            )

        calendar_page = f"DallasCityCouncilCalendar20{yr}.html"
        meeting_text, url = utils.meeting_text(calendar_page, agenda_id)

    comments = Comment.objects.filter(agenda=agenda_id)

    http_return = render(request, "votingRecord/agenda_text.html", {
        "text": meeting_text,
        "agenda_id": agenda_id,
        "full_url": url,
        "comments": comments
    })

    return http_return


@cache_page(864000)  # Cache for a day
def future_meeting(request):
    # CityCouncil meetings calendar:
    city_council_mtg = \
        "https://cityofdallas.legistar.com/DepartmentDetail.aspx?ID=36611&GUID=7206C089-E775-4BB6-BAFF-CAE8C01A3FB3&Mode=MainBody"
    agenda_list = utils.meeting_table(city_council_mtg, 'future')

    if not agenda_list:
        return HttpResponseNotFound('Agenda text not available. Check the '
                    'Calendar page at '
                    '<a href="https://cityofdallas.legistar.com/DepartmentDetail.aspx"> ' 
                    'https://cityofdallas.legistar.com/DepartmentDetail.aspx </a> ' 
                    'to see if it is accessible from the Meeting Details')

    agenda_table = []
    for row in agenda_list.contents:
        cells = {}
        try:
            cells["number"] = row.contents[3].text
            cells["text"] = row.a["href"]
            cells["type"] = row.contents[5].text
            cells["title"] = row.contents[6].text
            agenda_table.append(cells)
        except AttributeError:  # Not every element in table.contents is a Tag
            pass

    http_return = render(request, "votingRecord/future_agenda.html", {
        "council_meeting_agenda": agenda_table
    })
    return http_return


@login_required
def post_comment(request):
    # Composing a new email must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    if data.get("agenda_id") is not None:
        agenda = AgendaItem.objects.get(id=data.get('agenda_id'))
    else:
        return JsonResponse({"error": "agenda id required"}, status=400)

    new_comment = Comment(
        user=request.user,
        text=data.get("content"),
        agenda=agenda
    )
    new_comment.save()

    return JsonResponse({"message": "Comment saved"}, status=200)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("votingRecord:index"))
        else:
            return render(request, "votingRecord/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "votingRecord/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("votingRecord:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "votingRecord/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "votingRecord/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("votingRecord:index"))
    else:
        return render(request, "votingRecord/register.html")
