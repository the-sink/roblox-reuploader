import config
import uvicorn
import requests
import html
import os
import base64
import json
from bs4 import BeautifulSoup
from tqdm import tqdm
from pathlib import Path
from typing import List
from fastapi import FastAPI, Request, Response, status

# welcome to my horrific spaghetti code, enjoy your stay

app = FastAPI()
session = requests.Session()

max_ids_per_request: int = 30
creator_type_translation = ["User", "Group"]
invalid_characters = '<>:"/\|?*'

uploaded_id_list = {}
temp_id_list = {}
current_place_id = 0
current_creator_id = 0
current_creator_type = 0
csrf_token = 0

if not os.path.isfile('uploaded_id_list.json'):
    with open('uploaded_id_list.json', 'w+') as f:
        json.dump({}, f)
        f.close()
else:
    with open('uploaded_id_list.json', 'r') as f:
        uploaded_id_list = json.load(f)
        f.close()

session.cookies.update({".ROBLOSECURITY": config.roblosecurity, ".RBXID": config.rbxid})

## UTILITY

def save_uploaded_id_list():
    with open('uploaded_id_list.json', 'w') as f:
        json.dump(uploaded_id_list, f)
        f.close()

def split_into_chunks(list, size):
    for i in range(0, len(list), size):
        yield list[i:i + size]

def get_group_owner(group_id: int):
    group_info = session.get("https://groups.roblox.com/v1/groups/" + str(group_id))

    if group_info.status_code == 200:
        return group_info.json().get('owner').get('userId')
    else:
        return -1

def get_neccesary_downloads(ids: List[int], game_creator_id: int, game_creator_type: str, place_id: int):
    global current_place_id
    global current_creator_id
    global current_creator_type
    global csrf_token

    current_place_id = place_id
    current_creator_id = game_creator_id
    current_creator_type = game_creator_type
    csrf_token = 0
    
    id_chunks = split_into_chunks(ids, max_ids_per_request)

    download_list = []
    group_owner_cache = {}

    pbar = tqdm(id_chunks)
    pbar.set_description("Determining neccesary downloads")

    for chunk in pbar:
        str_list = [str(int) for int in chunk]

        url = "https://apis.roblox.com/toolbox-service/v1/items/details?assetIds=" + ",".join(str_list)

        audio_info = session.get(url)

        if audio_info.status_code == 200:
            for item in audio_info.json()['data']:
                asset = item.get('asset')
                creator = item.get('creator')

                creator_id = creator.get('id')
                creator_type = creator_type_translation[creator.get('type')-1]

                if not asset.get('typeId') == 3: # Ignore assets that are not audio
                    continue

                if creator_id == 1 or creator_id == 1750384777: # Ignore Roblox and Monstercat accounts
                    continue

                if asset.get('duration') < 6: # Audio length qualifies it as a sound effect
                    continue

                if asset.get('name') == "(Removed for copyright)" or asset.get('name') == "[ Content Deleted ]": # Ignore audio that has been removed for copyright/moderated
                    continue

                if game_creator_id == creator_id and game_creator_type == creator_type: # Ignore audio created by place owner
                    continue

                if creator_type == "Group":
                    if creator_id in group_owner_cache:
                        group_owner = group_owner_cache.get(creator_id)
                    else:
                        group_owner = get_group_owner(creator_id)
                        group_owner_cache[creator_id] = group_owner

                    if creator_id == group_owner: # Ignore audio created by group owner, if asset is owned by a group
                        continue
                
                download_list.append({"id": asset.get('id'), "name": asset.get('name')})
        else:
            pbar.write("Request error " + str(audio_info.status_code))

    if len(download_list) < 1:
        print("No assets have been detected that need to be reuploaded!")

    # obtain X-CSRF-TOKEN header in preparation for the upload process
    initial_request = session.post("https://publish.roblox.com/v1/audio")
    csrf_token = initial_request.headers.get("x-csrf-token")

    return download_list

## UPLOAD

def upload(id: int, data: str, name: str):
    global uploaded_id_list
    global csrf_token

    group_id = None
    existing_replacement = uploaded_id_list.get(str(id))

    if existing_replacement:
        if existing_replacement == -15:
            print(f"Skipping asset {str(id)} ({name}). It was previously attempted by the reuploader tool and was moderated! (possibly deleted for copyright)")
            return -1

        return existing_replacement

    if current_creator_type == "Group":
        group_id = current_creator_id

    #if csrf_token == 0:
    #    initial_request = session.post("https://publish.roblox.com/v1/audio")
    #    csrf_token = initial_request.headers.get("x-csrf-token")

    file_data = base64.b64encode(data).decode('ascii')
    upload = session.post("https://publish.roblox.com/v1/audio",
    json={"name": name, "file": file_data, "groupId": group_id},
    headers={"Content-Type": "application/json", "X-CSRF-TOKEN": csrf_token})

    if upload.status_code == 200:
        new_id = int(upload.json().get('Id'))
        uploaded_id_list[str(id)] = new_id
        save_uploaded_id_list() # save for every audio file uploaded (because i'm paranoid)
        print("Uploaded asset")

        return new_id
    else:
        error_data = json.loads(upload.text)
        error = error_data.get('errors')[0]
        print("UPLOAD ERROR! Error code: " + str(upload.status_code) + ", message: " + error.get('message'))

        if error.get('code') == 15: # Audio asset previously moderated and rejected
            uploaded_id_list[str(id)] = -15
            save_uploaded_id_list()
        
        return -1


### Gets a list of assets that need replacement


@app.post("/get-neccesary-downloads")
async def get_downloads(request: Request, creator_id: int, creator_type: str, place_id: int, response: Response):
    global temp_id_list
    temp_id_list = {}

    data = await request.json()

    response.status_code = status.HTTP_200_OK
    return get_neccesary_downloads(data, creator_id, creator_type, place_id)

### Downloads and re-uploads an asset

@app.post("/reupload")
async def reupload(asset_id: int, file_name: str, response: Response):
    page = session.get("https://www.roblox.com/library/" + str(asset_id))

    content = html.unescape(page.text)
    soup = BeautifulSoup(content, 'html.parser')

    button = soup.find('div', {'class': 'MediaPlayerIcon'})
    if button:
        url = button['data-mediathumb-url']

        audio_file = requests.get(url)
        uploaded_id = upload(asset_id, audio_file.content, file_name)

        response.status_code = status.HTTP_200_OK
        return uploaded_id

if __name__=="__main__":
    uvicorn.run("app:app", host='localhost', port=37007, workers=1)