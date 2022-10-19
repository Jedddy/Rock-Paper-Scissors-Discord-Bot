import aiosqlite
import discord

async def add_to_db(server_id: int, server_name: str) -> None:
    async with aiosqlite.connect("bot/database/leaderboards.db") as db:
       async with db.execute("SELECT * FROM servers") as guild_list:
        if (server_id, server_name) not in await guild_list.fetchall():
            await db.execute("INSERT INTO servers VALUES (?, ?);", (server_id, server_name))
            await db.commit()
        
async def add_wins(user_id: discord.Member, user: discord.Member, server_id: discord.Guild) -> None:
    async with aiosqlite.connect("bot/database/leaderboards.db") as db:
        async with db.execute("SELECT discord_id, discord_username, server_id FROM server_leaderboards") as leaderboards:
            if (user_id, user, server_id) not in await leaderboards.fetchall():
                await db.execute("INSERT INTO server_leaderboards(discord_id, discord_username, server_id, wins) VALUES (?, ?, ?, ?);", (user_id, user, server_id, 1))
                await db.commit()
            else:
                await db.execute("UPDATE server_leaderboards SET wins = wins + 1 WHERE discord_id = ? AND server_id = ? ;", (user_id, server_id))
                await db.commit()

async def check_leaderboards(server_id: discord.Guild) -> None:
    async with aiosqlite.connect("bot/database/leaderboards.db") as db:
        async with db.execute("SELECT discord_username, wins FROM server_leaderboards WHERE server_id = ? ORDER BY wins DESC LIMIT 10"
        , (server_id,)) as leaderboards:
            players = await leaderboards.fetchall()
            if not players:
                return None
            else:
                return players
  