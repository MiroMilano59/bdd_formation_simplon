import scrapy
from crawl_simplon.items import CrawlSimplonItem
import re
import logging

class SimplonspiderSpiderFormation(scrapy.Spider):
    
    name = "simplonspiderformation"
    allowed_domains = ["simplon.co", "francecompetences.fr"]
    start_urls = ["https://simplon.co/notre-offre-de-formation.html#nos-formations0"]
    
    custom_settings = {
        'ITEM_PIPELINES' : {
            "crawl_simplon.pipelines.CrawlSimplonPipelineFormation": 300,
            "crawl_simplon.pipelines.CrwalSimplonPipelineRncpInfoSave": 310,
            "crawl_simplon.pipelines.CrwalSimplonPipelineFormacodesInfoSave": 311,
            "crawl_simplon.pipelines.CrwalSimplonPipelineRsInfoSave": 312,
            "crawl_simplon.pipelines.CrwalSimplonPipelineNsfInfoSave": 313,
            "crawl_simplon.pipelines.CrwalSimplonPipelineFormationSave": 314,
            "crawl_simplon.pipelines.CrwalSimplonPipelineFormationFormacodeSave": 320,
            "crawl_simplon.pipelines.CrwalSimplonPipelineFormationNsfSave": 325,
            "crawl_simplon.pipelines.CrwalSimplonPipelineFormationRsfSave": 330,
            "crawl_simplon.pipelines.CrwalSimplonPipelineFormationRncpfSave": 331,
            "crawl_simplon.pipelines.CrwalSimplonPipelineFormationRncpNsfSave": 332,
            "crawl_simplon.pipelines.CrwalSimplonPipelineFormationRncpFormacodeSave": 333,
            "crawl_simplon.pipelines.CrwalSimplonPipelineFormationRsNsfSave": 334,
            "crawl_simplon.pipelines.CrwalSimplonPipelineFormationRsFormacodeSave": 335,
        },
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',
    }

    def parse(self, response):
        formation_urls = response.xpath("//div[@class='card-group-button']/a[contains(text(),'Découvrez')]/@href").getall()
        for formation_url in formation_urls:
            yield scrapy.Request(formation_url, callback=self.parse_formation)

    def parse_formation(self, response):
        item = CrawlSimplonItem()
        item['LibelleFormationSimplon'] = response.xpath("//h1/text()").get() # Nom de la formation sur le site simplon

        item['ResumeProgrammeSimplon'] = [programme.strip() for programme in response.xpath('//div[@id="programme-content"]//text()').getall() if programme.strip()]

        # Récupérer l'id et le nom url de chque formation
        url = response.url
        pattern = re.compile(r'https://simplon\.co/formation/([^/]+)/(\d+)')
        match = pattern.search(url)
        if match:
            nom_formation = match.group(1)
            id_formation = match.group(2)
            item["NomFormationUrl"] = nom_formation
            item["IdFormation"] = id_formation

        print(f"Parsing formation: {response.url}")

        item["RncpRsUrls"] = response.xpath("//a[contains(@href,'francecompetences.fr') and (contains(@href,'/rs/') or (contains(@href,'/rncp/')))]/@href").getall()

        if not item["RncpRsUrls"]:
            yield item
        
        elif item["RncpRsUrls"]:

            for url in item["RncpRsUrls"]:

                item["RncpRsUrl"] = url

                rs_match = re.search(r'rs/(\d+)', url)
                rncp_match = re.search(r'rncp/(\d+)', url)
                item['CodeRS'] = ""
                item['CodeRNCP'] = ""

                if rs_match:

                    item['CodeRS'] = rs_match.group(1)

                if rncp_match:

                    item['CodeRNCP'] = rncp_match.group(1)
                
                formacode_item = CrawlSimplonItem()
                formacode_item.update(item)

                yield scrapy.Request(url, callback=self.parse_all_formacode, meta={"item": formacode_item})
        
        else:
            pass

    
    def parse_all_formacode(self, response):
        
        item = response.meta["item"]

        item["IntituleCertification"] = response.xpath('//h1[@class="title--page--generic"]/text()').get()

        code_fiche_etat = response.xpath('//div[@class="banner--fcpt-certification__body__tags"]//span[@class="tag--fcpt-certification__status font-bold"]/text()').getall()
        if code_fiche_etat:
            # item["EtatCertification"] = f"Etat_{response.url.split('/')[-2]}-{code_fiche_etat[1]}"
            item["EtatCertification"] = code_fiche_etat[1]

        formacodesbruts = response.xpath("//div[contains(@class,'list--fcpt-certification') and contains(@class, '__text')]//text()").getall()
        formacodes = [code.strip() for code in formacodesbruts if code.strip()]
        item["FormacodesBrut"] = formacodes
        
        yield item
