import json
import requests


with open('../static/json/china.json', encoding='utf-8') as a:
    result = json.load(a)
    # for i,v in result.items():
    #     print(i,v)
    # print(result['features'])
    print('{',end='')
    for i in result['features']:
        # print(i['properties']['name'] + ':' + str(i['properties']['code']) + ',')
        st = str(i['properties']['code'])
        print("'"+i['properties']['name']+"'",end=':[')
        file = open("../static/json/city/"+st+".json", mode='w')
        res = requests.get('https://geojson.cn/api/data/'+st+'.json')
        if res.status_code == 200:
            res = json.loads(res.text)
            for j in res['features']:
                if j==res['features'][-1]:
                    print("'"+j['properties']["name"]+"'",end='],')
                else:
                    print("'"+j['properties']["name"]+"'",end=',')
        print()
    print('}')




    # for i in range(len(result['features'])):
    #     dict = result
    #     print(dict)
    # print(dict['name'],dict['code'])
