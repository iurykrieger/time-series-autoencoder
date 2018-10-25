from metrics import get_metrics_by_endpoint, parse_metrics, write_metrics_file
from plot import plot
from os import path

APIKEYS = [
    "centauro-v5",
    "netshoes-br",
    "netshoes-ar",
    "sephora-v6",
    "epocacosmeticos-intersect",
    "autoline",
    "extra",
    "pontofrio",
    "casasbahia"
]

ENDPOINTS = [
    "/raas/v2/pageview",
    "/raas/v2/cartview",
    "/raas/v2/search",
    "/raas/v2/views",
    "/raas/v2/transactions"
]

START = 1532646933
END = 1540422933

features = []
values = {}

for apikey in APIKEYS:

    apikey_data_file = "metrics/{apikey}_90d.csv".format(apikey=apikey)
    apikey_figure_file = "figures/{apikey}_90d.png".format(apikey=apikey)

    if not path.isfile(apikey_data_file):
        for endpoint in ENDPOINTS:
            parse_metrics(get_metrics_by_endpoint(apikey, endpoint, START, END), features, values)

        write_metrics_file(apikey, START, END, features, values)

    plot(apikey, apikey_data_file, apikey_figure_file)