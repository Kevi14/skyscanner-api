from rest_framework.pagination import PageNumberPagination

from config import API_LIST_DEFAULT_PAGE_SIZE, API_LIST_MAX_PAGE_SIZE


class CustomPaginator(PageNumberPagination):
    page_size = API_LIST_DEFAULT_PAGE_SIZE  # default
    max_page_size = API_LIST_MAX_PAGE_SIZE  # max definable page size
    page_size_query_param = "size"  # make size available
