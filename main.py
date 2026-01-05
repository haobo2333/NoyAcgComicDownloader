import tomllib
import tui

def gui():
    print("gui")

# Read config
with open(r"./config.toml","rb") as f:
    config = tomllib.load(f)

if config['gui'] == True:
    gui()
else:
    tui.app = tui.NoyComicDownloader(cookies=config['download']['cookies'],config=config)
    tui.app.run()