# -*- coding: utf8 -*-

# Код как вы видите старый, по-этому не удивляйтесь присутствующему тут говнокоду

import discord
from discord import *
from discord.ext import commands
import asyncio
import time
from random import randint
import random
import string
import os
import requests
import datetime
from asyncio import sleep

token = "bot token here"

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='n!', intents=intents)
client.remove_command('help') # удаляем встроенную команду хелпа

@client.command()
@commands.cooldown(1, 29, commands.BucketType.user)
async def generate(ctx, amount=1250):
  if amount == 1250:
    await ctx.send('Вы можете указывать необходимое кол-во кодов для генерации, например: `n!generate 1000`. Поскольку аргументы отсутствуют, генерирую 1250 кодов.')
  if int(amount) < 1:
    await ctx.send(f'{ctx.author.mention}, укажи число больше 1. Создатель бота уже устал фиксить малейшие недочёты.')
    return
  if int(amount) < 50001:
    timer = time.time()
    embed = discord.Embed(
        title = 'Генерация кодов Nitro',
        description = f'Запускаю процесс...',
        colour = discord.Colour.from_rgb(7, 128, 7)
    )

    msg = await ctx.send(embed=embed)
    value = 1
    file = f'Codes_{ctx.author.id}.txt'
    embed = discord.Embed(
        title = 'Генерация кодов Nitro',
        description = f'Генерация кодов запущена, пожалуйста, подождите...',
        colour = discord.Colour.from_rgb(7, 128, 7)
    )
    await msg.edit(embed=embed)
    while value <= int(amount):
        code = "https://discord.gift/" + ('').join(random.choices(string.ascii_letters + string.digits, k=16))
        f = open(f'Codes_{ctx.author.id}.txt', "a+")
        f.write(f'{code}\n')
        f.close()
        value += 1
    embed = discord.Embed(
        title = 'Генерация кодов Nitro',
        description = f'Успешно сгенерировано {amount} кодов!\nОперация заняла `{int(time.time()) - int(timer)} секунд`.',
        colour = discord.Colour.from_rgb(7, 128, 7)
    )
    await msg.edit(embed=embed)
    await ctx.send(file=discord.File(f'Codes_{ctx.author.id}.txt'))
    os.remove(f'Codes_{ctx.author.id}.txt')
  else:
    embed = discord.Embed(
        title = 'Генерация кодов Nitro',
        description = f'Вы можете генерировать максиум `50000` кодов!',
        colour = discord.Colour.from_rgb(255, 255, 0)
    )
    await ctx.send(embed=embed)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        tme = f'{round(error.retry_after, 1)}'
        ntme = '.'.join(tme.split('.')[:-1])
        embed = discord.Embed(
            title = 'Ошибка :x:',
            description = f'Вы сможете использовать эту команду только через `{ntme} секунд`.',
            colour = discord.Colour.from_rgb(255, 1, 7)
        )

        msg = await ctx.send(embed=embed)

@client.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def quick_gen(ctx, count=0):
    if int(count) == 0:
      await ctx.send(f'{ctx.author.mention}, укажи кол-во кодов. Подробнее: `n!help`')
      return
    if int(count) < 1:
      await ctx.send(f'{ctx.author.mention}, укажи число более 1!')
      return
    if int(count) > 26:
        await ctx.send(f'{ctx.author.mention}, максимальное кол-во кодов в данной команде - `25`.')
        return
    for i in range(int(count)):
        time.sleep(0.2)
        try:
          await ctx.author.send("https://discord.gift/" + ('').join(random.choices(string.ascii_letters + string.digits, k=16)))
        except:
          await ctx.send(f'{ctx.author.mention}, пожалуйста, открой ЛС, или удали бота из чс.')
          break
    await ctx.message.add_reaction('✅')

