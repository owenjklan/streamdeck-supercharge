#!/usr/bin/env python3
import logging
import playsound3 as playsound
from pathlib import Path

from flask import Flask, render_template, request, url_for

# from x11_focus_monitor import last_activation

HTML_BASE_DIR = Path(__file__).resolve().parent
AUDIO_BASE_DIR = HTML_BASE_DIR.parent / 'audio'
SEARCH_BASE_DIR = HTML_BASE_DIR / 'search'
print(f"HTML source base directory: {HTML_BASE_DIR}")
print(f"Audio base base directory: {AUDIO_BASE_DIR}")

app = Flask(
    __name__,
    # static_folder=HTML_BASE_DIR,
    # template_folder=HTML_BASE_DIR,
)

audio_confirmations = True
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
    app.run(host='127.0.0.1', port=33333, debug=True)