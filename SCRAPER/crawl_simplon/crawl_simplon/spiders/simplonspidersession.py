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
        all_sessions_url = response.xpath("//a[contains(@class, 'btn-formation') and contains(text(), 'Les sessions ouvertes')]/@href").get()
        if all_sessions_url:
            yield response.follow(all_sessions_url, meta={"item": item}, callback=self.parse_session)
        
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

