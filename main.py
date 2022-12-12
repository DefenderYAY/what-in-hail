import discord, os, datetime, praw
import random
from discord.ui import Button, View
from discord.ext import commands, tasks
from datetime import timedelta
from dotenv import load_dotenv
from discord.commands import Option, slash_command
from discord.ext.commands import has_permissions, MissingPermissions
from discord import (
    CategoryChannel,
    Member,
    Permissions,
    default_permissions,
    TextChannel,
)
reddit = praw.Reddit(client_id='PMGzmvodaccvvPJYFr6HuQ',
                     client_secret='Mro22mnIZIJHqMwzZUqLjzMiyq5b6g',
                     username = "python_praw_yay",
                     password = "hLG4bdSrF9FYR4",
                     user_agent='windows:tImBQ5GiNd7n7OdAQ57N_g:1.0.0 by u/DefenderOP'
                     )
intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(
    command_prefix="d!", help_command=None, intents=intents
)
@bot.event
async def on_ready():
    print("Bot is ready")
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.playing, name="WHAT THE HAIL IS THAT LMAO"
        ),
        status=discord.Status.dnd,
    )


@bot.slash_command(description = "help Command")
async def help(ctx):
    em = discord.Embed(
        title="Commands",
        description="Help has arrived!",
        color=discord.Color.dark_orange())
    em.add_field(
        name = "Times out a member",
        value = "This command is only can only be used __**moderators**__ or people with the __**Moderate Members**__ permission ",
        inline = False,  
    )
    em.add_field(
        name = "Reddit Command",
        value = "This is a group of commands with meme submissions from r/memes, r/me_irl, r/programminghumor.",
        inline = False,
    )
    em.add_field(
        name = "Create Command",
        value = "Create: A Group of Commands which helps moderators create simple channels thru commands.",
        inline = False,
    )
    await ctx.respond(embed = em)
@bot.slash_command(description = "Times a person out!")
@default_permissions(moderate_members = True)
async def timeout(ctx, member: discord.Member, until, *,reason = None):
    await member.timeout_for(duration = timedelta(minutes=int(until)) ,reason = reason)  
    await ctx.respond(f"Timed out {member}!")

@bot.slash_command()
async def hi(ctx):
    await ctx.respond(f"Hello {ctx.author}!")


create = discord.SlashCommandGroup(
    "create", "Commands that can help moderators create channels automaticaly."
)


@create.command(description="Creates a text channel!")
@default_permissions(manage_channels=True)
async def channel(ctx, name):
    await ctx.respond(f"A Text channel with the name {name}!", ephemeral=True)
    await ctx.guild.create_text_channel(name=name)


@create.command(description="Creates a voice channel for you!")
@default_permissions(manage_channels=True)
async def vc(ctx, name):
    await ctx.respond(f"Created a vc with name: {name}", ephemeral=True)
    await ctx.guild.create_voice_channel(name=name)


@create.command(description="Creates a forum channel for you!")
@default_permissions(manage_channels=True)
async def forum(ctx, name):
    await ctx.respond(f"Created a forum channel with name: {name}", ephemeral=True)
    await ctx.guild.create_forum_channel(name=name)


@create.command(description="Creates a stage channel for you!")
@default_permissions(manage_channels=True)
async def stage(ctx, name):
    await ctx.respond(f"Created a stage channel with the name: {name}!", ephemeral=True)
    await ctx.guild.create_stage_chanel(name=name)

@create.command(description = "Creates a role for you!")
async def role(ctx,name):
    await ctx.respond(f"Created a role with the name: {name}!", ephemeral = True)
    await ctx.guild.create_role(name=name)

bot.add_application_command(create)

redditstuff = discord.SlashCommandGroup(
    "reddit", "Get memes from a few subreddits!"
)
@redditstuff.command(description = "Memes from r/memes")
async def memes(ctx):
    subreddit = reddit.subreddit("memes")
    all_subs = []
    hot = subreddit.hot(limit = 50)
    for submission in hot:
        all_subs.append(submission)
    random_sub = random.choice(all_subs)

    name = random_sub.title
    url = random_sub.url

    emb = discord.Embed(title = name)
    emb.set_image(url = url)

    await ctx.respond(embed = emb)

@redditstuff.command(description = "Memes from r/me_irl")
async def me_irl(ctx):
    subreddit = reddit.subreddit("me_irl")
    all_subs = []
    hot = subreddit.hot(limit = 100)
    for submission in hot:
        all_subs.append(submission)
    random_sub = random.choice(all_subs)

    name = random_sub.title
    url = random_sub.url

    emb = discord.Embed(title = name)
    emb.set_image(url = url)

    await ctx.respond(embed = emb)


@redditstuff.command(description = "PROGRAMMING HUMOR? NANI???!?!")
async def programmerhumor(ctx):
    subreddit = reddit.subreddit("ProgrammerHumor")
    all_subs = []
    hot = subreddit.hot(limit = 100)
    for submission in hot:
        all_subs.append(submission)
    random_sub = random.choice(all_subs)

    name = random_sub.title
    url = random_sub.url

    emb = discord.Embed(title = name)
    emb.set_image(url = url)

    await ctx.respond(embed = emb)

bot.add_application_command(redditstuff)

@bot.slash_command(description = "Thanking the dudes who basically carried me thru development")
async def credits(ctx):
    em = discord.Embed(title = "THANKS TO EVERYONE IN THIS LIST ILYSM <3", color = discord.Colour.blurple())
    em.add_field(
        name="Code With Swastik:",
        value="This man basically carried my bot development, go show him some love(he has actually gone on a hiatus until july of 2023 but shh): [YouTube](https://www.youtube.com/@CodeWithSwastik) [Tweeter](https://twitter.com/codewithswastik) [Discord](https://discord.com/invite/9WeA3Au4rQ)",
        inline=False,
    )
    await ctx.respond(embed = em)
load_dotenv(".env")
bot.run(os.getenv("token"))