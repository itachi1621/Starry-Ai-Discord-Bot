import discord
from discord.ext import commands;
import aiohttp
import os
import dotenv
from discord import app_commands
import typing
import time
import re
import io
import random
import asyncio


intents = discord.Intents.default()
intents.message_content =True;
intents.members = True;
bot = commands.Bot(command_prefix='.',intents=intents)
client = discord.Client (intents=intents)

dotenv.load_dotenv();

TOKEN = os.getenv('DISCORD_BOT_TOKEN');
STAR_KEY=os.getenv('STARRY_AI_KEY')
PRIMARY_EMBED_COLOR = int(os.getenv("EMBED_COLOR"),16)
BOT_NAME=os.getenv('BOTNAME')
GENERATION_STEPS = os.getenv('GENERATION_STEPS')#im using 40 by default the app uses 50 40 should give good enough results
MAX_IMAGES = os.getenv('MAX_IMAGES')
VERSION="1.0.4"

smile = "\U0001F600"
frown = "\U0001F641"
heart = "🩷"
negative_prompt = """nudity,penis,clit,vagina,tits,dick,phallus,areola,cum,sperm,gore,
            naked,no clothes,testicles,nsfw,unclothed,butthole,asshole,prolapse,
            disembowelment,
            lowres, text, error, cropped, worst quality, low quality,
            jpeg artifacts, ugly, duplicate, morbid, mutilated,
            out of frame, extra fingers, mutated hands,
            poorly drawn hands, poorly drawn face, mutation,
            deformed, blurry, dehydrated, bad anatomy, bad proportions, extra limbs,
            cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs,
            extra arms, extra legs, fused fingers, too many fingers, long neck, username, watermark, signature
            """
friends = [
            "rosh007",
            "Persona Slates",
            "Switch",
            "thekwitt",
            "Ryno matic",
            "KawaiiWaifu",
            "Cthylla",
            "(Not) That Guy¹",
            "Manda"
        ]
friend_string = ""
for friend in friends:
    friend_string = friend_string + "\n" + friend + " " + heart

sizes = [
    "square",
    "landscape",
    "portrait",
    "wide"

]

#all; the good styles your welcome
art_styles = [
       # "hydra",
       # "fantasy",
       # "detailedIllustration",
       # "3dIllustration",
       # "flatIllustration",
        "realvisxl",
        "anime_2",
        "anime_stylized",
        #"anime_vintage",
        "pixelart",
        "luna_3d",

]

# not availbel yet..... cyberPunk""anime_3",
# too damn slow and low quality "animaginexl"
# Kinda not pretty mabee with more steps which more money which is more time .... "stylevisionxl",

#populating array with count values i.e 1,2... based on the max value set in max_images
image_numbers = []
for i in range (int(MAX_IMAGES)) :
    image_numbers.append(str(i+1))


art_styles.sort();

def remove_special_characters(string:str):
    allowed_characters = re.compile(r'[a-zA-Z0-9_\-\.]+') #regex to allow only alphanumeric characters and _ - . characters
    #its easier to find the allowed characters than to find the disallowed characters also i hate regex with a passion

    # Use the findall method to get a list of allowed character sequences
    allowed_parts = re.findall(allowed_characters, string)

    # Join the allowed parts to form the cleaned file name
    cleaned_string = ''.join(allowed_parts)
    return cleaned_string

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}');
    print('-----------')
    await bot.tree.sync()


@bot.tree.command(name="myfriends",description="These people inspired my creator to make me ")
async def myfriends(interaction:discord.Interaction):

    embed = discord.Embed(title="My Friends " + smile, color=PRIMARY_EMBED_COLOR)
    embed.add_field(name="This is my Name " + heart , value=BOT_NAME, inline=True)
    embed.add_field(name="Version", value=VERSION, inline=True)
    embed.add_field(name="Author", value="Scott/itachi/ZERO", inline=True)
    embed.add_field(name="Friends", value=friend_string, inline=False)
    embed.add_field(name="Thank you for helping to bring me into reality " + heart + heart + heart , value=BOT_NAME, inline=True)

    await interaction.response.send_message(embed=embed)

