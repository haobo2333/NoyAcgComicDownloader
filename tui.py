from textual.app import App, ComposeResult
from textual.containers import VerticalScroll, Vertical
from textual.widgets import Button, Footer, Header, DataTable, Label, TextArea
from textual import work, on
import getBook
import getBookInfo

INFO_KEYS = ["Bookname", "Bid", "Author", "Time",
             "Views", "Favorites", "Len", "Description"]


class NoyComicDownloader(App):
    CSS = """
    DataTable { height: auto; margin-bottom: 1; border: solid gray; }
    #container { height: 1fr; }
    """

    BINDINGS = [("q", "quit", "退出"), ("d", "toggle_dark", "亮暗模式")]

    def __init__(self, cookies: str = "", config: dict = None):
        super().__init__()
        self.cookies = cookies
        self.config = config or {"download": {"path": "./"}}

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical():
            yield TextArea(placeholder="每行输入一个 Bid", id="bid_inp")
            yield Button(label="搜索", variant="primary", id="search", disabled=True)
            # 用于放置表格
            with VerticalScroll(id="container"):
                pass
            yield Button(label="下载全部", variant="success", id="start", disabled=True)
        yield Footer()

    @on(TextArea.Changed, "#bid_inp")
    def input_watchdog(self):
        text = self.query_one("#bid_inp", TextArea).text.strip()
        self.query_one("#search").disabled = (text == "")

    async def handle_search(self) -> None:
        container = self.query_one("#container")
        await container.query(DataTable).remove()

        raw_text = self.query_one("#bid_inp", TextArea).text
        self.bid_list = [line.strip()
                         for line in raw_text.splitlines() if line.strip()]

        for bid in self.bid_list:
            # init new datatable
            table = DataTable(id=f"table_{bid}")
            table.add_columns("Property", "Value")
            table.show_header = False
            table.fixed_columns = 1
            await container.mount(table)
            # init done
            self.fetch_and_fill_data(bid, table)

    @work(thread=True)
    def fetch_and_fill_data(self, bid: str, table: DataTable):
        try:
            # 模拟获取数据: info = getBookInfo.getBookInfo(self.cookies, bid=bid)
            # info = {"Bookname": f"书籍 {bid}", "Bid": bid, "Author": "测试作者"}
            info = getBookInfo.getBookInfo(cookies=self.cookies, bid=bid)
            # 使用 call_from_thread 确保 UI 更新安全
            self.app.call_from_thread(self.fill_table, table, info)
        except Exception as e:
            self.notify(f"获取 {bid} 失败: {e}", severity="error")

    def fill_table(self, table: DataTable, data: dict):
        table.clear()
        for key in INFO_KEYS:
            table.add_row(key, str(data.get(key, "N/A")))
        self.query_one("#start").disabled = False

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "search":
            self.run_worker(self.handle_search())
        elif event.button.id == "start":
            self.handle_download()

    @work(exclusive=True, thread=True)
    async def handle_download(self) -> None:
        for bid in self.bid_list:
            info = getBookInfo.getBookInfo(self.cookies, bid=bid)
            self.notify(
                message=f"{info['Bookname']} | {info['Len']}Page(s) | 开始下载")
            return_message = getBook.getBook(
                bid=bid, path=self.config['download']['path'], bookinfo=info)
            if return_message != None:
                self.notify(message="错误："+str(return_message))
            self.notify(
                message=f"{info['Bookname']} | {info['Len']}Page(s) | 下载完成")
        self.notify(message="下载全部完成")


if __name__ == "__main__":
    app = NoyComicDownloader()
    app.run()
