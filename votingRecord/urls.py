from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("voting_table", views.voting_table, name="voting_table"),
    path("bio/<int:district>", views.bio, name="bio"),
    path("agenda_text/<str:agenda_id>", views.agenda_text, name="agenda_text")
]