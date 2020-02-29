from bs4 import BeautifulSoup
import bs4
import discord
import datetime
import asyncio
import requests
from urllib.request import urlopen, Request
import urllib

app = discord.Client()
token = open('c://token.txt', 'r').read()

@app.event
async def on_ready():
    print("Log in to next -> ", end = "")
    print(app.user.name, end = " : ")
    print(app.user.id)
    print("===============")


@app.event
async def on_message(message):

    if alreadyCustom(message.content) == 1:
        ab = runCustom(message.content).split('//')
        embed = discord.Embed(title = ab[1], color = 0x9966ff, timestamp = datetime.datetime.utcnow())
        embed.set_footer(text = "제노봇", icon_url = 'https://cdn.discordapp.com/avatars/682801427260768313/7b26360613f9844ccac4e1191210e107.png')
        embed.set_author(name = app.get_user(int(ab[2])).name + "님이 등록한 명령어입니다.", icon_url = app.get_user(int(ab[2])).avatar_url)
        await message.channel.send(embed = embed)

    if message.content.startswith("제노봇"):

        content = message.content[4:]


        #가입 없이 이용할 수 있는 서비스
        if content == "가입":
            if checkRegistered(message.author.id) == 1:
                embed = discord.Embed(title = "이미 가입되어 있습니다.", description = "XenoBot Beta.", color = 0x9966ff, timestamp = datetime.datetime.utcnow())
                embed.set_author(name = message.author.display_name, icon_url = message.author.avatar_url)
                embed.set_footer(text = "제노봇", icon_url = 'https://cdn.discordapp.com/avatars/682801427260768313/7b26360613f9844ccac4e1191210e107.png')
                await message.channel.send(embed = embed)
            else:
                embed = discord.Embed(title = "닉네임을 입력해 주세요.", description = "`취소`를 입력해 가입을 취소 할 수 있습니다.\n10초 동안 닉네임을 입력하지 않으면 자동으로 취소됩니다.", color = 0x9966ff, timestamp = datetime.datetime.utcnow())
                embed.set_footer(text = "제노봇", icon_url = 'https://cdn.discordapp.com/avatars/682801427260768313/7b26360613f9844ccac4e1191210e107.png')
                embed.set_author(name = message.author.display_name, icon_url = message.author.avatar_url)
                await message.channel.send(embed = embed)

                def check(m):
                    return m.channel == message.channel and m.author.id == message.author.id
                try:
                    msg = await app.wait_for('message', timeout = 10, check = check)
                except asyncio.TimeoutError:
                    embed = discord.Embed(title = "가입이 시간 초과로 자동 취소되었습니다.", color = 0x9966ff, timestamp = datetime.datetime.utcnow())
                    embed.set_footer(text = "제노봇", icon_url = 'https://cdn.discordapp.com/avatars/682801427260768313/7b26360613f9844ccac4e1191210e107.png')
                    embed.set_author(name = message.author.display_name, icon_url = message.author.avatar_url)
                    await message.channel.send(embed = embed)
                else:
                    if msg.content == "취소":
                        embed = discord.Embed(title = "정상적으로 취소되었습니다.", color = 0x9966ff, timestamp = datetime.datetime.utcnow())
                        embed.set_footer(text = "제노봇", icon_url = 'https://cdn.discordapp.com/avatars/682801427260768313/7b26360613f9844ccac4e1191210e107.png')
                        embed.set_author(name = message.author.display_name, icon_url = message.author.avatar_url)
                        await message.channel.send(embed = embed)
                    else:
                        register(msg.content.replace(" ", "_"), message.author.id)
                        embed = discord.Embed(title = "`" + msg.content + "`(으)로 가입되었습니다.", description = "`제노봇 탈퇴`로 탈퇴를 할 수 있습니다. 이왕이면 하지 말아 주세요:heart:\n`제노봇 닉변경`으로 닉네임을 변경 할 수 있습니다.", color = 0x9966ff, timestamp = datetime.datetime.utcnow())
                        embed.set_footer(text = "제노봇", icon_url = 'https://cdn.discordapp.com/avatars/682801427260768313/7b26360613f9844ccac4e1191210e107.png')
                        embed.set_author(name = message.author.display_name, icon_url = message.author.avatar_url)
                        await message.channel.send(embed = embed)

        elif content == "정보":
            embed = discord.Embed(title = " ", description = "XenoBot Beta.", color = 0x9966ff, timestamp = datetime.datetime.utcnow())
            embed.set_author(name = "제노봇 베타")
            embed.set_thumbnail(url = 'https://cdn.discordapp.com/avatars/682801427260768313/7b26360613f9844ccac4e1191210e107.png')
            embed.set_footer(text = "제노봇", icon_url = 'https://cdn.discordapp.com/avatars/682801427260768313/7b26360613f9844ccac4e1191210e107.png')
            await message.channel.send(embed = embed)

        else:
            if checkRegistered(message.author.id) == 1:


                #가입 후 이용할 수 있는 서비스
                if content == "닉변경":
                    embed = discord.Embed(title = "변경될 닉네임을 입력해 주세요.", description = "`취소`를 입력해 닉네임 변경을 취소 할 수 있습니다.\n10초 동안 닉네임을 입력하지 않으면 자동으로 취소됩니다.", color = 0x9966ff, timestamp = datetime.datetime.utcnow())
                    embed.set_footer(text = "제노봇", icon_url = 'https://cdn.discordapp.com/avatars/682801427260768313/7b26360613f9844ccac4e1191210e107.png')
                    embed.set_author(name = message.author.display_name, icon_url = message.author.avatar_url)
                    await message.channel.send(embed = embed)

                    def check(m):
                        return m.channel == message.channel and m.author.id == message.author.id
                    try:
                        msg = await app.wait_for('message', timeout = 10, check = check)
                    except asyncio.TimeoutError:
                        embed = discord.Embed(title = "닉네임 변경이 시간 초과로 자동 취소되었습니다.", color = 0x9966ff, timestamp = datetime.datetime.utcnow())
                        embed.set_footer(text = "제노봇", icon_url = 'https://cdn.discordapp.com/avatars/682801427260768313/7b26360613f9844ccac4e1191210e107.png')
                        embed.set_author(name = message.author.display_name, icon_url = message.author.avatar_url)
                        await message.channel.send(embed = embed)
                    else:
                        if msg.content == "취소":
                            embed = discord.Embed(title = "정상적으로 취소되었습니다.", color = 0x9966ff, timestamp = datetime.datetime.utcnow())
                            embed.set_footer(text = "제노봇", icon_url = 'https://cdn.discordapp.com/avatars/682801427260768313/7b26360613f9844ccac4e1191210e107.png')
                            embed.set_author(name = message.author.display_name, icon_url = message.author.avatar_url)
                            await message.channel.send(embed = embed)
                        else:
                            changeNick(message.author.id, msg.content)
                            embed = discord.Embed(title = "닉네임이 `" + msg.content + "`(으)로 변경되었습니다.", color = 0x9966ff, timestamp = datetime.datetime.utcnow())
                            embed.set_footer(text = "제노봇", icon_url = 'https://cdn.discordapp.com/avatars/682801427260768313/7b26360613f9844ccac4e1191210e107.png')
                            embed.set_author(name = message.author.display_name, icon_url = message.author.avatar_url)
                            await message.channel.send(embed = embed)

                elif content == "탈퇴":
                    embed = discord.Embed(title = "탈퇴하는 이유를 입력해 주세요.", description = "`취소`를 입력해 탈퇴를 취소 할 수 있습니다.\n30초 동안 사유를 입력하지 않으면 자동으로 취소됩니다.", color = 0x9966ff, timestamp = datetime.datetime.utcnow())
                    embed.set_footer(text = "제노봇", icon_url = 'https://cdn.discordapp.com/avatars/682801427260768313/7b26360613f9844ccac4e1191210e107.png')
                    embed.set_author(name = message.author.display_name, icon_url = message.author.avatar_url)
                    await message.channel.send(embed = embed)

                    def check(m):
                        return m.channel == message.channel and m.author.id == message.author.id
                    try:
                        msg = await app.wait_for('message', timeout = 30, check = check)
                    except asyncio.TimeoutError:
                        embed = discord.Embed(title = "시간 초과로 자동 취소되었습니다.", color = 0x9966ff, timestamp = datetime.datetime.utcnow())
                        embed.set_footer(text = "제노봇", icon_url = 'https://cdn.discordapp.com/avatars/682801427260768313/7b26360613f9844ccac4e1191210e107.png')
                        embed.set_author(name = message.author.display_name, icon_url = message.author.avatar_url)
                        await message.channel.send(embed = embed)
                    else:
                        if msg.content == "취소":
                            embed = discord.Embed(title = "정상적으로 취소되었습니다.", color = 0x9966ff, timestamp = datetime.datetime.utcnow())
                            embed.set_footer(text = "제노봇", icon_url = 'https://cdn.discordapp.com/avatars/682801427260768313/7b26360613f9844ccac4e1191210e107.png')
                            embed.set_author(name = message.author.display_name, icon_url = message.author.avatar_url)
                            await message.channel.send(embed = embed)
                        else:
                            deleteaccount(message.author.id)
                            embed = discord.Embed(title = "정상적으로 탈퇴 되었습니다.", color = 0x9966ff, timestamp = datetime.datetime.utcnow())
                            embed.set_footer(text = "제노봇", icon_url = 'https://cdn.discordapp.com/avatars/682801427260768313/7b26360613f9844ccac4e1191210e107.png')
                            embed.set_author(name = message.author.display_name, icon_url = message.author.avatar_url)
                            await message.channel.send(embed = embed)

                elif content.startswith("날씨"):
                    try:
                        location = content[3:]
                        enc_location = urllib.parse.quote(location + '+날씨')
                        url = 'https://search.naver.com/search.naver?ie=UTF-8&sm=whl_hty&query='+ enc_location
                        req = Request(url)
                        page = urlopen(req)
                        html = page.read()
                        soup = bs4.BeautifulSoup(html,'html5lib')

                        spot, temp = soup.find('span', class_='btn_select').text, soup.find('span', class_='todaytemp').text
                        weat = soup.find('p', class_='cast_txt').text.split(',')[0]

                        embed = discord.Embed(title = spot, description = "현재 기온 : " + temp + "℃ | 현재 날씨 : " + weat,\
                            color = 0x9966ff, timestamp = datetime.datetime.utcnow())
                        embed.set_footer(text = "제노봇", icon_url = 'https://cdn.discordapp.com/avatars/682801427260768313/7b26360613f9844ccac4e1191210e107.png')
                        embed.set_author(name = message.author.display_name, icon_url = message.author.avatar_url)
                        await message.channel.send(embed = embed)

                    except:
                            embed = discord.Embed(title = "죄송하지만 그런 지역은 없습니다.", color = 0x9966ff, timestamp = datetime.datetime.utcnow())
                            embed.set_footer(text = "제노봇", icon_url = 'https://cdn.discordapp.com/avatars/682801427260768313/7b26360613f9844ccac4e1191210e107.png')
                            embed.set_author(name = message.author.display_name, icon_url = message.author.avatar_url)
                            await message.channel.send(embed = embed)

                elif content.startswith("공지"):
                    contents = content[3:].split('//')
                    if len(contents) == 2:
                        Server = open('ServerList.txt', 'r').read().split(' ')
                        for x in range(len(Server)):
                            a = app.get_channel(int(Server[x]))
                            embed = discord.Embed(title = contents[0], description = contents[1], color = 0x9966ff, timestamp = datetime.datetime.utcnow())
                            embed.set_footer(text = "제노봇", icon_url = 'https://cdn.discordapp.com/avatars/682801427260768313/7b26360613f9844ccac4e1191210e107.png')
                            embed.set_author(name = message.author.display_name, icon_url = message.author.avatar_url)
                            await a.send(embed = embed)
                    else:
                        embed = discord.Embed(title = "입력이 올바르지 않습니다.", description = "올바른 형태 : `제노봇 공지 <제목>//<내용>", color = 0x9966ff, timestamp = datetime.datetime.utcnow())
                        embed.set_footer(text = "제노봇", icon_url = 'https://cdn.discordapp.com/avatars/682801427260768313/7b26360613f9844ccac4e1191210e107.png')
                        embed.set_author(name = message.author.display_name, icon_url = message.author.avatar_url)
                        await message.channel.send(embed = embed)

                elif content.startswith("명령어추가"):
                    contents = content[6:].split('//')
                    if len(contents) == 2:
                        if alreadyCustom(contents[0]):
                            embed = discord.Embed(title = "이미 있는 명령어입니다.", color = 0x9966ff, timestamp = datetime.datetime.utcnow())
                            embed.set_footer(text = "제노봇", icon_url = 'https://cdn.discordapp.com/avatars/682801427260768313/7b26360613f9844ccac4e1191210e107.png')
                            embed.set_author(name = message.author.display_name, icon_url = message.author.avatar_url)
                            await message.channel.send(embed = embed)
                        else:
                            if contents[0] == contents[1]:
                                embed = discord.Embed(title = "명령어와 응답이 같아 명령어를 등록할 수 없습니다.", color = 0x9966ff, timestamp = datetime.datetime.utcnow())
                                embed.set_footer(text = "제노봇", icon_url = 'https://cdn.discordapp.com/avatars/682801427260768313/7b26360613f9844ccac4e1191210e107.png')
                                embed.set_author(name = message.author.display_name, icon_url = message.author.avatar_url)
                                await message.channel.send(embed = embed)
                            else:
                                addcommand(contents[0], contents[1], message.author.id)
                                embed = discord.Embed(title = "명령어를 등록하였습니다.", description = "`<명령어>`로 응답을 들을 수 있습니다.\n`제노봇 명령어삭제 <명령어>`로 명령어를 삭제할 수 있습니다.", color = 0x9966ff, timestamp = datetime.datetime.utcnow())
                                embed.set_footer(text = "제노봇", icon_url = 'https://cdn.discordapp.com/avatars/682801427260768313/7b26360613f9844ccac4e1191210e107.png')
                                embed.set_author(name = message.author.display_name, icon_url = message.author.avatar_url)
                                await message.channel.send(embed = embed)


                    else:
                        embed = discord.Embed(title = "입력이 올바르지 않습니다.", description = "올바른 형태 : `제노봇 명령어추가 <제목>//<내용>", color = 0x9966ff, timestamp = datetime.datetime.utcnow())
                        embed.set_footer(text = "제노봇", icon_url = 'https://cdn.discordapp.com/avatars/682801427260768313/7b26360613f9844ccac4e1191210e107.png')
                        embed.set_author(name = message.author.display_name, icon_url = message.author.avatar_url)
                        await message.channel.send(embed = embed)

                elif content.startswith("명령어삭제"):
                    if alreadyCustom(content[6:]):
                        if runCustom(content[6:]).split('//')[2] == str(message.author.id):
                            deleteCustom(content[6:])
                            embed = discord.Embed(title = "정상적으로 삭제되었습니다.", color = 0x9966ff, timestamp = datetime.datetime.utcnow())
                            embed.set_footer(text = "제노봇", icon_url = 'https://cdn.discordapp.com/avatars/682801427260768313/7b26360613f9844ccac4e1191210e107.png')
                            embed.set_author(name = message.author.display_name, icon_url = message.author.avatar_url)
                            await message.channel.send(embed = embed)
                        else:
                            embed = discord.Embed(title = "자신이 만든 명령어만 삭제할 수 있습니다.", color = 0x9966ff, timestamp = datetime.datetime.utcnow())
                            embed.set_footer(text = "제노봇", icon_url = 'https://cdn.discordapp.com/avatars/682801427260768313/7b26360613f9844ccac4e1191210e107.png')
                            embed.set_author(name = message.author.display_name, icon_url = message.author.avatar_url)
                            await message.channel.send(embed = embed)
                    else:
                        embed = discord.Embed(title = "없는 명령어는 삭제할 수 없습니다.", color = 0x9966ff, timestamp = datetime.datetime.utcnow())
                        embed.set_footer(text = "제노봇", icon_url = 'https://cdn.discordapp.com/avatars/682801427260768313/7b26360613f9844ccac4e1191210e107.png')
                        embed.set_author(name = message.author.display_name, icon_url = message.author.avatar_url)
                        await message.channel.send(embed = embed)

                elif content.startswith("메세지삭제"):
                    print(message.guild.get_member(682801427260768313).guild_permissions)

                    def is_me(m):
                        return True
                    deleted = await message.channel.purge(limit = int(content[6:]), check = is_me)
                    await message.channel.send('Deleted {} message(s)'.format(len(deleted)))



            else:
                embed = discord.Embed(title = "가입이 안 되어 있습니다.", description = "`제노봇 가입`으로 가입해 주세요.", color = 0x9966ff, timestamp = datetime.datetime.utcnow())
                embed.set_footer(text = "제노봇", icon_url = 'https://cdn.discordapp.com/avatars/682801427260768313/7b26360613f9844ccac4e1191210e107.png')
                embed.set_author(name = message.author.display_name, icon_url = message.author.avatar_url)
                await message.channel.send(embed = embed)



