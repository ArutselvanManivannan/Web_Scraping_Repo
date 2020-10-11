import json
import scrapy
import requests
from ..items import CskPlayerImagesItem


class CskPlayerImage(scrapy.Spider):
    name = 'csk_player_images'
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
        items = CskPlayerImagesItem()
        image_url = []
        players = json.loads(response.text)
        players = players['stats']['content']

        for player in players:
            player_stats = player['player']
            player_id = player_stats['id']

            url = f"https://static.iplt20.com/players/210/{player_id}.png"
            res = requests.get(url)
            if res.status_code == 200:
                image_url.append(url)

        items['image_urls'] = image_url

        return items
