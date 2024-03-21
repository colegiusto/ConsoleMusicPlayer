import requests, vlc, asyncio, pickle, os
from shutil import rmtree
from concurrent.futures import ThreadPoolExecutor
from pytube import YouTube
from youtube_search import YoutubeSearch

API_KEY = ""

base_url = "http://ws.audioscrobbler.com/2.0"

home_path = "C://Users/coleg/Desktop/coding/python_pixels/"

os.environ['VLC_VERBOSE'] = '-1'

async def ainput(prompt: str = "") -> str:
    with ThreadPoolExecutor(1, 'ainput') as executor:
        return await asyncio.get_event_loop().run_in_executor(executor, input, prompt)

async def main():
    with open('library.pickle', 'rb') as f:
        library = pickle.load(f)
    
    history = []
    mlist: vlc.MediaList = vlc.MediaList()
    player: vlc.MediaListPlayer = vlc.MediaListPlayer()
    player.set_media_list(mlist)
    
    while True:
        action = await ainput(">>>")
        match action[0]:
            case 's':
                
                search = await ainput(">>>")

                search_params = {
                    "method" : "track.search",
                    "track" : search,
                    "api_key" : API_KEY,
                    "format" : "json",
                    "limit" : 5
                }
                

                res = requests.get(base_url, params=search_params).json()['results']['trackmatches']['track']
                print("RESULTS:\n")
                for i,r in enumerate(res):
                    print(f"{i+1}{':':<3} {r['name']: <60}{r['artist']}")

                sel = int(input('\n>>>'))
                song = res[sel-1]
                id = YoutubeSearch(f"{song['name']} by {song['artist']} (Audio)", max_results=1).to_dict()[0]['id']
                fname = YouTube(f"https://www.youtube.com/watch?v={id}").streams.get_audio_only().download(f"{home_path}/tmp/")
                mlist.add_media(fname)
                player.play()
                

            case 'q':
                with open('history.pickle', 'wb') as f:
                    pickle.dump(history, f)
                with open('library.pickle', 'wb') as f:
                    pickle.dump(library, f)
                rmtree(f"{home_path}/tmp")
                break
            case _:
                print("Unsupported")


asyncio.run(main())