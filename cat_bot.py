
import discord
from discord.ext import tasks, commands
from typing import Final
import os
from dotenv import load_dotenv
from PIL import Image
import requests
from io import BytesIO

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

urls = []
index = 0
with open("urls.txt", "r") as f:
    urls = f.read().split("\n")
    


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    
@bot.command()
async def unleash(ctx):
    print('Starting...')
    send_img.start(ctx)

@bot.command()
async def nextimg(ctx):
    await send_img(ctx)

@tasks.loop(seconds=5)
async def send_img(ctx):
    global index
    global urls
    url = urls[index]
    index += 1
    response = requests.get(url, headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36' })

    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        buffer = BytesIO()
        
        img.save(buffer, format="PNG")
        buffer.seek(0)
        file = discord.File(buffer, filename="image.png")
        await ctx.send(file=file)
        
    

bot.run(TOKEN)
