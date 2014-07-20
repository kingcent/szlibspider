#coding=utf-8

from time import time,localtime,strftime

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector, Selector
from scrapy.http import Request
from scrapy.item import Item
from scrapy import log

from selenium import selenium
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException

def ajax_complete(driver):
    try:
        return 0 == driver.execute_script("return jQuery.active")
    except WebDriverException:
        pass

class SzlibSpider(CrawlSpider):
    name = "szlibspider"
    start_urls = []
#    start_urls = ["http://www.szlib.gov.cn/libraryNetwork/selfLib/id-5.html"]

    rules = (
#        Rule(SgmlLinkExtractor(allow=('\.html', )), callback='parse_page',follow=True),
        Rule(SgmlLinkExtractor(allow=('\.html', )), callback='parse_page'),
    )

    def __init__(self):
        CrawlSpider.__init__(self)
	log.start(logfile="./log/szlib-%s.log" % strftime("%m%d-%H-%M",localtime(time())), loglevel=log.INFO,logstdout=False)
	log.msg("szlibspider start")
	print "szlibspider start"
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, "*firefox /usr/lib/firefox/firefox", "http://www.szlib.gov.cn/libraryNetwork/selfLib/id-5.html")
	ffdriver = Firefox()
	self.selenium.start(driver=ffdriver)
#	self.selenium.start()


        sel = self.selenium
#        sel.open("http://www.szlib.gov.cn/libraryNetwork/selfLib/id-5.html")
        ffdriver.get("http://www.szlib.gov.cn/libraryNetwork/selfLib/id-5.html")
	WebDriverWait(ffdriver,30).until(ajax_complete, "Timeout waiting page to load")	

        #Wait for javscript to load in Selenium
#        time.sleep(20)
#	sel.wait_for_condition("condition by js", 20000);
#	print "ul/li visible? %s" % sel.is_element_present("//ul[@class='servicepointlist']")

	elements = ffdriver.find_elements_by_xpath("//div[@class='boxtext']/div[@class='filterbox_1']/div[@class='text tab_4_tit district_list']/a")
	num = "wijefowaeofjwejf SSL0011"
	selflibs_num = []
	for district in elements[1:]:
		log.msg("%s selflibs:" % district.text)
		log.msg("==================")
		district.click()
		WebDriverWait(ffdriver,30).until(ajax_complete, "Timeout waiting to load selflibs")	
		selflibs_elements = ffdriver.find_elements_by_xpath("//ul[@class='servicepointlist']/li[@class='item']")
		for selflib_ele in selflibs_elements:
#			num = selflib_ele.find_element_by_class_name("num").text
			num = selflib_ele.find_element_by_class_name("num").get_attribute("textContent")
			log.msg("num %s" % num)
			selflibs_num.append(num[-7:])
			log.msg("numid %s" % num[-7:] )
			log.msg("%s" % selflib_ele.find_element_by_class_name("title").get_attribute("textContent"))
			log.msg("%s" % selflib_ele.find_element_by_class_name("text").get_attribute("textContent"))
			log.msg("---------------")


	log.msg("------1---------")
#	ffdriver.quit()
#	numstr = unicode("编号","utf-8")
#	numstr = unicode(num,"utf-8")
#	log.msg("numstr is in num? %s" % (numstr in num))
#	log.msg("%s,%s, %s" % (num,num[1], num[-7:]))

	for selflibnum in selflibs_num:
		selflib_url ="http://www.szlib.gov.cn/libraryNetwork/dispSelfLibBook/id-5/%s.html" % selflibnum 
		log.msg("selflib url %s" % selflib_url)
	        ffdriver.get(selflib_url)
		WebDriverWait(ffdriver,30).until(ajax_complete, "Timeout waiting to load booklist")	
		categorys_elements = ffdriver.find_elements_by_xpath("//div[@class='boxtext']/div[@class='filterbox_1']/div[@class='text tab_4_tit category']/a")
		for category_ele in categorys_elements[1:]:
			log.msg("%s" % category_ele.text)

	#ffdriver.back()
		
#		print "----kctest3:%s" % element.text()
        #Do some crawling of javascript created content with Selenium
#        sel.get_text("//div")
#	text2 =	sel.get_text("//ul[@class='servicepointlist']/li[1]/div[1]")
#	print "----kctest2:%s" % text2
#	element = ffdriver.find_element_by_xpath("//ul[@class='servicepointlist']/li[1]")


    def __del__(self):
        self.selenium.stop()
        print self.verificationErrors
        CrawlSpider.__del__(self)

    def parse_page(self, response):
        item = Item()

#        hxs = HtmlXPathSelector(response)
        hxs = Selector(response)
        #Do some XPath selection with Scrapy
	text = hxs.xpath('//div').extract()
#	text = hxs.xpath('//div[@id="u"]/a[@id="imsg"]').extract()
#	text = hxs.xpath("//div[@id='content']/div[@id='m']/p[@id='lk']/a[3]").extract()
	log.msg("-----kctest: %s" % text)

        sel = self.selenium
        sel.open(response.url)

        #Wait for javscript to load in Selenium
        time.sleep(4)

        #Do some crawling of javascript created content with Selenium
#        sel.get_text("//div")
	text2 =	sel.get_text("//ul[@class='servicepointlist']/li[1]/div[1]")
	log.msg("----kctest2:%s" % text2)
#        yield item

# Snippet imported from snippets.scrapy.org (which no longer works)
# author: wynbennett
# date  : Jun 21, 2011
