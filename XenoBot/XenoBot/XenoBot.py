import discord
import datetime
import asyncio
import time
import random

app = discord.Client()
token = open('C://Users//이정형//Documents//Xenotoken.txt', 'r').read()

information_commands = """
`ㅈ!내정보`, `ㅈ!서버정보`
"""
game_commands = """
`ㅈ!주사위`
"""

@app.event
async def on_ready():
    print("Log in to next -> ", end = "")
    print(app.user.name)
    game = discord.Game("ㅈ!도움")
    await app.change_presence(status=discord.Status.online, activity=game)

@app.event
async def on_message(message):
    if message.author.id == 682801427260768313:
        return

    cont, auth, chan = message.content, message.author, message.channel

    if cont == "ㅈ!도움":
        embed = embedgen("도움말", "모든 명령어는 서버에서만 가능합니다.")
        embed.add_field(name = ":smiling_face_with_3_hearts: 봇 초대하기", value = "[[ 봇 데려가기 ]](https://discordapp.com/api/oauth2/authorize?client_id=682801427260768313&permissions=8&scope=bot)")
        embed.add_field(name = ":information_source: 정보 명령어", value = information_commands)
        embed.add_field(name = ":video_game: 게임 명령어", value = game_commands)
        await chan.send(embed = embed)
        return

    if chan.type == discord.ChannelType.private:
        await chan.send(embed = embedgen("DM에서는 이용이 불가능합니다.", "[[ 봇 데려가기 ]](https://discordapp.com/api/oauth2/authorize?client_id=682801427260768313&permissions=8&scope=bot)"))
        return

    guil = message.guild
    memb = app.get_guild(guil.id).get_member(auth.id)

    if cont == "ㅈ!내정보":
        #기본
        embed = embedgen(auth.display_name + "님의 정보", "")
        embed.set_thumbnail(url = auth.avatar_url)
        embed.add_field(name = "닉네임", value = auth.name, inline = True)
        embed.add_field(name = "서버 별명", value = auth.display_name, inline = True)
        embed.add_field(name = "클라이언트 아이디", value = str(auth.id), inline = True)
        #디코가입
        create_time = auth.created_at + datetime.timedelta(hours = 9)
        created = str(create_time.year) + '-' + str(create_time.month) + '-' + str(create_time.day) + ' | '
        created += str(create_time.hour) + ':' + str(create_time.minute) + ':' + str(create_time.second)
        embed.add_field(name = "디스코드 가입", value = created, inline = True)
        #서버참여
        join_time = memb.joined_at + datetime.timedelta(hours = 9)
        joined = str(join_time.year) + '-' + str(join_time.month) + '-' + str(join_time.day) + ' | '
        joined += str(join_time.hour) + ':' + str(join_time.minute) + ':' + str(join_time.second)
        embed.add_field(name = "서버 참여", value = joined, inline = True)
        status = memb.status
        #상태
        if status == discord.Status.online: stat = "온라인"
        elif status == discord.Status.offline: stat = "오프라인"
        elif status == discord.Status.idle: stat = "자리 비움"
        elif status == discord.Status.dnd: stat = "다른 용무 중"
        embed.add_field(name = "상태", value = stat, inline = True)
        await chan.send(embed = embed)
    
    elif cont == "ㅈ!서버정보":
        #기본
        embed = embedgen(guil.name + "의 정보", "")
        embed.set_thumbnail(url = guil.icon_url)
        embed.add_field(name = "서버 이름", value = guil.name, inline = True)
        embed.add_field(name = "클라이언트 아이디", value = str(guil.id), inline = True)
        embed.add_field(name = "멤버 수", value = str(len(guil.members)), inline = True)
        embed.add_field(name = "서버 소유자", value = guil.get_member(guil.owner_id).mention, inline = True)
        #잠수채널
        if guil.afk_channel == None: embed.add_field(name = "잠수 채널", value = "없음", inline = True)
        else: embed.add_field(name = "잠수 채널", value = guil.afk_channel.name, inline = True)
        #서버생성
        create_time = guil.created_at + datetime.timedelta(hours = 9)
        created = str(create_time.year) + '-' + str(create_time.month) + '-' + str(create_time.day) + ' | '
        created += str(create_time.hour) + ':' + str(create_time.minute) + ':' + str(create_time.second)
        embed.add_field(name = "서버 생성", value = created, inline = True)

        await chan.send(embed = embed)

    elif cont == "ㅈ!주사위":
        await chan.send(embed = embedgen(str(random.randint(1, 6))+"(이)가 나왔습니다.", ""))

def embedgen(title, desc):
    embed = discord.Embed(title = title, description = desc, timestamp = datetime.datetime.utcnow())
    embed.set_footer(text = "제노봇", icon_url = app.user.avatar_url)
    return embed

app.run(token)