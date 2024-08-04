# ╔════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦════╗
# ║  ╔═╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩═╗  ║
# ╠══╣                                                                                                            ╠══╣
# ║  ║    ALBUM ARTWORK DISPLAY                   CREATED: 2023-10-14          https://github.com/jacobleazott    ║  ║
# ║══║                                                                                                            ║══║
# ║  ╚═╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦══════╦═╝  ║
# ╚════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩══════╩════╝
# ═══════════════════════════════════════════════════ DESCRIPTION ════════════════════════════════════════════════════
# This is a fun little project to create an album artwork display. It takes a track_info.db file with the track name,
#   album_name, and artist_name. It then needs to have an album cover in Album/<album_name>.png
#
# It displays on a 4:5 aspect ratio monitor vertically. It shows the album artwork with the track title, album title,
#   and artist name.
# ════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
import sqlite3
from tkinter import *
import tkinter.font as tkFont
from PIL import Image, ImageTk
import Settings

root = Tk()
title = StringVar()
album = StringVar()
artist = StringVar()
album_image_label = Label(bd=0)

DISPLAY_WIDTH = 1024
DISPLAY_HEIGHT = 1280
IMAGE_SIZE = 1024
MAX_TEXT_WIDTH = 1000
TRACK_INFO_DB = "track_info.db"


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DESCRIPTION: <Configure> event for labels to dynamically adjust size based on font, text size and screen width
INPUT: event - tkinter event passed in automatically by bind
       var - StringVar object we will grab text from and update 
OUTPUT: NA
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def fit_label(event, var):
    label = event.widget
    font_text = label.cget("font").split('}')
    fonts = tkFont.Font(family=font_text[0][1:], size=font_text[1][1:3])
    actual_width = fonts.measure(var.get())
    text = var.get()

    if actual_width > MAX_TEXT_WIDTH:
        while actual_width > MAX_TEXT_WIDTH and len(text) > 1:
            text = text[:-1]
            actual_width = fonts.measure(text + "...")
        var.set(text+"...")


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DESCRIPTION: Grabs a random track from our db, populates the tkinter elements, and updates every 20s
INPUT: NA
OUTPUT: NA
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def update_album():
    conn = sqlite3.connect(TRACK_INFO_DB)
    # This is solely here to protect against not having a specific album png to not fail the code
    while True:
        try:
            track_data = conn.execute("SELECT * FROM 'info' ORDER BY RANDOM() LIMIT 1;").fetchone()
            album_image = ImageTk.PhotoImage(Image.open(f"Albums/{track_data[3]}.png").resize((IMAGE_SIZE, IMAGE_SIZE)))
            break
        except FileNotFoundError:
            continue

    title.set(track_data[0])
    artist.set(track_data[1])
    album.set(track_data[2])

    album_image_label.configure(image=album_image)
    album_image_label.image = album_image

    # root.update_idletasks()
    root.update()
    root.after(2000, update_album)


def main():
    if not Settings.debug:
        root.attributes("-fullscreen", Settings.fullscreen)
        root.overrideredirect(1)

    root.title("Spotify PLayer")
    root.geometry(f"{DISPLAY_WIDTH}x{DISPLAY_HEIGHT}")
    root.configure(bg=Settings.top_bg, cursor='none')

    pad = (DISPLAY_WIDTH - IMAGE_SIZE) / 2
    album_image_label.grid(column=0, row=0, padx=pad, pady=pad, sticky="NW")

    text_frame = Frame(root, bg=Settings.top_bg)
    text_frame.grid(column=0, row=1, sticky="NW", padx=20, pady=10)

    label_title = Label(text_frame, cnf=Settings.title_font, textvariable=title)
    label_artist = Label(text_frame, cnf=Settings.artist_font, textvariable=artist)
    label_album = Label(text_frame, cnf=Settings.album_font, textvariable=album)

    label_title.grid(column=1, row=1, sticky="NW")
    label_artist.grid(column=1, row=2, sticky="NW")
    label_album.grid(column=1, row=3, sticky="NW")

    label_title.bind("<Configure>", lambda event: fit_label(event, title))
    label_artist.bind("<Configure>", lambda event: fit_label(event, artist))
    label_album.bind("<Configure>", lambda event: fit_label(event, album))

    update_album()
    root.mainloop()


if __name__ == "__main__":
    main()

# FIN ════════════════════════════════════════════════════════════════════════════════════════════════════════════════
