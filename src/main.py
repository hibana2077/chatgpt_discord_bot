'''
Author: hibana2077 hibana2077@gmail.com
Date: 2023-03-02 22:19:20
LastEditors: hibana2077 hibana2077@gmail.com
LastEditTime: 2023-03-07 12:04:03
FilePath: \chatgpt_discord_bot\src\main.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''

import bs4
import discord
import openai
import argparse
import datetime
import requests
import ccxt
#api_key 記得要刪除
#messages 的部分表示歷史對話，在某些對話中會有用到

parser = argparse.ArgumentParser(description="OpenAI ChatGPT Bot")
parser.add_argument("--token", type=str, help="Discord Bot Token")
parser.add_argument("--openai_key", type=str, help="OpenAI API Key")
args = parser.parse_args()

OPENAI_APIKEY = args.openai_key
DISCORD_TOKEN = args.token

if OPENAI_APIKEY == "DEFAULT" or DISCORD_TOKEN == "DEFAULT":
    raise ValueError("Please set your own OpenAI API Key and Discord Bot Token")
elif OPENAI_APIKEY == None or DISCORD_TOKEN == None:
    raise ValueError("Please set your own OpenAI API Key and Discord Bot Token")
print("OpenAI API Key: " + OPENAI_APIKEY)
print("Discord Bot Token: " + DISCORD_TOKEN)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
binance = ccxt.binance()
binance.load_markets()
qary_list = [i.split("/")[0] for i in binance.symbols if i.split("/")[-1] == "USDT"]

def keyword_extract(user_input:str):
    data = openai.ChatCompletion.create(api_key=OPENAI_APIKEY,
                                        model = "gpt-3.5-turbo",
                                        messages=[{"role": "system", "content": f"擷取這段文字中的關鍵字: {user_input}"},
                                                  {"role": "system", "content": "回傳格式為: 關鍵字1 關鍵字2 關鍵字3 ..."}])
    return data.choices[0]["message"]["content"]

def get_weather(city_name:str)->str:
    url = f"https://www.google.com/search?q={city_name}天氣"
    headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.57"
            }
    res = requests.get(url, headers=headers)
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    with open("test.html", "w", encoding="utf-8") as f:
        f.write(soup.prettify())
        f.close()
    print(f"Google search Done!")
    weather_block = soup.select(".nawv0d")
    temp_humid_wind_rain = weather_block[0].select(".UQt4rd")
    temp_c = bs4.BeautifulSoup(str(temp_humid_wind_rain[0].find("span", {"id": "wob_tm"})), "html.parser").text
    temp_f = bs4.BeautifulSoup(str(temp_humid_wind_rain[0].find("span", {"id": "wob_ttm"})), "html.parser").text
    raining_chance = bs4.BeautifulSoup(str(temp_humid_wind_rain[0].find("span", {"id": "wob_pp"})), "html.parser").text
    humidity = bs4.BeautifulSoup(str(temp_humid_wind_rain[0].find("span", {"id": "wob_hm"})), "html.parser").text
    wind = bs4.BeautifulSoup(str(temp_humid_wind_rain[0].find("span", {"id": "wob_ws"})), "html.parser").text
    return f"\n {city_name}目前天氣: \n 攝氏溫度: {temp_c}°C \n 華氏溫度: {temp_f}°F \n 降雨機率: {raining_chance} \n 濕度: {humidity} \n 風速: {wind} \n"


def get_realtime_data(user_input:str):
    need_to_check_list = [i for i in qary_list if i in user_input]
    data = [ccxt.binance().fetch_ticker(i+"/USDT")['info']['lastPrice'] for i in need_to_check_list]
    return_str = "以下是目前使用者詢問的商品價格(單位USDT):\n"
    for a,b in zip(need_to_check_list,data):
        return_str += f"{a} 價格: {b}\n"
    if data == []:
        return_str = "目前使用者沒有詢問的商品價格，以下為使用者詢問內容在google上的搜尋結果:\n"
    else:
        return_str += "以下為使用者詢問內容在google上的搜尋結果:\n"
    text = keyword_extract(user_input).replace("\n", "")
    print(f"({datetime.datetime.now()}) 使用者詢問: {user_input} 搜尋的關鍵字: {text}")
    url = f"https://www.google.com/search?q={text}"
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    title = soup.select(".BNeawe.vvjwJb.AP7Wnd")
    if "天氣" in user_input:
        return_str = "目前使用者沒有詢問的商品價格，以下為使用者詢問的天氣資訊:\n"
        return_str += get_weather(user_input.split("天氣")[0])
        print(f"({datetime.datetime.now()}) 使用者詢問: {user_input} return: {return_str}")
        return return_str
    for index,t in enumerate(title):
        link = soup.select(".egMi0.kCrYT")[index].select("a")[0]["href"]
        return_str += f"{index+1}. 連結名稱:{t.text}\t 連結:{link[7::]}\n"
    print(f"({datetime.datetime.now()}) 使用者詢問: {user_input} return: {return_str}")
    return return_str

@client.event
async def on_ready():
    print(f"({datetime.datetime.now()}) 目前登入身分為: {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:return
    if message.content.startswith("!"):
        data = openai.ChatCompletion.create(
            api_key=OPENAI_APIKEY,
            model = "gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一個使用GPT3.5驅動的Discord機器人，要回答使用者的問題，如果資料不足可以根據下方的資料進行回答。"},
                {"role": "system", "content": "這是你的程式碼庫: https://github.com/hibana2077/chatgpt_discord_bot \n"},
                {"role": "system", "content": "這位使用者的名字是: " + str(message.author)},
                {"role": "system", "content": get_realtime_data(message.content[1::])},
                {"role": "system", "content": "傳送連結時請使用: (連結網址)\n 的格式"},
                {"role": "user", "content": message.content[1::]}])
        print(f"({datetime.datetime.now()}) --> {message.author} 說: {message.content[1::]}")
        await message.channel.send(data.choices[0]["message"]["content"])

client.run(DISCORD_TOKEN)