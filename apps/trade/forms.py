from django import forms
from .models import Trade

class TradeChartsForm(forms.ModelForm):

    # def __init__(self, *args, **kwargs):
    #     super(TradeChartsForm, self).__init__(*args, **kwargs)
    #     for field_name, field in self.fields.items():
    #         field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Trade
        fields = ('chart_before', 'chart_after', )
