# Create a music bot that plays Lofi music whenever a user joins
# a voice channel

## This module requires Java 13 and Lavalink v3.4 to work, additional Python packages can be found in requirements.txt

# Import necessary libraries
from discord.ext import commands
import wavelink
import random

CHANNEL_ID = 1042653309380599839 # Replace this with your own channel ID
# How to get one: https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjio_Wns7T7AhVeyTgGHdkZCRIQFnoECA4QAw&url=https%3A%2F%2Fsupport.discord.com%2Fhc%2Fen-us%2Farticles%2F206346498-Where-can-I-find-my-User-Server-Message-ID-&usg=AOvVaw2PjlTirxZBuSBNWaEv1oLm

class NoLofiMusicChannel(Exception):
    def __str__(self):
        return "No lofi music channel available. Incorrect or missing music channel ID"
                
        
class MusicCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.playlist_url = "https://www.youtube.com/watch?v=HV6OlMPn5sI&list=PL6NdkXsPL07IOu1AZ2Y2lGNYfjDStyT6O"
        self.bot.loop.create_task(self.connect_nodes()) # Connect to Lavalink server
        
    @property
    def music_channel(self):
        try:
            return self.bot.get_channel(CHANNEL_ID)
        except Exception:
            raise NoLofiMusicChannel

    # Helper function that represents a node connecting to Lavalink
    async def connect_nodes(self):
        await self.bot.wait_until_ready()
        await wavelink.NodePool.create_node(
            bot=self.bot,
            host ='127.0.0.1', # replaces with your host IP address
            port=2333, # Destination port
            password='youshallnotpass'
        )
    
    # A function that starts the music whenever a user joins that music channel
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # Check whether music channel exists
        if self.music_channel is None:
            raise NoLofiMusicChannel
        # Whenever a member joins the music channel
        if after.channel == self.music_channel:
            # Check whether the bot is already in the music channel and 
            # there is at least one non-bot user in the music channel
            if len(self.music_channel.members) >= 1 and (self.bot.user not in self.music_channel.members):
                # Create a voice connection to the music channel
                self.bot.vc: wavelink.Player = await self.music_channel.connect(cls=wavelink.Player())
            if not self.bot.vc.is_playing():    
                await self.bot.vc.play(next(self.bot.music_playlist))
        # When a member leave the voice channel and there's only the music bot left
        if len(self.music_channel.members) <= 1 and (self.bot.user in self.music_channel.members):
            await self.bot.vc.disconnect()

    # A function that retrieves YouTube playlist 
    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f'Node: <{node.identifier}> is ready!')
        # Build a music playlist
        self.bot.search = await wavelink.YouTubePlaylist.search(self.playlist_url)
        random.shuffle(self.bot.search.tracks)
        self.bot.music_playlist = iter(self.bot.search.tracks[:])
        
    # A function that play the next track
    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player: wavelink.Player, track: wavelink.Track, reason):
        try:
            await player.play(next(self.bot.music_playlist))
        except StopIteration:
            random.shuffle(self.bot.search.tracks)
            self.bot.music_playlist = iter(self.bot.search.tracks[:])
            await player.play(next(self.bot.music_playlist))
        





