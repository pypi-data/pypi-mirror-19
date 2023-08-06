from django.db import models
from django.utils.translation import ugettext_lazy as _


class Topic(models.Model):
    text = models.CharField(max_length=200)
    order = models.PositiveIntegerField()

    class Meta:
        verbose_name = _('Topic')
        verbose_name_plural = _('Topics')
        ordering = ['order']

    def __unicode__(self):
        return u'({0}) {1}'.format(self.order, self.text)


class Question(models.Model):
    text = models.CharField(max_length=200)
    answer_text = models.TextField()
    topic = models.ForeignKey(Topic, related_name='questions')
    order = models.PositiveIntegerField()
    related_questions = models.ManyToManyField(
        'self',
        related_name='related_questions',
        blank=True,
    )

    class Meta:
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')
        ordering = ('order',)

    def __unicode__(self):
        return u'({0}) {1}'.format(self.order, self.text)
