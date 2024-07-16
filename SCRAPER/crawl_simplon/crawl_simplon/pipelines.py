# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter


# class CrawlSimplonPipeline:
#     def process_item(self, item, spider):
#         item = self.clean_libele_certification(item)
#         item = self.clean_organisme_partenaire(item)
#         item = self.clean_alternance(item)
#         item = self.clean_distance(item)
#         item = self.clean_niveau_sortie(item)
#         return item

#     def clean_libele_certification(self, item):
#         pass

#     def clean_organisme_partenaire(self, item):
#         pass

#     def clean_alternance(self, item):
#         pass

#     def clean_distance(self, item):
#         pass

#     def clean_niveau_sortie(self, item):
#         pass

from itemadapter import ItemAdapter
import sqlalchemy.exc as alchemyError
from BDD import models 


class CrawlSimplonPipeline:
    def process_item(self, item, spider):
        item = self.clean_organisme_partenaire(item)
        item = self.clean_alternance(item)
        item = self.clean_distance(item)
        item = self.clean_niveau_sortie(item)
        return item
    
    def clean_formacode(self, item):
        pass

    def clean_date_echeance_certification(self, item):
        pass

    def clean_organisme_partenaire(self, item):
        # Extraire les mots clés Microsoft, Apple et Google de "Libele_Certification"
        libele_certification = item.get('Libele_Certification', '')
        partenaires = ['Microsoft', 'Apple', 'Google']
        extracted_partenaires = [partenaire for partenaire in partenaires if partenaire in libele_certification]
        item['Organisme_Partenaire'] = extracted_partenaires
        return item

    def clean_alternance(self, item):
        # Vérifier si "Alternance" apparait dans "Type_Formation" et retourner True si c'est le cas
        type_formation = item.get('Type_Formation', [])
        item['Alternance'] = any('alternance' in tf.lower() for tf in type_formation)
        return item

    def clean_distance(self, item):
        # Vérifier si "Distance" apparait dans "Type_Formation" et retourner True si c'est le cas
        type_formation = item.get('Type_Formation', [])
        item['Distance'] = any('Distan' in tf for tf in type_formation)
        return item

    def clean_niveau_sortie(self, item):
        # Retirer "Sortie : " du début de la chaîne "Niveau_Sortie"
        niveau_sortie = item.get('Niveau_Sortie', [])
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