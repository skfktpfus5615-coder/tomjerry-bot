import discord
from discord.ext import commands
import random
import json
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 데이터 파일
if not os.path.exists("data.json"):
    with open("data.json", "w") as f:
        json.dump({}, f)

def load_data():
    with open("data.json", "r") as f:
        return json.load(f)

def save_data(data):
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)

@bot.event
async def on_ready():
    print(f"{bot.user} 로그인 성공!")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    data = load_data()
    user = str(message.author.id)

    if user not in data:
        data[user] = {
            "money": 100,
            "xp": 0,
            "level": 0
        }

    data[user]["xp"] += random.randint(5, 10)

    xp = data[user]["xp"]
    level = data[user]["level"]

    if xp >= (level + 1) * 100:
        data[user]["xp"] = 0
        data[user]["level"] += 1
        level = data[user]["level"]

        level_roles = {
            0: "🧀 ꒰Lv.0꒱",
            10: "🧀 ꒰Lv.10꒱",
            20: "🧀 ꒰Lv.20꒱",
            30: "🧀 ꒰Lv.30꒱",
            40: "🧀 ꒰Lv.40꒱",
            50: "🧀 ꒰Lv.50꒱",
            60: "🧀 ꒰Lv.60꒱",
            70: "🧀 ꒰Lv.70꒱",
            80: "🧀 ꒰Lv.80꒱",
            90: "🧀 ꒰Lv.90꒱",
            100: "🧀 ꒰Lv.100꒱"
        }

        if level in level_roles:
            role_name = level_roles[level]
            role = discord.utils.get(message.guild.roles, name=role_name)

            if role:
                await message.author.add_roles(role)

        await message.channel.send(f"{message.author.mention} 레벨업! 현재 레벨 : {level}")

    save_data(data)

    await bot.process_commands(message)

@bot.command()
async def 치즈(ctx):
    data = load_data()
    user = str(ctx.author.id)

    cheese = data[user]["money"]
    await ctx.send(f"🧀 {ctx.author.mention} 치즈 : {cheese}")

@bot.command()
async def 도박(ctx, amount: int):
    data = load_data()
    user = str(ctx.author.id)

    if amount <= 0:
        await ctx.send("돈을 입력해!")
        return

    if data[user]["money"] < amount:
        await ctx.send("돈이 부족해!")
        return

    if random.randint(0, 1) == 1:
        data[user]["money"] += amount
        await ctx.send(f"🎉 성공! {amount} 획득!")
    else:
        data[user]["money"] -= amount
        await ctx.send(f"💀 실패! {amount} 잃음!")

    save_data(data)

@bot.command()
async def 랭킹(ctx):
    data = load_data()

    ranking = sorted(data.items(), key=lambda x: x[1]["money"], reverse=True)

    msg = "💰 돈 랭킹\n"

    for i, (user_id, info) in enumerate(ranking[:10], start=1):
        user = bot.get_user(int(user_id))
        name = user.name if user else "Unknown"
        msg += f"{i}. {name} - {info['money']}\n"

    await ctx.send(msg)

@bot.command()
async def 출석(ctx):
    data = load_data()
    user = str(ctx.author.id)

    import time
    now = int(time.time())

    if user not in data:
        data[user] = {
            "money": 100,
            "xp": 0,
            "level": 0,
            "last_daily": 0
        }

    if "last_daily" not in data[user]:
        data[user]["last_daily"] = 0

    if now - data[user]["last_daily"] < 86400:
        await ctx.send("⏰ 이미 출석했어! 내일 다시 와!")
        return

    reward = random.randint(50, 100)
    data[user]["money"] += reward
    data[user]["last_daily"] = now

    save_data(data)

    await ctx.send(f"🧀 {ctx.author.mention} 출석 완료! {reward} 치즈 획득!")


bot.run("MTQ4MTIxMDEwNzYwMDU3MjUxNg.GQzC6a.Bd-gn8R4G9TCAerD_PuSIKCNVSc-G7l4v_SUkE")