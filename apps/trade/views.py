from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Q
from django.http import JsonResponse

from .models import *

class Dashboard(TemplateView):
    template_name = 'trade/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class TradeList(TemplateView):

    def get(self, *args, **kwargs):
        trades = Trade.objects.all()
        qry = trades.filter(
            Q(trader__exact=self.request.user)
        ).distinct()
        data = []
        if qry.count() != 0:
            for trade in qry:
                shared = '<span class="text-danger"><i class="fa fa-times"></></span>'
                if trade.share:
                    shared = '<span class="text-success"><i class="fa fa-check"></></span>'
                outcome = '<span class="text-success"><i class="fas fa-arrow-up"></i></span>'
                if trade.outcome == LOSS:
                    outcome = '<span class="text-danger"><i class="fas fa-arrow-down"></i></span>'
                status = '<span class="badge badge-success p-1">OPEN <i class="fas fa-door-open" aria-hidden="true"></i></span>'
                if trade.status == CLOSED:
                    status = '<span class="badge badge-warning p-1">CLOSED <i class="fas fa-door-closed" aria-hidden="true"></i></span>'
                data.append({
                    'pair': trade.pair.name,
                    'strategy': trade.strategy.name,
                    'outcome': outcome,
                    'pips': trade.pips,
                    'shared': shared,
                    'traded': trade.traded.strftime('%d-%b-%Y'),
                    'status': status,
                    'detail': '<a href="/trade/' + str(trade.pk )+ '/detail"><i class="fa fa-eye"><i></a>'
                })

        final = {
            'data': data
        }
        return JsonResponse(final)

class StrategiesList(TemplateView):

    def get(self, *args, **kwargs):
        strategies = Strategy.objects.all()
        qry = strategies.filter(
            Q(owner__exact=self.request.user)
        ).distinct()
        data = []
        trades = Trade.objects.all()
        if qry.count != 0:
            for strategy in qry:
                traded = Trade.objets.filter(
                    Q(strategy__exact=strategy) & Q(owner__exact=self.request.user)
                ).distinct()
                won = traded.filter(outcome__ecaxt=GAIN).distinct()
                count = traded.count()
                if count != 0:
                    rate = won/count
                else:
                    rate = 0
                shared = '<span class="text-danger"><i class="fa fa-times"></></span>'
                if strategy.share:
                    shared = '<span class="text-success"><i class="fa fa-check"></></span>'
                strategy.append({
                    'name': strategy.name,
                    'shared': shared,
                    'traded': count,
                    'rate': rate,
                    'detail': '<a href="/trade/strategy/' + str(strategy.pk )+ '/detail"><i class="fa fa-eye"><i></a>',
                })
        final = {
            'data': data
        }
        return JsonResponse(final)

class TradeDetail(DetailView):
    model = Trade
    pk_url_kwarg = 'trade_id'