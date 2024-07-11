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
        item['intitule_formation'] = response.xpath("//h1/text()").get()
        all_sessions_url = response.xpath("(//a[@class='btn btn-pricipale btn-formation'])[1]/@href").get()
        if all_sessions_url:
            meta = {"item": item}
            yield scrapy.Request(url=response.urljoin(all_sessions_url), meta=meta, callback=self.parse_session)
        
        formacodes_url = response.xpath("//a[contains(@href,'francecompetences.fr')]/@href").getall()
        if formacodes_url:
            for url in formacodes_url:
                meta = {"item": item}
                yield scrapy.Request(url=response.urljoin(url), meta=meta, callback=self.parse_formacode)
        else:
            yield item

    # def parse_formacode(self, response):
    #     item = response.meta["item"]
    #     formacodes_rs = response.xpath("//button[contains(normalize-space(),'Formacode(s)')]/following-sibling::div//p/code/text()").getall()
    #     formacodes_rncp = response.xpath("//button[contains(normalize-space(),'Formacode(s)')]/following-sibling::div/[@class='accordion--icon-text--dotted__content']/text()").getall()
    #     item.setdefault('formacodes_code', []).extend(formacodes_rncp)
    #     item.setdefault('formacodes_code', []).extend(formacodes_rs)
    #     yield item

    def parse_formacode(self, response):
        item = response.meta["item"]
        
        # Récupérer les formacodes_rs s'ils existent et les nettoyer
        formacodes_rs = response.xpath("//button[contains(normalize-space(),'Formacode(s)')]/following-sibling::div//p/code/text()").getall()
        formacodes_rs = [code.strip() for code in formacodes_rs if code.strip()]

        # Récupérer les formacodes_rncp s'ils existent et les nettoyer
        formacodes_rncp = response.xpath("//button[contains(normalize-space(),'Formacode(s)')]/following-sibling::div[@class='accordion--icon-text--dotted__content']/text()").getall()
        formacodes_rncp = [code.strip() for code in formacodes_rncp if code.strip()]

        # Cumul des formacodes
        item.setdefault('formacodes_code', [])
        item['formacodes_code'].extend(formacodes_rs)
        item['formacodes_code'].extend(formacodes_rncp)

        # Si au moins un des formacodes a été trouvé, on yield l'item
        if item['formacodes_code']:
            self.scraped_items.append(item)
            yield item



    def parse_session(self, response):
        item = response.meta["item"]
        sessions = response.xpath("//div[@class='smp-card']")
        for session in sessions:
            item['intitule_certification'] = session.xpath(".//h2/text()").get()
            day = session.xpath(".//span[@class='day']/text()").get().strip()
            month = session.xpath(".//span[@class='month']/text()").get().strip()
            year = session.xpath(".//div[@class='year']/text()").get().strip()
            item['date_limite_candidature'] = f"{day}/{month}/{year}"
            item['type_formation'] = session.xpath(".//div[@class='card-content-tag']/a/text()").get()
            item['lieu'] = [loc.strip() for loc in session.xpath(".//i[contains(text(),'location')]/parent::div/text()").getall() if loc.strip()]
            item['date_debut'] = [date.strip() for date in session.xpath(".//div[@class='card-session-info calendar']/text()").getall() if date.strip()]
            item['duree'] = [duree.strip() for duree in session.xpath(".//i[contains(text(),'hourglass_empty')]/parent::div/text()").getall() if duree.strip()]
            item['niveau_sortie'] = [niveau.strip() for niveau in session.xpath(".//i[contains(text(),'school')]/parent::div/text()").getall() if niveau.strip()]
            yield item
