import scrapy, logging, json
from scrapy.crawler import CrawlerProcess
from scrapy.utils.response import open_in_browser
import re

global website
website = 'http://www.itsecgames.com/'


class MySpider1(scrapy.Spider):
    # Your first spider definition
    name = 'Hello'
    start_urls = [website]

    def parse(self, response):

        # Website status
        print("-" * 50);
        print("\nWebsite --> {} OK! \n".format(response));
        print("-" * 50)

        # printing GET response header
        print("\nGet Response Header\n");
        print(response.headers.to_string().decode("utf-8"));
        print("-" * 50)

        # print(response.request.headers[b'User-Agent']) #Printing User-agent

        # Other links
        website_links = response.css('link').xpath("@href").extract()

        for each_link in website_links:
            all_links = website + each_link
            yield scrapy.Request(all_links, callback=self.website_other_links)

        # Extracting image links on root website
        website_image = response.css('img').xpath('@src').extract()  # Extracting any pictuces in website
        in_json_image = json.dumps(website_image)

        print("\nPrinting all image links in root website --> {} images found\n".format(len(website_image)))

        for image in json.loads(in_json_image):
            print(website + image + "\n")

        print("Opening in browser!")

    # open_in_browser(response)

    def website_other_links(self, response):
        for weblinks in response.body.decode("utf-8").split("\n"):
            if "background-image: url(../" in weblinks:
                # print(weblinks)
                source = re.findall("\\.\\..*\\;", weblinks)

                for source_images in source:
                    final_link = website + source_images.replace("..", "").replace(")", "")
                    print(final_link)


logging.getLogger('scrapy').propagate = False
process = CrawlerProcess({'USER_AGENT': "Mobile"})
process.crawl(MySpider1)
process.start()  # the script will block here until all crawling jobs are finished
