#!/usr/bin/env python3
"""
Custom pagination classes for the chat application
Extends PageNumberPagination for standard page-based pagination.
Sets page_size = 20 to fetch 20 messages per page.
Allows clients to override page_size via ?page_size=<number> (e.g., ?page_size=10).
Caps max_page_size at 100 to prevent excessive queries.
"""
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class MessagePagination(PageNumberPagination):
    """
    Custom pagination class for messages, with a page size of 20
    """

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        """
        customized paginated response
        """
        return Response(
            {
                "count": self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )
