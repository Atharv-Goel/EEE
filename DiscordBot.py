import discord
from discord import app_commands
import os
import asyncio

import keep_alive

allowed = {"e", "え", "エ", "一"}
with open("channels.txt") as file:
    channels = file.read().split("\n")
with open("reacts.txt") as file:
    reacts = file.read().split("\n")

def check(msg):
    return len(msg) and msg - allowed == set()

client = discord.Client(intents = discord.Intents.all())
tree = app_commands.CommandTree(client)

@tree.command(name = "eenable", description = "Toggles EEE bot responses on and off in this channel")
async def commandEenable(interaction):
    id = str(interaction.channel_id)
    if interaction.user.guild_permissions.administrator:
        if id not in channels:
            channels.append(id)
            with open("channels.txt", "w") as file:
                file.write("\n".join(channels))
            await interaction.response.send_message("EEE bot responses turned on")
        else:
            channels.remove(id)
            with open("channels.txt", "w") as file:
                file.write("\n".join(channels))
            await interaction.response.send_message("EEE bot responses turned off")
    else:
        await interaction.response.send_message("You need admin permissions for this command")

@tree.command(name = "reeact", description = "Toggles EEE bot reactions on and off in this channel")
async def commandReeact(interaction):
    id = str(interaction.channel_id)
    if interaction.user.guild_permissions.administrator:
        if id not in reacts:
            reacts.append(id)
            with open("reacts.txt", "w") as file:
                file.write("\n".join(reacts))
            await interaction.response.send_message("EEE bot reactions turned on") 
        else:
            reacts.remove(id)
            with open("reacts.txt", "w") as file:
                file.write("\n".join(reacts))
            await interaction.response.send_message("EEE bot reactions turned off")
    else:
        await interaction.response.send_message("You need admin permissions for this command")

async def react(channel):
    if len(channel) == 0: return
    async for message in client.get_channel(int(channel)).history():
        for reaction in message.reactions:
            if reaction.me: return
        await message.add_reaction("🇪")
        await message.add_reaction("<:RushE:1012953390596247632>")
        await message.add_reaction("<:EEE:1012954135387197562>")

@client.event
async def on_ready():
    await tree.sync()
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    id = str(message.channel.id)
    msg = message.content
  
    msgletters = set( "".join( filter(str.isalpha, msg) ).lower() )

    if message.author != client.user and id in channels and check(msgletters):
        await message.channel.send(message.content)

    asyncio.gather(*[react(channel) for channel in reacts])

client.run(os.environ['TOKEN'])
