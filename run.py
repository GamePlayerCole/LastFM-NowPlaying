
import sys
import time

from aiohttp import ClientSession
import asyncio

#Config
CHANNEL = input("Last.FM name: ")
WAIT_TIME = 10
SONG_FILE = "currentSong.txt"

#Global stuff
API_KEY = "460cda35be2fbf4f28e8ea7a38580730"
ENDPOINT = f'http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&format=json&limit=1&nowplaying=true&user={CHANNEL}&api_key={API_KEY}'

class SongHandler:

    def __init__(self):
        self.session = ClientSession()

    async def write_new_song(self, song):
        with open(SONG_FILE, "w") as f:
            print(song)
            f.write(song)

    async def request(self, method, endpoint):
        async with self.session.request(method, endpoint) as response:
            try:
                return await response.json()
            except json.decoder.JSONDecodeError:
                return {}
            else:
                return {}

    async def check_for_song(self):
        result = await self.request("GET", ENDPOINT)

        if result and result["recenttracks"] and result["recenttracks"]["track"] and result["recenttracks"]["track"][0]:
            track = result["recenttracks"]["track"][0]

            if track["artist"] and track["artist"]["#text"] and track["name"]:
                artist = track["artist"]["#text"]
                name = track["name"]

                return {"artist": artist, "name": name.replace(" ()", "")}

    async def run(self):
        running = True
        last_song = None

        try:
            while running:
                song = await self.check_for_song()
                if not song or song == last_song:
                    continue
                last_song = song

                await self.write_new_song(f"{song['artist']} - {song['name']}")

                time.sleep(WAIT_TIME)
        except KeyboardInterrupt:
            running = False
            await self.session.close()
            await self.write_new_song("Nothing currently playing")
            print("Closing...")

async def run():
    await SongHandler().run()

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
