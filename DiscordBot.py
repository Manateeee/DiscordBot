import asyncio
import time

import discord 
from discord import Member

client = discord.Client()

messages = 0
anzahlZüge = 0
feld = [['1','2','3'],['4','5','6'],['7','8','9']]

@client.event
async def on_ready():       #console text wenn gestartet und ready ist
    print("Hey dudes me is {}".format(client.user.name))
    client.loop.create_task(status_task())

async def update_stats():   #stats in stats.txt schreiben
    await client.wait_until_ready()
    global messages

    while not client.is_closed():
        try:
            with open("stats.txt", "a") as f:
                f.write(f"Time: {int(time.time())}, Messages: {messages}\n")

            messages = 0

            await asyncio.sleep(5)
        except Exception as e:
            print("Fehler beim reinschreiben in Datei: ", e)
            await asyncio.sleep(5)

async def status_task():    #status Leiste des bots ändern
    while True:
        await client.change_presence(activity=discord.Game("Mit dir"), status=discord.Status.online)
        await asyncio.sleep(5)
        await asyncio.sleep(5)
        await client.change_presence(activity=discord.Game("¤O¤ mit dir"), status=discord.Status.online)

@client.event
async def on_message(message):  #alle ifs bei unterschliedlichen commands 
    global feld
    global anzahlZüge
    global messages 
    messages += 1
    commands = ['!gayTester', '!userinfo', '!negerTester', '!TicTacTo']
    if message.author.bot:      
        return
    if '!INeedSomeHelp' in message.content:
        helpEmbed = discord.Embed(title='You need some help?',
                                  description='Here I give help:',
                                  color=0x22a7f0)
        helpEmbed.add_field(name='Commands:', value=commands, inline=True)
        await message.channel.send(embed=helpEmbed)
    if commands[0] in message.content: #gayTester
        member = discord.utils.get(message.guild.members, name="WhitePanda")
        if message.author == member:  
           await message.channel.send('you not gay')
        else:                                                                               
            messone = await message.channel.send('yes you gay')
            await messone.add_reaction('<:UGAY:642807039780716604>')
    if message.content.startswith(commands[1]): #userinfo                                                          
        args = message.content.split(' ')
        if len(args) == 2:
            member: Member = discord.utils.find(lambda m: args[1] in m.name, message.guild.members)
            if member:
                embed = discord.Embed(title='Userinfo für {}'.format(member.name),
                                      description='UserInfo von {}'.format(member.mention),
                                      color=0x22a7f0)
                embed.add_field(name='Server beigetreten', value=member.joined_at.strftime('%d/%m/%Y, %H:%M:%S'),
                                inline=True)
                rollen = ''
                for role in member.roles:
                    if not role.is_default():
                        rollen += '{} \r\n'.format(role.mention)
                if rollen:
                    embed.add_field(name='Rollen', value=rollen, inline=True)
                embed.set_thumbnail(url=member.avatar_url)
                embed.set_footer(text='_________________________.')
                await message.channel.send(embed=embed)
    if message.content.startswith(commands[2]): #!negerTester
        args = message.content.split(' ')
        if len(args) == 2:
            member: Member = discord.utils.find(lambda m: args[1] in m.name, message.guild.members)
            if member:
                await message.channel.send("yes {} is a neger".format(member.mention))
            else:
                await message.channel.send("yes you neger")
    if message.content.startswith(commands[3]): #!TicTacTo
        feld = [['1','2','3'],['4','5','6'],['7','8','9']]
        anzahlZüge = 0
        embed = discord.Embed(title="TicTacTo",color=0x22a7f0)
        embed.add_field(name="Neustart", value="Neustart")
        await message.channel.send(embed=embed)
    if message.content.startswith("!N"):
        args = message.content.split(' ')
        if len(args) == 2:
            if(Result(feld) == False):
                SpielfeldChange(feld, int(args[1]), anzahlZüge)
                anzahlZüge+=1
                embed = discord.Embed(title="TicTacTo",color=0x22a7f0)
                embed.add_field(name="Feld:",value=Spielfeld(feld))
                await message.channel.send(embed=embed)
                if(Result(feld) == True):
                    gewonnenMessage = await message.channel.send("Hast Gewonnen {0}".format(Spieler(anzahlZüge-1)))
                    await gewonnenMessage.add_reaction("<:GayAlex:642807888280027147>") 
                    await message.channel.send("zum Neustarten !TicTacTo schreiben")
                if(Unentschieden(feld) == True):
                    await message.channel.send("Unentschieden")
                    await message.channel.send("zum Neustarten !TicTacTo schreiben")                                                     

def Spielfeld(feld):
    spielfeld = ("{0} {1} {2} \n{3} {4} {5}\n{6} {7} {8}".format(feld[0][0],feld[0][1],feld[0][2],feld[1][0],feld[1][1],feld[1][2],feld[2][0],feld[2][1],feld[2][2]))
    return spielfeld

def SpielfeldChange(spielfeld, eingabefeld, anzahlZüge):
    raus = False
    printen = True
    for i in range(len(spielfeld)):
        if(raus == True):
            break
        for j in range(len(spielfeld[i])):
            eingabefeld-=1
            if(eingabefeld == 0):
                if(spielfeld[i][j] != 'X' and spielfeld[i][j] != 'O'):
                    spielfeld[i][j] = Spieler(anzahlZüge)
                    raus = True
                    break

def GleicheZeichen(eins, zwei, drei):
    alleGleich = False
    if(eins == 'X'):
        if(zwei == 'X'):
            if(drei == 'X'):
                alleGleich = True
    elif(eins == 'O'):
        if(zwei == 'O'):
            if(drei == 'O'):
                alleGleich = True
    return alleGleich    

def Unentschieden(feld):
    unentschieden = False
    belegt = 0
    for i in range(len(feld)):
        for j in range(len(feld[i])):
            if(feld[i][j] == 'X' or feld[i][j] == 'O'):
                belegt+=1
                if(belegt == 9):
                    unentschieden = True
    return unentschieden

def Result(feld):
    Gewonnen = False
    for i in range(3):
        if(GleicheZeichen(feld[i][0],feld[i][1],feld[i][2]) == True):
            Gewonnen = True
            break
        elif(GleicheZeichen(feld[0][i],feld[1][i],feld[2][i]) == True):
            Gewonnen = True
            break
    if(GleicheZeichen(feld[0][0],feld[1][1],feld[2][2]) == True):
        Gewonnen = True      
    elif(GleicheZeichen(feld[0][2],feld[1][1],feld[2][0]) == True):
        Gewonnen = True
    return Gewonnen

def Spieler(anzahlZüge):
    XO = 'X'
    if(anzahlZüge == 0 or anzahlZüge == 2 or anzahlZüge == 4 or anzahlZüge == 6 or anzahlZüge == 8):
        XO = 'X'    
    elif(anzahlZüge == 1 or anzahlZüge == 3 or anzahlZüge == 5 or anzahlZüge == 7 or anzahlZüge == 9):
        XO = 'O'
    return XO

client.loop.create_task(update_stats())
client.run("der token")

#https://discordapp.com/oauth2/authorize?permissions=271969383&scope=bot&client_id=678018272406405123