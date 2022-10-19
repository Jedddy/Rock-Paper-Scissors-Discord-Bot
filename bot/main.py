import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from database.db import add_to_db

load_dotenv("TOKEN.env")
token = os.getenv("TOKEN")  

class Client(commands.Bot):
    def __init__(self):
        self.synced = False
        super().__init__(
            command_prefix=".",
            intents=discord.Intents.all()
        )
    
    async def on_ready(self):
        await self.wait_until_ready()
        await self.change_presence(activity=discord.Game(name="/help"))
        print(f"{self.user} is Logged in.")
    
    async def setup_hook(self):
        for cog in os.listdir("bot/cogs"):
            if cog[-3:] == ".py":
                await self.load_extension(f"cogs.{cog[:-3]}")
        if not self.synced:
            await client.tree.sync()
            self.synced = True
    
    async def on_guild_join(self, guild: discord.Guild):
        await add_to_db(guild.id, guild.name)

client = Client()
client.run(token)

