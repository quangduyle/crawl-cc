import scrapy
from find_phone.items import FindPhoneItem
from find_phone.itemloaders import ProductLoader

class PhoneSpider(scrapy.Spider):
    name = "phone"
    allowed_domains = ["clickbuy.com.vn"]
    start_urls = ["https://clickbuy.com.vn"]

    def parse(self, response):
        for url in response.css('a.menu-category__link.is_has_child::attr(href)').getall():
            yield scrapy.Request(f'https://clickbuy.com.vn/{url}', callback=self.parse_category, dont_filter=True)

    def parse_category(self, response):
        products = response.css('div.list-products__item')
        phone_item = FindPhoneItem()
        for product in products:
            phone_item  = ProductLoader(item = FindPhoneItem(), selector =product)
            phone_item.add_css('name', 'h3.title_name::text')
            phone_item.add_css('price', 'ins.new-price.js-format-price::attr(data-price)')
            phone_item.add_css('old_price', 'del.old-price.js-format-price::attr(data-price)')
            phone_item.add_css('link', 'a::attr(href)')
            yield phone_item .load_item()

        next_page = response.css('a[rel="next"]::attr(href)').get() 
        if next_page is not None:
            yield response.follow(next_page, callback =  self.parse_category)

        pass
