import discord
from discord.ext import commands
import json 
from cmds.core import Cog_Extension
import os
from typing import Optional
from utils import (
    generate_puzzle_embed,
    process_message_as_guess,
    random_puzzle_id,
)
from info import(Todo,WORDLE,Number,System,Music)
todo_list = []
class Main(Cog_Extension):
        
    @commands.command()
    async def Hello(self, ctx):
        member = ctx.author.name
        await ctx.send(f"What's up, {member}!")

    @commands.command()
    async def Bye(self, ctx):
        member = ctx.author.name
        await ctx.send(f"See you next time, {member}!")
        
    @commands.command()
    async def wordle(self, ctx):
        embed = generate_puzzle_embed(ctx, random_puzzle_id())
        await ctx.send(embed=embed)

    
    @commands.command()
    async def add(self, ctx, *, task: str):
        todo_list.append(task)
        await ctx.send(f"Added task: {task}")

    @commands.command()
    async def remove(self, ctx, *, task: str):
        if task in todo_list:
            todo_list.remove(task)
            await ctx.send(f"Removed task: {task}")
        else:
            await ctx.send("Task not found in the todo list")

    @commands.command()
    async def clear(self, ctx):
        todo_list.clear()
        await ctx.send("Cleared all tasks")

    @commands.command()
    async def show(self, ctx, sort_by: str = None):
        sorted_todo_list = sorted(todo_list, key=lambda x: x.lower() if sort_by == "alphabetical" else todo_list.index(x))
        if sorted_todo_list:
            embed= discord.Embed(title="Todo list", color=discord.Color.blue())
            des = ""
            for i, task in enumerate(sorted_todo_list):
                des += f"{i+1}: {task}\n"
            embed.description = des
            await ctx.send(embed=embed)
        else:
            await ctx.send("Todo list is empty")


    @commands.command()
    async def info_wordle(self, ctx):
        embed = discord.Embed(title="WORDLE", color=discord.Colour.from_rgb(122, 196, 129))
        embed.set_footer(
        text="不知道要取什麼"
        )
        for key, value in WORDLE.items():
            embed.add_field(name=key, value=value, inline=False)
        await ctx.send(embed=embed)
    @commands.command()
    async def info_todo_list(self, ctx):
        embed = discord.Embed(title="Todo List", color=discord.Colour.from_rgb(122, 196, 129))
        embed.set_footer(
        text="不知道要取什麼"
        )
        for key, value in Todo.items():
            embed.add_field(name=key, value=value, inline=False)
        await ctx.send(embed=embed)
    @commands.command()
    async def info_number_bomb(self, ctx):
        embed = discord.Embed(title="Number Bomb", color=discord.Colour.from_rgb(122, 196, 129))
        embed.set_footer(
        text="不知道要取什麼"
        )
        for key, value in Number.items():
            embed.add_field(name=key, value=value, inline=False)
        await ctx.send(embed=embed)
    @commands.command()
    async def info_system_response(self, ctx):
        embed = discord.Embed(title="System Response", color=discord.Colour.from_rgb(122, 196, 129))
        embed.set_footer(
        text="不知道要取什麼"
        )
        for key, value in System.items():
            embed.add_field(name=key, value=value, inline=False)
        await ctx.send(embed=embed)
    @commands.command()
    async def info_music_bot(self, ctx):
        embed = discord.Embed(title="Music Bot", color=discord.Colour.from_rgb(122, 196, 129))
        embed.set_footer(
        text="不知道要取什麼"
        )
        for key, value in Music.items():
            embed.add_field(name=key, value=value, inline=False)
        await ctx.send(embed=embed)

    

async def setup(bot):
    await bot.add_cog(Main(bot))
