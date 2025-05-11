from django.contrib import admin

from match.models import LineUp, Match, MatchEvent, GameWeek, MatchAction
from team.models import Player


@admin.register(GameWeek)
class GameWeekAdmin(admin.ModelAdmin):
    list_display = ('number', 'actual_from', 'actual_to')


@admin.register(MatchAction)
class MatchActionAdmin(admin.ModelAdmin):
    list_display = ('name', 'for_display')


class MatchLineupInline(admin.TabularInline):
    model = LineUp
    extra = 0
    fields = ('player', 'in_start', )
    ordering = ('player__club', 'player__position')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'player':
            match_id = request.resolver_match.kwargs.get('object_id')
            if match_id:
                try:
                    match = Match.objects.get(pk=match_id)
                    kwargs['queryset'] = Player.objects.filter(club__in=[match.home_club, match.away_club])
                except Match.DoesNotExist:
                    pass
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class MatchEventInline(admin.TabularInline):
    model = MatchEvent
    extra = 0
    fields = ('minute', 'additional_minute', 'action', 'player')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name in ['player']:
            match_id = request.resolver_match.kwargs.get('object_id')
            if match_id:
                try:
                    match = Match.objects.get(pk=match_id)
                    kwargs["queryset"] = Player.objects.filter(club__in=[match.home_club, match.away_club])
                except Match.DoesNotExist:
                    pass
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    fields = ('home_club', 'away_club', 'home_club_goals', 'away_club_goals', 'start_time', 'full_time', 'gameweek')
    list_display = ('home_club', 'away_club', 'start_time', 'full_time')
    inlines = [MatchLineupInline, MatchEventInline]
    ordering = ('-start_time', )
