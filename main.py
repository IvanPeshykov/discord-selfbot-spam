import discord
from data.config import token, guilds, text, delay
import logging
import asyncio
from src.captcha_handler import CaptchaHandler

class MyClient(discord.Client):

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        if message.author == self.user or message.guild is None or (message.guild.id not in guilds and guilds):
            return

        try:
            with open('data/users_sent.txt', 'r') as f:
                users_sent = set(map(int, f.read().splitlines()))

            if message.author.id in users_sent:
                return

            print("Sending message to:", message.author)
            await asyncio.sleep(delay)
            await message.author.send(text)
            print("Successfully sent message to:", message.author)
            users_sent.add(message.author.id)

            with open('data/users_sent.txt', 'w') as f:
                f.write('\n'.join(map(str, users_sent)))

        except Exception as e:
            print("Couldn't send message to:", message.author)
            print("Error:", e)


def main():

    client = MyClient(captcha_handler=CaptchaHandler())
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

    try:
        client.run(token, log_handler=handler)
    except:
        print("Couldn't start bot, make sure your token is correct.")

if __name__ == "__main__":
    main()