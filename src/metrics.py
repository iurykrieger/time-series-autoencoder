from datetime import datetime
from prometheus import get_metrics_by_view_type

def write_metrics_file(apikey_data_file, features, values):
    if (len(features) > 0):
        out = open(apikey_data_file, 'w')
        out.write('timestamp')
        for feature in features:
            out.write(',' + feature)
        out.write('\n')

        for value in values:
            out.write('%s' % datetime.utcfromtimestamp(value).strftime('%Y-%m-%d %H:%M:%S'))
            for feature in features:
                out.write(',%.2f' % (values[value][feature] if feature in values[value] else 0))
            out.write('\n')

def parse_metrics(metrics):
    features = []
    values = {}
    if 'data' in metrics:
        for result in metrics['data']['result']:
            if (result['metric']['statusCode'] != 'undefined' and int(result['metric']['statusCode']) >= 200 and int(result['metric']['statusCode']) < 300):
                metric_name = result['metric']['path'].split('/')[-1] + '_success'
                if metric_name not in features:
                    features.append(metric_name)
                for value in result['values']:
                    if value[0] not in values:
                        values[value[0]] = {}
                    values[value[0]][metric_name] = values[value[0]][metric_name] + float(value[1]) if metric_name in values[value[0]] else float(value[1])
        return features, values
    else:
        raise Exception(metrics)

def get_page_views(api_key, start, end, step=1000, resolution="5m"):
    return parse_metrics(get_metrics_by_view_type(api_key, "pages", start, end, step, resolution))

def get_product_views(api_key, start, end, step=1000, resolution="5m"):
    return parse_metrics(get_metrics_by_view_type(api_key, "products", start, end, step, resolution))

def get_cart_views(api_key, start, end, step=1000, resolution="5m"):
    return parse_metrics(get_metrics_by_view_type(api_key, "carts", start, end, step, resolution))

def get_transaction_views(api_key, start, end, step=1000, resolution="5m"):
    return parse_metrics(get_metrics_by_view_type(api_key, "transactions", start, end, step, resolution))

def get_search_views(api_key, start, end, step=1000, resolution="5m"):
    return parse_metrics(get_metrics_by_view_type(api_key, "searches", start, end, step, resolution))

def get_all_views(api_key, start, end, step=1000, resolution="5m"):
    return parse_metrics(get_metrics_by_view_type(api_key, "all", start, end, step, resolution))