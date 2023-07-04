import requests

url = 'https://restapi.amap.com/v3/config/district?parameters'
params_city = {
    'key': '684a8c01bf2e3a37a298d5cdaf087f44',
    'keywords': '武汉',
    'subdistrict': '0',
    'extensions': 'base'
}


async def get_adcode_by_name(keywords: str) -> (str, str):
    params_city['keywords'] = keywords
    info = requests.get(url=url, params=params_city).json()
    print(info)
    try:
        adcode = info.get('districts')[0].get('adcode')
        city_name = info.get('districts')[0].get('name')
    except Exception:
        adcode = None
        city_name = ''
    return adcode, city_name

