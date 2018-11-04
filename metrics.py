import requests
from datetime import datetime
from pandas import rolling_mean

def moving_average(values, N = 3):
    cumsum, moving_aves = [0], []

    for index, value in enumerate(values, 1):
    cumsum.append(cumsum[index - 1] + value)
    if index >= N:
        moving_ave = (cumsum[index] - cumsum[index - N]) / N
        moving_aves.append(moving_ave)
    return moving_aves

def get_metrics_by_endpoint(session, apikey, endpoint, start, end, step = 1000):
    base_url = "http://metrics.chaordicsystems.com/api/datasources/proxy/31/api/v1/query_range"
    params = {
        "query": "sum by (method, path, statusCode)(increase(collect_server_http_outbound{{apiKey=\"{apikey}\", path=\"{path}\"}}[5m]))".format(apikey=apikey, path=endpoint),
        "start": start,
        "end": end,
        "step": step
    }
    cookies = {
        "grafana_sess": session
    }

    return requests.get(base_url, params=params, cookies=cookies).json()

def parse_metrics(metrics, features, values):
    for result in metrics['data']['result']:
        if (result['metric']['statusCode'] != 'undefined' and int(result['metric']['statusCode']) >= 200 and int(result['metric']['statusCode']) < 300):
            metric_name = result['metric']['method'].upper() + '_' + result['metric']['path'].split('/')[-1] + '_success'
            if metric_name not in features:
                features.append(metric_name)
            for value in result['values']:
                if value[0] not in values:
                    values[value[0]] = {}
                values[value[0]][metric_name] = values[value[0]][metric_name] + float(value[1]) if metric_name in values[value[0]] else float(value[1])

def write_metrics_file(apikey, start, end, features, values):
    if (len(features) > 0):
        days = (datetime.fromtimestamp(end) - datetime.fromtimestamp(start)).days
        out = open('metrics/{apikey}_{days}d.csv'.format(apikey=apikey, days=days), 'w')
        out.write('timestamp')
        for feature in features:
            out.write(',' + feature)
        out.write('\n')

        for value in values:
            out.write('%s' % datetime.utcfromtimestamp(value).strftime('%Y-%m-%d %H:%M:%S'))
            for feature in features:
                out.write(',%.2f' % (values[value][feature] if feature in values[value] else 0))
            out.write('\n')