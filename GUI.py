import tkinter
from tkinter import messagebox
from tkinter import filedialog
from coreprocess import CoreProcess

"""
    This sector handle GUI, and inherit from CoreProcess to process data.
"""

# VARIABLES
core_process = CoreProcess()
root = tkinter.Tk()
root.title("YouTube downloader/converter")
path = "./python_logo.png"
option_choose = tkinter.BooleanVar()
download_url_value = tkinter.StringVar()
keyword_value = tkinter.StringVar()
option_choose.set(0)


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


def on_click_download_button():
    if download_url_value.get():
        core_process.download_video(download_url_value.get())
    elif keyword_value.get():
        result = core_process.search_by_keywords(keyword_value.get())
        for var in result:
            print(var)
    else:
        title = "No data input"
        msg = "You haven't enter neither URL nor keywords yet. Enter it please!"
        messagebox.showwarning(title=title, message=msg)


def main():
    root.resizable(width=False, height=False)
    root.protocol("WM_DELETE_WINDOW", exit_messages_box)
    frame = tkinter.Frame(root)
    menu = tkinter.Menu(root)
    root.config(menu=menu)
    frame.pack()

    # -----     DECLARE     ----- #

    # MENU
    filemenu = tkinter.Menu(menu)
    menu.add_cascade(label="File", menu=filemenu)
    filemenu.add_command(label="New", command=new_file)
    filemenu.add_command(label="Open...", command=open_file_location)
    filemenu.add_command(label="Exit", command=exit_messages_box)

    # LOGO
    image = tkinter.PhotoImage(file='./python_logo.png')
    canvas_width = canvas_height = 240
    canvas = tkinter.Canvas(frame, width=canvas_width, height=canvas_height)
    canvas.create_image(30, 30, anchor=tkinter.NW, image=image)

    # LABEL
    download_from_url_label = tkinter.Label(frame, text="Direct download from URL:")
    search_label = tkinter.Label(frame, text="Search YouTube by keywords:")
    logo_title_label = tkinter.Label(frame, text="A Python applicant")
    result_text = tkinter.Text(frame, height=5, width=45)

    # ENTRY
    download_from_url_entry = tkinter.Entry(frame, textvariable=download_url_value)
    search_entry = tkinter.Entry(frame, textvariable=keyword_value)

    # RADIO BUTTON
    option1 = tkinter.Radiobutton(frame, text="Download from URL", variable=option_choose, value=1)
    option2 = tkinter.Radiobutton(frame, text="Search YouTube", variable=option_choose, value=0)

    # BUTTON
    open_file_location_button = tkinter.Button(frame, text="Open download folder", command=open_file_location)
    search_and_download_button = tkinter.Button(frame, text="Download/Search", command=on_click_download_button)
    exit_button = tkinter.Button(frame, text="Exit", command=exit_messages_box)

    # ----     LAYOUT     ---- #

    # LABEL
    download_from_url_label.grid(row=0, column=0, columnspan=2)
    search_label.grid(row=2, column=0, columnspan=2)
    logo_title_label.grid(row=7, column=2)

    # LOGO
    canvas.grid(row=0, column=2, rowspan=5)

    # ENTRY
    download_from_url_entry.grid(row=1, column=1)
    search_entry.grid(row=3, column=1)

    # RADIO BUTTON
    option1.grid(row=1, column=0)
    option2.grid(row=3, column=0)

    # TEXT
    result_text.grid(row=4, column=0, rowspan=10, columnspan=2)

    # BUTTON
    open_file_location_button.grid(row=8, column=2)
    search_and_download_button.grid(row=9, column=2)
    exit_button.grid(row=10, column=2)

    root.mainloop()


if __name__ == "__main__":
    main()
