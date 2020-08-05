from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator
from django.db import models


# ToDo: check max_lengths on the CharFields
class User(AbstractUser):
    # ToDo: make sure district field is in login
    #district = models.IntegerField(
    #    validators=[MaxValueValidator(14)]
    #)
    pass

class Comment(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE,
                             related_name='writer')
    agenda = models.ForeignKey('AgendaItem', on_delete=models.CASCADE)
    text = models.TextField()


class AgendaItem(models.Model):
    AGENDA = 'Agenda'
    ADDENDUM = 'Addendum'
    type_choices = [(AGENDA, 'Agenda'),
                    (ADDENDUM, 'Addendum')]
    id = models.CharField(max_length=100, primary_key=True)
    number = models.CharField(max_length=100)
    date = models.DateField()
    type = models.CharField(max_length=100, choices=type_choices)
    action = models.CharField(max_length=100)
    title = models.TextField()

    class Meta:
        ordering = ["-date", "id"]

    def __str__(self):
        return f"{self.id}"


class CouncilMember(models.Model):
    name = models.CharField(max_length=100)
    district = models.IntegerField()  # ToDo: make foreign key to district
    role = models.CharField(max_length=100)
    bio = models.TextField()

    def __str__(self):
        return f"{self.id}: {self.name}, {self.role} in district {self.district}"


class Vote(models.Model):
    voter = models.ForeignKey('CouncilMember', on_delete=models.PROTECT)
    agenda_item = models.ForeignKey('AgendaItem', on_delete=models.PROTECT)
    vote_for = models.CharField(max_length=100)  # ToDo make Boolean?

    def __str__(self):
        return f"{self.voter.name} " \
               f"voted {self.vote_for}" \
               f" on {self.agenda_item.id}"


# ToDo: Make District model
"""
"""

