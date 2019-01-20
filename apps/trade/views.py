from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Q
from django.db.models import Sum
from django.http import JsonResponse

from .models import *
from .forms import TradeChartsForm

class Dashboard(TemplateView):
    template_name = 'trade/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trader = self.request.user
        plan = trader.trader_plan
        portfolio = trader.trader_portfolio
        strategies = Strategy.objects.filter(owner__exact=trader)
        portfolio_strategies = portfolio.strategies.all()
        pairs = Pair.objects.all()
        portfolio_pairs = portfolio.pairs.all()
        if portfolio_pairs.count() == 0:
            context['pairs'] = pairs
        else:
            context['pairs'] = portfolio_pairs        
        context['excludes_pairs'] = pairs.exclude(id__in=portfolio_pairs)
        context['excludes_strategies'] = strategies.exclude(id__in=portfolio_strategies)
        context['strategies'] = portfolio_strategies
        context['trading_plan'] = plan
        context['trading_portfolio'] = portfolio
        return context

class UpdatePlan(TemplateView):
    model = TradingPlan

    def post(self, *args, **kwargs):
        plan = self.request.user.trader_plan
        details = self.request.POST
        update = details.get('update')
        plan.description=update
        plan.save()
        return redirect('home')

class UpdatePortfolio(TemplateView):
    model = Portfolio

    def post(self, *args, **kwargs):
        trader = self.request.user
        portfolio = self.request.user.trader_portfolio
        details = self.request.POST
        pairs = Pair.objects.all()
        strategies = Strategy.objects.filter(owner__exact=trader)
        _pairs = details.get('pairs')
        if not len(_pairs) == 0:            
            _pairs = _pairs.split(",")
            for p_id in _pairs:
                p_pair = pairs.get(pk=int(p_id))
                portfolio.pairs.add(p_pair)
        _strategies = details.get('strategies')
        if not len(_strategies) == 0:
            _strategies = _strategies.split(",")
            for s_id in _strategies:
                s_strategy = strategies.get(pk=int(s_id))
                portfolio.strategies.add(s_strategy)
        return JsonResponse({'message':"success"})

class UpdatePortfolioRemove(TemplateView):
    model = Portfolio

    def post(self, *args, **kwargs):
        trader = self.request.user
        portfolio = self.request.user.trader_portfolio
        details = self.request.POST
        pairs = Pair.objects.all()
        strategies = Strategy.objects.filter(owner__exact=trader)
        data_type = details.get('type')
        data_id = details.get('id')
        if data_type == "pair":
            _pair = pairs.get(pk=int(data_id))
            portfolio.pairs.remove(_pair)
        else:
            _strategy= strategies.get(pk=int(data_id))
            portfolio.strategies.remove(_strategy)
        return JsonResponse({})

class TradeList(TemplateView):

    def get(self, *args, **kwargs):
        trades = Trade.objects.all()
        qry = trades.filter(
            Q(trader__exact=self.request.user)
        ).distinct()
        data = []
        if qry.count() != 0:
            for trade in qry:
                shared = '<span class="text-danger"><span style="display:none">1</span><i class="fa fa-times"></></span>'
                if trade.share:
                    shared = '<span class="text-success"><span style="display:none">0</span><i class="fa fa-check"></></span>'
                position = '<span class="text-success"><span style="display:none">1</span><i class="fas fa-arrow-up"></i></span>'
                if trade.position == SHORT:
                    position = '<span class="text-danger"><span style="display:none">0</span><i class="fas fa-arrow-down"></i></span>'
                pips = '<span class="text-success">+ ' + str(trade.pips) + '</span>'
                if trade.outcome == LOSS:
                    pips = '<span class="text-danger">- ' + str(trade.pips) + '</span>'
                status = '<span class="badge badge-success p-1">OPEN <i class="fas fa-door-open" aria-hidden="true"></i></span>'
                if trade.status == CLOSED:
                    status = '<span class="badge badge-warning p-1">CLOSED <i class="fas fa-door-closed" aria-hidden="true"></i></span>'
                else:
                    pips = '---'
                data.append({
                    'pair': trade.pair.name,
                    'strategy': trade.strategy.name,
                    'position': position,
                    'pips': pips,
                    'shared': shared,
                    'traded': trade.traded.strftime('%d-%b-%Y'),
                    'status': status,
                    'detail': '<a href="/trade/' + str(trade.pk )+ '/detail"><i class="fa fa-eye"><i></a>'
                })

        final = {
            'data': data
        }
        return JsonResponse(final)


