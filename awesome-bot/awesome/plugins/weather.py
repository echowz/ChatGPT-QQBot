from nonebot import on_command, CommandSession
from . import adcode
import requests

url = 'https://restapi.amap.com/v3/weather/weatherInfo?parameters'
params_realtime = {
    'key': 'db5f322956c9cbc9c1dd570dc385c44f',
    'city': '420100',  # 从城市编码里获取的a丢包code
    'extensions': 'base'  # 获取实时天气
}



# on_command 装饰器将函数声明为一个命令处理器
# 这里 weather 为命令的名字，同时允许使用别名「天气」「天气预报」「查天气」
@on_command('weather', aliases=('天气', '天气预报', '查天气'))
async def weather(session: CommandSession):
    # 取得消息的内容，并且去掉首尾的空白符
    city_name = session.current_arg_text.strip()
    # 如果除了命令的名字之外用户还提供了别的内容，即用户直接将城市名跟在命令名后面，
    # 则此时 city_name 不为空。例如用户可能发送了："天气 南京"，则此时 city_name == '南京'
    # 否则这代表用户仅发送了："天气" 二字，机器人将会向其发送一条消息并且等待其回复
    #if not city_name:
    #    city_name = (await session.aget(prompt='你想查询哪个城市的天气呢？')).strip()
    #    # 如果用户只发送空白符，则继续询问
    #    while not city_name:
    #        city_name = (await session.aget(prompt='要查询的城市名称不能为空呢，请重新输入')).strip()
    # 获取城市的天气预报
    response_info = await get_weather_of_city(city_name)
    # 向用户发送天气预报
    await session.send(response_info)


async def get_weather_of_city(city_name: str) -> str:
    # 这里简单返回一个字符串
    # 实际应用中，这里应该调用返回真实数据的天气 API，并拼接成天气预报内容
    code, city_name = await adcode.get_adcode_by_name(city_name)
    if code is None:
        return '未查询到该地区的相关天气信息'
    params_realtime['city'] = code
    info = requests.get(url=url, params=params_realtime).json()
    weather = info.get('lives')[0].get('weather') # 天气 类型
    temperature_float = info.get('lives')[0].get('temperature_float') # 温度 浮点
    humidity_float = info.get('lives')[0].get('humidity_float') # 湿度 浮点
    winddirection = info.get('lives')[0].get('winddirection') # 风向 
    windpower = info.get('lives')[0].get('windpower') # 风能
    reporttime = info.get('lives')[0].get('reporttime') # 查询时间
    response_info = f'查询成功！\n[{city_name}] 的天气信息：\n' \
                    f'气象：{weather}\n' \
                    f'温度：{temperature_float}℃\n' \
                    f'湿度：{humidity_float}%\n' \
                    f'风向：{winddirection}方向\n' \
                    f'风能：{windpower}级\n' \
                    f'查询时间：{reporttime}\n'

    return response_info
