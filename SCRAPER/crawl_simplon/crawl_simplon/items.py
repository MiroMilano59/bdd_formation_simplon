# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

# import scrapy

# class CrawlSimplonItem(scrapy.Item):
#     Libelle = scrapy.Field()
#     Formacodes = scrapy.Field()
#     Libele_Certification = scrapy.Field()
#     Date_Limite_Candidature = scrapy.Field()
#     Type_Formation = scrapy.Field()
#     Nom_Dept = scrapy.Field()
#     Date_Debut = scrapy.Field()
#     Duree = scrapy.Field()
#     Niveau_Sortie = scrapy.Field()
#     Resume_Programme = scrapy.Field()

import scrapy

class CrawlSimplonItem(scrapy.Item):
    Libelle = scrapy.Field()
    Formacodes = scrapy.Field()
    Libele_Certification = scrapy.Field()
    Date_Limite_Candidature = scrapy.Field()
    Type_Formation = scrapy.Field()
    Nom_Dept = scrapy.Field()
    Date_Debut = scrapy.Field()
    Duree = scrapy.Field()
    Niveau_Sortie = scrapy.Field()
    Resume_Programme = scrapy.Field()
    Distance = scrapy.Field()
    Alternance = scrapy.Field()
    Organisme_Partenaire = scrapy.Field()
