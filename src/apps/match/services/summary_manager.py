from match.models import MatchEvent
from dataclasses import dataclass
from typing import Optional
from django.db.models import Q


@dataclass
class MatchEventDTO:
    minute: int
    additional_minute: int
    action: str
    major_player: str
    minor_player: Optional[str]=None


class SummaryManager:
    def __init__(self, match):
        self.match = match
        self.__complicated_events = ['goal', 'sub_on']
        self.__minor_events = ['assist', 'sub_off']

    def __get_summary(self, events):
        events_to_show = []
        is_complicated_event = False

        for event in events:
            if is_complicated_event and event.action.code in self.__minor_events:
                complicated_event = events_to_show[-1]
                complicated_event.minor_player = event.player.name_to_display()
                is_complicated_event = False
                continue

            events_to_show.append(
                MatchEventDTO(
                    minute=event.minute,
                    additional_minute=event.additional_minute,
                    action=event.action.code,
                    major_player=event.player.name_to_display(),
                )
            )
            is_complicated_event = event.action.code in self.__complicated_events

        return events_to_show

    def get_home_club_summary(self):
        events = MatchEvent.objects.filter(match=self.match, action__for_display=True).filter(
            (Q(player__club=self.match.home_club) & ~Q(action__code='own_goal')) |
            (Q(player__club=self.match.away_club) & Q(action__code='own_goal'))
        ).order_by('minute', 'additional_minute', 'created_at')
        return self.__get_summary(events)

    def get_away_club_summary(self):
        events = MatchEvent.objects.filter(match=self.match, action__for_display=True).filter(
            (Q(player__club=self.match.away_club) & ~Q(action__code='own_goal')) |
            (Q(player__club=self.match.home_club) & Q(action__code='own_goal'))
        ).order_by('minute', 'additional_minute', 'created_at')
        return self.__get_summary(events)
