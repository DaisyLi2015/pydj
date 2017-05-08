from suds.client import Client
from suds.xsd.doctor import Import, ImportDoctor

url = ' http://ws.webxml.com.cn/WebServices/WeatherWS.asmx?wsdl'


imp= Import('http://www.w3.org/2001/XMLSchema',
            location=' http://www.w3.org/2001/XMLSchema.xsd')
imp.filter.add('http://WebXml.com.cn/')

client = Client(url,plugins=[ImportDoctor(imp)])
print(client)

countrycode = client.service.getRegionDataset()
print(countrycode)

citycode =  client.service.getSupportCityString(311101)
print(citycode)

result = client.service.getWeather(792,'')
print(result)

# result = client.service.getWeather('北京')
# print(result)