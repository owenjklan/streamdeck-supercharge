from pathlib import Path

import Xlib.display

from streamdeck_actions import activate_group

AUDIO_BASE_DIR = Path(__file__).resolve().parent / 'audio'

print(AUDIO_BASE_DIR)

disp = Xlib.display.Display()
Xroot = disp.screen().root
NET_ACTIVE_WINDOW = disp.intern_atom('_NET_ACTIVE_WINDOW')
Xroot.change_attributes(event_mask=Xlib.X.PropertyChangeMask |
                        Xlib.X.SubstructureNotifyMask)


MAIN_DECK_INDEX = 1


def monitor_x11_focus(audio_base_dir: str | Path) -> None:
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
                activate_group("gimp", audio_dir=audio_base_dir)
            elif "kdenlive" in name.lower():
                activate_group("kdenlive", audio_dir=audio_base_dir)
