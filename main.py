# ------------------------------- #

#  This bot was made by amine or  #

#     AmineDev07 On github        #

# ------------------------------- #


# PACKAGES #
# ♻️ Importing the packages ♻️
import os # ❕ this will be used to get the replit secret ❕
import discord # ❕ this will be used to import the discord package ❕
from discord.ext import commands, tasks # ❕ this will get the commands and tasks from the discord package we have imported ❕
import asyncio
import urllib.parse # ❕ this will be used for parsing links ❕
import urllib.request 
from colorama import Fore, Back, Style # this is for the console log colors
import re
from discord.player import FFmpegPCMAudio, PCMVolumeTransformer # ⚠️ those are the most important packages for us to run a music client ⚠️ 
from youtube_dl import YoutubeDL # important ⚠️
from youtube_dl.utils import DownloadError, ExtractorError # important ⚠️
import validators # important ⚠️
# PACKAGES #


# BOT CONFIGURATIONS #
TOKEN = os.environ['TOKEN'] # 💡 this will get the token from the replit secret by the name u used 💡
PREFIX = os.environ['PREFIX']
client = discord.Client() # We defined the clinet
client = commands.Bot(command_prefix= PREFIX, case_insensitive=True) # We defined the prefix for the commands
 # We removed the help command tha was made by the package
# BOT CONFIGURATIONS #



# EMBED #
class Embed :
  footertext = 'Musicord' # Put your bot name here or you can easily do client.user.name
  footericon = 'https://images-ext-2.discordapp.net/external/KCItYeha6lpNFNiacUcXhWYoK9KWc8DxGr03xOUaNYg/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/760970424053268550/332db8e27228346ebbf4c57acb361703.png' # This is optional you can put your bot image or just f'{client.user.avatar_url}'
  
  
# EMBED #

# COLOR #

class Color : 
  success = 0x76B355
  error = 0xDD2F45
  null = 0xFECD4D
  main = 0x4456FF
# COLOR #

# EMOJIS #

class Emoji : 
  success = '<a:Success:1048363775587262545>'
  error = '<:ERROR:1048552914886598766>'
  null = '<a:Attention:991049448270475334>'
  music = '<:checked:1048549042877108307>'
  search = '<a:loading_bot:1048372362925572246>'
  ok = '<:okay:1048368956819390565>'
  main = '<:checked:1048549042877108307>'

# EMOJIS # 

# Error embed function #
async def error_embed(ctx, msg) :
  embed = discord.Embed(description = f'**{Emoji.error} | `{msg}`**', color = Color.error)
  embed.set_footer(text = Embed.footertext, icon_url = Embed.footericon)
  await ctx.send(embed=embed, delete_after=8)


# Success embed function #
async def success_embed(ctx, msg) :
  embed = discord.Embed(description = f'**{Emoji.success} | `{msg}`**', color = Color.success)
  await ctx.send(embed=embed, delete_after=20)







# YoutubeDL stuff

queue = []
repeat = 'none'
YDL_OPTIONS = {'format': 'bestaudio/best', 'noplaylist': 'True'}
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
# YoutubeDL stuff

# client once it ready it print the client user#tag in the console log with "has connected to discord"
@client.event
async def on_ready():
    print(Back.BLACK + Fore.RED + f'[{client.user.name}] has connected to Discord!')
    print(Style.RESET_ALL)
    print(Back.BLACK + Fore.BLUE+'All copyrights go to [AmineDev07] https://github.com/AmineDev07 On github')
    print(Style.RESET_ALL)


    


def player(ctx, voice):
    global music_title # Those we defined earlier on YoutubeDL 
    global music_thumbnail # Those we defined earlier on YoutubeDL 
    global music_url # Those we defined earlier on YoutubeDL 
    global client_activity # Those we defined earlier on YoutubeDL 


# 📲 EXTRACTING THE INFORMATIONS 📲

    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(queue[0], download=False)
    URL = info['formats'][0]['url']
    client_activity = info.get('title', None)
    music_url = queue[0]
    music_title = info.get('title', None)
    music_thumbnail = info.get('thumbnail')
    voice.play(FFmpegPCMAudio(
        URL, executable="ffmpeg", **FFMPEG_OPTIONS), after=lambda e: play_queue(ctx, voice))
    voice.is_playing()