async def style_autocompletion(
        interaction:discord.Interaction,
        current: str
    ) -> typing.List[app_commands.Choice[str]]:
        data = []
        for style_choice in art_styles:
            data.append(app_commands.Choice(name=style_choice,value=style_choice))
        return data;

async def size_autocompletion(
        interaction:discord.Interaction,
        current: str
    ) -> typing.List[app_commands.Choice[str]]:
        data = []
        for size_choice in sizes:
            data.append(app_commands.Choice(name=size_choice,value=size_choice))
        return data;

async def number_of_images_autocompletion(
        interaction:discord.Interaction,
        current: str
    ) -> typing.List[app_commands.Choice[str]]:
        data = []
        for number_choice in image_numbers:
            data.append(app_commands.Choice(name=number_choice,value=number_choice))
        return data;



@bot.tree.command(name="create_pic", description="give me a prompt to generate art")
@app_commands.autocomplete(style=style_autocompletion, size=size_autocompletion, number_of_images=number_of_images_autocompletion)
async def create_pic(interaction: discord.Interaction, *, prompt: str, style: str, size: str = "square", number_of_images: str = "1"):
    await interaction.response.defer()
    try:
        if len(prompt) >= 256:
            title = prompt[:128] + "..."
        else:
            title = prompt

        image_urls = []
        headers = {
            'X-API-Key': STAR_KEY,
            'Content-Type': "application/json"
        }
        payload = {
            "model": style,
            "aspectRatio": size,
            "highResolution": False,
            "images": int(number_of_images),
            "steps": int(GENERATION_STEPS),
            "prompt": prompt,
            "initialImageMode": "color",
            "negativePrompt":negative_prompt
        }

        link = "https://api.starryai.com/creations/"
        async with aiohttp.ClientSession() as session:
            async with session.post(link, json=payload, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    job_id = data['id']
                    creation_pickup_link = f"https://api.starryai.com/creations/{job_id}"

                    await asyncio.sleep(5)

                    files = []
                    sleeptime = 5
                    for i in range(10):
                        sleeptime += i + 1
                        async with session.get(creation_pickup_link, headers=headers) as response:
                            if response.status == 200:
                                data = await response.json()
                                if data['status'] == "completed":
                                    image_urls = data['images']
                                    break
                                else:
                                    await asyncio.sleep(sleeptime)
                            else:
                                break

                    for url in image_urls:
                        image_url = url['url']
                        async with session.get(image_url) as resp:
                            if resp.status != 200:
                                return await interaction.followup.send('Could not get image...')
                            data = io.BytesIO(await resp.read())
                            title = remove_special_characters(title)
                            random_numb = random.randrange(1000, 4000)
                            file_name = str(int(time.time())) + str(random_numb) + "_" + title + ".png"
                            files.append(discord.File(data, filename=file_name))

                    embed = discord.Embed(title="Here is your image of: " + title, color=PRIMARY_EMBED_COLOR)
                    await interaction.followup.send(embed=embed, files=files)
                else:
                    embed = discord.Embed(title="There was an error generating the image", color=PRIMARY_EMBED_COLOR)
                    await interaction.followup.send("Could not get image")
                    return
    except Exception as e:
        embed = discord.Embed(title="There was an error generating the image", color=PRIMARY_EMBED_COLOR)
        print(e)
        await interaction.followup.send("Could not get image, try again later")
        return
#help
@bot.tree.command(name="help",description="commands etc")
async def create_pic(interaction:discord.Interaction):
    await interaction.response.defer()
    embed = discord.Embed(title="Commands", color=PRIMARY_EMBED_COLOR)
    embed.add_field(name="create_pic", value="Generates an image based on the prompt", inline=False)
    embed.add_field(name="help", value="Shows this message", inline=False)
    await interaction.followup.send(embed=embed)

#version

@bot.tree.command(name="version",description="Get"+ BOT_NAME +" bot version")
async def version(interaction:discord.Interaction):
    embed = discord.Embed(title="My Version Info :D ", color=PRIMARY_EMBED_COLOR)
    embed.add_field(name="This is my Name :) ", value=BOT_NAME, inline=True)
    embed.add_field(name="Version", value=VERSION, inline=True)
    embed.add_field(name="Author", value="Scott/itachi", inline=True)
    await interaction.response.send_message(embed=embed)









bot.run(TOKEN);
