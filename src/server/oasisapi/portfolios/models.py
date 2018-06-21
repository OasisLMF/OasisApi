from __future__ import absolute_import, print_function

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.encoding import python_2_unicode_compatible
from model_utils.models import TimeStampedModel

from ..files.models import RelatedFile


@python_2_unicode_compatible
class Portfolio(TimeStampedModel):
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='portfolios')

    accounts_file = models.ForeignKey(RelatedFile, null=True, default=None, related_name='accounts_file_portfolios')
    location_file = models.ForeignKey(RelatedFile, null=True, default=None, related_name='location_file_portfolios')
    reinsurance_info_file = models.ForeignKey(RelatedFile, null=True, default=None, related_name='reinsurance_info_file_portfolios')
    reinsurance_source_file = models.ForeignKey(RelatedFile, null=True, default=None, related_name='reinsurance_source_file_portfolios')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('portfolio-detail', args=[self.pk])

    def get_absolute_create_analysis_url(self):
        return reverse('portfolio-create-analysis', args=[self.pk])

    def get_absolute_accounts_file_url(self):
        return reverse('portfolio-accounts-file', args=[self.pk])

    def get_absolute_location_file_url(self):
        return reverse('portfolio-location-file', args=[self.pk])

    def get_absolute_reinsurance_info_file_url(self):
        return reverse('portfolio-reinsurance-info-file', args=[self.pk])

    def get_absolute_reinsurance_source_file_url(self):
        return reverse('portfolio-reinsurance-source-file', args=[self.pk])
