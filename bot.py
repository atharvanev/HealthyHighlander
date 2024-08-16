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
model = genai.GenerativeModel('gemini-1.5-flash')

bot = commands.Bot(command_prefix="!", intents= discord.Intents.all())

@bot.event
async def on_ready():
    print("Hello Healthy Highlander the boy is ready!!")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Healthy Highlander checking in with the Server!")

@bot.command()
async def hello(ctx):
    await ctx.send("Hello!")

@bot.command()
async def menu(ctx):
    food = get_items()  # Get the food items
    date,breakfast, lunch, dinner = food  # Unpack the lists

    # Join the items in each list into a single string, separated by commas
    breakfast_str = ', '.join(breakfast)
    lunch_str = ', '.join(lunch)
    dinner_str = ', '.join(dinner)

    embed = discord.Embed(title=f"{date[0]} Today's Menu", color = discord.Color.blue())
    embed.add_field(name="Breakfast", value=breakfast_str if breakfast_str else "No items", inline=False)
    embed.add_field(name="Lunch", value=lunch_str if lunch_str else "No items", inline=False)
    embed.add_field(name="Dinner", value=dinner_str if dinner_str else "No items", inline=False)
    embed.set_footer(text="Healthy Highlander Bot")

    # Construct the response message
    # response = (
    #     f"**Today's Menu**\n\n"
    #     f"**Breakfast:** {breakfast_str}\n\n"
    #     f"**Lunch:** {lunch_str}\n\n"
    #     f"**Dinner:** {dinner_str}"
    # )
    await ctx.send(embed=embed)

@bot.command()
async def makemeal(ctx,*,calcount:int):
    
    response = model.generate_content(f"generate a meal of {calcount} calories for the full day and its okay to estimate make length less than 2000",
        generation_config = genai.GenerationConfig(
            max_output_tokens=1000,
        )
    )
    await ctx.reply(response.text)


bot.run(BOT_TOKEN)