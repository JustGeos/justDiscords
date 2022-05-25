import discord
import asyncio
import random
from itertools import cycle
from discord.ext import commands
intents = discord.Intents.all()
client = commands.Bot(command_prefix = '.', intents=intents)
client.remove_command("help")

#displays bot is ready in terminal when bot becomes active
@client.event
async def on_ready():
    print('bot is ready')

status = ['Dead by Daylight',  
            'Overwatch', 
            'Lego Harry Potter', 
            'etc...'
            ]
#Displays "playing" and name of a different game randomized from the status array
async def change_status():
    await client.wait_until_ready()
    
    while client.is_closed:
        current_status = random.choice(status)
        await client.change_presence(activity=discord.Game(name=current_status))
        await asyncio.sleep(60*150)

#create a help command to tell users what the bot does (you can change the color to whatever you like by changing where it says gold)
@client.group(invoke_without_command=True)
async def help(ctx):
    em = discord.Embed(title = "Help", description = "List of .commands that you can use", color = ctx.author.color.gold())
    em.add_field(name = "name of command", value = 'What the command does')
    await ctx.send(embed = em)

#things to happen when a member joins the server
@client.event
async def on_member_join(member):
    #change the name to what your welcome channel is named (where the weclome message will be sent)
    channel = discord.utils.get(member.guild.text_channels, name="👋│welcome")
    #member.send will send a DM to the users inbox for a personal welcome
    await member.send("Welcome to ther server. If you want a list of commands you can send me to use in the server or in our DMs just reply with '.help'")
    #channel.send will send the message to the welcome channel to welcome the member
    await channel.send(f"Hey {member.mention}, Welcome to Marx's Lemonade Stand! Grab a cup and go make some friends!")
    await channel.send(f"Also, if you'd like to add your pronouns head over to the pronouns channel and just type '.pronouns (your pronouns)' and it will be updated for you!")

#this command will change the members nickname to add their pronouns to the end
#ex: .pronouns he/him
#Nickname was changed for MemberName (he/him)
@client.command(pass_context=True)
async def pronouns(ctx, nick):
    member = ctx.message.author
    name = member.display_name
    arr = name.split()
    name = arr[0]
    await member.edit(nick= name + ' (' + nick + ')')
    await ctx.send(f'Nickname was changed for {member.mention} ')

#for sending a saying when a user invokes a command
@client.command(pass_contect=True)
async def saying(ctx):
    await ctx.send("This is what it is going to send")

#to send a gif or other image
@client.command(pass_contect=True)
async def gifname(ctx):
    await ctx.send(file=discord.File('location of image file.gif'))

#can be used to moderate or respond when a member types a word in their message
@client.event
async def on_message(message):
    msg = message.content
    msg = msg.lower()
    if 'word' in msg:
        await message.channel.send("Please don't say that word")
    await client.process_commands(message)

client.loop.create_task(change_status())
client.run('run code')