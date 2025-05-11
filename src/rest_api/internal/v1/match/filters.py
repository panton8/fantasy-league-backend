from django_filters import rest_framework as filters

from match.models import Match


class MatchFilter(filters.FilterSet):
    class Meta:
        model = Match
        fields = ('full_time', )
