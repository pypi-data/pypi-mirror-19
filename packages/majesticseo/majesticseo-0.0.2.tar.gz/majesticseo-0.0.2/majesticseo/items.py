class Item(object):
    """
    Base Item of an element analysed by the API (URL, subdomain or domain).
    """
    def __init__(self, body):
        self.json = body
        self.source = body['Item']
        self.type = self.get_item_type()
        self.trust_flow = body['TrustFlow']
        self.citation_flow = body['CitationFlow']
        self.tf = body['TrustFlow']
        self.cf = body['CitationFlow']
        self.referring_domains_size = body['RefDomains']
        self.backlinks_size = body['ExtBackLinks']
        # self.api_costs = self.get_api_costs()

        # Following attributes are empty but can be filled using appropriates methods.
        self.referring_domains = None
        self.backlinks = None

    def get_item_type(self):
        if self.json['ItemType'] == 3:
            return 'url'
        elif self.json['ItemType'] == 1:
            return 'domain'
        else:  # itemtype = 2
            return 'subdomain'

    def get_referring_domains(self):
        pass

    def get_backlinks(self, max_per_domain=1 ):
        pass

