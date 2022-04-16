from unittest import result
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from results.models import WeatherStation
from .apps import ResultsConfig
import pmdarima as pm
import pandas as pd
import numpy as np
from datetime import date

# Create your views here.
def results(request):
    if request.method == 'POST':
        #call trainmodel function
        context, envcontext = trainModel(request)
        request.session['access_pages'] = True
        request.session['results_context'] = context
        request.session['env_context'] = envcontext
        return render(request, 'results/results.html', context)
    elif 'access_pages' in request.session:
        return render(request, 'results/results.html', request.session['results_context'])
    else:
        return HttpResponseRedirect('/')


def trainModel(request):
    #Get the inputs from the request
    station = request.POST['location_input']
    user_location = request.POST['location_name']
    size = request.POST['size']
    azimuth = request.POST['azimuth']
    tilt = request.POST['tilt']

    #Efficiency Matrix - for calculating solar panel efficiency based on tilt + azimuth
    efficiency_matrix = {
        'Horizontal_S':     0.897,  '15_S':        0.965,  '30_S':     1.00,    '45_S':     0.998,   '60_S':     0.956,   '75_S':     0.877,   'Vertical_S':       0.765,     
        'Horizontal_SE/SW': 0.897,  '15_SE/SW':    0.936,  '30_SE/SW': 0.951,   '45_SE/SW': 0.936,   '60_SE/SW': 0.890,   '75_SE/SW': 0.818,   'Vertical_SE/SW':   0.720,
        'Horizontal_E/W':   0.897,  '15_E/W':      0.865,  '30_E/W':   0.825,   '45_E/W':   0.779,   '60_E/W':   0.724,   '75_E/W':   0.659,   'Vertical_E/W':     0.585,
        'Horizontal_NE/NW': 0.897,  '15_NE/NW':    0.790,  '30_NE/NW': 0.685,   '45_NE/NW': 0.600,   '60_NE/NW': 0.534,   '75_NE/NW': 0.480,   'Vertical_NE/NW':   0.429,
        'Horizontal_N':     0.897,  '15_N':        0.757,  '30_N':     0.629,   '45_N':     0.518,   '60_N':     0.431,   '75_N':     0.387,   'Vertical_N':       0.354 
    }

    #Get the Irradiance
    irradiance = getIrradiance(station)

    #Get the grid demand
    demand = getDemand()
    
    #kwh per month generated
    generated_KwH = getKwH(irradiance, size, azimuth, tilt, efficiency_matrix)

    #amount of savings per month
    savings, prices = getPrices(list(demand.Demand.values), generated_KwH)

    #get values in correct format
    yearly_vals, monthly_vals, result_specs, envcontext = arrangeData(size, demand, generated_KwH, prices, savings)
    result_specs = dict(result_specs, **{'user_location': user_location, 'size': size, 'azimuth': azimuth, 'tilt': tilt})
    #Create context 
    context = {'yearly_vals': yearly_vals, 'monthly_vals': monthly_vals, 'result_specs': result_specs, 'active': 'results'}

    #return render(request, 'results/results.html', context)
    return context, envcontext

#Forecast Global Irradiance - Jcm^2
def getIrradiance(station):
    #Try catch for weather station - raise Http404 if it does not exist in DB
    #Should not raise error however as input is validated before request sent
    try:
        #'timeseries' is the weather station's values as a dataframe
        timeseries = pd.DataFrame(list(WeatherStation.objects.filter(LOCATION=station).values()))
    except WeatherStation.DoesNotExist:
        raise Http404("Weather Station does not exist")

    #Convert 'DATE' to datetime object to be used by SARIMAX model and set as index
    timeseries['DATE'] = pd.to_datetime(timeseries['DATE'])
    timeseries['DATE'] = timeseries["DATE"].dt.strftime('%Y-%d-%m')
    timeseries = timeseries.set_index("DATE")

    #Create the model
    weather_model = pm.auto_arima(timeseries.GLORAD, exogenous=timeseries.maxtp.values.reshape(-1, 1),
        start_p=0, start_q=0,
        test='adf',
        max_p=3, max_q=3, m=12,
        start_P=0, seasonal=True,
        max_P= 0, max_Q= 0, start_Q= 0,
        d=0, D=1, trace=False,
        error_action='ignore',  
        suppress_warnings=False, 
        stepwise=True)

    #Exogenous values needed for predictions
    eX = timeseries['maxtp'].values.reshape(-1, 1)
    eX = np.concatenate( (eX, eX[-12:-8] ) )
    eX = np.repeat(eX, 3)
    eX = eX.reshape(-1,1)

    #Get the number of months elapsed so there is parity between the predictions and when the predictions are made
    end_date = date.today()
    start_date = date(2021, 8, 31)
    num_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)

    irradiance = list(weather_model.predict(n_periods = (20*12)+num_months, exogenous=eX[:(20*12)+num_months]))[num_months:]
    return irradiance

