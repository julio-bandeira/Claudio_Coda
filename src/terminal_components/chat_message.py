from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Label


class ChatMessage(Container):

    def __init__(
        self,
        author: str,
        role: str,
        content: str = ""
    ):
        super().__init__(
            classes=f"chat_item role-{role}"
        )

        self.author = author
        self.role = role
        self.content = content

    def compose(self) -> ComposeResult:

        yield Container(

            Label(
                self.author,
                classes="chat_container_header"
            ),

            Label(
                self.content,
                id="content",
                classes="chat_container_content",
                markup=False
            ),

            classes="chat_container"
        )

    def append_chunk(self, chunk: str):

        self.content += chunk

        label = self.query_one(
            "#content",
            Label
        )

        label.update(self.content)

        label.refresh()

        self.refresh(layout=True)