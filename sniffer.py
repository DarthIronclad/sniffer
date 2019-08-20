import scrapy, logging, json, unittest
from scrapy.crawler import CrawlerProcess
import re

global website
website = 'http://Google.com'  # URL to Scrape http://172.18.58.238/zipper/


class MySpider1(scrapy.Spider):  # USE to execute Scrapy
    # Your first spider definition
    name = 'Hello'  # Name of the scraper
    start_urls = [website]  # Website to scrapt

    def got_http(self, data):  # Full link
        if "http" in data:
            return data

        else:
            return website + data

    def parse(self, response):  # Compulsory function to execute scrapy codes

        # Website status
        print("-" * 100);
        print("\nWebsite status code -> {}  \n".format(response.status));
        print("-" * 100)  # Printing Status code

        print("\nGet Response Header\n");
        print(response.headers.to_string().decode("utf-8"));
        print("-" * 100)  # Printing GET Response Header

        print("\nGET Request Header\n");
        print(response.request.headers.to_string().decode("utf-8"));
        print("-" * 100)  # Printing User-agent

        print("Opening in browser!");
        print("-" * 100)  # OPen Browser
        # scrapy.utils.response.open_in_browser(response)

        # Extracting image links on root website
        website_image = response.css('img').xpath('@src').extract()  # Extracting any pictures in website

        in_json_image = json.dumps(website_image)  # putting it in a json format

        print("\nPrinting all image links in root website\n")  # Print how many images are there

        for image in json.loads(in_json_image):  # Extracting the json

            print(self.got_http(image) + "\n")  # Printing the links

        print("-" * 100)

        # Other links
        self.website_links = response.css('link').xpath("@href").extract()  # Extracting other links in the root website

        print("\nPrinting all image links in other websites\n")

        self.other_image = []

        for each_link in self.website_links:
            all_links = self.got_http(each_link)

            yield scrapy.Request(all_links,
                                 callback=self.website_other_links)  # Scraping the other websites using a generator something like return but better and sening the response to a function

    def website_other_links(self, response):

        for weblinks in response.body.decode("utf-8").split(
                "\n"):  # Split all the data new line by new line as its in byte format

            if "background-image: url(../" in weblinks:  # Find this specific string in the response

                source = re.findall("\\.\\..*\\;", weblinks)  # A regex to find the image link

                for source_images in source:  # For everything it find in the regex command above , append it to the list which is called (self.weblist)

                    link = self.got_http(
                        source_images)  # If there's http in the link , no need to add an extra http format

                    final_link = link.replace("..", "").replace(")", "").replace(";",
                                                                                 "")  # Extra string manupliation to remove unwanted charathers

                    in_json_image = json.dumps([final_link])  # in json format

                    for each in json.loads(in_json_image):  # print image links from the json

                        print(each)


class TestScript(unittest.TestCase):  # Unittest Class

    def test(self):
        self.assertTrue("http" in website, "invalid address format")  # Test if the string has http in it.
        logging.getLogger('scrapy').propagate = False  # Off scrapy verbose crap
        process = scrapy.crawler.CrawlerProcess({'USER_AGENT': "Mobile"})  # Modify mobile agent
        process.crawl(MySpider1)  # Selecting spider class
        process.start()  # the script will block here until all crawling jobs are finished


unittest.main()  # Execting the whole script
