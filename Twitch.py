import requests, os, time, sys

for Folder in ["./Downloads", "./Downloads/Streamers", "./Downloads/Categories"]:
    if not os.path.exists(Folder):
        os.mkdir(Folder)

if not os.path.exists("client_id.txt"):
    ClientID = input("Enter Client ID (For Twitch API): ")
    ClientID_file = open("client_id.txt", "w+").write(ClientID)

if not os.path.exists("Streamers.txt"):
    Streamers = open("Streamers.txt", "w+").write("Lilypichu\nPokimane\nScarra\nSykkuno")

if not os.path.exists("Categories.txt"):
    Categories = open("Categories.txt", "w+").write("Just Chatting\nAmong Us")

Streamers = []
Categories = []

def Main():

    global Streamers
    global Categories
    os.system("cls")

    Mode = input(f'[1] Streamer [2] Category\n\nSelect Mode:')

    if Mode == "1":

        os.system("cls")
        
        with open("Streamers.txt", "r+", encoding="UTF-8", errors="Ignore") as file:
            for line in file:
                line = line.strip()
                Streamers.append(line)

        try:
            Clip_count = int(input(f"Loaded {len(Streamers)} Streamers\n\nHow many clips you want to download per Streamer?: "))

        except ValueError:
            print("Only Numbers!")
            Streamers = []
            time.sleep(2)
            Main()

    elif Mode == "2":
        
        os.system("cls")

        with open("Categories.txt", "r+", encoding="UTF-8", errors="Ignore") as file:
            for line in file:
                line = line.strip()
                Categories.append(line)
        
        try:
            Clip_count = int(input(f"Loaded {len(Categories)} Categories\n\nHow many clips you want to download per Category?: "))
        except ValueError:
            print("Only Numbers!")
            Streamers = []
            time.sleep(2)
            Main()

    else:
        print("Wrong Input")
        time.sleep(2)
        Main()

    try:
        os.system("cls")
        Period = int(input(f"[1] Day [2] Week [3] Month [4] All\n\nEnter Clip Period: "))
    except ValueError:
        print("Only Numbers!")
        Streamers = []
        time.sleep(2)
        Main()

    if Period == 1: Period = "day"
    elif Period == 2: Period = "week"
    elif Period == 3: Period = "month"
    elif Period == 4: Period = "all"

    Download(Clip_count, Mode, Period)

def Download(Clip_count, Mode, Period):

    global Streamers
    global Categories

    os.system("cls")

    ClientID = open("client_id.txt", "r+").read()
    headers = {'Accept':"application/vnd.twitchtv.v5+json", 'Client-ID': ClientID}

    Clips = []
    Banned_Characters = ["?", "\\", "/", "*", ":", "<", ">", "|", '"']
        
    if Mode == "1":
        for Streamer in Streamers:
            response = requests.get("https://api.twitch.tv/kraken/clips/top", params = {"channel": Streamer, "trending": "false", "period": Period, "limit": Clip_count, "language": "en"}, headers=headers).json()
            Clips.append(response)
        
    elif Mode == "2":
        for Category in Categories:
            response = requests.get("https://api.twitch.tv/kraken/clips/top", params = {"game": Category, "trending": "false", "period": Period, "limit": Clip_count, "language": "en"}, headers=headers).json()
            Clips.append(response)

    for jsonobj in Clips:
        for json in jsonobj["clips"]:
            
            title = ''.join(i for i in json["title"] if i not in Banned_Characters)
            Channel = ''.join(i for i in json["broadcaster"]["display_name"] if i not in Banned_Characters)
            Category = ''.join(i for i in json["game"] if i not in Banned_Characters)
            dl_link = json["vod"]["preview_image_url"].replace('-preview.jpg', '.mp4')

            if Mode == "1": 
                Filename = f"./Downloads/Streamers/{Channel}/{title}.mp4"
                if not os.path.exists(f"./Downloads/Streamers/{Channel}"):
                    os.mkdir(f"./Downloads/Streamers/{Channel}")
            elif Mode == "2": 
                Filename = f"./Downloads/Categories/{Category}/{title}.mp4"
                if not os.path.exists(f"./Downloads/Categories/{Category}"):
                    os.mkdir(f"./Downloads/Categories/{Category}")

            if not os.path.exists(Filename):
                
                response = requests.get(dl_link)

                with open(Filename, 'wb') as fd:
                    for chunk in response.iter_content(chunk_size=100000):
                        fd.write(chunk)
                
                print(f"Downloaded: {title}.mp4 - {Channel}")
            
            else: print(f"Already Downloaded: {title}.mp4 - {Channel}")

    input("Done! Press any key to download more clips...")
    
    Streamers = []
    Categories = []
    Clips = []
    
    Main()

Main()