#Convert Irradiance into the costs
def getKwH(irradiance, size, azimuth, tilt, efficiency_matrix):
    #Formula to be used - Output (kWh) = 0.8 x kWp x S x E 
    #Kwp: Installed Peak Power | S: Solar Irradiance | E: efficiency depending on roof orientation and tilt
    #As irradiance is in Jcm^2 we need to convert to KWHm^2 - so multiple by 0.0027777777777778 to *roughly* convert
    generated_KwH = []
    E = tilt + '_' + azimuth
    E = efficiency_matrix[E]
    Z = 1
    Kwp = float(size)
    for monthlyGlorad in irradiance:
        SI = monthlyGlorad * 0.0027777777777778
        generated_KwH.append( ((0.8 * Kwp) * SI) * E )

    return generated_KwH

#Forecast Grid Demand
def getDemand():
    #get number of days elapsed between now and end of training set
    end_date = date.today()
    start_date = date(2019, 12, 30)
    num_days = (end_date - start_date).days
    num_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)

    #make prediction
    gridDemand_model = ResultsConfig.gridDemand_model
    demand = gridDemand_model.forecast(num_days+(20*366))

    #turn prediction into dataframe then group by months
    demand_df = pd.DataFrame(list(demand), list(demand.index), columns = ['Demand'])

    demandMonths_df = demand_df.groupby(pd.Grouper(freq="M"))
    demandMonths_df = demandMonths_df.sum()
    demandMonths_df.Demand = demandMonths_df.Demand/10
    
    return demandMonths_df[num_months+1:]

def getPrices(demand, generated_KwH):
    #this gets us the list of savings and electricity prices for each month
    elecModel = ResultsConfig.elecPrices_model
    prices = []
    for month_demand in demand:
        prices.append(elecModel.predict(np.array([month_demand]).reshape(1, 1))[0])

    savings = [a*b for a,b in zip(prices,generated_KwH)]

    return savings, prices 

def arrangeData(size, demand, generated_KwH, prices, savings):
    
    if(len(demand.index) > len(generated_KwH)):
        demand = demand[1:]
    
    data_df = pd.DataFrame(list(zip(generated_KwH, prices, savings)), columns = [['KwH', 'ElecCost', 'Savings']], index=demand.index)

    yearly_totals = data_df.groupby(pd.Grouper(freq="Y"))
    yearly_totals = yearly_totals.sum()

    
    #Get the number of months elapsed so there is parity between the predictions and when the predictions are made
    end_date = date.today()
    start_date = date(2021, 8, 31)

    if float(size) < 1:
        grant = 0
    elif 1 <= float(size) < 2:
        grant = 900
    elif 2 <= float(size) < 3:
        grant = 1800
    elif 3 <= float(size) < 4:
        grant = 2100
    elif float(size) >= 4:
        grant = 2400

    initial_cost = float(size) * 1900
    final_cost = initial_cost - float(grant)
    total = 0.0
    end_year = 0

    for index, year in enumerate(yearly_totals.Savings.values.ravel().tolist()):
        total += int(year)
        if total >= final_cost:
            end_year = index
            break

    twenty_year_savings = round(sum(yearly_totals.Savings.values.ravel().tolist()), 2)
    yearly_totals = yearly_totals.iloc[:end_year]

    yearly_KwH = yearly_totals.KwH.values.ravel().tolist()
    yearly_savings = yearly_totals.Savings.values.ravel().tolist()
    yearly_labels = yearly_totals.index.strftime("%Y").tolist()
    yearly_vals = {'yearly_KwH': yearly_KwH, 'yearly_savings': yearly_savings, 'yearly_labels': yearly_labels}

    monthly_vals = {}
    for year in yearly_labels:
        df = data_df[data_df.index.year == int(year)]
        vals = {'monthly_KwH': df.KwH.values.ravel().tolist(),
                'monthly_savings': df.Savings.values.ravel().tolist(),
                'monthly_elec': df.ElecCost.values.ravel().tolist(),
                'monthly_labels': df.index.month_name().str.slice(stop=3).tolist()}
        
        monthly_vals[year] = vals


    envimpact = getEnvImpact(sum(yearly_KwH)/len(yearly_KwH))
    result_specs = {'investment_cost': int(final_cost), 'payback': len(yearly_labels), '20_year_savings': twenty_year_savings}
    return yearly_vals, monthly_vals, result_specs, envimpact

def getEnvImpact(KwH):
    #co2 reduction - 0.23314 * kwh (gives kg)
    co2_reduction = KwH * 0.23314
    #car offset - 2.75 / co2 (in tonnes so multiply by 0.001)
    car_offset = co2_reduction / 2750
    #tree offset - 5.9kg for a seedling or 22kg for a fully grown tree
    tree_offset = co2_reduction / 22
    sapling_offset = co2_reduction / 5.9
    
    envimpact = {'co2_reduction': str(round(co2_reduction, 2)), 'car_offset': str(round(car_offset, 2)), 'KwH': round(KwH, 2),
                 'tree_offset': str(round(tree_offset, 2)), 'sapling_offset': str(round(sapling_offset, 2)), 'active': 'envimpact'}

    return envimpact