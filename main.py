import tomllib
import tui
import getBookInfo


def gui():
    print("gui")

# Read config
with open(r"./config.toml", "rb") as f:
    config = tomllib.load(f)

# Check
print("cookie可用") if getBookInfo.check(config['download']['cookie']) else (print("cookie不可用"), exit())

if config['gui'] == True:
    print("Starting GUI......")
    gui()
else:
    print("Starting TUI......")
    tui.app = tui.NoyComicDownloader(
        cookie=config['download']['cookie'], config=config)
    tui.app.run()