# 📲 EXTRACTING THE INFORMATIONS 📲


# ------------------------------- #

#  This bot was made by amine or  #

#     AmineDev07 On github        #

# ------------------------------- #

# 🖥️ THE BEGIN OF THE COMMANDS 🖥️
def play_queue(ctx, voice):
    global repeat
    try:
        if repeat == 'yes':
            player(ctx, voice)
        elif len(queue) >= 1:
            del queue[0]
            player(ctx, voice)
    except IndexError:
        print(f'Queue finished')

@client.command(name='join')
async def join(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if not ctx.message.author.voice:
          await error_embed(ctx, f'{ctx.author.name} You are not in a voice channel')

    else:
        if voice is None:
            channel = ctx.message.author.voice.channel
            await channel.connect()
            await ctx.guild.change_voice_state(channel=channel, self_mute=False, self_deaf=True)
            await ctx.send(f'**{Emoji.ok} Joined <#{channel.id}> bound to {ctx.message.channel.mention}**')
        else:
            await error_embed(ctx , f'{client.user.name} is already in another channel')


@client.command(name='play', aliases=['p'])
async def play(ctx, *, url: str):
    channel = ctx.message.author.voice.channel
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice is None:
            await channel.connect()
            await ctx.guild.change_voice_state(channel=channel,self_mute = False,self_deaf=True)
            voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    y_link = 'https://www.youtube.com/results?search_query='
    query_string = urllib.parse.urlencode({'search_query': url})
    htm_content = urllib.request.urlopen(y_link + query_string)
    link = y_link + url.replace(' ', '+')
    search_results = re.findall(
        r"watch\?v=(\S{11})", htm_content.read().decode())
    top_result = 'http://www.youtube.com/watch?v=' + search_results[0]

    valid_url = validators.url(url)
    try:
        if not voice.is_playing():
            if valid_url == True:
                try:
                    queue.append(url)
                    music_url = url
                    await ctx.send(f'**{Emoji.main} Searching for {Emoji.search}**'+f'`{url}`')
                    player(ctx, voice)
                    embed=discord.Embed(title=music_title, url=music_url, description='> Now playing', color = Color.main)
                    embed.set_footer(text=f'Requested by {ctx.message.author}')
                    embed.set_image(url=music_thumbnail)
                    await ctx.send(embed=embed)
                except ExtractorError:
                    await error_embed(ctx, 'Invalid URL')
                except DownloadError:
                    await error_embed(ctx, 'Invalid URL')
            else:
                queue.append(top_result)
                music_url = top_result
                await ctx.send(f'**{Emoji.music} Searching for {Emoji.search}**'+f'`{url}`')
                player(ctx, voice)
               
                embed=discord.Embed(title=music_title, url=music_url, description='> Now playing', color = Color.main)
                embed.set_footer(text=f'Requested by {ctx.message.author}')
                embed.set_image(url=music_thumbnail)
                await ctx.send(embed=embed)
        else:
            if valid_url == True:
                queue.append(url)
                await success_embed(ctx, 'Added to queue')
            else:
                queue.append(top_result)
                await success_embed(ctx, 'Added to queue')
    except AttributeError:
        await ctx.send('Joined a voice channel, please use the command again to play')

@client.command(name='nowplaying', aliases=['np'])
async def now(ctx):
    global music_title
    global music_url
    global music_thumbnail
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice:
        if voice.is_playing():
                    embed=discord.Embed(title=music_title, url=music_url, description='> Now playing', color = Color.main)
                    embed.set_footer(text=f'Requested by {ctx.message.author}')
                    embed.set_thumbnail(url=music_thumbnail)
                    await ctx.send(embed=embed)
        else:
            await error_embed(ctx , f'{ctx.author.name} Nothing is playing.')
    else:
        await error_embed(ctx, f'{client.user.name} is not connected to a voice channel')


@client.command(name='queue')
async def queue_display(ctx):
    global queue_list
    if len(queue) == 0:
        await error_embed(ctx, f'{ctx.author.name} No queue available')
    else:
        i = 0
        for x in queue:
            with YoutubeDL(YDL_OPTIONS) as ydl:
                info=ydl.extract_info(x, download=False)
            i = i + 1
            title = str(info.get('title'))
            queue_list = f'```\n{i}. {title}\n```'
            await ctx.send(embed = discord.Embed(title =f"{Emoji.music} Queue list" ,description = queue_list, color = Color.main))

@client.command(name='skip')
async def skip(ctx):
    global music_title
    global music_url
    global music_thumbnail
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        try:
            if repeat == 'yes':
                await success_embed(ctx, f'{ctx.author.name} Skipping')
                voice.pause()
                del queue[0]
                play_queue(ctx, voice)
                embed=discord.Embed(title=music_title, url=music_url, description='> Now playing', color = Color.main)
                embed.set_footer(text=f'Requested by {ctx.message.author}')
                embed.set_image(url=music_thumbnail)
                await ctx.send(embed=embed)
            elif repeat == 'none':
                await success_embed(ctx, f'{ctx.author.name} Skipping')
                voice.pause()
                # del queue[0]
                play_queue(ctx, voice)
                embed=discord.Embed(title=music_title, url=music_url, description='> Now playing', color = Color.main)
                embed.set_footer(text=f'Requested by {ctx.message.author}')
                embed.set_image(url=music_thumbnail)
                await ctx.send(embed=embed)
        except IndexError:
            await error_embed(ctx, f'{ctx.author.name} There is no songs in the queue.')
    else:
        await error_embed(ctx, f'{ctx.author.name} There is no music playing')

@client.command(name='loop')
async def loop(ctx):
    global repeat
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        if repeat == 'none':
            repeat = 'yes'
            await success_embed(ctx, f'{ctx.author.name} Loop is enabled')
        elif repeat == 'yes':
            repeat = 'none'
            await error_embed(ctx, f'{ctx.author.name} Loop is disabled')
    else:
        await error_embed(ctx, f'{ctx.author.name} There is no songs in the queue.')
            
@client.command(name='pause')
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
        await success_embed(ctx, f'{ctx.author.name} Music has been paused')
    else:
        await error_embed(ctx, f'{ctx.author.name} There is no songs in the queue.')


@client.command(name='resume')
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
        
        await success_embed(ctx, f'{ctx.author.name} Music has been resumed')
    else:
        await success_embed(ctx, f'{ctx.author.name} Music is not paused to resume it ._.')

@client.command(name='stop')
async def stop(ctx):
    global queue
    global queue_list
    global client_activity
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    queue.clear()
    queue_list = ''
    voice.stop()
    client_activity = 'Musicord'
    await success_embed(ctx, f'{ctx.author.name} Music has been stopped')

@client.command(name='leave', aliases=['disconnect'])
async def leave(ctx):
    global queue
    global queue_list
    global client_activity
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        queue.clear()
        queue_list = ''
        client_activity = 'Musicord'
        await voice.disconnect()
        await success_embed(ctx, f'{client.user.name} has been disconnected')
    else:
        await error_embed(ctx, f'{client.user.name} is not in a voice channel ')

@client.command(name='ping')
async def ping(ctx):

    await ctx.send(f'Pong! In {round(client.latency * 1000)}ms')


@client.command(name='invite')
async def invite(ctx):
    
    await success_embed(ctx, f'{ctx.author.name} Check your dm')
    await ctx.message.author.send('<:okay:1048368956819390565>Here is the invite link<:okay:1048368956819390565>. \n' + f'https://discord.com/api/oauth2/authorize?client_id={client.user.id}&permissions=8&scope=bot%20applications.commands')


client.run(TOKEN)
# COPYRIGHT #


# ------------------------------- #

#  This bot was made by amine or  #

#     AmineDev07 On github        #

# ------------------------------- #


# ------------------------------- #

#  This bot was made by amine or  #

#     AmineDev07 On github        #

# ------------------------------- #


# ------------------------------- #

#  This bot was made by amine or  #

#     AmineDev07 On github        #

# ------------------------------- #


# COPYRIGHT #

