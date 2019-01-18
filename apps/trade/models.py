from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.utils import timezone
from django.template.defaultfilters import slugify

GAIN = 'G'
LOSS = 'L'
OUTCOMES = (
    _(GAIN, _('Gain')),
    _(LOSS, _('Loss'))
)

class Pair(models.Model):
    """
    Currency pairs
    """
    name = models.CharField(
        _('name'),
        max_length=7
    )

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

class Trade(models.Model):
    pair = models.ForeignKey(
        Pair,
        on_delete=models.PROTECT
    )
    strategy = models.ForeignKey(
        Strategy,
        on_delete=models.PROTECT
    )
    outcome = models.CharField(
        _('outcome'),
        max_length=10,
        choices=OUTCOMES,
        default=GAIN
    )
    pips = models.SmallIntegerField(
        _('pips')
    )
    share = models.BooleanField(
        _('share'),
        default=False
    )
    traded = models.DateTimeField(auto_now=True)
    trader = models.OneToOneField(
        'auth.User',
        related_name='trader_trades',
        on_delete=models.PROTECT
    )

class TradeFollowUp(models.Model):
    trade = models.ForeignKey(
        Trade,
        on_delete=models.PROTECT
    )
    description = models.TextField(
        _('description')
    )
    posted = models.DateTimeField(auto_now=True)
    poster = models.OneToOneField(
        'auth.User',
        on_delete=models.PROTECT
    )
