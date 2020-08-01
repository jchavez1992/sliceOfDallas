import csv
from datetime import datetime
from pathlib import Path
from .models import CouncilMember, AgendaItem, Vote

# ToDo: Change this to access the API
path = Path('/Users/jchavez/Documents/CS33/DallasVoting/')


def csv_to_model():

    with open(path / 'akDallasVotes.csv') as csv_in:
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
                            description=row['AGENDA ITEM DESCRIPTION'],
                            date=dt)
            v = Vote(voter=cm,
                     agenda_item=ai,
                     vote_for=row['VOTE CAST'])
            ai.save()
            # cm.save() Apparently don't need it with get_or_create
            v.save()

    # ToDo: Put some asserts in here to check the conversion to model went
    #   smoothly
