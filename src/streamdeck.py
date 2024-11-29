import subprocess
from pathlib import Path

STREAMDECKC_PATH = "/home/owen/.local/bin/streamdeckc"

import logging

logger = logging.getLogger(__name__)

"""
Wrapper class around the 'streamdeckc' control program

  -a NAME, --action=NAME
                        the action to be performed. valid options (case-
                        insensitive): SET_PAGE, SET_BRIGHTNESS, SET_TEXT,
                        SET_ALIGNMENT, SET_CMD, SET_KEYS, SET_WRITE, SET_ICON,
                        CLEAR_ICON, SET_STATE
  -d INDEX, --deck=INDEX
                        the deck to be manipulated. defaults to the currently
                        selected deck in the ui
  -p INDEX, --page=INDEX
                        the page to be manipulated. defaults to the currently
                        active page
  -b INDEX, --button=INDEX
                        the button to be manipulated
  -s INDEX, --state=INDEX
                        the button state to be manipulated
  --icon=PATH           path to an icon. used with SET_ICON
  --brightness=VALUE    brightness to set, 0-100. used with SET_BRIGHTNESS
  --text=VALUE          button text to set. used with SET_TEXT
  --write=VALUE         text to be written when the button is pressed. used
                        with SET_WRITE
  --command=VALUE       button command to set. used with SET_CMD
  --keys=VALUE          button keys to set. used with SET_KEYS
  --alignment=VALUE     button text alignment. used with SET_ALIGNMENT. valid
                        values: top, middle-top, middle, middle-bottom, bottom

"""

COMMON_ACTION_ARGS = "--page={page_index} --button={button_index} --state={state_index}"


class StreamDeck(object):
    def __init__(self, deck_index: int = 0):
        self.deck_index = deck_index

    def run_control_program(self, args: list[str]):
        execution_args = [STREAMDECKC_PATH, f"--deck={self.deck_index}"] + args

        try:
            subprocess.run(execution_args)
        except Exception as e:
            logger.info(f"Failed running: {' '.join(execution_args)}! {e}")
            return

    def common_args(self, button_index: int, state_index: int, page_index: int):
        common_args = COMMON_ACTION_ARGS.format(
            button_index=button_index, state_index=state_index, page_index=page_index
        ).split()
        return common_args

    def perform_action(self, action: str, args: list[str]):
        action_args = [f"--action={action}"] + args
        self.run_control_program(action_args)

    def set_page(self, page_index: int = 0):
        self.perform_action("SET_PAGE", [f"--page={page_index}"])

    def set_text(
        self,
        text: str,
        button_index: int = 0,
        page_index: int = 0,
        state_index: int = 0,
    ):
        args = [
            f"--text={text}",
        ] + self.common_args(button_index, state_index, page_index)
        self.perform_action("SET_TEXT", args)

    def set_icon(
        self,
        icon_path: str | Path,
        button_index: int = 0,
        page_index: int = 0,
        state_index: int = 0,
    ):
        args = [
            f"--icon={str(icon_path)}",
        ] + self.common_args(button_index, state_index, page_index)
        self.perform_action("SET_TEXT", args)

    def set_command(
        self,
        command: str,
        button_index: int = 0,
        page_index: int = 0,
        state_index: int = 0,
    ):
        args = [
            f"--command={command}",
        ] + self.common_args(button_index, state_index, page_index)
        self.perform_action("SET_CMD", args)

    def set_keys(
        self,
        keys: str,
        button_index: int = 0,
        page_index: int = 0,
        state_index: int = 0,
    ):
        args = [
            f"--keys={keys}",
        ] + self.common_args(button_index, state_index, page_index)
        self.perform_action("SET_KEYS", args)

    def set_alignment(
        self,
        alignment: str,
        button_index: int = 0,
        page_index: int = 0,
        state_index: int = 0,
    ):
        args = [
            f"--alignment={alignment}",
        ] + self.common_args(button_index, state_index, page_index)
        self.perform_action("SET_ALIGNMENT", args)

    def set_state(self, state_index: int, button_index: int = 0, page_index: int = 0):
        args = [
            f"--state={state_index}",
        ] + self.common_args(button_index, state_index, page_index)
        self.perform_action("SET_STATE", args)

    def clear_icon(
        self, button_index: int = 0, page_index: int = 0, state_index: int = 0
    ):
        args = self.common_args(button_index, state_index, page_index)
        self.perform_action("CLEAR_ICON", args)


class StreamDeckChain(object):
    def __init__(
        self, deck_index: int, button_index: int, page_index: int, state_index: int = 0
    ):
        self.deck_index = deck_index
        self.button_index = button_index
        self.page_index = page_index
        self.state_index = state_index
        self.deck = StreamDeck(self.deck_index)

    def clear_icon(self):
        self.deck.clear_icon(self.button_index, self.page_index, self.state_index)
        return self

    def text(self, text: str):
        self.deck.set_text(text, self.button_index, self.page_index, self.state_index)
        return self

    def alignment(self, alignment: str):
        self.deck.set_alignment(
            alignment, self.button_index, self.page_index, self.state_index
        )
        return self
