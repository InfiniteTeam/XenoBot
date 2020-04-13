import discord
import datetime, random, time
import json, sys, asyncio
#############################
app = discord.Client()
basedict = json.load(open('dict.json', 'r', encoding = 'utf-8'))
#############################
@app.event
async def on_ready():
    print("Login Successful")
    game = discord.Game("ㅈ!도움, %d서버, %d유저"%(len(app.guilds), len(app.users)))
    basedict["usingxenotool"].clear()
    savejson()
    await app.change_presence(status = discord.Status.online, activity = game)
#############################
@app.event
async def on_message(msg):
    cont, chan, auth = msg.content, msg.channel, msg.author
    #======!(----------------------[ ㄴ('o')ㄱ ]----------------------)!======#
    if chan.id in basedict["usingxenotool"]:
        return
    if auth.id == 682801427260768313:
        return
    if msg.channel.type == discord.ChannelType.group or msg.channel.type == discord.ChannelType.private:
        await chan.send(embed = get_error(5, auth))
        await chan.send(embed = get_embed("봇 데려가기", "[[여기를 누르세요]](https://discordapp.com/api/oauth2/authorize?client_id=682801427260768313&permissions=8&scope=bot)"))
        return
    #======!(----------------------[ ㄴ('o')ㄱ ]----------------------)!======#
    if cont in basedict["custom"]:
        embed = get_embed(random.choice(basedict["custom"][cont]), "")
        await chan.send(embed = embed)
    #======!(----------------------[ ㄴ('o')ㄱ ]----------------------)!======#
    if cont == "ㅈ!도움":
        embed = get_embed("도움말", "제노봇의 명령어 목록입니다.")
        embed.add_field(name = ":speech_balloon:커스텀명령어", value = basedict["commands"]["custom"])
        await chan.send(embed = embed)
    #======!(----------------------[ ㄴ('o')ㄱ ]----------------------)!======#
    if cont == "꺼져":
        if auth.id == 534145145109741569:
            embed = get_embed("봇을 종료합니다.", "")
            await chan.send(embed = embed)
            sys.exit(1)
        else:
            embed = get_error(1, auth)
            await chan.send(embed = embed)
    #======!(----------------------[ ㄴ('o')ㄱ ]----------------------)!======#
    if cont.startswith("ㅈ!공지"):
        if auth.id == 534145145109741569:
            channels = app.get_all_channels()
            fail = 0
            for channel in channels:
                if "공지" in channel.name:
                    try:
                        await channel.send(cont[5:])
                    except:
                        fail += 1
            embed = get_embed("공지 전송 완료", "")
            await chan.send(embed = embed)
        else:
            embed = get_error(1, auth)
            await chan.send(embed = embed)
    #======!(----------------------[ ㄴ('o')ㄱ ]----------------------)!======#
    if cont.startswith("ㅈ!eval"):
        if auth.id == 534145145109741569:
            embed = get_embed("Eval", str(eval(cont[7:])))
            await chan.send(embed = embed)
        else:
            embed = get_error(1, auth)
            await chan.send(embed = embed)
    #======!(----------------------[ ㄴ('o')ㄱ ]----------------------)!======#
    if cont.startswith("ㅈ!exec"):
        if auth.id == 534145145109741569:
            embed = get_embed("Exec", str(exec(cont[7:])))
            await chan.send(embed = embed)
        else:
            embed = get_error(1, auth)
            await chan.send(embed = embed)
    #======!(----------------------[ ㄴ('o')ㄱ ]----------------------)!======#
    if cont.startswith("ㅈ!커맨드추가"):
        subcont = cont[8:].split(';')
        if len(subcont) > 1:
            if subcont[0] in basedict["custom"]:
                embed = get_error(0, auth)
                await chan.send(embed = embed)
            elif subcont[0].startswith("ㅈ!"):
                embed = get_error(4, auth)
                await chan.send(embed = embed)
            elif "" in subcont[1:]:
                embed = get_error(3, auth)
                await chan.send(embed = embed)
            else:
                embed = get_embed("커맨드가 등록되었습니다.", "")
                await chan.send(embed = embed)
                basedict["custom"][subcont[0]] = subcont[1:]
                savejson()
        else:
            embed = get_error(2, auth)
            await chan.send(embed = embed)
    #======!(----------------------[ ㄴ('o')ㄱ ]----------------------)!======#
    if cont.startswith("ㅈ!제노툴"):
        def finishtool():
            basedict["usingxenotool"].remove(chan.id)
            savejson()
        basedict["usingxenotool"].append(chan.id)
        savejson()
        complete = ""
        embed = get_embed("완성된 코드", "```py\n" + complete + "```")
        completed = await chan.send(embed = embed)
        main = await chan.send(embed = get_embed("단계 1", "시작 트리거를 골라주세요.\n:one: 특정 단어\n:two: 특정 단어로 시작\n:three: 특정 단어로 끝남\n:four: 특정 단어를 포함"))
        await main.add_reaction('1️⃣')
        await main.add_reaction('2️⃣')
        await main.add_reaction('3️⃣')
        await main.add_reaction('4️⃣')
        def check(reaction, user):
            return user == auth
        try:
            reaction, user = await app.wait_for('reaction_add', timeout = 30.0, check = check)
        except asyncio.TimeoutError:
            await start.delete()
            finishtool()
            return
        # @(^o^)==@ @==(^o^)@
        else:
            savejson()
            if str(reaction.emoji) == '1️⃣':
                await main.clear_reactions()
                await main.edit(embed = get_embed("단계 1-1", "명령어를 입력하세요."))
                def check(m):
                    return m.author == auth and m.channel == chan
                inputs = await app.wait_for('message', check = check)
                complete += "if message.content==\"" + inputs.content.replace("\\", "\\\\").replace("\"", "\\\"") + "\":\n"
                await completed.edit(embed = get_embed("완성된 코드", "```py\n" + complete + "```"))
                await inputs.delete()
            if str(reaction.emoji) == '2️⃣':
                await main.clear_reactions()
                await main.edit(embed = get_embed("단계 1-1", "명령어의 시작 부분을 입력하세요."))
                def check(m):
                    return m.author == auth and m.channel == chan
                inputs = await app.wait_for('message', check = check)
                complete += "if message.content.startswith(\"" + inputs.content.replace("\\", "\\\\").replace("\"", "\\\"") + "\"):\n"
                await completed.edit(embed = get_embed("완성된 코드", "```py\n" + complete + "```"))
                await inputs.delete()
            if str(reaction.emoji) == '3️⃣':
                await main.clear_reactions()
                await main.edit(embed = get_embed("단계 1-1", "명령어의 끝 부분을 입력하세요."))
                def check(m):
                    return m.author == auth and m.channel == chan
                inputs = await app.wait_for('message', check = check)
                complete += "if message.content.endswith(\"" + inputs.content.replace("\\", "\\\\").replace("\"", "\\\"") + "\"):\n"
                await completed.edit(embed = get_embed("완성된 코드", "```py\n" + complete + "```"))
                await inputs.delete()
            if str(reaction.emoji) == '4️⃣':
                await main.clear_reactions()
                await main.edit(embed = get_embed("단계 1-1", "단어를 입력하세요."))
                def check(m):
                    return m.author == auth and m.channel == chan
                inputs = await app.wait_for('message', check = check)
                complete += "if \"" + inputs.content.replace("\\", "\\\\").replace("\"", "\\\"") + "\" in message.content:\n"
                await completed.edit(embed = get_embed("완성된 코드", "```py\n" + complete + "```"))
                await inputs.delete()
        # @(^o^)==@ @==(^o^)@
        await main.edit(embed = get_embed("단계 2", "이벤트를 골라주세요.\n" + basedict["event"]))
        await main.add_reaction('1️⃣')
        await main.add_reaction('2️⃣')
        while True:
            def check(reaction, user):
                return user == auth
            try:
                reaction, user = await app.wait_for('reaction_add', timeout = 30.0, check = check)
            except asyncio.TimeoutError:
                await main.delete()
                finishtool()
                return
            else:
                if str(reaction.emoji) == "1️⃣":
                    await main.delete()
                    finishtool()
                    return
                elif str(reaction.emoji) == "2️⃣":
                    await reaction.remove(auth)
                    real = await chan.send(embed = get_embed("단계 2-1\n", "메시지를 입력해 주세요."))
                    def check(m):
                        return m.author == auth and m.channel == chan
                    inputs = await app.wait_for('message', check = check)
                    complete += "    await message.channel.send(\"" + inputs.content.replace("\\", "\\\\").replace("\"", "\\\"") + "\")\n"
                    await completed.edit(embed = get_embed("완성된 코드", "```py\n" + complete + "```"))
                    await inputs.delete()
                    await real.delete()
        await main.delete()
        finishtool()
#############################
def get_embed(title, description):
    embed = discord.Embed(title = title, description = description, timestamp = datetime.datetime.utcnow())
    return embed
def get_error(error_id, auth):
    embed = get_embed("오류 발생!", "```등록된 오류 : " + basedict["error"][error_id] + "```")
    embed.add_field(name = "명령어를 제대로 입력하였는지 확인해 주세요.", value = "그래도 문제를 못 찾으셨다면 <@534145145109741569>에게 문의해 주세요.")
    embed.set_footer(text = auth.display_name, icon_url = auth.avatar_url)
    return embed
def savejson():
    global basedict
    with open('dict.json', 'w', encoding = 'utf-8') as d:
        json.dump(basedict, d, indent = 4, sort_keys = True, ensure_ascii = False)
#############################
print("==============")
app.run(basedict["token"])
