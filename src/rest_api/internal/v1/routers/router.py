from rest_api.internal.v1.match.viewsets import MatchViewSet, NewsViewSet
from rest_api.internal.v1.team.viewsets import TeamViewSet, ClubViewSet, PlayerViewSet, CommunityLeagueViewSet, \
    CommunityLeagueMembersViewSet
from rest_api.internal.v1.user.viewsets.profile import UserProfileViewSet
from rest_api.internal.v1.user.viewsets.refresh_token import RefreshTokenViewSet
from rest_api.internal.v1.user.viewsets.sign_in import SignInViewSet
from rest_api.internal.v1.user.viewsets.sign_up import SignUpViewSet
from rest_framework import routers

router = routers.DefaultRouter()


router.register(r'user/refresh-token', RefreshTokenViewSet, basename='user_refresh_token')
router.register(r'user/sign-up', SignUpViewSet, basename='user_sign_up')
router.register(r'user/sign-in', SignInViewSet, basename='user_sign_in')
router.register(r'user/team', TeamViewSet, basename='user_team')
router.register(r'user', UserProfileViewSet, basename='user')
router.register(r'club', ClubViewSet, basename='club')
router.register(r'match', MatchViewSet, basename='match')
router.register(r'player', PlayerViewSet, basename='player')
router.register(r'news',  NewsViewSet, basename='news')
router.register(r'community_league', CommunityLeagueViewSet, basename='community_league')
router.register(r'community_league_members', CommunityLeagueMembersViewSet, basename='community_league_members')