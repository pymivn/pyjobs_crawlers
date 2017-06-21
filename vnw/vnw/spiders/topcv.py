# -*- coding: utf-8 -*-
import logging
import scrapy
from scrapy_splash import SplashRequest

from ..keywords import KWS
from ..items import PyjobItem
from ..pymods import xtract

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger()

script = """
function main(splash)
    local url = splash.args.url
    assert(splash:go(url))
    assert(splash:wait(5))

    return {
        html = splash:html()
    }
end
"""

script_next_page = """
function main(splash)
    local url = splash.args.url
    assert(splash:go(url))
    assert(splash:wait(0.5))

    return {
        html = splash:html()
    }
end
"""


class TopCVSpider(scrapy.Spider):
    name = "topcv"
    allowed_domains = ["topcv.vn"]
    login_page = "https://www.topcv.vn/login"  # TODO: wage
    start_urls = [
        ("https://www.topcv.vn/viec-lam/"
         "tat-ca-nganh-nghe/moi-nhat?tim-kiem=" + kw) for kw in KWS
    ]
    fmt_base_url = ('https://www.topcv.vn/viec-lam/tat-ca-nganh-nghe/'
                    'moi-nhat?tim-kiem={}')

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, endpoint='execute',
                                args={'lua_source': script})

    def parse(self, resp):
        keyword = resp.url.split("?tim-kiem=")[1].split("&")[0]
        base_url = self.fmt_base_url.format(keyword)
        for href in resp.xpath('//div[@class="box box-white job"]'
                               '//h4/a/@href').extract():
            request = scrapy.Request(resp.urljoin(href), self.parse_content)
            request.meta["keyword"] = keyword
            yield request

        try:
            page_selector = resp.xpath(
                '//div[@class="box box-white"]//'
                'div[@class="col-sm-9 col-md-8"]'
                '/div[@class="text-center"]/text()'
            )
            current_page = page_selector.extract_first().split()[1]
            total_page = page_selector.extract_first().split()[3]
            if int(current_page) < int(total_page):
                url = base_url + "&page={}".format(
                    int(current_page) + 1
                )
                yield SplashRequest(url, endpoint='execute',
                                    args={'lua_source': script_next_page})

        except ValueError as e:
            _logger.error(e)

    def parse_content(self, resp):
        item = PyjobItem()
        item["keyword"] = resp.meta["keyword"]
        item['url'] = resp.url
        item['name'] = xtract(
            resp,
            ('//div[@class="box box-white"]//h1/text()')
        )
        item['company'] = xtract(
            resp,
            ('//div[@class="box box-white"]'
             '//div[@class="company-title"]/a/text()')
        )
        item["address"] = xtract(
            resp,
            ('//div[@class="box box-white"]'
             '//div[contains(@class, "company-meta")]/text()')
        )

        job_meta = ('//div[@class="box box-white"]'
                    '//div[contains(@class, "job-meta")]/div/div[{}]/text()')
        item["expiry_date"] = xtract(
            resp,
            job_meta.format(1)
        )
        item["post_date"] = ''
        item["wage"] = xtract(
            resp,
            job_meta.format(2)
        )
        item["province"] = xtract(
            resp,
            job_meta.format(3)
        )

        job_detail = ('//div[@class="box box-white padding-list"]'
                      '[{}]/div/p/text()')

        if xtract(resp, job_detail.format(1)):
            item["work"] = xtract(resp, job_detail.format(1))
        else:
            item["work"] = xtract(
                resp,
                ('//div[@class="box box-white padding-list"][1]'
                 '/div/ul/li/text()')
            )

        if xtract(resp, job_detail.format(2)):
            item["specialize"] = xtract(
                resp,
                job_detail.format(2)
            )
        else:
            item["specialize"] = xtract(
                resp,
                ('//div[@class="box box-white padding-list"][2]'
                 '/div/ul/li/text()')
            )

        item["welfare"] = xtract(
            resp,
            ('//div[@class="box box-white padding-list"]'
             '[3]/div/div/text()')
        )

        item["size"] = ''
        yield item
