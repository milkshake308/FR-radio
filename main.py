import asyncio
import datetime
import json
import vlc
import threading
from aiohttp import web
from misc import log

vlc_instance = vlc.Instance()
player = vlc_instance.media_player_new()

#  GLOBAL SETTINGS
CONFIG = "config.json"

# default URL if not in config
stream_url = "http://hydra.cdnstream.com/1540_128"

schedule = []
state_override = False

# Fonction asynchrone pour démarrer la lecture de la vidéo
async def play_video():
    global stream_url
    media = vlc_instance.media_new(stream_url)
    player.set_media(media)
    player.play()
    log("PLAYER", "Démarrage du lecteur")
    await asyncio.sleep(0)  # Indiquer que la tâche est terminée

# Fonction pour arrêter la lecture de la vidéo
def stop_video():
    player.stop()
    log("PLAYER", "Arret du lecteur")

# Vérifier si l'heure actuelle est dans la plage de temps autorisée
def is_within_allowed_time():
    now = datetime.datetime.now()
    for set in schedule:
        if now.weekday() in set["active_days"] and set["start_hour"] <= now.hour < set["end_hour"]:
            return True
    return False

# Charger la programmation horaire à partir d'un fichier JSON
def load_config_from_json(filename):
    global schedule
    global stream_url
    with open(filename) as file:
        data = json.load(file)
        stream_url = data["stream_url"]
        schedule = data["schedule"]
    log("APP", "Chargement du fichier de configuration")

def save_config_to_json(filename):
    data = {
        "stream_url": stream_url,
        "schedule": schedule
    }
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    log("APP", "Enregistrement du fichier de configuration")

# GET - START PLAYER
async def start_handler(request):
    global state_override
    loop = asyncio.get_running_loop()
    loop.create_task(play_video())
    state_override = True
    log("APP", "Déblocage du lecteur")
    return web.Response(text='Lecture démarrée.')

# GET - STOP PLAYER
async def stop_handler(request):
    global state_override
    loop = asyncio.get_running_loop()
    loop.call_soon(stop_video)
    state_override = False
    log("APP", "Blocage du lecteur")
    return web.Response(text='Lecture arrêtée.')

#  GET - PLAYER STATUS
async def status_handler(request):
    if player.is_playing():
        return web.Response(text='Lecteur actif.')
    else:
        return web.Response(text='Lecteur arrêté.')

#  GET - STREAM URL
async def get_url_handler(request):
    return web.Response(text=stream_url)

#  POST - NEW STREAM URL
async def set_url_handler(request):
    global stream_url
    try:
        data = await request.json()
        new_url = data.get("stream_url")
        if new_url:
            stream_url = new_url.strip()
            
            log("APP", "Enregistrement d'une nouvelle URL de flux", stream_url)
            save_config_to_json(CONFIG)
            return web.Response(text='URL mise à jour.')
        else:
            return web.Response(text='Paramètre "stream_url" manquant dans le JSON.', status=400)
    except json.JSONDecodeError:
        return web.Response(text='Erreur lors de la lecture du JSON.', status=400)
    
async def get_schedule_handler(request):
    return web.json_response(schedule)

async def set_schedule_handler(request):
    global schedule
    try:
        data = await request.json()
        new_schedule = data.get("schedule")
        if new_schedule:
            schedule = new_schedule
            log("APP", "Mise à jour de la programmation horaire", schedule)
            save_config_to_json(CONFIG)
            return web.Response(text='Programmation horaire mise à jour.')
        else:
            return web.Response(text='Paramètre "schedule" manquant dans le JSON.', status=400)
    except json.JSONDecodeError:
        return web.Response(text='Erreur lors de la lecture du JSON.', status=400)




# Créer l'application web asynchrone
app = web.Application()
app.router.add_get('/start', start_handler)
app.router.add_get('/stop', stop_handler)
app.router.add_get('/status', status_handler)
app.router.add_get('/url', get_url_handler)
app.router.add_post('/url', set_url_handler)
app.router.add_get('/schedule', get_schedule_handler)
app.router.add_post('/schedule', set_schedule_handler)

# Charger la programmation horaire à partir du fichier JSON
load_config_from_json(CONFIG)

# Créer une nouvelle boucle d'événements
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

web_thread = threading.Thread(target=lambda: web.run_app(app))
web_thread.start()

#  Gestion de la planification horaire

#  Vérifier périodiquement la programmation horaire et démarrer/arrêter le lecteur en conséquence
async def check_schedule():
    while True:
        if not state_override and is_within_allowed_time() and not player.is_playing():
            log("SCHDUL", "Démarrage du lecteur", "MOTIF : Planification horaire")
            await play_video()
        elif not is_within_allowed_time() and player.is_playing():
            log("SCHDUL", "Arrêt du lecteur", "MOTIF : Planification horaire")
            stop_video()
        await asyncio.sleep(10)  # Vérifier toutes les 60 secondes

loop.create_task(check_schedule())
loop.run_forever()
