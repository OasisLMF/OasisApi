from __future__ import absolute_import

from django.utils.translation import ugettext_lazy as _
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.settings import api_settings

from ..filters import TimeStampedFilter
from ..files.views import handle_related_file
from ..files.serializers import RelatedFileSerializer
from .models import AnalysisModel
from .serializers import AnalysisModelSerializer


class AnalysisModelFilter(TimeStampedFilter):
    supplier_id = filters.CharFilter(
        help_text=_('Filter results by case insensitive `supplier_id` equal to the given string'),
        lookup_expr='iexact'
    )
    supplier_id__contains = filters.CharFilter(
        help_text=_('Filter results by case insensitive `supplier_id` containing the given string'),
        lookup_expr='icontains',
        field_name='supplier_id'
    )
    model_id = filters.CharFilter(
        help_text=_('Filter results by case insensitive `model_id` equal to the given string'),
        lookup_expr='iexact'
    )
    model_id__contains = filters.CharFilter(
        help_text=_('Filter results by case insensitive `model_id` containing the given string'),
        lookup_expr='icontains',
        field_name='model_id'
    )
    version_id = filters.CharFilter(
        help_text=_('Filter results by case insensitive `version_id` equal to the given string'),
        lookup_expr='iexact'
    )
    version_id__contains = filters.CharFilter(
        help_text=_('Filter results by case insensitive `version_id` containing the given string'),
        lookup_expr='icontains',
        field_name='version_id'
    )
    user = filters.CharFilter(
        help_text=_('Filter results by case insensitive `user` equal to the given string'),
        lookup_expr='iexact',
        field_name='creator_name'
    )

    class Meta:
        model = AnalysisModel
        fields = [
            'supplier_id',
            'supplier_id__contains',
            'model_id',
            'model_id__contains',
            'version_id',
            'version_id__contains',
            'user',
        ]


class AnalysisModelViewSet(viewsets.ModelViewSet):
    """
    list:
    Returns a list of Model objects.

    ### Examples

    To get all models with 'foo' in their name

        /models/?supplier_id__contains=foo

    To get all models with 'bar' in their name

        /models/?version_id__contains=bar

    To get all models created on 1970-01-01

        /models/?created__date=1970-01-01

    To get all models updated before 2000-01-01

        /models/?modified__lt=2000-01-01

    retrieve:
    Returns the specific model entry.

    create:
    Creates a model based on the input data

    update:
    Updates the specified model

    partial_update:
    Partially updates the specified model (only provided fields are updated)
    """

    queryset = AnalysisModel.objects.all()
    serializer_class = AnalysisModelSerializer
    filter_class = AnalysisModelFilter


    def get_serializer_class(self):
        if self.action in ['resource_file']:
            return RelatedFileSerializer
        else:
            return super(AnalysisModelViewSet, self).get_serializer_class()

    @property
    def parser_classes(self):
        if getattr(self, 'action', None) in ['resource_file']:
            return [MultiPartParser]
        else:
            return api_settings.DEFAULT_PARSER_CLASSES





    @action(methods=['get', 'post', 'delete'], detail=True)
    def resource_file(self, request, pk=None, version=None):
        """
        get:
        Gets the models `resource_file` contents

        post:
        Sets the models `resource_file` contents

        delete:
        Disassociates the moodels `resource_file` contents
        """
        return handle_related_file(self.get_object(), 'resource_file', request, ['application/json'])

