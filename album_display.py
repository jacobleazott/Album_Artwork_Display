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
from PIL import Image, ImageTk, ImageStat
import pathlib

import Settings

root = Tk()
fullscreen = True

title = StringVar()
album = StringVar()
artist = StringVar()

DISPLAY_WIDTH = 1024
DISPLAY_HEIGHT = 1280
IMAGE_SIZE = 1024

pwd = str(pathlib.Path().absolute()) + '/'
track_info_db = "track_info.db"

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DESCRIPTION: Grabs a random track from our db, populates the tkinter elements, and updates every 20s
INPUT: NA
OUTPUT: NA
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def update_album():
    conn = sqlite3.connect(track_info_db)

    track_data = conn.execute("SELECT * FROM 'info' ORDER BY RANDOM() LIMIT 1;").fetchone()

    title.set(track_data[0])
    artist.set(track_data[1])
    album.set(track_data[2])

    img = Image.open(pwd + f"Albums/{track_data[3]}.png")
    img = img.resize((IMAGE_SIZE, IMAGE_SIZE))
    img2 = ImageTk.PhotoImage(img)

    album_image_label.configure(image=img2)
    album_image_label.image = img2

    # Find median color value
    # try:
    #     stat = ImageStat.Stat(img).median
    #     value = '#%02x%02x%02x' % (int(stat[0]), int(stat[1]), int(stat[2]))
    # except IndexError:
    #     value = '#000000'

    # Bring text and album above gradient
    album_image_label.lift()
    # text_frame.lift()
    root.update_idletasks()

    root.after(2000, update_album)


def main():
    if not Settings.debug:-
    root.attributes("-fullscreen", fullscreen)
    root.overrideredirect(1)
    root.title("Spotify PLayer")
    root.geometry(f"{DISPLAY_WIDTH}x{DISPLAY_HEIGHT}")
    root.configure(bg=Settings.top_bg, cursor='none')
    # root.wm_attributes('-transparentcolor', '#606060')

    # Album
    album_image_label = Label(bd=0)
    pad = (DISPLAY_WIDTH - IMAGE_SIZE) / 2
    album_image_label.grid(column=0, row=0, padx=pad, pady=pad, sticky="NW")


    text_frame = Frame(root, bg=Settings.top_bg, width=1024, height=300)
    text_frame.grid(column=0, row=1, sticky="NW", padx=20, pady=20)

    """
    canvas = Canvas(text_frame, width=1024, height=100)
    image = ImageTk.PhotoImage(GUI_Gradient.gradient("#0000FF", "#181818", 100, 1024))
    canvas.create_image(0, 0, image=image, anchor=NW)
    canvas.create_text(0, 0, text="Is There Anyone Out There", font=('times', 60), anchor=NW)
    canvas.grid(column=1, row=0, sticky="NW", padx=0, pady=20)
    """
    label_title = Label(text_frame, Settings.title_font, textvariable=title, width=1024, anchor="w")
    label_artist = Label(text_frame, Settings.artist_font, textvariable=artist)
    label_album = Label(text_frame, Settings.album_font, textvariable=album)

    label_title.grid(column=1, row=0, sticky="W", pady=5)
    label_artist.grid(column=1, row=1, sticky="W", pady=5)
    label_album.grid(column=1, row=2, sticky="W", pady=5)

    update_album()
    root.mainloop()


if __name__ == "__main__":
    main()

# FIN ════════════════════════════════════════════════════════════════════════════════════════════════════════════════