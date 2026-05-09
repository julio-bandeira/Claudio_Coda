from textual.containers import ScrollableContainer

from terminal_components.chat_message import ChatMessage

class ChatPanel(ScrollableContainer):

    DEFAULT_CLASSES = "chat-panel"
    
    def add_message(
        self,
        author: str,
        content: str,
        role: str
    ) -> ChatMessage:

        message = ChatMessage(
            author=author,
            role=role,
            content=content
        )

        self.mount(message)

        self.scroll_end(animate=False)

        return message

    def create_message(
        self,
        author: str,
        role: str
    ) -> ChatMessage:

        message = ChatMessage(
            author=author,
            role=role,
            content=""
        )

        self.mount(message)

        self.scroll_end(animate=False)

        return message