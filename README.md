<!--
 * @Author: hibana2077 hibana2077@gmail.com
 * @Date: 2023-03-02 22:19:20
 * @LastEditors: hibana2077 hibana2077@gmail.com
 * @LastEditTime: 2023-03-07 12:32:40
 * @FilePath: \chatgpt_discord_bot\README.md
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
# Chatgpt Discord bot

## Status

![GitHub](https://img.shields.io/github/license/hibana2077/chatgpt_discord_bot)
![GitHub last commit](https://img.shields.io/github/last-commit/hibana2077/chatgpt_discord_bot)

## Description

![python](https://img.shields.io/badge/python-3.10-blue?style=plastic-square&logo=python)
![discord.py](https://img.shields.io/badge/discord.py-2.2.2-blue?style=plastic-square&logo=discord)
![openai](https://img.shields.io/badge/openai-0.27.0-blue?style=plastic-square&logo=openai)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-4.11.2-blue?style=plastic-square&logo=BeautifulSoup)

This is a discord bot that uses the [ChatGPT-API](https://platform.openai.com/docs/guides/chat) to generate responses to messages with real-time data from google search.

## Usage

### normal

#### Requirements

- python 3.10

#### Install

```bash
pip install -r requirements.txt
```

#### Run

```bash
python main.py --token <your discord bot token> --openai <your openai api key>
```

### Docker

#### Requirements

- docker

#### Pull image

```bash
docker pull hibana2077/chatgpt_discord_bot
```

image link: [https://hub.docker.com/r/hibana2077/chatgpt_discord_bot](https://hub.docker.com/r/hibana2077/chatgpt_discord_bot)

image size: 51.05 MB

---

#### Run

```bash
docker run -d --name chatgpt_discord_bot hibana2077/chatgpt_discord_bot --DISCORD_TOKEN <your discord bot token> --OPENAI_API <your openai api key>
```

### Commands

send message with prefix `!` to bot.

![](https://media.discordapp.net/attachments/962678338512625664/1082503500837175428/image.png)

you can get crypto currency price with `!<crypto currency name>`. (ex. `!btc`)

![](https://media.discordapp.net/attachments/962678338512625664/1081495918496448582/image.png)

also you can get weather information with `!<city name>天氣`. (ex. `!東京市天氣`) (only support chinese)

![](https://media.discordapp.net/attachments/962678338512625664/1082503911321116772/image.png)

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Author

[hibana2077](https://www.hibana2077.com)

## Reference

- [ChatGPT-API](https://platform.openai.com/docs/guides/chat)
- [Docker使用教學](https://yeasy.gitbook.io/docker_practice/)
- [discord.py](https://discordpy.readthedocs.io/en/latest/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/)