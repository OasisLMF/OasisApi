from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _
from django_filters import rest_framework as filters
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.settings import api_settings

from ..filters import TimeStampedFilter
from .views import handle_related_file
from .serializers import RelatedFileSerializer
from .models import RelatedFile


class FilesFilter(TimeStampedFilter):
    content_type = filters.CharFilter(
        help_text=_('Filter results by case insensitive `supplier_id` equal to the given string'),
        lookup_expr='iexact',
        field_name='content_type'
    )   
    filename__contains = filters.CharFilter(
        help_text=_('Filter results by case insensitive `supplier_id` containing the given string'),
        lookup_expr='icontains',
        field_name='filename'
    )   
    user = filters.CharFilter(
        help_text=_('Filter results by case insensitive `model_id` equal to the given string'),
        lookup_expr='iexact',
        field_name='creator_name'
    )   
    class Meta:
        model = RelatedFile
        fields = [
            'content_type',
            'filename__contains',
            'user',
        ]


class FilesViewSet(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """ Add doc string here
    """
    queryset = RelatedFile.objects.all()
    serializer_class = RelatedFileSerializer
    filter_class = FilesFilter

