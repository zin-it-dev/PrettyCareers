from rest_framework.pagination import PageNumberPagination as BasePageNumberPagination
from rest_framework.response import Response


class PageNumberPagination(BasePageNumberPagination):
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'page_size': self.page_size,
            'results': data
        })
    
    
class SmallResultsSetPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 50
    
    
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    max_page_size = 500
    
    
class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    max_page_size = 10000