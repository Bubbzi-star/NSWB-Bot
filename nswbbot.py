import discord
from discord.ext import commands
import random

# Aktivera alla intents så boten ser meddelanden
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Kategorier
CATEGORIES = [
    "showjumping",
    "dressage",
    "crosscountry",
    "hunterjumper",
    "hunteundersaddle",
    "halter"
]

# Lagra deltagare per kategori
participants = {}
contest_active = False

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# Ping-kommandot för att testa att boten svarar
@bot.command()
async def ping(ctx):
    await ctx.send("pong!")

# Admin check – bara de med "Manage Server" kan starta/avsluta
def is_admin():
    async def predicate(ctx):
        return ctx.author.guild_permissions.manage_guild
    return commands.check(predicate)

# Starta tävling (admin only)
@bot.command()
@is_admin()
async def start(ctx):
    global participants, contest_active
    participants = {category: {} for category in CATEGORIES}
    contest_active = True
    await ctx.send(
        "🏁 The Show has started!\n\n"
        "Available categories:\n"
        "• Showjumping\n"
        "• Dressage\n"
        "• Cross Country\n"
        "• Hunter Jumper\n"
        "• Hunter Under Saddle\n"
        "• Halter\n\n"
        "Enter using: !enter CategoryName (attach your image)"
    )

# Deltagare skickar in hästbild i kategori
@bot.command()
async def enter(ctx, category: str):
    global contest_active

    if not contest_active:
        await ctx.send("❗ There is no active contest right now.")
        return

    category = category.lower().replace(" ", "")

    if category not in CATEGORIES:
        await ctx.send("❗ Invalid category.")
        return

    if len(ctx.message.attachments) == 0:
        await ctx.send("📸 You must attach an image of your horse!")
        return

    if ctx.author in participants[category]:
        await ctx.send("❗ You have already entered this category.")
        return

    participants[category][ctx.author] = ctx.message.attachments[0].url
    await ctx.send(f"✅ {ctx.author.mention} entered {category.title()}!")

# Avsluta tävling och slumpa placeringar (admin only)
@bot.command()
@is_admin()
async def end(ctx):
    global contest_active

    if not contest_active:
        await ctx.send("❗ No active contest.")
        return

    contest_active = False

    for category, users in participants.items():
        if len(users) < 1:
            continue

        shuffled = list(users.keys())
        random.shuffle(shuffled)

        result_text = f"\n🏆 **{category.title()} Results** 🏆\n"

        for i, user in enumerate(shuffled):
            if i == 0:
                medal = "🥇"
            elif i == 1:
                medal = "🥈"
            elif i == 2:
                medal = "🥉"
            else:
                medal = "🏅"
            result_text += f"{medal} {user.mention}\n"

        await ctx.send(result_text)

# Sätt din token här:
bot.run("MTQ3NTI1OTE2MDEzMTE0MTc2Mw.GG8OZB.iyMuzVoaCcvZ8hBeYK6jNRauArgjnjmFclzy6c")
