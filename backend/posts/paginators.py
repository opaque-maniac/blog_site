from rest_framework import pagination
from rest_framework import exceptions
from django.utils.translation import gettext_lazy as _

class PostPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50

    def paginate_queryset(self, queryset, request, view=None):
        if 'page_size' in request.query_params:
            try:
                requested_page_size = int(request.query_params['page_size'])
                if not 1 <= requested_page_size <= self.max_page_size:
                    raise exceptions.ValidationError(_('Page size must be between 1 and %(max_size)s.' % {'max_size': self.max_page_size}))
                self.page_size = requested_page_size
            except ValueError:
                raise exceptions.ValidationError(_('Invalid page_size'))
        return super().paginate_queryset(queryset, request, view)

class CommentPaginaton(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 20

    def paginate_queryset(self, queryset, request, view=None):
        if 'page_size' in request.query_params:
            try:
                requested_page_size = int(request.query_params['page_size'])
                if not 1 <= requested_page_size <= self.max_page_size:
                    raise exceptions.ValidationError(_('Page size must be between 1 and %(max_size)s.' % {'max_size': self.max_page_size}))
                self.page_size = requested_page_size
            except ValueError:
                raise exceptions.ValidationError(_('Invalid page_size'))
        return super().paginate_queryset(queryset, request, view)