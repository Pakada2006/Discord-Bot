import discord
from python_settings import settings
from discord.ext import commands
import utils
import os
from cmds.core import Cog_Extension
import random
import asyncio

mini0 = 1
maxi0 = 100

class SimpleView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.on_game = False

    @discord.ui.button(label="離開遊戲", style=discord.ButtonStyle.success)
    async def leave(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.on_game = True
        await interaction.response.send_message("你已離開遊戲。請在聊天框中輸入任意數字查看答案", ephemeral=True)

class Event(Cog_Extension):
    

    @commands.Cog.listener()
    async def on_member_join(self, member):
        g_channel = self.bot.get_channel(int(os.getenv("general_channel")))
        if g_channel:   await g_channel.send(f"Welcome aboard, {member.mention}!")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        system_channel = member.guild.system_channel
        if system_channel:
            await system_channel.send(f"Goodbye {member.display_name}！இдஇ")

    @commands.command()
    async def setmax(self, ctx,ma):
        global maxi0
        maxi0=int(ma)
        print(maxi0)
        await ctx.send(f"已將最大值改為{ma}")

    @commands.command()
    async def setmini(self, ctx,mi):
        global mini0
        mini0=int(mi)
        await ctx.send(f"已將最小值改為{mi}")
        
    @commands.command()
    async def guess(self, ctx):

        global mini0, maxi0
        mini = mini0
        maxi = maxi0
        
        number_to_guess = random.randint(mini, maxi)

        def check(msg):
            return msg.author == ctx.author and msg.content.isdigit()

        attempts = 0
        
        view = SimpleView()

        message = await ctx.send(f"輸入一個 {mini} 到 {maxi} 之間的數字：", view=view)

        while True:
            try:
                guess = await self.bot.wait_for('message', check=check, timeout=30.0)
                guess_number = int(guess.content)
                attempts += 1

                if view.on_game:
                    await ctx.send(f"上輪遊戲答案為 {number_to_guess}")
                    break

                if guess_number < mini or guess_number > maxi:
                    await ctx.send(f"超出範圍，請輸入 {mini} 到 {maxi} 之間的數字！",view=view)
                elif guess_number == number_to_guess:
                    await ctx.send(f"恭喜你，你猜對了！答案是 {number_to_guess}。你一共猜了 {attempts} 次。")
                    break
                elif guess_number < number_to_guess:
                    mini = guess_number + 1
                    await ctx.send(f"猜的太小了！請輸入 {mini} 到 {maxi} 之間的數字！",view=view)
                else:
                    maxi = guess_number - 1
                    await ctx.send(f"猜的太大了！請輸入 {mini} 到 {maxi} 之間的數字！",view=view)


            except ValueError:
                await ctx.send(f"請輸入一個{mini} 到 {maxi} 之間的有效數字。",view=view)

            except asyncio.TimeoutError:
                await ctx.send("時間已經用完了，遊戲結束。")
                break

async def setup(bot):
    await bot.add_cog(Event(bot))
