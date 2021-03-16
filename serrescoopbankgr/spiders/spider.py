import scrapy

from scrapy.loader import ItemLoader

from ..items import SerrescoopbankgrItem
from itemloaders.processors import TakeFirst


class SerrescoopbankgrSpider(scrapy.Spider):
	name = 'serrescoopbankgr'
	start_urls = ['https://www.serrescoopbank.gr/%CE%AD%CF%84%CE%BF%CF%82-2008.html']

	def parse(self, response):
		post_links = response.xpath('//*/article')
		for post in post_links:
			title = post.xpath('.//h2//text()[normalize-space()]').get()
			description = post.xpath('.//section[@class="article-intro clearfix"]//text()[normalize-space() and not(ancestor::time)]').get()
			date = post.xpath('.//time/text()').get()
			if date:
				date = date.split(':')[1]

			item = ItemLoader(item=SerrescoopbankgrItem(), response=response)
			item.default_output_processor = TakeFirst()
			item.add_value('title', title)
			item.add_value('description', description)
			item.add_value('date', date)
			yield item.load_item()

		next_page = response.xpath('//*[(@id = "Mod1")]//a/@href').getall()
		yield from response.follow_all(next_page, self.parse)
