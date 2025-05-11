from django_filters import rest_framework as filters

from team.models import Player


class PlayerFilter(filters.FilterSet):
    cost = filters.RangeFilter(field_name='cost')

    class Meta:
        model = Player
        fields = ('position', 'club', 'cost')
