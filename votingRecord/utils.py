import csv
import re
from datetime import datetime
from pathlib import Path
import requests
import filecmp
from bs4 import BeautifulSoup
from .models import CouncilMember, AgendaItem, Vote

# ToDo: Change this to access the API
path = Path('/Users/jchavez/Documents/CS33/DallasVoting/')


def API_changed():

    csv_get = requests.get("https://www.dallasopendata.com/resource/ts5d-gdq6.csv")

    with open('temp.csv', 'wb') as csv_in:
        csv_in.write(csv_get.content)

    try:
        diff = filecmp.cmp('temp.csv', 'ts5d-gdg6.csv')
    except FileNotFoundError:
        # If the csv doesn't exist already, clearly the temp needs to be the csv
        diff = True
    if diff:
        Path('temp.csv').replace('ts5d-gdq6.csv')
        return True

    return False


def csv_to_model():

    with open(path / 'akDallasVotes.csv') as csv_in:  # ToDo: path will be different
        reader = csv.DictReader(csv_in)
        for row in reader:
            dt = datetime.strptime(row['DATE'], '%m/%d/%Y')
            # ToDo: Test that this will work How??
            cm, created = CouncilMember.objects.get_or_create(
                               name=row['VOTER NAME'],
                               district=row['DISTRICT'],
                               role=row['TITLE'])
            ai = AgendaItem(id=row['AGENDA_ID'],
                            number=row['AGENDA_ITEM_NUMBER'],
                            action=row['FINAL ACTION TAKEN'],
                            title=row['AGENDA ITEM DESCRIPTION'],
                            date=dt)
            v = Vote(voter=cm,
                     agenda_item=ai,
                     vote_for=row['VOTE CAST'])
            ai.save()
            # cm.save() Apparently don't need it with get_or_create
            v.save()

    # ToDo: Put some asserts in here to check the conversion to model went
    #   smoothly


def find_bio(cm_id):
    """"
    Given a url to dallascityhall.com bio page, it will return the contents
    of the bio section
    """
    council_m = CouncilMember.objects.get(id=cm_id)
    if council_m.district < 15:
        district_text = f"citycouncil/district{council_m.district}"
    else:
        # The mayor is listed as district 15, but isn't in the citycouncil/ path
        district_text = "citymayor"

    city_bio_url = f"https://dallascityhall.com/government/" \
                   f"{district_text}/Pages/Biography.aspx"
    print(f"city bio url is {city_bio_url}")
    bio_page = requests.get(city_bio_url)
    soup = BeautifulSoup(bio_page.content, "html.parser")
    bio_div = soup.find(id="ctl00_PlaceHolderMain_RichHtmlField2_"
                           "_ControlWrapper_RichHtmlField")

    if not bio_div:  # Some districts had no bio page. Try this url
        if council_m.district == 8:
            # Doh! District 8 misspelled "Biography" (swapped the 'ph')
            district_url = "https://dallascityhall.com/government/citycouncil/" \
                           "district8/Pages/Biograhpy.aspx"
        else:
            # Otherwise the main district page probably has a brief bio.
            district_url = f"https://dallascityhall.com/government/citycouncil/" \
                       f"district{council_m.district}/Pages/default.aspx"
        print(f"no bio page for {city_bio_url}? Trying {district_url}")
        bio_page = requests.get(district_url)
        soup = BeautifulSoup(bio_page.content, "html.parser")
        bio_div = soup.find(id="ctl00_PlaceHolderMain_RichHtmlField2_"
                           "_ControlWrapper_RichHtmlField")

    bio_innerHTML = ""
    try:        # Just a catch in case neither site works
        for tag in bio_div.contents:
            bio_innerHTML = bio_innerHTML + str(tag)
    except AttributeError:
        bio_title_innerHTML = f"Bio not found for {council_m.name}"
        bio_innerHTML = f"Neither https://dallascityhall.com/ pages for the " \
                        f"district had the bio. "
        return bio_title_innerHTML, bio_innerHTML

    bio_title = soup.find(id="ctl00_PlaceHolderMain_RichHtmlmaintitle_"
                             "_ControlWrapper_RichHtmlField")
    bio_title_innerHTML = ""
    for tag in bio_title.contents:
        bio_title_innerHTML = bio_title_innerHTML + str(tag)


    return bio_title_innerHTML, bio_innerHTML


