from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.utils import timezone
from django.template.defaultfilters import slugify
import os

from django.conf import settings
ATTACHMENT_UPLOAD_TO = getattr(settings, 'ATTACHMENT_UPLOAD_TO', 'charts')

GAIN = 'G'
LOSS = 'L'
OUTCOMES = (
    (GAIN, _('Gain')),
    (LOSS, _('Loss')),
)

OPEN = 'O'
CLOSED = 'C'
STATUSES = (
    (OPEN, _('Open')),
    (CLOSED, _('Closed')),
)

class Pair(models.Model):
    """
    Currency pairs
    """
    name = models.CharField(
        _('name'),
        max_length=7
    )

    def __str__(self):
        return f'{self.name}'

class Strategy(models.Model):
    name = models.CharField(
        _('name'),
        max_length=100
    )
    description =models.TextField(
        _('description')
    )
    owner = models.ForeignKey(
        'auth.User',
        related_name='trader_strategies',
        on_delete=models.PROTECT
    )
    share = models.BooleanField(
        _('share'),
        default=False
    )
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        verbose_name = _('strategy')
        verbose_name_plural = _('strategies')

class TradingPlan(models.Model):
    title = models.CharField(
        _('title'),
        max_length=100
    )
    description = models.TextField(
        _('description')
    )
    owner = models.OneToOneField(
        'auth.User',
        related_name='trader_plan',
        on_delete=models.PROTECT
    )
    share = models.BooleanField(
        _('share'),
        default=False
    )
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}'

def file_upload_to_dispatcher(entry, filename):
    return entry.file_upload_to(filename)

class Trade(models.Model):
    pair = models.ForeignKey(
        Pair,
        on_delete=models.PROTECT
    )
    strategy = models.ForeignKey(
        Strategy,
        related_name='strategy_trades',
        on_delete=models.PROTECT
    )
    outcome = models.CharField(
        _('outcome'),
        max_length=10,
        choices=OUTCOMES,
        default=GAIN
    )
    status = models.CharField(
        _('status'),
        max_length=10,
        choices=STATUSES,
        default=OPEN
    )
    pips = models.SmallIntegerField(
        _('pips')
    )
    share = models.BooleanField(
        _('share'),
        default=False
    )
    traded = models.DateTimeField(auto_now=True)
    trader = models.ForeignKey(
        'auth.User',
        related_name='trader_trades',
        on_delete=models.PROTECT
    )

    def file_upload_to(self, filename):
        now = timezone.now()
        filename, extension = os.path.splitext(filename)

        return os.path.join(
                ATTACHMENT_UPLOAD_TO,
                now.strftime('%Y'),
                now.strftime('%m'),
                now.strftime('%d'),
                '%s%s' % (slugify(filename), extension)
            )

    chart_before = models.FileField(
        _('chart before'), 
        blank=True,
        upload_to=file_upload_to_dispatcher,
        help_text=_('Attach Before Chart')
        )

    chart_after = models.FileField(
        _('chart after'), 
        blank=True,
        upload_to=file_upload_to_dispatcher,
        help_text=_('Attach After Chart')
        )

    def get_absolute_url(self):
        return reverse('trade:detail', kwargs={'trade_id': self.pk})

    def __str__(self):
        return f'{self.pair.name} Trade'

class TradeFollowUp(models.Model):
    trade = models.ForeignKey(
        Trade,
        on_delete=models.PROTECT
    )
    description = models.TextField(
        _('description')
    )
    posted = models.DateTimeField(auto_now=True)
    poster = models.ForeignKey(
        'auth.User',
        on_delete=models.PROTECT
    )

    def __str__(self):
        return f'{self.trade.pair.name} Follow Up'

class Portfolio(models.Model):
    name = models.CharField(
        _('name'),
        max_length=100
    )
    statement = models.TextField(
        _('statement')
    )
    strategies = models.ManyToManyField(
        Strategy,
        blank=True
    )
    pairs = models.ManyToManyField(
        Pair,
        blank=True
    )
    owner = models.OneToOneField(
        'auth.User',
        on_delete=models.PROTECT
    )
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'
