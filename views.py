import json
import matplotlib.pyplot as plt
from datetime import datetime

APIKEYS = {
    'netshoes-br': [
        'netshoes-br-pageview-30d.json',
        'netshoes-br-cartview-30d.json',
        'netshoes-br-productview-30d.json',
        'netshoes-br-searchview-30d.json',
        'netshoes-br-transaction-30d.json'
    ],
    'centauro-v5': [
        'centauro-v5-pageview-30d.json',
        'centauro-v5-cartview-30d.json',
        'centauro-v5-productview-30d.json',
        'centauro-v5-searchview-30d.json',
        'centauro-v5-transaction-30d.json',
    ]
}
    
for apikey in APIKEYS:
    data = {}
    metrics = []
    out = open('%s.csv' % apikey, 'w')
    for json_data in APIKEYS[apikey]:
        viewdata = json.load(open('metrics/' + json_data, 'r'))

        for result in viewdata['data']['result']:
            if (result['metric']['statusCode'] != 'undefined'):
                status = int(result['metric']['statusCode'])
                if status >= 200 and status < 300:
                    status = 'success'
                elif status >= 400:
                    status = 'fail'
            else:
                status = result['metric']['statusCode']

            metric = result['metric']['method'] + '_' + result['metric']['path'] + '_' + status
            if metric not in metrics:
                metrics.append(metric)
            for value in result['values']:
                if value[0] not in data:
                    data[value[0]] = {}
                data[value[0]][metric] = data[value[0]][metric] + float(value[1]) if metric in data[value[0]] else float(value[1])


    out.write('timestamp;')
    print(len(metrics))
    for metric in metrics:
        print(metric)
        out.write(metric + ',')
    out.write('\n')

    for row in data:
        out.write('%s,' % datetime.utcfromtimestamp(row).strftime('%Y-%m-%d %H:%M:%S'))
        for metric in metrics:
            out.write('%.2f,' % (data[row][metric] if metric in data[row] else 0))
        out.write('\n')