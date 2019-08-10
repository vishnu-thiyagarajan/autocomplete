from django.shortcuts import render
import requests
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from .forms import CurrencyPredictionForm
import copy
import math
from django.core.cache import cache


# Create your views here.
def HomeView(request):
    if request.method == "GET":
        form = CurrencyPredictionForm(request.GET or None)
        request.session['R_square'] = ''
        request.session['std_error'] = ''
        context = {"form": form}
    if request.method == "POST":
        form = CurrencyPredictionForm(request.POST or None)
        context = {"form": form}
        if form.is_valid():
            try:
                amount = form.cleaned_data.get('amount')
                waiting_time = form.cleaned_data.get('waiting_time_in_days')
                start_date = form.cleaned_data.get('start_date', date.today())
                future_date = None
                if start_date > date.today():
                    future_date = start_date
                    start_date = date.today()
                base_currency = form.cleaned_data.get('base_currency')
                target_currency = form.cleaned_data.get('target_currency')
                hist_start_date = start_date + relativedelta(months=-2)
                params = {"start_at": hist_start_date.strftime("%Y-%m-%d"),
                          "end_at": start_date.strftime("%Y-%m-%d")
                          }
                get_list = []
                while hist_start_date <= start_date:
                    get_list.append(hist_start_date.strftime("%Y-%m-%d"))
                    hist_start_date += relativedelta(days=1)
                data = cache.get_many(get_list)
                no_val_data = list(set(get_list) - set(data.keys()))
                date_obj_list = []
                for date_str in no_val_data:
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                    if date_obj.weekday() not in (5, 6):
                        date_obj_list.append(date_obj)
                if date_obj_list:
                    params = {"start_at": min(date_obj_list).strftime("%Y-%m-%d"),
                              "end_at": max(date_obj_list).strftime("%Y-%m-%d")
                              }
                if params['start_at'] != params['end_at'] and date_obj_list:
                    html_var = requests.get(url="https://api.exchangeratesapi.io/history", params=params)
                    data.update(html_var.json()['rates'])
                    cache.set_many(data)
                context['myobject'], R_square, std_error = predict(data,
                                                                   amount,
                                                                   waiting_time,
                                                                   future_date,
                                                                   start_date,
                                                                   base_currency,
                                                                   target_currency)
                request.session['R_square'] = R_square
                request.session['std_error'] = std_error
            except Exception:
                request.session['R_square'] = ''
                request.session['std_error'] = ''
                context = {}
    return render(request, "home.html", context)


def predict(data, amount, waiting_time, future_date, start_date, base_currency, target_currency):

    ordered_data = sorted(data.items(), reverse=False)
    ordered_base_data = []
    for item in ordered_data:
        ordered_base_data.append([item[0], {target_currency: item[1][target_currency] / item[1][base_currency]}])
    mean_date = datetime.strptime(ordered_base_data[int(len(ordered_base_data) / 2)][0], "%Y-%m-%d")
    mean_value = 0
    date_list = []
    value_list = []
    for item in ordered_base_data:
        diff = (datetime.strptime(item[0], "%Y-%m-%d") - mean_date).days
        date_list.append(diff)
        value_list.append(item[1][target_currency])
        mean_value += item[1][target_currency]
    mean_value = mean_value / len(ordered_base_data)
    val_list = copy.deepcopy(value_list)
    value_list = [val - mean_value for val in value_list]

    slope = sum([a * b for a, b in zip(date_list, value_list)]) / sum(list(map(lambda x: x * x, date_list)))
    intercept = mean_value - (slope * int(len(ordered_base_data) / 2))
    value_sqr_list = list(map(lambda y: y * y, value_list))
    est_start_date = date_list[-1]
    if future_date:
        est_start_date = (future_date - mean_date.date()).days
    estimated_date_list = range(est_start_date, est_start_date + waiting_time)
    estimated_val_list = list(map(lambda val: intercept + (slope * val), estimated_date_list))
    estimated_amount_list = [amount * val for val in estimated_val_list]
    estimated_mean_value_diff = [val - mean_value for val in estimated_val_list]
    estimated_value_diff = [a - b for a, b in zip(estimated_val_list, val_list)]
    R_square = sum(list(map(lambda x: x * x, estimated_mean_value_diff))) / sum(value_sqr_list)
    std_error = math.sqrt(sum(list(map(lambda x: x * x, estimated_value_diff))) / (len(ordered_base_data) - 2))
    kv_dict = []
    for days in range(0, waiting_time):
        key = (future_date or start_date) + relativedelta(days=days)
        value = estimated_amount_list[days]
        kv_dict.append({"key": key.strftime("%d/%m/%Y"),
                        "value": value,
                        })
    return kv_dict, R_square, std_error
