from datetime import datetime

from django.test import Client, TestCase
from django.db.models import Max

from .models import AgendaItem, CouncilMember, Vote


# Create your tests here.


class VotingRecordTestCase(TestCase):

    def setUp(self):
        ai_1 = AgendaItem.objects.create(
            id='070522_AG_15',
            number='15',
            date=datetime(2022, 7, 5),
            type='Agenda',
            action='Approved',
            title='Something interesting'
        )
        ai_2 = AgendaItem.objects.create(
            id='070522_AG_15',
            number='23',
            date=datetime(2022, 7, 5),
            type='Agenda',
            action='Deferred to 08/10',
            title='Something more interesting'
        )

        cm_1 = CouncilMember.objects.create(
            name="Bob Woodward",
            district=1,
            role="CouncilMember",
            bio="Journalist turned politician"
        )
        cm_2 = CouncilMember.objects.create(
            name="Priscilla Kawaihai",
            district=2,
            role="Mayor Pro Tem",
            bio="I <3 Dallas"
        )

        v_1 = Vote.objects.create(
            voter=cm_1,
            agenda_item=ai_1,
            vote_for="Yes"
        )
        v_2 = Vote.objects.create(
            voter=cm_2,
            agenda_item=ai_2,
            vote_for="No"
        )

