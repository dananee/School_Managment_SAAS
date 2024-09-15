from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict


class StandardResultsSetPagination(PageNumberPagination):
    """
    A geoJSON implementation of a pagination serializer.
    """
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 20

    def get_paginated_response(self, data):
        total_pages = self.page.paginator.num_pages if self.page.paginator.count else 1

        return Response(
            OrderedDict(
                [
                    ("count", self.page.paginator.count),
                     ("total_pages", total_pages),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                ]
            )
        )





class CustomPagination(PageNumberPagination):
    page_size = 20 # Default number of items per page
    page_size_query_param = 'page_size'  # Allow client to set the page size
    max_page_size = 100 
