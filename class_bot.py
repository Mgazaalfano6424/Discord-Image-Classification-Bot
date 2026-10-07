# test-bot (bot class)
# This example requires the 'members' and 'message_content' privileged intents to function.

import discord
import random
from discord.ext import commands
from bot_logic import gen_pass
import os
import requests
import math

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# command prefix
bot = commands.Bot(
    command_prefix='$',
    description=description,
    intents=intents
)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


# =========================
# KALKULATOR
# =========================

@bot.command()
async def add(ctx, left: int, right: int):
    await ctx.send(left + right)


@bot.command()
async def min(ctx, left: int, right: int):
    await ctx.send(left - right)


@bot.command()
async def times(ctx, left: int, right: int):
    await ctx.send(left * right)


@bot.command()
async def divide(ctx, left: int, right: int):
    if right == 0:
        await ctx.send("❌ Tidak bisa dibagi dengan 0.")
        return

    await ctx.send(left / right)


@bot.command()
async def exp(ctx, left: int, right: int):
    await ctx.send(left ** right)


@bot.command()
async def mod(ctx, left: int, right: int):
    if right == 0:
        await ctx.send("❌ Modulo dengan 0 tidak bisa dilakukan.")
        return

    await ctx.send(left % right)


@bot.command()
async def floor(ctx, number: float):
    await ctx.send(math.floor(number))


@bot.command()
async def ceil(ctx, number: float):
    await ctx.send(math.ceil(number))


# =========================
# MEME
# =========================

@bot.command()
async def mem(ctx):
    try:
        with open('images/mem1.jpg', 'rb') as f:
            picture = discord.File(f)

        await ctx.send(file=picture)

    except FileNotFoundError:
        await ctx.send("❌ File mem1.jpg tidak ditemukan.")


@bot.command()
async def meme(ctx):
    try:
        img_name = random.choice(os.listdir('images'))

        with open(f'images/{img_name}', 'rb') as f:
            picture = discord.File(f)

        await ctx.send(file=picture)

    except (FileNotFoundError, IndexError):
        await ctx.send("❌ Folder images tidak ditemukan atau kosong.")


# =========================
# DOG API
# =========================

def get_dog_image_url():
    url = 'https://random.dog/woof.json'
    res = requests.get(url, timeout=10)
    data = res.json()
    return data['url']


@bot.command()
async def dog(ctx):
    try:
        image_url = get_dog_image_url()
        await ctx.send(image_url)

    except Exception:
        await ctx.send("❌ Gagal mengambil gambar anjing.")


# =========================
# DUCK API
# =========================

def get_duck_image_url():
    url = 'https://random-d.uk/api/random'
    res = requests.get(url, timeout=10)
    data = res.json()
    return data['url']


@bot.command()
async def duck(ctx):
    try:
        image_url = get_duck_image_url()
        await ctx.send(image_url)

    except Exception:
        await ctx.send("❌ Gagal mengambil gambar bebek.")


# =========================
# TULIS / BACA FILE
# =========================

@bot.command()
async def tulis(ctx, *, my_string: str):
    with open('kalimat.txt', 'w', encoding='utf-8') as t:
        t.write(my_string)

    await ctx.send("✅ Kalimat berhasil ditulis.")


@bot.command()
async def tambahkan(ctx, *, my_string: str):
    with open('kalimat.txt', 'a', encoding='utf-8') as t:
        t.write("\n" + my_string)

    await ctx.send("✅ Kalimat berhasil ditambahkan.")


@bot.command()
async def baca(ctx):
    try:
        with open('kalimat.txt', 'r', encoding='utf-8') as t:
            document = t.read()

        if document:
            await ctx.send(document)
        else:
            await ctx.send("📄 File masih kosong.")

    except FileNotFoundError:
        await ctx.send("❌ File kalimat.txt belum dibuat.")


# =========================
# REPEAT
# =========================

@bot.command()
async def repeat(ctx, times: int, content='repeating...'):

    if times < 1:
        await ctx.send("❌ Jumlah pengulangan harus lebih dari 0.")
        return

    if times > 10:
        await ctx.send("❌ Maksimal 10 kali pengulangan.")
        return

    for i in range(times):
        await ctx.send(content)


# =========================
# PASSWORD GENERATOR
# =========================

@bot.command()
async def pw(ctx):
    await ctx.send(
        f'🔐 Kata sandi yang dihasilkan: {gen_pass(10)}'
    )


# =========================
# BYE
# =========================

