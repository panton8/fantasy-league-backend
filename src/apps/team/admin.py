from django.contrib import admin

from team.models import Club, ClubInfo, Player


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('name', )


@admin.register(ClubInfo)
class ClubInfoAdmin(admin.ModelAdmin):
    list_display = ('club', )


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('surname', 'club')
    list_filter = ('club', )
