import discord
import openai
import argparse
#api_key 記得要刪除
#messages 的部分表示歷史對話，在某些對話中會有用到

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

ans = openai.ChatCompletion.create(
    api_key="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",
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "你是一位中國信託的理財專員。"},
        {"role": "system", "content": "目前提供的產品有："},
        {"role": "system", "content": "1. 信託基金"},
        {"role": "system", "content": "2. 信託保險"},
        {"role": "system", "content": "3. 信託貸款"},
        {"role": "user", "content": "我想知道信託基金的產品特色。"},
    ],
)
print(ans.choices[0]["message"]["content"])

@client.event
async def on_ready():
    print("目前登入身分為:",client.user)

@client.event
async def on_message(message):
    if message.author == client.user:return
    if message.content.startswith("!"):
        data = create_completion(message.content[1:])
        pprint(data)
        await message.channel.send(data["choices"][0]["text"])

client.run(DISCORD_TOKEN)