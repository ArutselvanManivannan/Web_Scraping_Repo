import scrapy
from ..items import CskSquad


class csk_overview(scrapy.Spider):
    name = 'csk_overview'
    start_urls = ['https://www.iplt20.com/teams/chennai-super-kings/archive']

    def parse(self, response):
        items = CskSquad()

        players = []
        year_count = 0

        container = response.css('div.archive-item')
        year = container.css('div.year strong::text').getall()
        top_stats = container.css('ul.year-stats li p.player::text').getall()

        for i in range(0, len(top_stats), 2):
            players.append([top_stats[i].strip(), top_stats[i + 1].strip()])
            items['year'] = year[year_count]
            items['orange_cap'] = top_stats[i].strip()
            items['purple_cap'] = top_stats[i + 1].strip()

            year_count += 1

            yield items
