import requests
from django.shortcuts import render

SUBSCRIPTION_KEY = "ecfa19b128f644199ea57911f98343e9"

def charity_name(charity_name):
    url = f"https://api.charitycommission.gov.uk/register/api/searchCharityName/{charity_name}"
    headers = {"Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY}
    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except:
        return None

def charity_details(RegisteredNumber, suffix=0):
    url = f"https://api.charitycommission.gov.uk/register/api/allcharitydetailsV2/{RegisteredNumber}/{suffix}"
    headers = {"Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY}
    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return None
    except:
        return None

def index(request):
    if request.method == 'POST':
        name = request.POST.get('charity_name')
        if not name:
            return render(request, 'charitycheck/index.html')
        number = charity_name(name)
        if not number:
            return render(request, 'charitycheck/index.html')
        reg_charity_number = number[0].get('reg_charity_number')
        if not reg_charity_number:
            return render(request, 'charitycheck/index.html')
        details = charity_details(reg_charity_number)
        if not details:
            return render(request, 'charitycheck/index.html')
        context = {
            'reg_charity_number': details.get('reg_charity_number'),
            'charity_name': details.get('charity_name'),
            'reg_status': details.get('reg_status'),
            'date_of_registration': details.get('date_of_registration'),
            'address_line_one': details.get('address_line_one'),
            'address_post_code': details.get('address_post_code'),
            'phone': details.get('phone'),
            'email': details.get('email'),
            'web': details.get('web'),
            'last_modified_time': details.get('last_modified_time'),
        }
        return render(request, 'charitycheck/index.html', context)
    return render(request, 'charitycheck/index.html', {})