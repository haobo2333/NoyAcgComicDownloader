from textual.app import App, ComposeResult
from textual.containers import Horizontal, VerticalScroll, Vertical
from textual.widgets import Button, Footer, Header, Input, Label, DataTable

BOOK_INFO = {
    "Bookname": "请先开始搜索",
    "Bid": "",
    "Author": "",
    "Time": "",
    "Views": "",
    "Favorites": "",
    "Len": "",
    "Description": "",
    "Pname": "",
    "Ptag": "",
    "Otag": "",
}


class NoyComicDownloader(App):
    CSS_PATH = "tui.tcss"
    BINDINGS = [('q', 'quit', '退出'), ("d", "change_mode", "亮暗模式"),
                ("?", "get_help", "帮助")]

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical():
            with Horizontal(id="input_bar"):
                yield Input(placeholder="输入Bid", type="number", max_length=6, id="bid_inp")
                yield Button(label="搜索", variant="primary", id="search")
            with VerticalScroll():
                yield DataTable()
            yield Button(label="下载", variant="success", id="start")
        yield Footer()


    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_column("Property")
        table.add_column("Value")
        for key, value in BOOK_INFO.items():
            table.add_row(key, str(value))
        table.show_header = False
        table.fixed_columns = 1

    def action_change_mode(self) -> None:
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

'''
    def compose(self) -> ComposeResult:
        yield Header()

        with VerticalScroll():
            with Horizontal():
                bid_inp = Input(placeholder="输入Bid",
                                type="number", max_length=6, id="bid_inp")
                yield bid_inp
                yield Button(label="搜索", variant="primary", flat=True, id="search")
            yield DataTable(id="table")
            yield Button(label="下载", flat=True, id="start")
        yield Footer()
'''


if __name__ == "__name__":
    app = NoyComicDownloader()
    app.run()
