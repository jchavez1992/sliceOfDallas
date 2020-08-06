from django.urls import path

from . import views

app_name = "votingRecord"
urlpatterns = [
    path("", views.index, name="index"),
    path("login_view", views.login_view, name="login_view"),
    path("logout_view", views.logout_view, name="logout_view"),
    path("register", views.register, name="register"),
    path("voting_table", views.voting_table, name="voting_table"),
    path("future_agenda", views.future_meeting, name="future_meeting"),
    path("bio/<int:council_member_id>", views.bio, name="bio"),
    path("agenda_text/post_comment", views.post_comment, name="post_comment"),
    path("agenda_text/<str:agenda_id>", views.agenda_text, name="agenda_text")
]