@client.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def gen_and_check(ctx):
    try:
      ms = await ctx.author.send(f'Все рабочие коды будут указаны тут, если они будут найдены.')
    except:
      await ctx.send(f'{ctx.author.mention}, не могу продолжить работу. Для продолжения работы бота открой ЛС.')
      return
    em = await ctx.send('Генерация и проверка кодов | Nitro Bot')
    for i in range(10):
                nitro = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
                url = f"https://discordapp.com/api/v9/entitlements/gift-codes/{nitro}?with_application=false&with_subscription_plan=true"
                response = requests.get(url)
                if response.status_code == 200:            
                    await ctx.author.send(f'Valid - https://discord.gift/{nitro}')
                
                  
                    embed = discord.Embed(
                        title = 'Генерация и проверка кодов Nitro',
                        description = f'```py\nhttps://discord.gift/{nitro}```\nСтатус: `Рабочий`',
                        colour = discord.Colour.from_rgb(0, 128, 0)
                    )
                    await em.edit(embed=embed)
                    await ms.edit(content=f'{nitro} - данный код является рабочим.')
                    time.sleep(5)
                else:
                    embed = discord.Embed(
                        title = 'Генерация и проверка кодов Nitro',
                        description = f'```py\nhttps://discord.gift/{nitro}```\nСтатус: `Не рабочий`',
                        colour = discord.Colour.from_rgb(0, 128, 0)
                    )
                    await em.edit(embed=embed,content='')
                    asyncio.sleep(1)

    embed = discord.Embed(
            title = 'Генерация и проверка кодов Nitro',
            description = f'Процесс успешно завершён! Все рабочие коды, если они были найдены, были отправлены тебе в лс | :white_check_mark:',
            colour = discord.Colour.from_rgb(0, 128, 0)
    )
    await em.edit(embed=embed,content='')
  
@client.command()
async def help(ctx):
    embed = discord.Embed(
            title = 'Nitro Bot | Помощь :tools:',
            description = f'`[ ]` - обязательный аргумент, `( )` - не обязательный аргумент\n\nСгенерирует указанное кол-во кодов и отправит их вам файлом.\n```py\nn!generate ( кол-во кодов )```\nСгенерирует указанноее кол-во кодов и отправит вам в ЛС.\n```py\nn!quick_gen [ кол-во кодов ]```\nСгенерировать 10 кодов и проверить их на валид\n```py\nn!gen_and_check```\nВывести информацию о боте\n```py\nn!bot```\n\n:link: [Сервер поддержки](https://discord.gg/3BsRy2B9nk)\n:robot: [Пригласить бота](https://discord.com/api/oauth2/authorize?client_id={client.user.id}&permissions=8&scope=bot)',
            colour = discord.Colour.from_rgb(103, 166, 50)
    )
    embed.set_footer(text='Nitro Bot | Все права защищены')
    await ctx.send(embed=embed)

@client.event
async def on_ready():
        global startTime
        startTime = time.time()
        await client.change_presence(activity=discord.Game(name=f"n!help | {len(client.guilds)} серверов"))

@client.event
async def on_guild_join(guild):
    await client.change_presence(activity=discord.Game(name=f"n!help | {len(client.guilds)} серверов"))

@client.command()
async def bot(ctx):
    ping = client.latency * 1000
    ping = '.'.join(str(ping).split('.')[:-1])
    servers = len(client.guilds)
    uptime = str(datetime.timedelta(seconds=int(round(time.time()-startTime))))
    embed = discord.Embed(
            title = 'Nitro Bot | Информация :bulb:',
            description = f'Приветик! Меня зовут Nitro Bot, и возможно, я сделаю твоё пребывание в дискорде счастливым :ok_hand:\nВот кратенькая информация обо мне:\n\n:champagne_glass: Кол-во серверов:\n```py\n{servers}```\n:snake: Язык программирования:\n```py\nPython 3.8.8```\n:notebook_with_decorative_cover: Библиотека:\n```py\ndiscord.py```\n:star2: Дата создания:\n```py\n25.10.2021```\n:thread: Последнее обновление:\n```py\n26.10.2021```\n:trophy: Версия:\n```py\n1.1 Release```\n:hourglass: Аптайм:\n ```py\n{uptime}```\n:game_die: Пинг:\n```py\n{ping} ms```',
            colour = discord.Colour.from_rgb(0, 140, 0)
    )
    await ctx.send(embed=embed)

client.run(token, bot=True)
