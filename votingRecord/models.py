from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator
from django.db import models


class User(AbstractUser):
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
    id = models.CharField(max_length=15, primary_key=True)
    number = models.CharField(max_length=5)  # Some numbers start with Z or PH
    date = models.DateField()
    type = models.CharField(max_length=50, choices=type_choices)
    action = models.CharField(max_length=300)  # Some are a small paragraph
    title = models.TextField()

    class Meta:
        ordering = ["-date", "id"]

    def __str__(self):
        return f"{self.id}"


class CouncilMember(models.Model):
    name = models.CharField(max_length=50)
    district = models.IntegerField()
    role = models.CharField(max_length=25)
    bio = models.TextField()

    def __str__(self):
        return f"{self.name}, {self.role} district: {self.district}"


class Vote(models.Model):
    voter = models.ForeignKey('CouncilMember', on_delete=models.PROTECT)
    agenda_item = models.ForeignKey('AgendaItem', on_delete=models.PROTECT)
    vote_for = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.voter.name} " \
               f"voted {self.vote_for}" \
               f" on {self.agenda_item.id}"

