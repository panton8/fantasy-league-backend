from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination as BasePageNumberPagination
from rest_framework.response import Response


class PageNumberPagination(BasePageNumberPagination):
    page_size_query_param = 'page_size'

    def get_next_link(self):
        if not self.page.has_next():
            return None

        return self.page.next_page_number()

    def get_previous_link(self):
        if not self.page.has_previous():
            return None

        return self.page.previous_page_number()

    def get_paginated_response(self, data):
        pagination = OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
        ])

        return Response(OrderedDict([
            ('pagination', pagination),
            ('results', data)
        ]))