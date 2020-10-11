import scrapy
from ..items import CskItem


class csk_archive(scrapy.Spider):
    name = 'csk_archive'
    start_urls = [
        'https://www.iplt20.com/matches/results/men/2019',
        'https://www.iplt20.com/matches/results/men/2018',
        'https://www.iplt20.com/matches/results/men/2015',
        'https://www.iplt20.com/matches/results/men/2014',
        'https://www.iplt20.com/matches/results/men/2013',
        'https://www.iplt20.com/matches/results/men/2012',
        'https://www.iplt20.com/matches/results/men/2011',
        'https://www.iplt20.com/matches/results/men/2010',
        'https://www.iplt20.com/matches/results/men/2009',
        'https://www.iplt20.com/matches/results/men/2008'
    ]

    def parse(self, response):
        items = CskItem()
        season = response.url.split('/')[-1]
        results = response.css('.result')

        for result in results:
            teams = result.css('div.result__teams')
            team_names = teams.css('div.result__team p.result__team-name::text').getall()

            result_links = result.css('div.result__links')
            final_result = result_links.css('p.result__outcome.u-hide-phablet::text').get()
            match = result_links.css('p.result__info.u-hide-phablet span.result__description::text').get()
            venue = result_links.css('p.result__info.u-hide-phablet::text')[1].get()
            stadium = venue.split(', ')[1].strip()
            city = venue.split(', ')[2].strip()
            winner = final_result.split('won')[0].strip()

            if 'Chennai Super Kings' in team_names:
                team_names.remove('Chennai Super Kings')
                items['match'] = match
                items['opponent'] = team_names[0]
                items['winner'] = winner
                items['result'] = final_result
                items['city'] = city
                items['stadium'] = stadium
                items['season'] = season

                yield items
