from .story import Story


class Debt(Story):
    ident = 'D'
    typename = 'Debt'
    api_detail_name = 'debt-detail'
    api_list_name = 'debt-list'