def meeting_link(html_file, agenda_id):

    if html_file[0:5] == 'https':
        page = requests.get(html_file)
        soup = BeautifulSoup(page.content, "html.parser")
    else:
        with open(html_file) as fp:
            soup = BeautifulSoup(fp, "html.parser")

    # Convert date in agenda id to the date format of calendar
    if agenda_id != 'future':
        mtg_mo = agenda_id[0:2]
        mtg_day = agenda_id[2:4]
        mtg_yr = agenda_id[4:6]
        mtg_date = f'{mtg_mo}/{mtg_day}/20{mtg_yr}'

        # find link in table for that date
        date_td = soup.find(text=re.compile(mtg_date))
        mtg_row = date_td.parent.parent
        link_text = mtg_row.find(text=re.compile("^Meeting.details$"))
        mtg_link = link_text.parent.attrs["href"]

    else:
        table = soup.tbody
        mtg_link = None
        for row in reversed(table.contents):  # Next meeting at bottom of list
            try:
                element = row.find(text=re.compile("^Meeting.details$"))
                print(f"{element.parent.parent.attrs}")
                mtg_link = element.parent.parent.attrs["href"]
                if mtg_link:
                    mtg_link = f"https://cityofdallas.legistar.com/{mtg_link}&FullText=1"
                    break
            except:
                pass

    # give back link (or None if not found)
    return mtg_link


def meeting_table(html_file, agenda_id):
    # Find link in calendar page
    mtg_link = meeting_link(html_file, agenda_id)

    if not mtg_link:
        return None

    # ToDo: put a test that the link has "MeetingDetail.aspx" in it

    mtg_page = requests.get(mtg_link)
    soup = BeautifulSoup(mtg_page.content, "html.parser")

    # return the table
    return soup.tbody


def agenda_link(html_file, agenda_id):
    # Get the beautifulsoup table from the meeting table
    mtg_table = meeting_table(html_file, agenda_id)
    agenda_item = agenda_id.split('_')[2]

    if not mtg_table:
        return None

    # Find agenda item on table
    for row in mtg_table.contents:
        try:
            if agenda_item in row.contents[3].text:
                row_with_item = row
                break
        except AttributeError:  # Not every element in table.contents is a Tag
            pass

    # ToDo: test that row_with_item is not null
    table_link = row_with_item.a["href"]
    # ToDo: test that table_link starts with "LegislationDetail"

    full_link = f"https://cityofdallas.legistar.com/{table_link}&FullText=1"

    return full_link


def meeting_text(html_file, agenda_id):
    if agenda_id != 'future':
        # if it is not from the future, have to search the calendar to find the text
        legislation_url = agenda_link(html_file, agenda_id)
    else:
        # The text of future agenda items is easier to find and already known.
        legislation_url = html_file

    if not legislation_url:
        text = 'Agenda text not available. Check the Calendar page at ' \
               '<a href="https://cityofdallas.legistar.com/Calendar.aspx"> ' \
               'https://cityofdallas.legistar.com/ </a> ' \
               'to see if it is accessible from the Meeting Details'
        return text, legislation_url

    legislation_page = requests.get(legislation_url)
    soup = BeautifulSoup(legislation_page.content, "html.parser")

    # ToDo: Somehow getting double text
    elements = soup.find(id="ctl00_ContentPlaceHolder1_divText").contents[2]
    text = ''
    for el in elements:#.contents[1]:
        text = text + str(el)

    return text, legislation_url


