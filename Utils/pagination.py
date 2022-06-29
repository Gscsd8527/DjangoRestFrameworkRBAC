from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    """
    自定义分页
    """
    page_size = 10  # default page size
    page_size_query_param = 'size'  # ?page=xx&size=??
    max_page_size = 10  # max page size