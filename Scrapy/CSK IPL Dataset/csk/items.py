# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CskItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    opponent = scrapy.Field()
    match = scrapy.Field()
    result = scrapy.Field()
    winner = scrapy.Field()
    city = scrapy.Field()
    stadium = scrapy.Field()
    season = scrapy.Field()


class CskSquad(scrapy.Item):
    year = scrapy.Field()
    orange_cap = scrapy.Field()
    purple_cap = scrapy.Field()


class CskPlayerStatsItem(scrapy.Item):
    season = scrapy.Field()
    player_id = scrapy.Field()
    player_name = scrapy.Field()
    player_nationality = scrapy.Field()
    fifties = scrapy.Field()
    hundreds = scrapy.Field()
    innings = scrapy.Field()
    matches = scrapy.Field()
    runs = scrapy.Field()
    fours = scrapy.Field()
    sixes = scrapy.Field()
    notout = scrapy.Field()
    highest = scrapy.Field()
    batting_strike_rate = scrapy.Field()
    batting_average = scrapy.Field()
    wickets = scrapy.Field()
    bowling_average = scrapy.Field()
    economy = scrapy.Field()
    fourw_haul = scrapy.Field()
    catches = scrapy.Field()
    runouts = scrapy.Field()
    stumping = scrapy.Field()


class CskPlayerImagesItem(scrapy.Item):
    images = scrapy.Field()
    image_urls = scrapy.Field()
