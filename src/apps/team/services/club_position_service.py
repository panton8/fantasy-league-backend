from team.models import Club


class ClubPositionService:
    def get_actual_table(self):
        return Club.objects.order_by('-wins', '-draws', '-goals_for', 'goals_against', 'played', 'name')