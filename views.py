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
data = {}
metrics = []
    
for apikey in APIKEYS:
    out = open('%s.csv' % apikey, 'w')
    for json_data in APIKEYS[apikey]:
        viewdata = json.load(open('metrics/' + json_data, 'r'))

        for result in viewdata['data']['result']:
            metric = apikey + '_' + result['metric']['method'] + '_' + result['metric']['path'] #+ '_' + result['metric']['statusCode']
            if metric not in metrics:
                metrics.append(metric)
            for value in result['values']:
                if value[0] not in data:
                    data[value[0]] = {}
                data[value[0]][metric] = data[value[0]][metric] + float(value[1]) if metric in data[value[0]] else float(value[1])


out.write('timestamp;')
for metric in metrics:
    print(metric)
    out.write(metric + ';')
out.write('\n')

X = []
Y = []

for row in data:
    out.write(datetime.utcfromtimestamp(row).strftime('%Y-%m-%d %H:%M:%S'))
    X.append(int(row))
    l = []
    for metric in metrics:
        l.append((data[row][metric] if metric in data[row] else 0))
        out.write('%.2f;' % (data[row][metric] if metric in data[row] else 0))
    Y.append(l)
    out.write('\n')

plt.plot(X, Y)
plt.gcf().autofmt_xdate()
plt.show()