import requests
from django.shortcuts import render
from decimal import Decimal

SUBSCRIPTION_KEY = "ecfa19b128f644199ea57911f98343e9"

def fetch_data(url):
    headers = {"Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY}
    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def charity_name(name):
    url = f"https://api.charitycommission.gov.uk/register/api/searchCharityName/{name}"
    return fetch_data(url)

def charity_details(registered_number, suffix=0):
    url = f"https://api.charitycommission.gov.uk/register/api/allcharitydetailsV2/{registered_number}/{suffix}"
    return fetch_data(url)

def finances(registered_number, suffix=0):
    url = f"https://api.charitycommission.gov.uk/register/api/charityfinancialhistory/{registered_number}/{suffix}"
    return fetch_data(url)

def per_pound(amount_to_charity, total):
    try:
        amount_to_charity = Decimal(amount_to_charity or 0)
        total = Decimal(total or 0)
        if total > 0:
            return f"{amount_to_charity / total:.2f}"
        return "Not enough available data"
    except Exception as e:
        return "There was an error. Try again."

def index(request):
    if request.method == 'POST':
        name = request.POST.get('charity_name')
        if not name:
            return render(request, 'charitycheck/index.html')
        charity_data = charity_name(name)
        if not charity_data or len(charity_data) == 0:
            return render(request, 'charitycheck/index.html', {'error_message': 'Charity not found. Try again, I guess.'})
        reg_number = charity_data[0].get('reg_charity_number')
        if not reg_number:
            return render(request, 'charitycheck/index.html')
        details = charity_details(reg_number)
        financial_data = finances(reg_number)
        if not details:
            return render(request, 'charitycheck/index.html')
        if not financial_data:
            return render(request, 'charitycheck/index.html')
        financial_record = financial_data[0] if isinstance(financial_data, list) else {}
        date_of_registration = details.get('date_of_registration', '').split('T')[0]
        last_modified_time = details.get('last_modified_time', '').split('T')[0]
        amount_to_charity = financial_record.get('exp_charitable_activities', 0) or 0
        exp_total = financial_record.get('exp_total', 0) or 0
        expenditure = details.get('latest_expenditure', 0) or 0
        raw_status = details.get('reg_status', '')
        reg_status = ' Registered' if raw_status == 'R' else ' No longer registered' if raw_status == 'RM' else 'Unavailable'
        context = {
                'reg_charity_number': details.get('reg_charity_number'),
                'charity_name': details.get('charity_name'),
                'reg_status': reg_status,
                'date_of_registration': date_of_registration,
                'latest_income': f"{int(details.get('latest_income', 0)):,}",
                'latest_expenditure': f"{int(expenditure):,}",
                'address_line_one': details.get('address_line_one'),
                'address_line_two': details.get('address_line_two'),
                'address_post_code': details.get('address_post_code'),
                'phone': details.get('phone'),
                'email': details.get('email'),
                'web': details.get('web'),
                'last_modified_time': last_modified_time,
                'exp_charitable_activities': f"{int(amount_to_charity):,}",
                'perpound_latest': per_pound(amount_to_charity, exp_total), 
                'perpound_total': per_pound(amount_to_charity, expenditure),
                }

        return render(request, 'charitycheck/index.html', context)
    return render(request, 'charitycheck/index.html')