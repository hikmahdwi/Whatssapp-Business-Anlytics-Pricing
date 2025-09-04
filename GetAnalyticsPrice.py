import requests
from credentials import base, token, version
import json
import datetime
from json import dumps

def requests_to_meta(batch_requests):
    payload = {
        'access_token': token,
        'batch': json.dumps(batch_requests)
    }
    response = requests.post(base, data=payload)
    response.raise_for_status() 
    return response.json()

def get_insights_batch(waba_id, version, start_date, end_date):
    try:
        all_requests = []
        for i in range(len(waba_id)):
            _id=waba_id[i]['waba_id']
            relative_url = f"/{version}/{_id}/?fields=pricing_analytics.start({start_date}).end({end_date}).granularity(MONTHLY).dimensions(PRICING_CATEGORY,PRICING_TYPE,TIER,COUNTRY)"
                
            all_requests.append({
                "method": "GET",
                "relative_url": relative_url
            })

        batch_request = []
        for i in range(0, len(all_requests), 50):
            batch = all_requests[i:i + 50]
            batch_request.append(batch)
        print(len(batch_request))

        result_requests = []
        for i in batch_request:
            result = requests_to_meta(i)
            result_requests.extend(result)

        return result_requests
    except requests.exceptions.RequestException as e:
        print(f"Terjadi kesalahan saat melakukan request: {e}")
        return None

today = datetime.date.today()

first_day_of_current_month = today.replace(day=1)
date_in_previous_month = first_day_of_current_month - datetime.timedelta(days=4)
first_month = date_in_previous_month - datetime.timedelta(30)
start_of_prev_month_dt = datetime.datetime.combine(first_month, datetime.time.min)
unix_start_of_previous_month = int(start_of_prev_month_dt.timestamp())

end_of_prev_month_date = today.replace(day=1)
end_of_prev_month_dt = datetime.datetime.combine(end_of_prev_month_date, datetime.time.max)
unix_end_of_previous_month = int(end_of_prev_month_dt.timestamp())

# See GetWabaId.py to get list of waba_ids
analytics_req = get_insights_batch(waba_ids, version, unix_start_of_previous_month, unix_end_of_previous_month)
print(analytics_req)
analytics_val = []
for data in analytics_req:
    print(data)
    if data['body']:
        body_load = json.loads(data['body'])
        if 'pricing_analytics' in body_load:
            analytics_val.append(body_load)
