import tkinter


def create_components():
    root = tkinter.Tk()
    root.title("YouTube downloader/converter")
    # root.geometry("170x200+30+30")
    frame = tkinter.Frame(root)

    # VARIABLES
    option_choose = tkinter.BooleanVar()
    option_choose.set(0)

    frame.pack()

    # -----     DECLARE     ----- #

    download_from_url_LABEL = tkinter.Label(frame, text="Direct download from URL:")
    search_LABEL = tkinter.Label(frame, text="Search YouTube by keywords:")
    download_from_url_ENTRY = tkinter.Entry(frame)
    search_ENTRY = tkinter.Entry(frame)

    logo = tkinter.PhotoImage(file="./python_logo.png")
    logo_LABEL = tkinter.Label(frame, image=logo)
    logo_title_LABEL = tkinter.Label(frame, text="A Python applicant")

    result_TEXT = tkinter.Text(frame, height=5, width=30)

    open_file_location_BUTTON = tkinter.Button(frame, text="Open download folder", command=quit)
    search_and_download_BUTTON = tkinter.Button(frame, text="download/search", command=quit)
    exit_BUTTON = tkinter.Button(frame, text="Exit", command=quit)

    # ----     LAYOUT     ---- #

    # LABEL
    download_from_url_LABEL.grid(row=0, column=0, columnspan=2)
    search_LABEL.grid(row=2, column=0, columnspan=2)
    logo_LABEL.grid(row=0, column=2, rowspan=3)
    logo_title_LABEL.grid(row=3, column=2)

    # ENTRY
    download_from_url_ENTRY.grid(row=1, column=1)
    search_ENTRY.grid(row=3, column=1)

    # RADIO BUTTON
    tkinter.Radiobutton(frame, text="text 1", variable=option_choose, value=1).grid(row=1, column=0)
    tkinter.Radiobutton(frame, text="text 2", variable=option_choose, value=2).grid(row=3, column=0)

    # TEXT
    result_TEXT.grid(row=4, column=0, rowspan=3, columnspan=2)

    # BUTTON
    open_file_location_BUTTON.grid(row=4, column=2)
    search_and_download_BUTTON.grid(row=5, column=2)
    exit_BUTTON.grid(row=6, column=2)

    root.mainloop()


def main():
    create_components()


if __name__ == "__main__":
    main()
