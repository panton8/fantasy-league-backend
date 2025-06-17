from django.contrib import admin

from statistics.models import GameWeekStats


@admin.register(GameWeekStats)
class GameWeekAdmin(admin.ModelAdmin):
    list_display = ('player', 'gameweek')
    ordering = ('-gameweek__number', )