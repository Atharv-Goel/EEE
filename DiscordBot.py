import discord
import os

client = discord.Client(intents = discord.Intents.all())

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    msgletters = set( "".join( filter(str.isalpha, message.content) ).lower() )
    if msgletters == {"e"} and message.author != client.user:
        await message.channel.send(message.content)
    async for message in client.get_channel(1012230396852842536).history():
        for reaction in message.reactions:
            if reaction.me: return
        await message.add_reaction("🇪")
        await message.add_reaction("<:RushE:1012953390596247632>")
        await message.add_reaction("<:EEE:1012954135387197562>")

client.run(os.environ['TOKEN'])
