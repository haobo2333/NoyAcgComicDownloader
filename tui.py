from textual.app import App, ComposeResult
from textual.containers import Horizontal, VerticalScroll, Vertical
from textual.widgets import Button, Footer, Header, Input, DataTable
from textual import work
import getBookInfo
import getBook

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
        bid = self.query_one("#bid_inp", Input).value
        info = getBookInfo.getBookInfo(self.cookies, bid=bid)
        self.update_table(info)

    @work(exclusive=True, thread=True)
    async def handle_download(self) -> None:
        bid = self.query_one("#bid_inp", Input).value
        info = getBookInfo.getBookInfo(self.cookies, bid=bid)
        self.notify(message=f"{info['Bookname']} | {info['Len']}Page(s) | 开始下载")
        return_message = getBook.getBook(bid=bid,path=self.config['download']['path'],bookinfo=info)
        if return_message != None:
            self.notify(message="错误："+str(return_message))
        self.notify(message=f"{info['Bookname']} | {info['Len']}Page(s) | 下载完成")

if __name__ == "__name__":
    app = NoyComicDownloader()
    app.run()
