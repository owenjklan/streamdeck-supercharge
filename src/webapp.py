#!/usr/bin/env python3
import logging
from pathlib import Path
from threading import Thread

import playsound3 as playsound
from flask import Flask, request

import x11_focus_monitor
from streamdeck_actions import activate_group_page

# from x11_focus_monitor import last_activation

HTML_BASE_DIR = Path(__file__).resolve().parent
AUDIO_BASE_DIR = HTML_BASE_DIR.parent / 'audio'
SEARCH_BASE_DIR = HTML_BASE_DIR / 'search'
print(f"HTML source base directory: {HTML_BASE_DIR}")
print(f"Audio base base directory: {AUDIO_BASE_DIR}")


app = Flask(
    __name__,
)

app.__setattr__("focus_monitor_started", False)

keyclicks = True


@app.route("/play/<active_page>", methods=['GET'])
def play_event(active_page: str):
    if keyclicks:
        playsound.playsound(AUDIO_BASE_DIR / "_system" / "keyclick.wav")

    if not audio_confirmations:
        return "OK (muted)"

    request_args = request.args
    logging.info(f"Requested to play: {request_args['event']}")

    audio_path = AUDIO_BASE_DIR / active_page / f"{request_args['event']}.wav"

    playsound.playsound(audio_path)
    return "OK"


@app.route("/activate_page/<activation_group>")
def activate_page(activation_group: str):
    request_args = request.args
    page = int(request_args["page"])

    activate_group_page(activation_group, page, audio_dir=AUDIO_BASE_DIR)
    return "OK"


@app.route("/enable_keyclick", methods=['GET'])
def enable_keyclicks():
    global keyclicks
    request_args = request.args
    keyclicks = bool(int(request_args['enable']))
    print("Keyclicks now: " + str(keyclicks))
    if keyclicks:
        playsound.playsound(AUDIO_BASE_DIR / "_system" / "keyclick.wav")

    return "OK"


@app.route("/enable_confirmations", methods=['GET'])
def enable_confirmations():
    global audio_confirmations
    request_args = request.args
    audio_confirmations = bool(int(request_args['enable']))
    logging.info(f"Audio confirmations: { not audio_confirmations }")

    sound_file = "audio-confirmations-enabled.wav" if audio_confirmations else "audio-confirmations-disabled.wav"
    audio_path = AUDIO_BASE_DIR / "_system" / sound_file

    playsound.playsound(audio_path)

    return "OK"


if __name__ == '__main__':
    # Start X11 focus watching thread
    if not app.__getattribute__("focus_monitor_started"):
        focus_monitor_thread = Thread(target=x11_focus_monitor.monitor_x11_focus, args=(AUDIO_BASE_DIR,))
        focus_monitor_thread.start()
        app.__setattr__("focus_monitor_started", True)

    app.run(host='127.0.0.1', port=33333, debug=True)
