from match.models import GameWeek
from django.utils import timezone


class GameweekManager:
    def get_actual_gameweek(self):
        actual_dtm = timezone.now()
        actual_gameweek = GameWeek.objects.get(actual_from__lte=actual_dtm, actual_to__gt=actual_dtm)

        return actual_gameweek
