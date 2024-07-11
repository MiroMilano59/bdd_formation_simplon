# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class CrawlSimplonItem(scrapy.Item):
    intitule_formation = scrapy.Field()
    formacodes_code = scrapy.Field()
    intitule_certification = scrapy.Field()
    date_limite_candidature = scrapy.Field()
    type_formation = scrapy.Field()
    lieu = scrapy.Field()
    date_debut = scrapy.Field()
    duree = scrapy.Field()
    niveau_sortie = scrapy.Field()