@bot.command()
async def bye(ctx):
    await ctx.send('🙂')


# =========================
# COINFLIP
# =========================

@bot.command()
async def coinflip(ctx):

    num = random.randint(1, 2)

    if num == 1:
        await ctx.send('🪙 It is Head!')

    else:
        await ctx.send('🪙 It is Tail!')


# =========================
# DICE
# =========================

@bot.command()
async def dice(ctx):

    nums = random.randint(1, 6)

    await ctx.send(f'🎲 It is {nums}!')


# =========================
# WELCOME / JOINED
# =========================

@bot.command()
async def joined(ctx, member: discord.Member):
    await ctx.send(
        f'{member.name} joined '
        f'{discord.utils.format_dt(member.joined_at)}'
    )


# =========================
# LOCAL DRIVE
# =========================

@bot.command()
async def local_drive(ctx):

    try:
        folder_path = "./files"
        files = os.listdir(folder_path)

        if not files:
            await ctx.send("📁 Folder files masih kosong.")
            return

        file_list = "\n".join(files)

        await ctx.send(
            f"📁 **Files in the files folder:**\n{file_list}"
        )

    except FileNotFoundError:
        await ctx.send("❌ Folder not found.")


# =========================
# SHOW LOCAL FILE
# =========================

@bot.command()
async def showfile(ctx, filename):

    folder_path = "./files/"
    file_path = os.path.join(folder_path, filename)

    try:
        await ctx.send(file=discord.File(file_path))

    except FileNotFoundError:
        await ctx.send(
            f"❌ File '{filename}' not found."
        )


# =========================
# UPLOAD FILE
# =========================

@bot.command()
async def simpan(ctx):

    if ctx.message.attachments:

        for attachment in ctx.message.attachments:

            file_name = attachment.filename

            os.makedirs("./files", exist_ok=True)

            await attachment.save(
                f"./files/{file_name}"
            )

            await ctx.send(
                f"💾 Menyimpan {file_name}"
            )

    else:
        await ctx.send(
            "❌ Anda lupa mengunggah file :("
        )


# =========================
# HALAMAN RAHASIA
# =========================

@bot.command()
async def rahasia(ctx):

    secret = random.choice([
        "🎉 Kamu menemukan halaman rahasia!",
        "🪙 Koin rahasia muncul!",
        "👾 Halo agen rahasia!",
        "🚀 Selamat datang di markas tersembunyi!",
        "🔥 Kamu membuka mode rahasia!",
        "🎲 Angka keberuntunganmu hari ini: 7"
    ])

    await ctx.send(secret)


# =========================
# CUACA
# =========================

def get_weather(kota):

    API_KEY = "3def36e1a9189b8fc1334a8a963d1a16"

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": kota,
        "appid": API_KEY,
        "units": "metric",
        "lang": "id"
    }

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    data = response.json()

    if response.status_code != 200:
        return None

    return data


@bot.command()
async def cuaca(ctx, *, kota: str = "Bandung"):

    try:

        data = get_weather(kota)

        if data is None:
            await ctx.send(
                f"❌ Kota **{kota}** tidak ditemukan."
            )
            return

        nama_kota = data["name"]
        negara = data["sys"]["country"]

        suhu = data["main"]["temp"]
        terasa = data["main"]["feels_like"]
        kelembapan = data["main"]["humidity"]

        angin = data["wind"]["speed"]

        kondisi = data["weather"][0]["description"]

        await ctx.send(
            f"🌦️ **Cuaca {nama_kota}, {negara}**\n\n"
            f"🌡️ Suhu: **{suhu}°C**\n"
            f"🤔 Terasa seperti: **{terasa}°C**\n"
            f"💧 Kelembapan: **{kelembapan}%**\n"
            f"💨 Kecepatan angin: **{angin} m/s**\n"
            f"☁️ Kondisi: **{kondisi.capitalize()}**"
        )

    except requests.exceptions.RequestException:
        await ctx.send(
            "⚠️ Tidak bisa terhubung ke layanan cuaca."
        )

    except Exception as e:
        print(e)

        await ctx.send(
            "⚠️ Terjadi kesalahan saat mengambil data cuaca."
        )


# =========================
# MENJALANKAN BOT
# =========================

# GANTI dengan TOKEN DISCORD BARU KAMU
bot.run("MTQ4ODg3NTY1MTYyNzg3NjM5Mg.GoGqGB.MaI64syp_6Zr0efNq822CbssppGYrX2rxpl0fU")
