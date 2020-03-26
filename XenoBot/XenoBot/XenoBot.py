from bs4 import BeautifulSoup
import bs4
import discord
import datetime
import asyncio
import requests
import time
from urllib.request import urlopen, Request
import urllib

app = discord.Client()
token = open('C://Users//이정형//Documents//Xenotoken.txt', 'r').read()

@app.event
async def on_ready():
    print("Log in to next -> ", end = "")
    print(app.user.name)


@app.event
async def on_message(message):
    cont, auth = message.content, message.author



app.run(token)