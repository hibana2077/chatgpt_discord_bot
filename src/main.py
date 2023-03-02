import discord
import openai
import argparse
import time
import ccxt
#api_key 記得要刪除
#messages 的部分表示歷史對話，在某些對話中會有用到

parser = argparse.ArgumentParser(description="OpenAI ChatGPT Bot")
parser.add_argument("--token", type=str, help="Discord Bot Token")
parser.add_argument("--openai_key", type=str, help="OpenAI API Key")
args = parser.parse_args()

OPENAI_APIKEY = args.openai_key
DISCORD_TOKEN = args.token

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

def get_price(symbol:str):
    binance = ccxt.binance()

@client.event
async def on_ready():
    print(f"({time.time()}) 目前登入身分為: {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:return
    if message.content.startswith("!"):
        data = openai.ChatCompletion.create(
            api_key=OPENAI_APIKEY,
            model = "gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一Discord機器人，要回答使用者的問題。"},
                {"role": "user", "content": message.content[1::]}])
        print(f"({time.time()}) {message.author} 說: {message.content[1::]}")
        await message.channel.send(data.choices[0]["message"]["content"])

client.run(DISCORD_TOKEN)