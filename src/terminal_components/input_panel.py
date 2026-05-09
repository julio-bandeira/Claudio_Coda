from textual import on
from textual.app import ComposeResult
from textual.widgets import Label, Input, LoadingIndicator, TextArea
from textual.containers import Container, ScrollableContainer

from terminal_components.custom_textarea import CustomTextArea

class InputPanel(Container):
    
    DEFAULT_CLASSES = "input-panel"
    
    def __init__(self, *children, name = None, id = None, classes = None, disabled = False, markup = True):
        super().__init__(*children, name=name, id=id, classes=classes, disabled=disabled, markup=markup)
    
    def compose(self) -> ComposeResult:
        #yield LoadingIndicator(id="thinking")
        yield ScrollableContainer(
            Label(">", id="input-mark"),
            CustomTextArea(
                "",
                placeholder="Ask Something",
                id="input-in"
            ),
            classes="terminal-input"
        )
    
    @on(CustomTextArea.Changed)
    def scroll_terminal_input_to_end(self, event: CustomTextArea.Changed):
        scroll_terminal = self.query_one(".terminal-input", ScrollableContainer)

        scroll_terminal.scroll_end(animate=False)