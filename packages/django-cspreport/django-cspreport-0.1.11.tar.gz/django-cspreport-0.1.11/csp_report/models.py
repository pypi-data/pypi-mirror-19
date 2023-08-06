# -*- coding: utf-8 -*-
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.template.defaultfilters import truncatechars


class CSPReport(models.Model):
    host = models.TextField(blank=True, null=True, default='')
    document_uri = models.TextField()
    blocked_uri = models.TextField()
    referrer = models.TextField(blank=True, null=True, default='')

    body = JSONField(default={}, blank=True, null=True)
    request_meta = JSONField(default={}, blank=True, null=True)

    date = models.DateTimeField(auto_now_add=True)

    @property
    def short_blocked_uri(self):
        return truncatechars(self.blocked_uri, 100)

    def __str__(self):
        return 'CSPReport {}'.format(self.id)


class CleanedCSPReport(models.Model):
    report = models.ForeignKey(CSPReport)

    document_scheme = models.TextField(blank=True, null=True, default='')
    document_domain = models.TextField(blank=True, null=True, default='')
    document_path = models.TextField(blank=True, null=True, default='')
    document_query = models.TextField(blank=True, null=True, default='')

    blocked_domain = models.TextField(blank=True, null=True, default='')
    blocked_url = models.TextField(blank=True, null=True, default='')

    @property
    def short_blocked_url(self):
        return truncatechars(self.blocked_url, 100)

    @property
    def short_document_query(self):
        return truncatechars(self.document_query, 100)

class CSPReportFilter(models.Model):
    filter_type = models.TextField()
    value = models.TextField()
    is_enabled = models.BooleanField(default=True)

    def __str__(self):
        return '{}: {}'.format(self.filter_type, self.value)
