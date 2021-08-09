# i can probably turn this into a bot command hahaha that would be epic
def main():
    cogname = input("  The classes name: ")
    botname = input("  Your bot instance's name: ")
    cognametitle = cogname.title()

    code = f"""
import discord
import asyncio
from discord.ext import commands 


class {cognametitle}(commands.Cog):
    def __init__(self, {botname}):
        self.{botname} = {botname}
    

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{cognametitle} has been loaded.")
        
    
    
    
    
def setup({botname}):
    {botname}.add_cog({cognametitle}({botname}))"""

    with open(f"{cogname}.py", "w") as f:
        f.write(code)

    input(f"{cognametitle} has been successfully created.")

main()