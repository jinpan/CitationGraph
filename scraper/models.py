from django.db import models
from django.utils.translation import ugettext_lazy as _

class JournalQueue(models.Model):
    URL = models.URLField(
        _("URL to scrape"))

class PaperQueue(models.Model):

    URL = models.URLField(
        _("URL to scrape"))
    journal = models.ForeignKey('website.Journal')
    queue_insert_time = models.DateTimeField(
        _("Time entered in the queue"),
        editable=False,
        auto_now_add=True)
    queue_update_time = models.DateTimeField(
        _("Time updated in the queue"),
        editable=False,
        auto_now=True)
    attempts = models.IntegerField(
        _("Number of attempts"),
        default=0)

    def process(self):
        # get the appropriate scraper
        # attempt to scrape the URL
        # if successful, save in website.Paper
        # else, increment attempts by 1
        pass

