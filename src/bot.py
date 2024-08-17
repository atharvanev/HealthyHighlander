import discord
from discord.ext import commands
from menu_generator import get_items
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
API_KEY = os.getenv("GEMINI_KEY")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-001')

bot = commands.Bot(command_prefix="!", intents= discord.Intents.all())




def missingCal():
    embed = discord.Embed(title="please include the calorie count you want after ex: ```!meal 3000``` ", color= discord.Color.red())
    return embed

@bot.event
async def on_ready():
    print("Hello Healthy Highlander the bot is ready!!")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Healthy Highlander checking in with the Server!")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            title = "Invalid Command",
            description="Oops! That command doesn't exist. Here are some commands you can use:",
            color = discord.Color.red()
        )
        embed.add_field(name="!help", value="Show this help message", inline=False)
        embed.add_field(name="!meal <calories>", value="Generate a meal plan for the whole day based on the specified calorie count", inline=False)
        embed.add_field(name="!breakfast <calories>", value="Generate a meal plan for breakfast based on the specified calorie count", inline=False)
        embed.add_field(name="!lunch <calories>", value="Generate a meal plan for lunch based on the specified calorie count", inline=False)
        embed.add_field(name="!dinner <calories>", value="Generate a meal plan for dinner based on the specified calorie count", inline=False)
        await ctx.reply(embed=embed)
    elif isinstance(error, commands.CommandOnCooldown):
        remaining_time = round(error.retry_after, 2)  # Rounded to 2 decimal places
        await ctx.reply(f"You're on cooldown! Please try again after {remaining_time} seconds.")
    else:
        raise error  



@bot.command()
async def hello(ctx):
    await ctx.send("Hello!")

@bot.command()
async def menu(ctx):
    food = get_items() 
    date,breakfast, lunch, dinner = food  

    breakfast_str = ', '.join(breakfast)
    lunch_str = ', '.join(lunch)
    dinner_str = ', '.join(dinner)

    embed = discord.Embed(title=f"{date[0]} Today's Menu", color = discord.Color.blue())
    embed.add_field(name="Breakfast", value=breakfast_str if breakfast_str else "No items", inline=False)
    embed.add_field(name="Lunch", value=lunch_str if lunch_str else "No items", inline=False)
    embed.add_field(name="Dinner", value=dinner_str if dinner_str else "No items", inline=False)
    embed.set_footer(text="Healthy Highlander Bot")

    await ctx.send(embed=embed)

@bot.command()
async def meal(ctx,*,calcount:int = None):
    await ctx.typing()

    if calcount is None:
        await ctx.reply(embed=missingCal())
        return

    food = get_items()
    date,breakfast, lunch, dinner = food  

    breakfast_str = ', '.join(breakfast)
    lunch_str = ', '.join(lunch)
    dinner_str = ', '.join(dinner)


    meal_prompt = (
        f"Breakfast options: {breakfast_str}\n"
        f"Lunch options: {lunch_str}\n"
        f"Dinner options: {dinner_str}\n"
        f"Generate a meal plan with a total of {calcount} calories for the full day. "
        "It's okay to estimate and keep the length under 2000 characters, and include a serving count, keep snacks under 300 calories if included"
    )

    response = model.generate_content(meal_prompt)
    await ctx.reply(response.text+ "\n these are merely estimates please refer to ucr dining page for more accurate calorie counts")

@bot.command()
@commands.cooldown(rate=3, per=60, type=commands.BucketType.user)
async def breakfast(ctx,*,calcount:int = None):
    await ctx.typing()

    if calcount is None:
        await ctx.reply(embed=missingCal())
        return
    
    food = get_items()
    breakfast = food[1]  

    breakfast_str = ', '.join(breakfast)

    meal_prompt = (
        f"Breakfast options: {breakfast_str}\n"
        f"Generate a meal plan with a total of {calcount} calories for breakfast"
        "It's okay to estimate and keep the length under 2000 characters, and include a serving count, keep snacks under 300 calories if included and give the total caloire count at the end"
    )

    response = model.generate_content(meal_prompt)
    await ctx.reply(response.text+ "\n these are merely estimates please refer to ucr dining page for more accurate calorie counts")

@bot.command()
@commands.cooldown(rate=3, per=60, type=commands.BucketType.user)
async def lunch(ctx,*,calcount:int = None):
    await ctx.typing()

    if calcount is None:
        await ctx.reply(embed=missingCal())
        return

    food = get_items()
    lunch = food[2]  

    lunch_str = ', '.join(lunch)

    meal_prompt = (
        f"Breakfast options: {lunch_str}\n"
        f"Generate a meal plan with a total of {calcount} calories for lunch"
        "It's okay to estimate and keep the length under 2000 characters, and include a serving count, keep snacks under 300 calories if included and give the total caloire count at the end"
    )

    response = model.generate_content(meal_prompt)
    await ctx.reply(response.text+ "\n these are merely estimates please refer to ucr dining page for more accurate calorie counts")

@bot.command()
@commands.cooldown(rate=3, per=60, type=commands.BucketType.user)
async def dinner(ctx,*,calcount:int = None):
    await ctx.typing()

    if calcount is None:
        await ctx.reply(embed=missingCal())
        return

    food = get_items()
    dinner = food[3]  

    dinner_str = ', '.join(dinner)

    meal_prompt = (
        f"Breakfast options: {dinner_str}\n"
        f"Generate a meal plan with a total of {calcount} calories for dinner"
        "It's okay to estimate and keep the length under 2000 characters, and include a serving count, keep snacks under 300 calories if included and give the total caloire count at the end"
    )

    response = model.generate_content(meal_prompt)
    await ctx.reply(response.text+ "\n these are merely estimates please refer to ucr dining page for more accurate calorie counts")

bot.remove_command('help')

@bot.command()
async def help(ctx):

    embed = discord.Embed(title="Here are some possible commands", color= discord.Color.green())
    embed.add_field(name="!help", value="Show this help message", inline=False)
    embed.add_field(name="!meal <calories>", value="Generate a meal plan for the whole day based on the specified calorie count", inline=False)
    embed.add_field(name="!breakfast <calories>", value="Generate a meal plan for breakfast based on the specified calorie count", inline=False)
    embed.add_field(name="!lunch <calories>", value="Generate a meal plan for lunch based on the specified calorie count", inline=False)
    embed.add_field(name="!dinner <calories>", value="Generate a meal plan for dinner based on the specified calorie count", inline=False)

    await ctx.reply(embed=embed)



bot.run(BOT_TOKEN)