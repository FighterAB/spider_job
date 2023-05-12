import json
import os
import django

from myApp.utils.getPublicData import city

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Jop_spider.settings')
django.setup()

from myApp.models import Province,City

class get():
    def getProvince(self,city):
        provinceList = {}
        for i in city['zpData']['cityList']:
            provinceList[i['name']] = i['code']
        return provinceList


    def getCity(self,city):
        cityList = {}
        city = city['zpData']['cityList']
        for i in city:
            dict = {}
            for k in i['subLevelModelList']:
                dict[k['name']] = k['code']
            cityList[i['name']] = dict
        return  cityList


    def getHotCityList(self,city):
        hotCity ={}
        hotCityList = city['zpData']['hotCityList']
        for i in hotCityList:
            if hotCity.get(i['name'],-1)==-1:
                hotCity[i['name']] = i['code']
        return hotCity

    def save_sql_province(self,provinceList):
        for key,value in provinceList.items():
            Province.objects.create(
                name=key,
                code=value
                )

    def save_sql_city(self,cityList,hotCityList,provinceList):
        for key,value in cityList.items():
            pro_code = provinceList.get(key)
            for k,v in value.items():
                bool = k in hotCityList
                obj = Province.objects.get(code=pro_code)
                City.objects.create(
                    name=k,
                    code=v,
                    hotCity=bool,
                    pro_code=obj
                )

    def __int__(self):
        pass

    def test(self,cityList,hotCityList,provinceList):
        for key,value in cityList.items():
            pro_code = provinceList.get(key)
            for k,v in value.items():
                bool = k in hotCityList
                print(k,v,bool,pro_code)



if __name__ == '__main__':
    city = json.load(open('city.json', encoding='utf8'))
    provinceList = get().getProvince(city)
    hosCityList = get().getHotCityList(city)
    cityList= get().getCity(city)
    # get().save_sql_province(provinceList)
    get().save_sql_city(cityList,hosCityList,provinceList)
    # print(hosCityList)
    # get().test(cityList,hosCityList,provinceList)

