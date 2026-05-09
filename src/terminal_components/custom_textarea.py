from textual.widgets import TextArea
from textual.events import Key
from textual.message import Message


class CustomTextArea(TextArea):

    class Submitted(Message):

        def __init__(self, text: str):
            self.text = text
            super().__init__()

    async def on_key(self, event: Key):

        if "newline" in event.aliases:
            self.insert('\n')
            return

        if "enter" not in event.aliases:
            return

        event.prevent_default()

        text = self.text

        if not text.strip():
            return

        self.post_message(
            CustomTextArea.Submitted(text)
        )

        self.text = ""