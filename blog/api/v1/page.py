from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class DefaultPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        page_size = 4
        page_size_query_param = "page_size"
        max_page_size = 200
        return Response(
            {
                "links": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
                "total_object": self.page.paginator.count,
                "num_pages": self.page.paginator.num_pages,
                "results": data,
            }
        )
