from django.db import models


class Journal(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()

    aliases = models.ForeignKey('JournalAlias')


class JournalAlias(models.Model):
    name = models.CharField(max_length=100)


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    current_affiliation = models.CharField(max_length=100)


class Paper(models.Model):
    date = models.DateField()
    url = models.URLField()
    journal = models.ForeignKey('Journal')
    volume = models.CharField(max_length=100)
    issue = models.CharField(max_length=100)

    full_text = models.TextField()
    title = models.CharField(max_length=100)


    authors = models.ManyToManyField('Author')
    citations = models.ForeignKey('Citation', related_name='citer')


class Citation(models.Model):
    paper = models.OneToOneField('Paper')
    text = models.CharField(max_length=500)

