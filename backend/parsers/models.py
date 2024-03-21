from chrome_create_and_configurate import chrome_configuration


class Parser:
    def __init__(self, site_url, company_name):
        self.site_url = site_url
        self.company_name = company_name
        self.browser = chrome_configuration()
        self.last_results = dict()
