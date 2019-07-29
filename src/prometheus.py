import requests
from datetime import datetime
from os.path import isfile

ENDPOINTS = {
    "pages": "/raas/v2/pageview",
    "carts": "/raas/v2/cartview",
    "searches": "/raas/v2/search",
    "products": "/raas/v2/views",
    "transactions": "/raas/v2/transactions",
    "all": "/raas/v2/cartview|/raas/v2/search|/raas/v2/views|/raas/v2/transactions"
}

def build_query_by_view_type (api_key, view_type, resolution):
    return "sum by (method, path, statusCode)(increase(collect_server_http_outbound{{apiKey=\"{api_key}\", path=~\"{path}\"}}[{resolution}]))".format(
        api_key=api_key,
        path=ENDPOINTS[view_type],
        resolution=resolution
    )

def get_metrics_by_view_type (api_key, view_type, start, end, step = 1000, resolution = '5m'):
    base_url = "http://prometheus.dc.chaordicsystems.com:9090/api/v1/query_range"
    params = {
        "query": build_query_by_view_type(api_key, view_type, resolution),
        "start": start.timestamp(),
        "end": end.timestamp(),
        "step": step
    }
    return requests.get(base_url, params=params).json()
