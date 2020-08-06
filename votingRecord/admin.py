from django.contrib import admin
from .models import AgendaItem, CouncilMember, Vote, User, Comment

# Register your models here.
admin.site.register(AgendaItem)
admin.site.register(CouncilMember)
admin.site.register(Vote)
admin.site.register(User)
admin.site.register(Comment)
