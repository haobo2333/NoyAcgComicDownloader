from textual.app import App, ComposeResult
from textual.containers import VerticalScroll, Vertical
from textual.widgets import Button, Footer, Header, DataTable, Label, TextArea
from textual import work, on
import getBook
import getBookInfo
import getUserInfo

INFO_KEYS = ["Bookname", "Bid", "Author", "Time",
             "Views", "Favorites", "Len", "Description"]


class NoyComicDownloader(App):
    CSS_PATH = "tui.tcss"

    BINDINGS = [("q", "quit", "退出"), ("d", "toggle_dark", "亮暗模式")]

    def __init__(self, cookie: str = "", config: dict = None):
        super().__init__()
        self.cookie = cookie
        self.config = config or {"download": {"path": "./"}}
        self.userinfo = getUserInfo.getUserInfo(self.cookie)

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Vertical():
            yield TextArea(placeholder="每行输入一个 Bid", id="bid_inp")
            yield Button(label="搜索", variant="primary", id="search", disabled=True)
            # 用于放置表格
            with VerticalScroll(id="container"):
                pass
            yield Button(label="下载全部", variant="success", id="start", disabled=True)
        yield Footer()

    def on_mount(self) -> None:
        self.title = "NoyAcg下载器"
        self.sub_title = f"{self.userinfo['Username']}[UID{self.userinfo['Uid']}][{self.userinfo['Email']}]"

    @on(TextArea.Changed, "#bid_inp")
    def input_watchdog(self):
        text = self.query_one("#bid_inp", TextArea).text.strip()
        self.query_one("#search").disabled = (text == "")

    async def handle_search(self) -> None:
        container = self.query_one("#container")
        await container.query(DataTable).remove()

        raw_text = self.query_one("#bid_inp", TextArea).text
        temp_bid_list = [line.strip()
                         for line in raw_text.splitlines() if line.strip()]
        self.bid_list = []
        for i in temp_bid_list:
            if i in self.bid_list:
                self.notify(message=f"填写了重复的Bid{i}，已忽略",severity="warning")
            else:
                self.bid_list.append(i)

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
            info = getBookInfo.getBookInfo(cookie=self.cookie, bid=bid)
            self.app.call_from_thread(self.fill_table, table, info)
        except Exception as e:
            self.notify(f"错误：获取 {bid} 失败: {e}", severity="error")

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
        self.query_one("#start", Button).disabled = True
        for bid in self.bid_list:
            info = getBookInfo.getBookInfo(self.cookie, bid=bid)
            if info['Bid'] == 1:
                self.notify(message=f"错误：BID{bid}无效",severity="error")
                continue
            self.notify(
                message=f"{info['Bookname']} | {info['Len']}Page(s) | 开始下载")
            return_message = getBook.getBook(
                bid=bid, path=self.config['download']['path'], bookinfo=info)
            if return_message != None:
                self.notify(message="错误："+str(return_message),severity="error")
            self.notify(
                message=f"{info['Bookname']} | {info['Len']}Page(s) | 下载完成")
        self.query_one("#start", Button).disabled = False
        self.notify(message="下载全部完成")


if __name__ == "__main__":
    app = NoyComicDownloader()
    app.run()