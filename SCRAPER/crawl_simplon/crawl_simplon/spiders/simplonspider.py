import scrapy
from crawl_simplon.items import CrawlSimplonItem


class SimplonspiderSpider(scrapy.Spider):
    name = "simplonspider"
    allowed_domains = ["simplon.co", "francecompetences.fr"]
    start_urls = ["https://simplon.co/notre-offre-de-formation.html#nos-formations0"]

    def parse(self, response):
        formation_urls = response.xpath("//div[@class='card-group-button']/a[contains(text(),'Découvrez')]/@href").getall()
        for formation_url in formation_urls:
            yield scrapy.Request(response.urljoin(formation_url), callback=self.parse_formation)
        
    def parse_formation(self, response):
        item = CrawlSimplonItem()
        item['Formacodes'] = [] 
        item['Libelle'] = response.xpath("//h1/text()").get()
        item['Resume_Programme'] = [programme.strip() for programme in response.xpath('//div[@id="programme-content"]//text()').getall() if programme.strip()]
        all_sessions_url = response.xpath("(//a[@class='btn btn-pricipale btn-formation'])[1]/@href").get()
        if all_sessions_url:
            meta = {"item": item}
            yield scrapy.Request(url=response.urljoin(all_sessions_url), meta=meta, callback=self.parse_session)
        
        formacodes_url = response.xpath("//a[contains(@href,'francecompetences.fr') and (contains(@href,'/rs/') or (contains(@href,'/rncp/')))]/@href").getall()
        if formacodes_url:
            for url in formacodes_url:
                meta = {"item": item}
                yield scrapy.Request(url=response.urljoin(url), meta=meta, callback=self.parse_formacode)

    def parse_formacode(self, response):
        item = response.meta["item"]
        
        formacodes = response.xpath("//div[contains(@class,'list--fcpt-certification') and contains(@class, '__text')]//text()").getall()
        formacodes = [code.strip() for code in formacodes if code.strip()]

        if formacodes:
            item['Formacodes'].extend(formacodes)
            
        yield item

    def parse_session(self, response):
        item = response.meta["item"]
        sessions = response.xpath("//div[@class='smp-card']")
        for session in sessions:
            item['Libele_Certification'] = session.xpath(".//h2/text()").get()
            day = session.xpath(".//span[@class='day']/text()").get().strip()
            month = session.xpath(".//span[@class='month']/text()").get().strip()
            year = session.xpath(".//div[@class='year']/text()").get().strip()
            item['Date_Limite_Candidature'] = f"{day}/{month}/{year}"
            item['Type_Formation'] = [typeforma.strip() for typeforma in session.xpath(".//div[@class='card-content-tag-container']//text()").getall() if typeforma.strip()]
            item['Nom_Dept'] = [loc.strip() for loc in session.xpath(".//i[contains(text(),'location')]/parent::div/text()").getall() if loc.strip()]
            item['Date_Debut'] = [date.strip() for date in session.xpath(".//div[@class='card-session-info calendar']/text()").getall() if date.strip()]
            item['Duree'] = [duree.strip() for duree in session.xpath(".//i[contains(text(),'hourglass_empty')]/parent::div/text()").getall() if duree.strip()]
            item['Niveau_Sortie'] = [niveau.strip() for niveau in session.xpath(".//i[contains(text(),'school')]/parent::div/text()").getall() if niveau.strip()]
            yield item
