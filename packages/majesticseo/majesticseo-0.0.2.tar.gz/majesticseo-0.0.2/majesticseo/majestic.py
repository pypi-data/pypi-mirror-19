import requests
from majesticseo.items import Item

# -*- coding: utf-8 -*-


class Majestic(object):

    """
    Core class which create a Majestic object which will trigger requests to the API
    """
    def __init__(self, api_key):
        self.api_key = api_key
        self.endpoint = 'https://api.majestic.com/api/json?'
        self.subscription_info = self.get_subscription_info()
        # self.res_units = self.subscription_info['TotalAnalysisResUnits']

    def get_subscription_info(self):
        params = {
            'cmd': 'GetSubscriptionInfo',
            'app_api_key': self.api_key
        }
        r = requests.get(self.endpoint, params=params)
        return r.json()

    def get_info(self, items):
        """
        Standard method that takes a list of items (Urls, subdomains or domains) and return
        description data of each item.
        :param items: List of domains/subdomains
        :return: List of Item objects.
        """
        params = {
            'items': len(items),
            'app_api_key': self.api_key,
            'cmd': 'GetIndexItemInfo',
            'datasource': 'fresh'
        }
        for i, item in enumerate(items):
            params['item{}'.format(i)] = item
        r = requests.get(self.endpoint, params=params)
        response_object = InfoResponse(r.json())
        return response_object

    def get_backlinks(self, item, max_results=1000, max_per_domain=1, max_per_source=1, remove_deleted=True):
        params = {
            'app_api_key': self.api_key,
            'cmd': 'GetBackLinkData',
            'MaxSourceURLsPerRefDomain': max_per_domain,
            'MaxSameSourceURLs': max_per_source,
            'Mode': int(remove_deleted),
            'Count': max_results,
            'item': item
        }
        r = requests.get(self.endpoint, params=params)
        return r.json()


class InfoResponse(object):

    def __init__(self, response):
        self.json = response
        self.code = response['Code']
        self.error_message = response['ErrorMessage']
        self.index_type = self.parse_index_type()
        self.domains_analysed = response['QueriedRootDomains']
        self.subdomains_analysed = response['QueriedSubDomains']
        self.urls_analysed = response['QueriedURLs']
        self.items = self.parse_response_items()

    def parse_index_type(self):
        if self.json.get('IndexType') == 0:
            return 'historic'
        return 'fresh'

    def parse_response_items(self):
        items = list()
        for item in self.json['DataTables']['Results']['Data']:
            item = self.create_item(item)
            items.append(item)
        return items

    def create_item(self, item):
        item = Item(item)
        return item


if __name__ == '__main__':
    majestic = Majestic(api_key='770234E562D7E51D66DCB1138DBB27B3')
    print(majestic.subscription_info)
