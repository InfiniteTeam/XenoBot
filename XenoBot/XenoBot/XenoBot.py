import discord
import datetime
import asyncio
import time
import random
import json

with open('dict.json', 'r', encoding='utf-8') as jf:
    basedict = json.load(jf)

app = discord.Client()
token = basedict["token"]

information_commands = """
`ㅈ!내정보`, `ㅈ!서버정보`
"""
game_commands = """
`ㅈ!주사위`, `ㅈ!가위바위보`
"""
tool_commands = """
`ㅈ!메시지삭제`, `ㅈ!밴`, `ㅈ!밴해제`
"""
point_commands = """
`ㅈ!포인트`, `ㅈ!지갑`, `ㅈ!적립`
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

    if basedict["users"].get(str(message.author.id)) == None:
        basedict["users"][str(message.author.id)] = {}
        basedict["users"][str(message.author.id)]["money"] = 0
        basedict["users"][str(message.author.id)]["level"] = 0
        basedict["users"][str(message.author.id)]["xpcnt"] = 0
    basedict["users"][str(message.author.id)]["xpcnt"] += len(message.content)
    savejson()

    cont, auth, chan = message.content, message.author,message.channel

    if cont == "ㅈ!도움":
        embed = embedgen("도움말", "모든 명령어는 서버에서만 가능합니다.")
        embed.add_field(name = ":smiling_face_with_3_hearts: 봇 초대하기", value = "[[ 봇 데려가기 ]](https://discordapp.com/api/oauth2/authorize?client_id=682801427260768313&permissions=8&scope=bot)", inline = False)
        embed.add_field(name = ":information_source: 정보 명령어", value = information_commands, inline = False)
        embed.add_field(name = ":tools: 서버 관리 명령어", value = tool_commands, inline = False)
        embed.add_field(name = ":video_game: 놀이 명령어", value = game_commands, inline = False)
        embed.add_field(name = ":moneybag: 포인트 명령어", value = point_commands, inline = False)
        await chan.send(embed = embed)
        return

    if chan.type == discord.ChannelType.private:
        await chan.send(embed = embedgen("DM에서는 이용이 불가능합니다.", "[[ 봇 데려가기   (https://discordapp.com/api/oauth2/authorize?client_id=682801427260768313&permissions=8&scope=bot)"))
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
  
    if cont == "ㅈ!서버정보":
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

    if cont == "ㅈ!주사위":
        embed = embedgen("주사위를 굴리는 중...", "2초가 소요됩니다.")
        embed.set_image(url = "https://playentry.org/uploads/discuss/6m/i7/image/6mi7l2vak89sys2b000x2a3ce22ku3mr.gif")
        a = await chan.send(embed = embed)
        output = random.randint(0, 5)
        time.sleep(2)
        embed = embedgen(str(output + 1) + "(이)가 나왔습니다.", "")
        urls = ["https://playentry.org/uploads/discuss/qu/ns/image/qunsrb6kk89sys4i000x2a3ce23wc31l.png","https://playentry.org/uploads/discuss/nj/95/image/nj95xvufk89sys46000x2a3ce23ovow9.png",\
                "https://playentry.org/uploads/discuss/ai/ql/image/aiqlwx1jk89sys3u000x2a3ce23hm4z6.png","https://playentry.org/uploads/discuss/qv/o4/image/qvo4omd8k89sys3h000x2a3ce23ab3jc.png",\
                "https://playentry.org/uploads/discuss/12/yj/image/12yjx144k89sys32000x2a3ce2311z7z.png","https://playentry.org/uploads/discuss/u5/yh/image/u5yh4p7wk89sys2o000x2a3ce22sxeif.png"]
        embed.set_image(url = urls[output])
        await a.edit(embed = embed)

    if cont == "ㅈ!가위바위보":
        embed = embedgen("반응을 눌러보세요", "5초간 안 누를 시 게임이 종료됩니다")
        a = await chan.send(embed = embed)
        await a.add_reaction('✌️')
        await a.add_reaction('🖐️')
        await a.add_reaction('✊')
        def check(reaction, user):
            return (user == message.author) and (str(reaction.emoji) == '✌️' or str(reaction.emoji) == '🖐️' or str(reaction.emoji) == '✊')
        try:
            reaction, user = await app.wait_for('reaction_add', timeout=5, check=check)
        except asyncio.TimeoutError:
            embed = embedgen("당신은 졌습니다", "기권승")
            await a.delete()
            await chan.send(embed = embed)
        else:
            win = {'✌️':':fist:','🖐️':':v:','✊':':hand_splayed:'}
            embed = embedgen("당신은 " + str(reaction.emoji) + "(을)를 내서 졌습니다", "봇이 낸 건 " + win[str(reaction.emoji)] + "입니다!")
            await chan.send(embed = embed)
            await a.delete()

    if cont.startswith("ㅈ!메시지삭제"):
        if cont == "ㅈ!메시지삭제":
            embed = embedgen("올바른 사용법", "`ㅈ!메시지삭제 <수량>`")
            await chan.send(embed = embed)
        else:
            try:
                count = int(cont[8:])
            except:
                embed = embedgen("올바른 사용법", "`ㅈ!메시지삭제 <수량>`")
                await chan.send(embed = embed)
            else:
                def is_me(m):
                    return True
                try:
                    deleted = await chan.purge(limit = count + 1, check = is_me)
                except:
                    embed = embedgen("흠, 안되네요.", "봇에게 메시지 삭제 권한이 있는지 다시 확인해 주세요.")
                    await chan.send(embed = embed)
                else:
                    embed = embedgen(str(len(deleted) - 1) + "개의 메시지가 삭제되었습니다.", "이 메시지는 2초후 삭제됩니다.")
                    a = await chan.send(embed = embed)
                    time.sleep(2)
                    await a.delete()

    if cont.startswith("ㅈ!밴해제"):
        if cont == "ㅈ!밴해제":
            embed = embedgen("올바른 사용법", "`ㅈ!밴해제 <멘션>`")
            await chan.send(embed = embed)
        elif len(message.mentions) > 0:
            try:
                await guil.unban(message.mentions[0])
            except:
                embed = embedgen("흠, 안되네요.", "멤버가 밴이 아니거나 봇에게 멤버 밴 해제 권한이 있는지 다시 확인해 주세요.")
                await chan.send(embed = embed)
            else:
                embed = embedgen("밴 해제 되었습니다.", "")
                await chan.send(embed = embed)
        else:
            embed = embedgen("올바른 사용법", "`ㅈ!밴해제 <멘션>`")
            await chan.send(embed = embed)

    elif cont.startswith("ㅈ!밴"):
        if cont == "ㅈ!밴":
            embed = embedgen("올바른 사용법", "`ㅈ!밴 <멘션>`")
            await chan.send(embed = embed)
        elif len(message.mentions) > 0:
            try:
                await guil.get_member(auth.id).ban()
            except:
                embed = embedgen("흠, 안되네요.", "봇에게 멤버 밴 권한이 있는지 다시 확인해 주세요.")
                await chan.send(embed = embed)
            else:
                embed = embedgen("밴 되었습니다.", "")
                await chan.send(embed = embed)
        else:
            embed = embedgen("올바른 사용법", "`ㅈ!밴 <멘션>`")
            await chan.send(embed = embed)

    elif cont == "ㅈ!지갑":
        await chan.send(str(basedict['users'][str(auth.id)]['money']) + ":moneybag:")

    elif cont == "ㅈ!포인트":
        await chan.send(str(basedict['users'][str(auth.id)]['xpcnt']) + "포인트")
        
    elif cont == "ㅈ!적립":
        point = basedict['users'][str(auth.id)]['xpcnt']
        added = int(point / 10)
        basedict['users'][str(auth.id)]['money'] += added
        basedict['users'][str(auth.id)]['xpcnt'] = point - added * 10
        savejson()
        await chan.send(str(added) + ":moneybag:이(가) 적립되었습니다.")

def embedgen(title, desc):
  embed = discord.Embed(title = title, description = desc, timestamp = datetime.datetime.utcnow())
  embed.set_footer(text = "제노봇", icon_url = app.user.avatar_url)
  return embed

def savejson():
    global basedict
    with open('dict.json', 'w', encoding='utf-8') as d:
        json.dump(basedict, d, indent=4, sort_keys=True, ensure_ascii=False)

app.run(token)