'''
Created on 18-Apr-2013

@author: nitin
'''

from django import forms

class PricerForm(forms.Form):
    evaluation_date = forms.CharField(label="Evaluation Date", initial="18 April 2013", widget=forms.TextInput, error_messages={'required': 'Please enter evaluation date'})
    settlement_date = forms.CharField(label="Settlement Date", initial="31 December 2013", widget=forms.TextInput)
    risk_factor = forms.CharField(label="Risk Factor", initial="0.06")
    volatility = forms.CharField(label="Volatility", initial="0.20")
    reference_value = forms.CharField(label="Reference Value", initial="4.48667344")
    put = forms.CharField(label="Payoff/Put", initial="40.0")
    underlying = forms.CharField(label="Underlying", initial="36.0")
    dividend_yield = forms.CharField(label="Divident Yield", initial="0.0")
    time_steps = forms.CharField(label="Time Steps", initial="801")
    grid_points = forms.CharField(label="Grid Points", initial="800")
