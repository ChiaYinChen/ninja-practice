import math
from typing import TypeVar

from django.db.models import QuerySet
from ninja import Field, Schema

ModelType = TypeVar("ModelType")


class PaginationParams(Schema):
    """Parameters used for pagination control."""

    page: int = Field(default=1, description="The current page number, starting from 1.")
    per_page: int = Field(default=10, description="The number of items to display per page.")

    @property
    def skip(self) -> int:
        """Calculate the number of records to skip based on the current page and per page."""
        return (self.page - 1) * self.per_page

    @property
    def limit(self) -> int:
        """Get the maximum number of records to retrieve for the current page."""
        return self.per_page


class Paginated(Schema):
    """Pagination metadata."""

    current_page: int = Field(1, description="Current page number being displayed.")
    total_pages: int = Field(1, description="Total pages available, calculated from the query results.")
    per_page: int = Field(10, description="Number of items displayed on each page.")
    total_counts: int = Field(0, description="Total number of items based on current query.")


def get_paginated_response(
    queryset: QuerySet[ModelType],
    paging_params: PaginationParams,
) -> tuple[Paginated, QuerySet[ModelType]]:
    """Paginate the results of a database query."""
    # Total number of items in the queryset
    total_counts = queryset.count()

    # Calculate the total number of pages based on the total item count and items per page
    total_pages = math.ceil(total_counts / paging_params.per_page)

    # Retrieve the items for the current page
    items = queryset[paging_params.skip : (paging_params.skip + paging_params.limit)]

    # Create the PaginationWindow object that contains pagination information
    page_info = Paginated(
        current_page=paging_params.page,
        total_pages=total_pages,
        per_page=paging_params.per_page,
        total_counts=total_counts,
    )

    return page_info, items
