'''
Created on 18-Apr-2013

@author: nitin
'''

from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.template import RequestContext

from django.shortcuts import render_to_response
from MVPricer.forms import PricerForm 

from QuantLib import *

refValue = 0.0
report_list = {}

def report(method, x):
    e = '%.4f' % abs(x - refValue)
    x = '%.5f' % x
    report_list[method] = [x, e]

def calculate(evaluation_date, settlement_date, risk_factor, volatility, reference_value,\
                              put, underlying, dividend_yield,time_steps, grid_points ):
    
    global refValue;
    #evaluation_date
    day, month, year = evaluation_date.split(' ')
    if month == 'April':
        todaysDate = Date(int(day),QuantLib.April,int(year))
    
    Settings.instance().evaluationDate = todaysDate
    
    #settlement_date
    day, month, year = settlement_date.split(' ')
    if month == 'December':
        settlementDate = Date(int(day),QuantLib.December,int(year))
    
    #risk_factor
    riskFreeRate = FlatForward(settlementDate, float(risk_factor), Actual365Fixed())
    
    # option parameters
    exercise = AmericanExercise(settlementDate, Date(17,May,2014))
    payoff = PlainVanillaPayoff(Option.Put, float(put))
    
    # market data
    underlying = SimpleQuote(float(underlying))
    volatility = BlackConstantVol(todaysDate, TARGET(), float(volatility), Actual365Fixed())
    dividendYield = FlatForward(settlementDate, float(dividend_yield), Actual365Fixed())
    
    
    process = BlackScholesMertonProcess(QuoteHandle(underlying),
                                    YieldTermStructureHandle(dividendYield),
                                    YieldTermStructureHandle(riskFreeRate),
                                    BlackVolTermStructureHandle(volatility))

    option = VanillaOption(payoff, exercise)

    refValue=float(reference_value)    
    report('reference value',refValue)

    
    # method: analytic
    option.setPricingEngine(BaroneAdesiWhaleyEngine(process))
    report('Barone-Adesi-Whaley',option.NPV())

    option.setPricingEngine(BjerksundStenslandEngine(process))
    report('Bjerksund-Stensland',option.NPV())

    
    # method: finite differences
    timeSteps = int(time_steps)
    gridPoints = int(grid_points)

    option.setPricingEngine(FDAmericanEngine(process,timeSteps,gridPoints))
    report('finite differences',option.NPV())

    # method: binomial
    timeSteps = int(time_steps)

    option.setPricingEngine(BinomialVanillaEngine(process,'jr',timeSteps))
    report('binomial (JR)',option.NPV())

    option.setPricingEngine(BinomialVanillaEngine(process,'crr',timeSteps))
    report('binomial (CRR)',option.NPV())

    option.setPricingEngine(BinomialVanillaEngine(process,'eqp',timeSteps))
    report('binomial (EQP)',option.NPV())

    option.setPricingEngine(BinomialVanillaEngine(process,'trigeorgis',timeSteps))
    report('bin. (Trigeorgis)',option.NPV())

    option.setPricingEngine(BinomialVanillaEngine(process,'tian',timeSteps))
    report('binomial (Tian)',option.NPV())

    option.setPricingEngine(BinomialVanillaEngine(process,'lr',timeSteps))
    report('binomial (LR)',option.NPV())

    return report_list

def pricer(request):
    c = {}
    c.update(csrf(request))
    value = {}
    if request.method == 'POST':
        #risk_factor = request.GET.get('risk_factor','')
        form = PricerForm(request.POST)
        if form.is_valid():
            evaluation_date = form.cleaned_data['evaluation_date'];
            settlement_date = form.cleaned_data['settlement_date'];
            risk_factor = form.cleaned_data['risk_factor'];
            volatility = form.cleaned_data['volatility'];
            reference_value = form.cleaned_data['reference_value'];
            put = form.cleaned_data['put'];
            underlying = form.cleaned_data['underlying'];
            dividend_yield = form.cleaned_data['dividend_yield'];
            time_steps = form.cleaned_data['time_steps'];
            grid_points = form.cleaned_data['grid_points'];
            
            value = calculate(evaluation_date, settlement_date, risk_factor, volatility, reference_value,\
                              put, underlying, dividend_yield,time_steps, grid_points )
    else:
        form = PricerForm()
    return render_to_response('pricer.html',{'form':form, 'report_list':value}, context_instance=RequestContext(request))


