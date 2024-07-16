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
        
        formacodes_urls = response.xpath("//a[contains(@href,'francecompetences.fr') and (contains(@href,'/rs/') or (contains(@href,'/rncp/')))]/@href").getall()
        for formacode_url in formacodes_urls:
            yield response.follow(formacode_url, meta={"item": item}, callback=self.parse_formacode)
        
        yield item

    def parse_formacode(self, response):
        item = response.meta["item"]
        formacodes = response.xpath("//div[contains(@class,'list--fcpt-certification') and contains(@class, '__text')]//text()").getall()
        formacodes = [code.strip() for code in formacodes if code.strip()]

        if formacodes:
            item['Formacodes'].extend(formacodes)
            
        yield item

