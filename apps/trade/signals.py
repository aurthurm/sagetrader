from django.db.models.signals import post_save
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import *


def create_pf_tp(instance, sender, **kwargs):
    if kwargs['created']:
	    #Auto Add a Portfolio
        port = Portfolio.objects.create(
            name="Sage Folio",
            statement="These are boundaries of my trading playground",
            owner=instance
        )
	    #Auto Add a Prading Plan
        plan = TradingPlan.objects.create(
            title="Sage Plan",
            description="I shall follow everything stated in this trading plan according to my portfolio specifications.",
            owner=instance,
            share=False
        )
    else:
        pass

post_save.connect(create_pf_tp, sender=User)