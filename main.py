import discord
from discord import message
from discord import colour
from discord.ext import commands
from discord.ext.commands.errors import CommandInvokeError
import requests
from urllib.request import urlopen
import json
import os

client = commands.Bot(command_prefix="!")

vs_currency = "USD"

@client.event
async def on_ready():
    print("Logado como {0.user}".format(client))

@client.command()
async def price(ctx):
    currency = ctx.message.content.split("!price ",1)[1].upper()
    # print(currency)
    global vs_currency

    url = "https://api.nomics.com/v1/currencies/ticker?key=bdba36cf31bfb1d4319a89f095fd8af8b04a6263&ids={}&interval=1d,30d&convert={}&per-page=100&page=1".format(currency, vs_currency)

    with urlopen(url) as response:
        data = json.load(response)
        # print(data)

    if not data:
        await ctx.send("Essa moeda não está disponível. Tente outro tipo de moeda. Ex: BTC, ETH e etc.")

    coin_title = data[0]['name']
    coin_price = float(data[0]['price'])
    coin_price_real = "{:.2f}".format(coin_price)
    await ctx.send("O valor de " + coin_title + ' é ' + vs_currency + ' {}.'.format(coin_price_real))

@client.command()
async def set(ctx):
    other_currency = ctx.message.content.split("!set ",1)[1].upper()

    url = "https://api.nomics.com/v1/currencies/ticker?key=bdba36cf31bfb1d4319a89f095fd8af8b04a6263&ids=DOGE&interval=1d,30d&convert={}&per-page=100&page=1".format(other_currency)

    with urlopen(url) as response:
        data = json.load(response)
        print(data)

    if data[0]['price'] == '0.00000000':
        await ctx.send("Essa moeda não está disponível. Tente outro tipo de moeda. Ex: USD, EUR e etc.")
        return None

    print(other_currency)
    global vs_currency
    vs_currency = other_currency
    await ctx.send("A sua moeda de comparação foi trocada para " + other_currency)

@client.command()
async def currency(ctx):
    await ctx.send("A sua moeda de comparação atual é " + vs_currency)

@client.command()
async def ajuda(ctx):
    embed = discord.Embed(title = "Comandos do Bot", description="Lista de comandos do bot.", colour=discord.Colour.red())

    embed.add_field(name="!price", value="Veja o preço da moeda desejada. Ex: BTC, ETH, DOGE e etc.", inline=False)
    embed.add_field(name="!set", value="Mude o preço da sua moeda de comparação. Ex: USD, EUR, BRL e etc.", inline=False)
    embed.add_field(name="!currency", value="Veja a sua moeda de comparação atual.", inline=False)
    embed.add_field(name="!ajuda", value="Veja os comandos disponíveis.", inline=False)
    
    await ctx.send(embed=embed)

client.run("ODgzMDE4MjEwMzA2MzAxOTgz.YTD0yw.l_UocwtPqJITeEtjwirYeMGxj1Y")