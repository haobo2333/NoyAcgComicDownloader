from textual.app import App, ComposeResult
from textual.containers import Horizontal, VerticalScroll, Vertical
from textual.widgets import Button, Footer, Header, Input, DataTable
from textual import work
import getBookInfo
import getBook
import time

INFO_KEYS = [
    "Bookname", "Bid", "Author", "Time", "Views", "Favorites", "Len", "Description", "Pname", "Ptag", "Otag"
]

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

    def __init__(self, cookies: str = "", config: dict = None):
        super().__init__()
        self.cookies = cookies
        self.config = config or {}

    def on_mount(self) -> None:
        # init datatable
        table = self.query_one(DataTable)
        table.add_column("Property")
        table.add_column("Value")
        for key, value in BOOK_INFO.items():
            table.add_row(key, str(value))
        table.show_header = False
        table.fixed_columns = 1
        # run a background funtion
        self.run_worker(self.is_bid_inp_empty(), thread=True)
        self.run_worker(self.is_search(), thread=True)

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical():
            with Horizontal(id="input_bar"):
                yield Input(placeholder="输入Bid", type="number", max_length=6, id="bid_inp")
                yield Button(label="搜索", variant="primary", disabled=True, id="search")
            with VerticalScroll():
                yield DataTable()
            yield Button(label="下载", variant="success", disabled=True, id="start")
        yield Footer()

    def action_change_mode(self) -> None:
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "search":
            self.handle_search()
        elif event.button.id == "start":
            self.handle_download()

    def update_table(self, data: dict) -> None:
        table = self.query_one(DataTable)
        table.clear()
        for key in INFO_KEYS:
            value = data.get(key, "N/A")
            table.add_row(key, str(value))
        self.notify(message="获取Bookinfo成功")

    def handle_search(self) -> None:
        self.bid = self.query_one("#bid_inp", Input).value
        self.notify(self.bid)
        info = getBookInfo.getBookInfo(self.cookies, bid=self.bid)
        self.update_table(info)

    @work(exclusive=True, thread=True)
    async def handle_download(self) -> None:
        self.notify(self.bid)
        info = getBookInfo.getBookInfo(self.cookies, bid=self.bid)
        self.notify(
            message=f"{info['Bookname']} | {info['Len']}Page(s) | 开始下载")
        return_message = getBook.getBook(
            bid=self.bid, path=self.config['download']['path'], bookinfo=info)
        if return_message != None:
            self.notify(message="错误："+str(return_message))
        self.notify(
            message=f"{info['Bookname']} | {info['Len']}Page(s) | 下载完成")

    async def is_bid_inp_empty(self) -> None:
        while True:
            if self.query_one("#bid_inp", Input).value != "":
                self.query_one("#search", Button).disabled = False
            else:
                self.query_one("#search", Button).disabled = True
            time.sleep(0.1)

    async def is_search(self) -> None:
        while True:
            if self.query_one(DataTable).get_cell_at((0, 1)) != "请先开始搜索":
                self.query_one("#start", Button).disabled = False
            else:
                self.query_one("#start", Button).disabled = True
            time.sleep(0.1)


if __name__ == "__name__":
    app = NoyComicDownloader()
    app.run()
