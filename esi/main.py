from scrapy import cmdline

# settings = cmdline.get_project_settings()


cmdline.execute("scrapy crawl esi".split())
