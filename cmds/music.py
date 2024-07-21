import discord
from discord.ext import commands
import os
from cmds.core import Cog_Extension
import requests
import re
import time

class Music(Cog_Extension):
    
    def __init__(self, bot):
        super().__init__(bot)
        self.playlist = []
        self.PlayList = {}
    
    def song_finished(self, ctx):
        if not self.playlist:
            return
        
        os.remove(self.PLAYLIST[0])
        self.PlayList.pop(str(self.playlist[0]))
        self.playlist = list(self.PlayList.keys())
        self.PLAYLIST = list(self.PlayList.values())
        if self.playlist:
            self.play_song(ctx)
    
            
    def play_song(self, ctx):
        if not self.playlist:
            return
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice is None:
            voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='一般')
            voiceChannel.connect(timeout = 600.0)
            voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice and not voice.is_playing() and self.playlist:
            voice.play(discord.FFmpegPCMAudio(executable = r".\ffmpeg-7.0.1-essentials_build\bin\ffmpeg.exe", source = self.PLAYLIST[0]), after=lambda e: self.song_finished(ctx))
            
    
    @commands.command()
    async def add_song(self, ctx, song_name):
        
        search=""
        query = song_name.replace(' ', '+')
        url = f"https://www.youtube.com/results?search_query={query}"
  
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
                
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            if response.text:
                match = re.search(r'/watch\?v=[^"]+', response.text)
                if match:
                    video_id = match.group(0)
                    video_url = f"https://www.youtube.com{video_id}"
                    search= video_url
                    
        output_path = "./songs/%(title)s.%(ext)s"
        os.system(f"yt-dlp.exe --extract-audio --audio-format mp3 --audio-quality 0 -o{output_path} {search}")
        
        files = [os.path.join("./songs", f) for f in os.listdir("./songs")]
        files = [f for f in files if os.path.isfile(f)]
        latest_file = max(files, key=os.path.getctime)
        self.PlayList[song_name] = latest_file

        self.playlist = list(self.PlayList.keys())
        self.PLAYLIST = list(self.PlayList.values())
        await ctx.send(f"{song_name} is added.")


    @commands.command()
    async def insert_song(self, ctx, position: int, song_name):
        if position == 1:
            await ctx.send("You cannot insert the song to the first one.")
        else:
            search = ""
            query = song_name.replace(' ', '+')
            url = f"https://www.youtube.com/results?search_query={query}"

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            response = requests.get(url, headers=headers)
            if response.status_code == 200 and response.text:
                match = re.search(r'/watch\?v=[^"]+', response.text)
                if match:
                    video_id = match.group(0)
                    video_url = f"https://www.youtube.com{video_id}"
                    search = video_url

            output_path = "./songs/%(title)s.%(ext)s"
            os.system(f"yt-dlp --extract-audio --audio-format mp3 --audio-quality 0 -o {output_path} {search}")

            files = [os.path.join("./songs", f) for f in os.listdir("./songs")]
            files = [f for f in files if os.path.isfile(f)]
            latest_file = max(files, key=os.path.getctime)

            self.playlist.insert(position - 1, song_name)
            self.PLAYLIST.insert(position - 1, latest_file)
            self.PlayList = {self.playlist[i]: self.PLAYLIST[i] for i in range(len(self.playlist))}
        
            await ctx.send(f"{song_name} is inserted in the {position} position.")

        
    @commands.command()
    async def play(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice is None:
            voice_channel = discord.utils.get(ctx.guild.voice_channels, name='一般')
            await voice_channel.connect(timeout=600.0)
            voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            await ctx.send("Wait for the current playing music to end or use the 'next_song' command")
        else:
            if len(self.playlist) == 0:
                await ctx.send("The playlist is empty.")
            else:
                self.play_song(ctx)
                await ctx.send(f"Now playing: {self.playlist[0]}")
                

    @commands.command()
    async def playlist(self, ctx):
        embed = discord.Embed(title="Playlist", colour=discord.Colour.from_rgb(190, 230, 131))
        embed.set_footer(
        text='Add a song to the playlist with $add_song!'
        )
        if len(self.playlist) == 0:
            embed.description = "The playlist is empty."
        else:
            for i in self.playlist:
                embed.add_field(name=f"{self.playlist.index(i)+1}. {i}", value='', inline=False)
        await ctx.send(embed=embed)
   
    
    @commands.command()
    async def leave(self,ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        try:
                await voice.disconnect()
        except:
            await ctx.send("The bot is not connected to a voice channel.")


    @commands.command()
    async def pause(self,ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        try: 
            if voice.is_playing():
                voice.pause()
                await ctx.send("The song is pause.")
            else:
                await ctx.send("Currently no audio is playing.")
        except:
            await ctx.send("Bot is not connected to a voice channel.")


    @commands.command()
    async def resume(self,ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        try:
            if voice.is_paused():
                voice.resume()
            else:
                await ctx.send("The audio is not paused.")
        except:
            await ctx.send("Bot is not connected to a voice channel.")

    @commands.command()
    async def stop(self,ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        try:
            voice.stop()
            await ctx.send("The song is stop.")
        except:
            await ctx.send("Bot is not connected to a voice channel.")

    @commands.command()
    async def remove_song(self, ctx, song_name):
        try:
            file = self.PlayList[song_name]
            os.remove(file)
            await ctx.send(f"{song_name} is removed.")
            self.PlayList.pop(song_name)
            self.playlist = list(self.PlayList.keys())
            self.PLAYLIST = list(self.PlayList.values())
        except KeyError:
            await ctx.send(f"{song_name} not found in the playlist.")

    @commands.command()
    async def clear_playlist(self,ctx):
        for file in self.PlayList.values():
            os.remove(file)
        self.PlayList.clear()
        self.playlist.clear()
        self.PLAYLIST.clear()
        await ctx.send("The playlist is cleared.")



    
async def setup(bot):
    await bot.add_cog(Music(bot))
