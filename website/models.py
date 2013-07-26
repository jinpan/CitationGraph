from django.db import models
from django.utils.translation import ugettext_lazy as _


class Journal(models.Model):
    name = models.CharField(
        _("Journal Name"),
        max_length=100)
    url = models.URLField(
        _("Journal Homepage"))

    meta_data = models.TextField(
        _("Misc data we accumulate as we scrape. Should be in JSON"),
        blank=True)


class Author(models.Model):
    first_name = models.CharField(
        _("First Name"),
        max_length=100)
    last_name = models.CharField(
        _("Last Name"),
        max_length=100)

    meta_data = models.TextField(
        _("Misc data we accumulate as we scrape. Should be in JSON"),
        blank=True)


class Paper(models.Model):
    title = models.CharField(
        _("Paper Title"),
        max_length=100)

    date = models.DateField(
        _("Publication Date"))

    journal = models.ForeignKey(
        'Journal')
    volume = models.CharField(
        _("Publication Journal Volume"),
        max_length=100)
    issue = models.CharField(
        _("Publication Journal Issue"),
        max_length=100)

    url = models.ForeignKey(
        ('Paper_URL'))

    authors = models.ManyToManyField(
        'Author')

    citations = models.ForeignKey(
        'self',
        related_name='my_citations')
    citers = models.ForeignKey(
        'self',
        related_name='my_citers')

    doi = models.CharField(max_length=100, null=True)
    pubmed_id = models.CharField(max_length=100, null=True)

    meta_data = models.TextField(
        _("Misc data we accumulate as we scrape. Should be in JSON"),
        blank=True)


class Paper_URL(models.Model):
    url = models.URLField(
        _("Paper URL"))

