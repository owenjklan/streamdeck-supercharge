import subprocess
from pathlib import Path

import playsound3 as playsound

import Xlib.display

AUDIO_BASE_DIR = Path(__file__).resolve().parent / 'audio'

print(AUDIO_BASE_DIR)

disp = Xlib.display.Display()
Xroot = disp.screen().root
NET_ACTIVE_WINDOW = disp.intern_atom('_NET_ACTIVE_WINDOW')
Xroot.change_attributes(event_mask=Xlib.X.PropertyChangeMask |
                        Xlib.X.SubstructureNotifyMask)

windows = []
last_activation = ""

while True:
    # loop until an event happens that we care about
    # we care about a change to which window is active
    # (NET_ACTIVE_WINDOW property changes on the root)
    # or about the currently active window changing
    # in size or position (ConfigureNotify event for
    # our window or one of its ancestors)
    event = disp.next_event()
    if (event.type == Xlib.X.PropertyNotify and
            event.atom == NET_ACTIVE_WINDOW):
        active = disp.get_input_focus().focus
        try:
            name = active.get_wm_class()[1]
        except TypeError:
            name = "unknown"
        # print("The active window has changed! It is now", name)
        if "gimp" in name.lower():
            if last_activation != "gimp":
                last_activation = "gimp"
                subprocess.run(["streamdeckc", "-a", "SET_PAGE", "-p", "1"])
                playsound.playsound(AUDIO_BASE_DIR / "gimp" / "activated.wav")
        elif "kdenlive" in name.lower():
            if last_activation != "kdenlive":
                last_activation = "kdenlive"
                # Switch to KDEnlive page on StreamDeck
                subprocess.run(["streamdeckc", "-a", "SET_PAGE", "-p", "0"])
                playsound.playsound(AUDIO_BASE_DIR / "kdenlive" / "activated.wav")
