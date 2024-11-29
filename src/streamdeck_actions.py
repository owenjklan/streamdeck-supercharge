from pathlib import Path

import playsound3 as playsound

from src.streamdeck import StreamDeck

main_streamdeck = StreamDeck(deck_index=1)

last_group: str = ""
last_group_page: dict[str, int] = {
    "kdenlive": 3,  # Default: KDEnlive Editing
    "gimp": 4  # Default: GIMP Editing
}


def activate_group_page(
        group: str,
        page_index: int = 0,
        audio_dir: str | Path = "."
):
    global last_group, last_group_page
    previous_last_page = last_group_page[group]
    last_group_page[group] = page_index

    print(f"Activating group page: {group}[{page_index}]")
    print(f"Last page was: {previous_last_page}, now set to {page_index}")
    main_streamdeck.set_page(page_index=page_index)


def activate_group(
        group: str | Path,
        audio_dir: str | Path = "."
):
    global last_group

    group_str = str(group)

    print(f"Activating group: {group_str}")

    if last_group != group_str:
        playsound.playsound(audio_dir / group_str / "activated.wav")
        last_group = group_str
        print(f"Last group set to {last_group}")

    group_page = last_group_page.get(group_str, 1)

    print(f"Calling Stream Deck activation: {group_str}, last page {group_page}")
    main_streamdeck.set_page(page_index=group_page)
