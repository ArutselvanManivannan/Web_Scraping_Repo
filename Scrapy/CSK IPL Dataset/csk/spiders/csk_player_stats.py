import json
import scrapy
from ..items import CskPlayerStatsItem


class CskPlayerStats(scrapy.Spider):
    name = 'csk_player_stats'
    start_urls = [
        'https://cricketapi.platform.iplt20.com/stats/players?teamIds=1&tournamentIds=10192&scope=TOURNAMENT&pageSize=30',
        'https://cricketapi.platform.iplt20.com/stats/players?teamIds=1&tournamentIds=7749&scope=TOURNAMENT&pageSize=30',
        'https://cricketapi.platform.iplt20.com/stats/players?teamIds=1&tournamentIds=2785&scope=TOURNAMENT&pageSize=30',
        'https://cricketapi.platform.iplt20.com/stats/players?teamIds=1&tournamentIds=2374&scope=TOURNAMENT&pageSize=30',
        'https://cricketapi.platform.iplt20.com/stats/players?teamIds=1&tournamentIds=605&scope=TOURNAMENT&pageSize=30',
        'https://cricketapi.platform.iplt20.com/stats/players?teamIds=1&tournamentIds=1&scope=TOURNAMENT&pageSize=30',
        'https://cricketapi.platform.iplt20.com/stats/players?teamIds=1&tournamentIds=81&scope=TOURNAMENT&pageSize=30',
        'https://cricketapi.platform.iplt20.com/stats/players?teamIds=1&tournamentIds=80&scope=TOURNAMENT&pageSize=30',
        'https://cricketapi.platform.iplt20.com/stats/players?teamIds=1&tournamentIds=79&scope=TOURNAMENT&pageSize=30',
        'https://cricketapi.platform.iplt20.com/stats/players?teamIds=1&tournamentIds=78&scope=TOURNAMENT&pageSize=30'
    ]

    def parse(self, response):
        items = CskPlayerStatsItem()

        season_id = {'10192': '2019', '7749': '2018', '2785': '2015', '2374': '2014', '605': '2013', '1': '2012', '81': '2011', '80': '2010', '79': '2009', '78': '2008'}
        season = season_id[response.url.split('&')[1].split('=')[-1]]

        players = json.loads(response.text)
        players = players['stats']['content']

        for player in players:
            player_stats = player['player']
            items['player_id'] = player_stats['id']
            items['player_name'] = player_stats['fullName']
            items['player_nationality'] = player_stats['nationality']

            image_url = f"https://static.iplt20.com/players/210/{player_stats['id']}.png"

            if not player['stats']:
                items['season'] = season
                items['fifties'] = 0
                items['hundreds'] = 0
                items['innings'] = 0
                items['matches'] = 0
                items['runs'] = 0
                items['fours'] = 0
                items['sixes'] = 0
                items['notout'] = 0
                items['highest'] = 0
                items['batting_strike_rate'] = 0
                items['batting_average'] = 0

                items['wickets'] = 0
                items['bowling_average'] = 0
                items['economy'] = 0
                items['fourw_haul'] = 0

                items['catches'] = 0
                items['runouts'] = 0
                items['stumping'] = 0

                yield items
            else:
                items['season'] = season

                batting_stats = player['stats'][0]['battingStats']
                items['fifties'] = batting_stats['50s']
                items['hundreds'] = batting_stats['100s']
                items['innings'] = batting_stats['inns']
                items['matches'] = batting_stats['m']
                items['runs'] = batting_stats['r']
                items['fours'] = batting_stats['4s']
                items['sixes'] = batting_stats['6s']
                items['notout'] = batting_stats['no']
                items['highest'] = batting_stats['hs']
                items['batting_strike_rate'] = batting_stats['sr']
                items['batting_average'] = batting_stats['a']

                bowling_stats = player['stats'][0]['bowlingStats']
                items['wickets'] = bowling_stats['w']
                items['bowling_average'] = bowling_stats['a']
                items['economy'] = bowling_stats['e']
                items['fourw_haul'] = bowling_stats['4w']

                fielding_stats = player['stats'][0]['fieldingStats']
                items['catches'] = fielding_stats['c']
                items['runouts'] = fielding_stats['ro']
                items['stumping'] = fielding_stats['s']

                yield items
