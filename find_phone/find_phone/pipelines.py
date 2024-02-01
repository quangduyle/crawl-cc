# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class FindPhonePipeline:
    def process_item(self, item, spider):
        return item

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

class USDPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Lấy giá và giá cũ từ item
        gia = adapter.get('price')
        gia_cu = adapter.get('old_price')

        # Kiểm tra xem có giá không và chuyển đổi nếu có
        if gia:
            if isinstance(gia, list):
                adapter['price'] = [round(x / 23000, 2) for x in gia]
            else:
                adapter['price'] = round(gia / 23000,2)

        # Kiểm tra xem có giá cũ không và chuyển đổi nếu có
        if gia_cu:
            if isinstance(gia_cu, list):
                adapter['old_price'] = [round(x / 23000,2) for x in gia_cu]
            else:
                adapter['old_price'] = round(gia_cu / 23000, 2)

        return item
    

class DuplicatePipeline:
    def __init__(self):
        self.items_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # # price_key = tuple(adapter.get('price', []))
        # # old_price_key = tuple(adapter.get('old_price', []))

        # # Create a tuple as a combined key
        # key = (adapter['name'][0], adapter['price'], adapter['old_price'], adapter['link'][0])
        name = adapter.get('name', [])
        price = adapter.get('price', [])
        old_price = adapter.get('old_price', [])
        link = adapter.get('link', [])

        # Chuyển đổi thành tuple, đồng thời loại bỏ giá trị null hoặc không có

        # price_tuple = tuple(price) if price else None
        # old_price_tuple = tuple(old_price) if old_price else None

        # Tạo khóa kết hợp
        key = (name[0] if name else None, price[0] if price else None, old_price[0] if old_price else None, link[0] if link else None)
        if key in self.items_seen:
            raise DropItem(f"Duplicate found: {item!r}")
        else:
            self.items_seen.add(key)
            return item