class PlaceTrade(TemplateView):
    model = Trade

    def post(self, *args, **kwargs):
        data = {}
        response = self.request.POST
        _pair = response.get('pair')
        pair = Pair.objects.get(pk=int(_pair))
        position = response.get('position')
        _share = response.get('share')
        if _share == 'true':
            share = True
        else:
            share = False
        _strategy = response.get('strategy')
        strategy = Strategy.objects.get(pk=int(_strategy))
        status = response.get('status')
        if status == CLOSED:
            outcome = response.get('outcome')
            pips = int(response.get('pips'))
        else:
            outcome = OPEN
            pips = None
        description = response.get('description')
        Trade.objects.create(
            pair=pair,
            position=position,
            share=share,
            strategy=strategy,
            status=status,
            outcome=outcome,
            pips=pips,
            description=description,
            trader=self.request.user
        )
        data['message'] = "success"
        return JsonResponse(data)

class TradeDetail(DetailView):
    model = Trade
    pk_url_kwarg = 'trade_id'

class AddFollowUp(TemplateView):
    model = Trade
    
    def post(self, *args, **kwargs):
        data = {}
        response = self.request.POST
        description = response.get('description')
        parent = response.get('parent')
        trade = get_object_or_404(Trade, pk=int(self.kwargs.get('trade_id')))
        TradeFollowUp.objects.create(
            trade=trade,
            description=description,
            poster=trade.trader
        )
        return JsonResponse({})

class AddChart(UpdateView):
    model = Trade
    form_class = TradeChartsForm
    pk_url_kwarg = 'trade_id'
    template_name = 'trade/charts-form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        trade = get_object_or_404(Trade, pk=self.kwargs.get('trade_id'))
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        chart_before = request.FILES.get('chart_before')
        chart_after = request.FILES.get('chart_after')
        if chart_after:
            trade.chart_after = chart_after
        if chart_before:
            trade.chart_before = chart_before
        trade.save()
        return redirect('trade:trade-detail', trade_id=trade.pk)

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
                traded = trades.filter(
                    Q(strategy__exact=strategy) & Q(trader__exact=self.request.user)
                ).distinct()
                open_trades = traded.filter(status__exact=OPEN)
                closed_trades = traded.filter(status__exact=CLOSED)
                won = closed_trades.filter(outcome__exact=GAIN)
                lost = closed_trades.filter(outcome__exact=LOSS)
                lost_pips = lost.aggregate(Sum('pips'))
                won_pips = won.aggregate(Sum('pips'))
                total = traded.count()
                if closed_trades.count() != 0:
                    rate = str(round(won.count()/closed_trades.count() * 100, 2))+ " %"
                else:
                    rate = "---"
                shared = '<span class="text-danger"><i class="fa fa-times"></></span>'
                if strategy.share:
                    shared = '<span class="text-success"><i class="fa fa-check"></></span>'
                data.append({
                    'name': strategy.name,
                    # 'shared': shared,
                    'trades': total,
                    'open': open_trades.count(),
                    'closed': closed_trades.count(),
                    'wins': won.count(),
                    'losses': lost.count(),
                    'rate': rate,
                    'pipsGained': won_pips['pips__sum'],
                    'pipsLost': lost_pips['pips__sum'],
                    'detail': '<a href="/trade/strategy/' + str(strategy.pk )+ '/detail"><i class="fa fa-eye"><i></a>',
                })
        final = {
            'data': data
        }
        return JsonResponse(final)

class StrategyCreate(TemplateView):
    
    def post(self, *args, **kwargs):
        data = {}
        details = self.request.POST
        name = details.get('name')
        description = details.get('description')
        Strategy.objects.create(
            name=name,
            description=description,
            share=False,
            owner=self.request.user
        )
        data['message'] = "success"
        return JsonResponse(data)

