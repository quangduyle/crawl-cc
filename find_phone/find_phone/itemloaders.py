from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst


class ProductLoader(ItemLoader):
    default_input_processor = TakeFirst()
    price_in = MapCompose(lambda x: float(x))
    old_price_in = MapCompose(lambda x: float(x))
    link_in = MapCompose(lambda x: "https://clickbuy.com.vn" + x)