from dataclasses import dataclass, asdict
from typing import List

from match.models import Match
from rest_api.internal.v1.match.serializers import GameWeekMatchesSerializer


@dataclass(frozen=True)
class GameWeekMatches:
    gameweek: int
    matches: List[Match]


class MatchService:
    def gameweek_matches(self, matches):
        gameweek_matches = []
        if matches:
            curr_week = matches.first().gameweek.number
        matches_butch = []
        for match in matches:
            if match.gameweek.number != curr_week:
                gameweek_matches.append(GameWeekMatches(curr_week, matches_butch))
                curr_week -= 1
                matches_butch = []
            matches_butch.append(match)
        if matches:
            gameweek_matches.append(GameWeekMatches(curr_week, matches_butch))
        return gameweek_matches
