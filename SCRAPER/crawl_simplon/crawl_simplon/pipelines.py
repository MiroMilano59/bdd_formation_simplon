# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter

from itemadapter import ItemAdapter
import re
import dateparser
from scrapy.exceptions import NotConfigured



class CrawlSimplonPipelineFormation:

    def __init__(self, spider_name):
        self.spider_name = spider_name


    @classmethod
    def from_crawler(cls, crawler):
        spider_name = crawler.spider.name
        if spider_name != 'simplonspiderformation':
            raise NotConfigured
        return cls(spider_name)


    def process_item(self, item, spider):
        item = self.clean_formacode_brut(item)
        item = self.clean_rncp_rs_urls(item)
        item = self.clean_date_echance_enregistrement(item)
        item = self.clean_nfs(item)
        item = self.clean_formacode(item)
        
        return item
    
    def clean_rncp_rs_urls(self, item):
        adapter = ItemAdapter(item)
        formacodes = adapter.get("RncpRsUrls")

        if formacodes:
            formacodes_url_https = [code.replace("http://", "https://").rstrip("/") for code in formacodes]
            item["RncpRsUrls"] = set(formacodes_url_https)
        else:
            item["RncpRsUrls"] = "FormationNonCertifiante"
            
        return item
    
    def clean_formacode_brut(self, item):
        adapter = ItemAdapter(item)
        formacodes = adapter.get("FormacodesBrut")
        if formacodes:
            formacodes_strip = [formacode.replace(":", "").replace(",", "").replace("(", "").replace(")", "").strip() for formacode in formacodes]
            item["FormacodesBrut"] = formacodes_strip

        return item

    def clean_date_echance_enregistrement(self, item):
        adapter = ItemAdapter(item)
        formacodes = adapter.get("FormacodesBrut")

        if formacodes:
            adapter["DateEchanceEnregistrement"] = dateparser.parse(formacodes[-1], settings={'DATE_ORDER': 'DMY'}).date()
            adapter["NiveauDeSortie"] = formacodes[0] if "Niveau" in formacodes[0] else ""
        
        return item

    def clean_nfs(self, item):
        adapter = ItemAdapter(item)
        formacodes = adapter.get("FormacodesBrut")
  
        nfs_codes = []
        libelle_nfs_codes = []
  
        regex_nsf = re.compile(r"^\d{3}[a-zA-Z]$")
        if formacodes:
            for i, element in enumerate(formacodes):
                if regex_nsf.match(element) and i + 1 < len(formacodes):
                    nfs_codes.append(element)
                    libelle_nfs_codes.append(formacodes[i + 1])
                
        item["NfsCode"] = nfs_codes
        item["LibelleNfsCode"] = libelle_nfs_codes

        return item

    def clean_formacode(self, item):
        adapter = ItemAdapter(item)
        formacodes = adapter.get("FormacodesBrut")
  
        forma_codes = []
        libelle_nforma_codes = []
        regex_formacode = re.compile(r"^\d{5}$")

        if formacodes:
            for i, element in enumerate(formacodes):
                if regex_formacode.match(element) and i + 1 < len(formacodes):
                    forma_codes.append(element)
                    libelle_nforma_codes.append(formacodes[i + 1])
                
        item["FormaCode"] = forma_codes
        item["LibelleFormaCode"] = libelle_nforma_codes

        return item


class CrawlSimplonPipelineSession:

    def __init__(self, spider_name):
        self.spider_name = spider_name

    @classmethod
    def from_crawler(cls, crawler):
        spider_name = crawler.spider.name
        if spider_name != 'simplonspidersession':
            raise NotConfigured
        return cls(spider_name)

    def process_item(self, item, spider):
        item = self.clean_organisme_partenaire(item)
        item = self.clean_alternance(item)
        item = self.clean_distance(item)
        item = self.clean_niveau_sortie(item)
        return item
      
    def clean_organisme_partenaire(self, item):
        # Extraire les mots clés Microsoft, Apple et Google de "Libele_Certification"
        libele_certification = item.get('Libele_Certification', '')
        partenaires = ['Microsoft', 'Apple', 'Google']
        extracted_partenaires = [partenaire for partenaire in partenaires if partenaire in libele_certification]
        item['Organisme_Partenaire'] = extracted_partenaires
        return item

    def clean_alternance(self, item):
        adapter = ItemAdapter(item)
        # Vérifier si "Alternance" apparait dans "Type_Formation" et retourner True si c'est le cas
        type_formation = adapter.get('Type_Formation', [])
        item['Alternance'] = any('alternance' in tf.lower() for tf in type_formation)
        return item

    def clean_distance(self, item):
        adapter = ItemAdapter(item)
        # Vérifier si "Distance" apparait dans "Type_Formation" et retourner True si c'est le cas
        type_formation = adapter.get('Type_Formation', [])
        item['Distance'] = any('Distan' in tf for tf in type_formation)
        return item

    def clean_niveau_sortie(self, item):
        adapter = ItemAdapter(item)
        # Retirer "Sortie : " du début de la chaîne "Niveau_Sortie"
        niveau_sortie = adapter.get('Niveau_Sortie', [])
        cleaned_niveau_sortie = [niveau.replace('Sortie : ', '').strip() for niveau in niveau_sortie]
        item['Niveau_Sortie'] = cleaned_niveau_sortie
        return item


class FormationDataBasePipeline:

    def open_spider(self, spider):
        self.session_maker = models.db_connect(echo=False)
        self.session = self.session_maker()


    def add_and_commit(self, item, warner=""):
        """
        Commit changes if ACID compliant or rollback otherwise with message.

        Parameter(s):
            item (MobieDB): Instance (i.e. row) of one table to be added to it. 
            warner (str): OPTIONAL. Message to display if transaction aborted.
                          Default: `Transaction aborted. Session rolled back`
                          Optionally : `warner` can be set to None in order not
                          to show any warning message. At your own risk !
        """
        # PROCESSING WARNING MESSAGE
        txt = "Transaction aborted. Session rolled back"
        warner = txt if warner == "" else warner

        # ADDING GIVEN INSTANCE TO THE DATABASE
        self.session.add(item)

        # COMMITING PROCESS (validation of the transaction)
        try:
            self.session.commit()
        except alchemyError.IntegrityError:
            self.session.rollback()
            if warner:
                print(warner)