def checkRegistered(id):
    User = open('UserList.txt', 'r').read().split('\n')
    for x in range(len(User)):
        if User[x].split(' ')[0] == str(id):
            return 1
    return 0

def register(name, id):
    a = open('UserList.txt', 'r')
    User = a.read()
    a.close()
    b = open('UserList.txt', 'w')
    b.write(User + '\n' + str(id) + ' ' + name + ' 0')
    b.close()
    print("`" + app.get_user(id).name + "`(이)가 가입했습니다.")

def changeNick(id, name):
    User = open('UserList.txt', 'r').read().split('\n')
    coin = 0
    for x in range(len(User)):
        if User[x].split(' ')[0] == str(id):
            coin = User[x].split(' ')[2]
            break
    strs = ""
    for x in range(len(User)):
        if User[x].split(' ')[0] == str(id):
            strs += str(id) + ' ' + name + ' ' + coin
        else:
            strs += User[x]
        if x < len(User) - 1:
            strs += '\n'
    a = open('UserList.txt', 'w')
    a.write(strs)
    a.close()

def deleteaccount(id):
    User = open('UserList.txt', 'r').read().split('\n')
    strs = ""
    for x in range(len(User)):
        if User[x].split(' ')[0] != str(id):
            strs += User[x]
        if 0 < x < len(User) - 2:
            strs += '\n'
    a = open('UserList.txt', 'w')
    a.write(strs)
    a.close()
    print("`" + app.get_user(id).name + "`(이)가 탈퇴했습니다.")

def alreadyCustom(name):
    Custom = open('CustomList.txt', 'r').read().split('\n')
    for x in range(len(Custom)):
        if Custom[x].split('//')[0] == name:
            return 1
    return 0

def runCustom(name):
    Custom = open('CustomList.txt', 'r').read().split('\n')
    for x in range(len(Custom)):
        if Custom[x].split('//')[0] == name:
            return Custom[x]

def addcommand(ques, ans, id):
    Custom = open('CustomList.txt', 'r').read()
    open('CustomList.txt', 'w').write(Custom + '\n' + ques + '//' + ans + '//' + str(id))

def deleteCustom(ques):
    Custom = open('CustomList.txt', 'r').read().split('\n')
    strs = ""
    for x in range(len(Custom)):
        if Custom[x].split('//')[0] != ques:
            strs += Custom[x]
        if 0 < x < len(Custom) - 2:
            strs += '\n'
    open('CustomList.txt', 'w').write(strs)

app.run(token)