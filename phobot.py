import discord
from discord.ext import commands
from googlesearch import search as gsearch
from bs4 import BeautifulSoup
import random
import smtplib
import ssl
from email.message import EmailMessage
import cassiopeia as cass
from cassiopeia import Summoner
from config import discord_token

TOKEN = discord_token

client = commands.Bot(command_prefix='!', intents=discord.Intents.all(), help_command=None)
client.remove_command('help')

@client.command()
async def help(ctx):
    embed = discord.Embed(
        title= 'Bot Commands',
        description='🍜List of all phobot commands🍜 *!(command name)*  \n-------------------------------------------------------------------',
        color= discord.Color.gold()
    )
    embed.set_thumbnail(url='https://media.istockphoto.com/id/1149007841/vector/mirror_drawing.jpg?s=612x612&w=0&k=20&c=EBYpUShnaivNjtEN5IWwhbabxCsf-R9xGjAcYIg5ILU=')

    embed.add_field(name="• !lol (Summoner Name)",value='Returns League of Legends Summoner Data',inline=False)
    embed.add_field(name="• !search (query)",value='Returns the first 10 google search results of a given query ',inline=False)
    embed.add_field(name="• !email (*email adress*) (email body) ",value='Phobot sends an email message to the given email adress',inline=False)
    embed.add_field(name="• !joke",value='Phobot cracks a joke!',inline=False)
    embed.add_field(name="• !roll / roll100",value='Rolls a random number from 0-10 or 0-100',inline=False)
    embed.add_field(name="• !ping",value='Returns bot latency (ms) ',inline=False)


    await ctx.send(embed=embed)

@client.command()
async def lol(ctx, user):
    cass.set_riot_api_key('RGAPI-512c0811-f29a-4ba4-aadb-0133a49f3cc9')
    usr = cass.Summoner(name=str(user), region='NA')

    name = usr.name

    region = usr.region

    good_with = usr.champion_masteries.filter(lambda cm: cm.level >=6) 
    masteries = [cm.champion.name for cm in good_with]

    level = usr.level

    rk = usr.ranks[cass.data.Queue.ranked_solo_fives]

    embed = discord.Embed(
        title= f'League of Legends data search for \"{user}\"',
        description= '-------------------------------------------------------------------'
    )
    embed.set_thumbnail(url= 'https://cdnb.artstation.com/p/assets/images/images/021/422/255/large/t-j-geisen-lol-icon-rendered-v001.jpg?1571640551')
    embed.add_field(name="• Summoner",value=str(user),inline=False)
    embed.add_field(name="• Region",value='NA',inline=False)
    embed.add_field(name="• Rank",value=str(rk),inline=False)
    embed.add_field(name="• Masteries",value= masteries,inline=False)
    embed.add_field(name="• Level",value=str(level),inline=False)

    await ctx.send(embed=embed)




@client.event
async def on_ready():
    print(f'{client.user} is now running!')

@client.command()
async def email(ctx, to, body):
    email_sender = 'phobot.discord@gmail.com'
    email_password = 'ydyodzvhhjiwcvmu'
    email_receiver = str(to)

    subject = 'Discord Bot Message'
    body = str(body)

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
    await ctx.send('Email Sent!')

@client.command()
async def search(ctx,search_msg):
    results = ''
    count = 1
    for URL in gsearch(search_msg,stop=10):
        results += f'\n \n {count})  {URL}'
        count += 1
        embed = discord.Embed( 
            color= discord.Color.from_rgb(255,255,255)
        )
    embed.set_thumbnail(url= 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSK5q0FP74VV9wbfwP378_7kj7iDomHuKrxkXsxDdUT28V9dlVMNUe-EMzaLwaFhneeuZI&usqp=CAU')
    await ctx.send(embed=embed)

@client.command()
async def ping(ctx):
    bot_latency = round(client.latency *1000)
    await ctx.send(f'🏓Pong! \nping: {bot_latency} (ms)')

@client.command()
async def joke(ctx):
    jokes = ['What do kids play when their mom is using the phone? Bored games.', 'What do you call an ant who fights crime? A vigilANTe!', 'What does a storm cloud wear under his raincoat? Thunderwear.', 'What is fast, loud and crunchy? A rocket chip.', 'How does the ocean say hi? It waves!', 'What do you call a couple of chimpanzees sharing an Amazon account? PRIME-mates.', 'Name the kind of tree you can hold in your hand? A palm tree!', 'What do birds give out on Halloween? Tweets.', 'What did one pickle say to the other? Dill with it.', 'Why is a football stadium always cold? It has lots of fans!', 'Why do ducks have feathers on their tails? To cover their buttquacks.', 'What kind of math do birds love? Owl-gebra!', 'Why can’t you ever tell a joke around glass? It could crack up.', 'How do you stop an astronaut’s baby from crying? You rocket.', 'What kind of shoes do frogs love? Open-toad!', 'What is a witch’s favorite subject in school? Spelling.', 'What’s brown and sticky? A stick.', 'What kind of nut doesn’t like money? Cash ew.', 'What has three letters and starts with gas? A car.', 'How does the moon cut his hair? Eclipse it.', 'What did the elf learn in school? The elf-abet.', 'Why are ghosts terrible liars? Because you can see right through them.', 'Why don’t oysters share? They’re shell-fish!', 'I went to buy some camo pants but couldn’t find any.', 'I was wondering why the frisbee kept getting bigger and bigger, but then it hit me.', 'Russian dolls are so full of themselves.', 'Build a man a fire and he’ll be warm for a day. Set a man on fire and he’ll be warm for the rest of his life.', 'People who take care of chickens are literally chicken tenders.', 'Blunt pencils are really pointless.', 'The man who invented Velcro has died. RIP.']
    await ctx.send(jokes[random.randint(0,30)])

@client.command(aliases = ['roll10', "r10"])
async def roll(ctx):
    await ctx.send(str(random.randint(0,10)))

@client.command()
async def roll100(ctx):
    await ctx.send(str(random.randint(0,100)))

@client.event
async def on_member_join(member):
    channel = client.get_channel(id=1059649114847055932) 
    await channel.send(f"Welcome to the server, {member.mention}!")

@client.event
async def on_member_leave(member):
    channel = client.get_channel(id=1059649114847055932) 
    print("Recognised that a member called " + member.name + " left")
    embed=discord.Embed(
        title="😢 Goodbye "+member.name+"!",
        color=discord.Color.red() 
    )
    await channel.send(embed)

client.run(TOKEN)