from rest_framework import pagination


class MedicinePaginator(pagination.PageNumberPagination):
    page_size = 24
