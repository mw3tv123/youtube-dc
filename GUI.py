from tkinter import *
from tkinter import messagebox
from tkinter import filedialog


def create_components():
    root = Tk()
    root.title("YouTube downloader/converter")
    # root.geometry("170x200+30+30")
    frame = Frame(root)
    menu = Menu(root)
    root.config(menu=menu)

    # VARIABLES
    option_choose = BooleanVar()
    option_choose.set(0)

    frame.pack()

    # -----     DECLARE     ----- #

    # MENU
    filemenu = Menu(menu)
    menu.add_cascade(label="File", menu=filemenu)
    filemenu.add_command(label="New", command=new_file)
    filemenu.add_command(label="Open...", command=open_file_location)
    filemenu.add_command(label="Exit", command=exit_messages_box)

    # LABEL
    download_from_url_LABEL = Label(frame, text="Direct download from URL:")
    search_LABEL = Label(frame, text="Search YouTube by keywords:")
    logo = PhotoImage(file="./python_logo.png")
    logo_LABEL = Label(frame, image=logo)
    logo_title_LABEL = Label(frame, text="A Python applicant")
    result_TEXT = Text(frame, height=5, width=30)

    # ENTRY
    download_from_url_ENTRY = Entry(frame)
    search_ENTRY = Entry(frame)

    # BUTTON
    open_file_location_BUTTON = Button(frame,
                                       text="Open download folder",
                                       command=open_file_location
                                       )
    search_and_download_BUTTON = Button(frame,
                                        text="Download/Search",
                                        command=root.quit
                                        )
    exit_BUTTON = Button(frame, text="Exit", command=exit_messages_box)

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
    Radiobutton(frame, text="text 1", variable=option_choose, value=1).grid(row=1, column=0)
    Radiobutton(frame, text="text 2", variable=option_choose, value=2).grid(row=3, column=0)

    # TEXT
    result_TEXT.grid(row=4, column=0, rowspan=3, columnspan=2)

    # BUTTON
    open_file_location_BUTTON.grid(row=4, column=2)
    search_and_download_BUTTON.grid(row=5, column=2)
    exit_BUTTON.grid(row=6, column=2)

    root.mainloop()


def new_file():
    print("New File!")


def about():
    print("This is a simple example of a menu!")


def exit_messages_box():
    if messagebox.askyesno(title='Confirm log', message='Really want to exit the program?'):
        quit()


def open_file_location():
    file_manager_dialog = filedialog.askopenfilename()
    print(file_manager_dialog)


def main():
    create_components()


if __name__ == "__main__":
    main()
