import json
import logging
import requests

from .constants import FBA_ENDPOINT

from .utils.http_util import request_status

logging.basicConfig(level='INFO')
logger = logging.getLogger(__name__)


class League(object):
    """Get league instance from ESPN"""
    def __init__(self, league_id: int, year: int, team_id: int, cookies, debug=False):
        self.league_id = league_id
        self.year = year
        self.current_week = 0
        self.nba_day = 0
        self.team_id = team_id
        self.cookies = cookies
        if self.cookies:
            self.cookies = cookies
        else:
            logger.error(f'No Authorization Credentials')
            raise Exception

        self._fetch_league()
        self._fetch_team_id()
        self._fetch_teams()
        self.roster = self._fetch_roster()

    def __repr__(self):
        return f'League: {self.league_id} Year: {self.year}'

    def _fetch_league(self):
        req = f'{FBA_ENDPOINT}{self.year}/segments/0/leagues/{self.league_id}'
        resp = requests.get(req, params='', cookies=self.cookies)

        self.status = resp.status_code
        request_status(self.status)

        league_data = resp.json()
        logger.info(f'League Data: {json.dumps(league_data, indent=4)}')

        self.current_week = league_data['status']['currentMatchupPeriod']
        self.nba_day = league_data['status']['latestScoringPeriod']

    def _fetch_team_id(self):
        params = {
            'view': 'mTeam'
        }

        req = f'{FBA_ENDPOINT}{self.year}/segments/0/leagues/{self.league_id}'
        resp = requests.get(req, params=params, cookies=self.cookies)

        self.status = resp.status_code
        request_status(self.status)

        teams = resp.json()['teams']

        # NOTE: This can be fixed up to be faster
        team_id_data = [x for x in teams if x.get('id') == self.team_id]

        logger.info(f'My Team Data: {json.dumps(team_id_data, indent=4)}')

    def _fetch_teams(self):
        params = {
            'view': 'mTeam'
        }

        req = f'{FBA_ENDPOINT}{self.year}/segments/0/leagues/{self.league_id}'
        resp = requests.get(req, params=params, cookies=self.cookies)

        self.status = resp.status_code
        request_status(self.status)

        team_data = resp.json()

    def _fetch_roster(self):
        # here we will get players on waiver wire
        params = {
            'view': 'mRoster',
            'scoringPeriod': self.current_week
        }

        req = f'{FBA_ENDPOINT}{self.year}/segments/0/leagues/{self.league_id}'
        resp = requests.get(req, params=params, cookies=self.cookies)

        self.status = resp.status_code
        request_status(self.status)

        rosters = resp.json()['teams']

        team_id_roster = [x for x in rosters if x.get('id') == self.team_id]

        return team_id_roster


