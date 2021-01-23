import random
import requests
import discord
import asyncio
from bs4 import BeautifulSoup
from urllib.request import urlretrieve

client = discord.Client()

token = "your token"
@client.event
async def on_ready():
    print("=========================")
    print("다음으로 로그인 합니다 : ")
    print(client.user.name)
    print("connection was successful")
    game = discord.Game("궁금하다면? $사용법")
    print("=========================")
    await client.change_presence(status=discord.Status.online, activity=game)

@client.event
async def on_message(message):
    if message.content.startswith("$사용법"):
        embed = discord.Embed(title="숫자야구 봇 사용방법", description="숫자야구 봇으로 활용할 수 있는 명령어 목록입니다", color=0xd5d5d5)
        embed.add_field(name="$초기화",value="숫자야구 봇이 처음 구동됐을 때 사용합니다" ,inline=False)
        embed.add_field(name="$시작",value="게임을 시작할 때 사용합니다" ,inline=False)
        embed.add_field(name="$정답",value="게임 도중 정답을 외칠 때 사용합니다 ex)$정답 1234" ,inline=False)
        await message.channel.send(embed=embed)

    if message.content.startswith("$초기화"):
        global Number
        global Number_list
        global tries
        Number = "0"
        Number_list = []
        tries = 0
        await message.channel.send("초기화 완료, 게임을 시작해주세요.")
    else:
        if message.content.startswith('$시작'):

            if Number == "0":

                Number_list.append(random.randrange(1, 10))
                while True:
                    a = random.randrange(0, 10)
                    if len(Number_list) == 4:
                        break
                    elif a in Number_list:
                        continue
                    else:
                        Number_list.append(a)
                Number = str(Number_list[0]) + str(Number_list[1]) + str(Number_list[2]) + str(Number_list[3])
                print(Number_list)
                embed = discord.Embed(title="", description="", color=0xd5d5d5)
                embed.add_field(name="숫자가 세팅되었습니다",value="이제 게임을 진행해 주세요" ,inline=True)

                await message.channel.send(embed=embed)

            else:
                await message.channel.send("게임이 진행중입니다.")

        if message.content.startswith('$정답'):
            if Number == "0":
                await message.channel.send("세팅을 먼저 진행해 주세요")
            else:
                Score = message.content[4:len(message.content)]
                if len(Score) == 4:
                    Strike = 0
                    Ball = 0
                    Index = [] #Strike, Ball index list
                    for i in range(0, 4):
                        if Score[i] == Number[i]: #Strike
                            Strike += 1
                            Index.append(i)
                    tries += 1
                    if len(Index) == 4:
                        embed = discord.Embed(title="", description="", color=0xd5d5d5)
                        embed.add_field(name="정답입니다!",value=str(tries)+"시도 만에 성공하였습니다" ,inline=False)
                        embed.add_field(name="초기화가 완료되었습니다",value="다시시작 하려면 $시작" ,inline=False)
                        await message.channel.send(embed=embed)
                        Number = "0"
                        Number_list = []
                        tries = 0

                    else: #Here is Ball Algorithm
                        for i in range(0, 4):
                            if i not in Index:
                                print(i)
                                if int(Score[i]) in Number_list:
                                    Ball += 1
                        await message.channel.send(str(Strike)+"S "+str(Ball)+"B")
                else:
                    embed = discord.Embed(title="", description="", color=0xd5d5d5)
                    embed.add_field(name="오류가 발생했습니다",value="정답은 4자리 수로 적어주세요" ,inline=False)
                    await message.channel.send(embed=embed)


client.run(token)
