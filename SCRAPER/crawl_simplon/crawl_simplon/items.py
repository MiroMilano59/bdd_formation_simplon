# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class CrawlSimplonItem(scrapy.Item):
    LibelleFormationSimplon = scrapy.Field()
    ResumeProgrammeSimplon = scrapy.Field()
    NomFormationUrl = scrapy.Field()
    IdFormation = scrapy.Field()
    RncpRsUrls = scrapy.Field()
    RncpRsUrl = scrapy.Field()
    CodeRS = scrapy.Field()
    CodeRNCP = scrapy.Field()
    IntituleCertification = scrapy.Field()
    EtatCertification = scrapy.Field()
    FormacodesBrut = scrapy.Field()
    DateEchanceEnregistrement = scrapy.Field()
    NiveauDeSortie = scrapy.Field()
    NfsCode = scrapy.Field()
    LibelleNfsCode = scrapy.Field()
    FormaCode = scrapy.Field()
    LibelleFormaCode = scrapy.Field()
 
class CrawlSimplonItemSession(scrapy.Item):
    Libele_Certification = scrapy.Field()
    Date_Limite_Candidature = scrapy.Field()
    Type_Formation = scrapy.Field()
    Nom_Dept = scrapy.Field()
    Date_Debut = scrapy.Field()
    Duree = scrapy.Field()
    Niveau_Sortie = scrapy.Field()
    Organisme_Partenaire = scrapy.Field()
    Alternance = scrapy.Field()
    Distance = scrapy.Field()
    NomSessionUrl = scrapy.Field()
    IdSession = scrapy.Field() 
    Code_Session = scrapy.Field()
    Ville = scrapy.Field()
    Code_Dept = scrapy.Field()
