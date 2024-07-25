import scrapy
from crawl_simplon.items import CrawlSimplonItemSession
import re

class SimplonspiderSpiderSession(scrapy.Spider):

    name = "simplonspidersession"

    allowed_domains = ["simplon.co", "francecompetences.fr"]
    start_urls = ["https://simplon.co/notre-offre-de-formation.html#nos-formations0"]

    custom_settings = {
        'ITEM_PIPELINES': {
            "crawl_simplon.pipelines.CrawlSimplonPipelineSession": 310,
            "crawl_simplon.pipelines.CrwalSimplonPipelineSessionSave": 315,
        },
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',
    }

    def parse(self, response):
        formation_urls = response.xpath("//div[@class='card-group-button']/a[contains(text(),'Découvrez')]/@href").getall()
        for formation_url in formation_urls:
            yield scrapy.Request(response.urljoin(formation_url), callback=self.parse_formation)

    def parse_formation(self, response):

        item = CrawlSimplonItemSession()

        all_sessions_url = response.xpath("//a[contains(@class, 'btn-formation') and contains(text(), 'Les sessions ouvertes')]/@href").get()
        if all_sessions_url:
            yield scrapy.Request(all_sessions_url, meta={"item": item}, callback=self.parse_session)
        
        yield item

    def parse_session(self, response):
        item = response.meta["item"]
        sessions = response.xpath("//div[@class='smp-card']")

        # Récupérer l'id et le nom url de chaque formation
        url = response.url
        pattern = re.compile(r'https://simplon\.co/i-apply/([^/]+)/(\d+)')
        match = pattern.search(url)
        if match:
            nom_session = match.group(1)
            id_session = match.group(2)
            item["NomSessionUrl"] = nom_session
            item["IdSession"] = id_session

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
            item['Ville'] = [ville.strip() for ville in session.xpath(".//div[@class='card-content']//text()").getall() if ville.strip()]


            # Extract the session detail URL and follow it
            session_url = session.xpath(".//a[contains(text(),'Découvrez')]/@href").get()
            if session_url:
                yield scrapy.Request(response.urljoin(session_url), meta={"item": item}, callback=self.parse_session_detail)
            else:
                yield item

    def parse_session_detail(self, response):
        item = response.meta["item"]
        # Extract the code session from the URL
        url = response.url
        self.logger.info(f"Processing session URL: {url}")  # Debug statement
        pattern = re.compile(r'https://simplon\.co/session/[^/]+/(\d+)$')
        match = pattern.search(url)
        if match:
            item["Code_Session"] = match.group(1)
        else:
            self.logger.warning(f"URL did not match pattern: {url}")  # Debug statement
        yield item