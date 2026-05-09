from textual.app import App, ComposeResult

from textual import on
from textual import work

from terminal_components.banner_panel import BannerPanel
from terminal_components.chat_message import ChatMessage
from terminal_components.chat_panel import ChatPanel
from terminal_components.input_panel import InputPanel
from terminal_components.input_panel import CustomTextArea

from configs.system_config import (
    NAME,
    VERSION,
    SYSTEM,
    CURRENT_PATH_TILDE
)

from configs.global_config import load_config
from ollama_controller import OllamaController


config = load_config()

ollama_controller = OllamaController(model= config["model"])

class TerminalController(App):
    CSS_PATH = "terminal_style.css"
    
    def __init__(self, driver_class = None, css_path = None, watch_css = False, ansi_color = None):
        super().__init__(driver_class, css_path, watch_css, ansi_color)
    
    def compose(self) -> ComposeResult:
        yield BannerPanel(
            title=NAME,
            version=VERSION,
            model=config["model"],
            system=SYSTEM,
            path=CURRENT_PATH_TILDE
        )
        yield ChatPanel()
        yield InputPanel()
    
    @on(CustomTextArea.Submitted)
    async def handle_submit(
        self,
        event: CustomTextArea.Submitted
    ):

        chat = self.query_one(ChatPanel)

        ollama_controller.add_message("user", event.text)

        chat.add_message(
            "Você",
            event.text,
            "user"
        )

        llm_stream_message = chat.create_message("Claudio", "assistant")

        self.generate_answer(llm_stream_message)
    
    @work(thread=True)
    def generate_answer(self, llm_stream_message: ChatMessage):

        llm_output = ollama_controller.generate_message()

        llm_answer = ""

        chat = self.query_one(ChatPanel)

        for chunk in llm_output:

            msg = chunk.get("message")

            if not msg:
                continue

            chunk_think = msg.get("thinking")
            
            if chunk_think:
                llm_answer += chunk_think

            chunk_content = msg.get("content")

            if not chunk_content:
                continue

            llm_answer += chunk_content

            self.call_from_thread(
                llm_stream_message.append_chunk,
                chunk_content
            )

        ollama_controller.add_message(
            "assistant",
            llm_answer
        )