import math

from rest_framework import pagination
from rest_framework.response import Response


class LinkHeaderPagination(pagination.PageNumberPagination):
    """
    Pagination class that utilizes link headers. It additionally includes the x-total-count header.
    """

    def get_paginated_response(self, data):
        next_url = self.get_next_link()
        previous_url = self.get_previous_link()
        first_url = self.get_first_link()
        last_url = self.get_last_link()

        if next_url is not None and previous_url is not None:
            link = '<{next_url}>; rel="next", <{previous_url}>; rel="prev"'
        elif next_url is not None:
            link = '<{next_url}>; rel="next"'
        elif previous_url is not None:
            link = '<{previous_url}>; rel="prev"'
        else:
            link = ''

        if link:
            link += ', <{first_url}>; rel="first", <{last_url}>; rel="last"'

        link = link.format(next_url=next_url, previous_url=previous_url, first_url=first_url, last_url=last_url)
        headers = {'Link': link, 'X-Total-Count':  self.page.paginator.count} if link else {}

        return Response(data, headers=headers)

    def get_first_link(self):
        url = self.request.build_absolute_uri()
        return pagination.replace_query_param(url, self.page_query_param, 1)

    def get_last_link(self):
        url = self.request.build_absolute_uri()
        count = self.page.paginator.count
        page_size = self.get_page_size(self.request)

        total_pages = int(math.ceil(count/float(page_size)))

        return pagination.replace_query_param(url, self.page_query_param, total_pages)
