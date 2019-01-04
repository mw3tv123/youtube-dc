import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from coreprocess import CoreProcess


class YoutubeDownloaderApp(object):
    """This sector handle GUI, and inherit from CoreProcess to process data."""
    core_process = CoreProcess()
    LOGO_PATH = "/home/tqhung1/Works/github/CompletedPY/youtube-dl/python_logo.png"

    def __init__(self, parent):
        """Constructor"""
        self.root = parent
        self.root.title("YouTube downloader/converter")
        self.root.resizable(width=False, height=False)
        self.root.protocol("WM_DELETE_WINDOW", self.exit_messages_box)
        self.frame = tk.Frame(parent)
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        self.frame.pack()

        option_choose = tk.BooleanVar()
        download_url_value = tk.StringVar()
        keyword_value = tk.StringVar()

        # ------------ MENU BAR -------------- #
        menu_bar = tk.Menu(self.menu)
        self.menu.add_cascade(label="File", menu=menu_bar)
        menu_bar.add_command(label="Open...", command=self.open_file_location)
        menu_bar.add_command(label="About", command=self.about)
        menu_bar.add_command(label="Exit", command=self.exit_messages_box)

        # ------------ LOGO -------------- #
        image = tk.PhotoImage(file=self.LOGO_PATH)
        canvas_width = canvas_height = 240
        self.canvas = tk.Canvas(self.frame, width=canvas_width, height=canvas_height)
        self.canvas.create_image(30, 30, anchor=tk.NW, image=image)

        # ------------ LABEL -------------- #
        self.download_from_url_label = tk.Label(self.frame, text="Direct download from URL:")
        self.search_label = tk.Label(self.frame, text="Search YouTube by keywords:")
        self.logo_title_label = tk.Label(self.frame, text="A Python applicant")
        self.result_text = tk.Text(self.frame, bd=2, height=20, width=40, state=tk.DISABLED)

        # ------------ ENTRY -------------- #
        self.download_from_url_entry = tk.Entry(self.frame, textvariable=download_url_value)
        self.search_entry = tk.Entry(self.frame, textvariable=keyword_value, state=tk.DISABLED)

        # ------------ RADIO BUTTON -------------- #
        self.option1_rb = tk.Radiobutton(self.frame,
                                         text="Download from URL",
                                         variable=option_choose,
                                         value=0
                                         )
        self.option2_rb = tk.Radiobutton(self.frame,
                                         text="Search YouTube",
                                         variable=option_choose,
                                         value=1
                                         )

        # ------------ BUTTON -------------- #
        self.open_file_location_button = tk.Button(self.frame,
                                                   text="Open download folder",
                                                   command=self.open_file_location
                                                   )
        self.search_and_download_button = tk.Button(self.frame,
                                                    text="Download/Search",
                                                    command=lambda: self.on_click_download_button(self.result_text, download_url_value, keyword_value)
                                                    )
        self.exit_button = tk.Button(self.frame, text="Exit", command=self.exit_messages_box)

        self.window_layout()

    def window_layout(self):
        """Manage components layout of the window"""
        # LABEL
        self.download_from_url_label.grid(row=0, column=0, columnspan=2)
        self.search_label.grid(row=2, column=0, columnspan=2)
        self.logo_title_label.grid(row=7, column=2)

        # LOGO
        self.canvas.grid(row=0, column=2, rowspan=7)

        # ENTRY
        self.download_from_url_entry.grid(row=1, column=1)
        self.search_entry.grid(row=3, column=1)

        # RADIO BUTTON
        self.option1_rb.grid(row=1, column=0)
        self.option2_rb.grid(row=3, column=0)

        # TEXT
        self.result_text.grid(padx=10, pady=10, row=4, column=0, rowspan=10, columnspan=2)

        # BUTTON
        self.open_file_location_button.grid(row=8, column=2)
        self.search_and_download_button.grid(row=9, column=2)
        self.exit_button.grid(row=10, column=2)

    def about(self):
        """"""
        title = "About"
        info_msg = "YouTube Downloader/Converter\nVersion0.10.2412"
        messagebox.showinfo(title=title, message=info_msg)

    def exit_messages_box(self):
        """"""
        title = "Confirm messages"
        confirm_msg = "Really want to exit the program?"
        if messagebox.askyesno(title=title, message=confirm_msg) is True:
            self.root.quit()

    def open_file_location(self):
        """"""
        file_manager_dialog = filedialog.askopenfilename()
        print(file_manager_dialog)

    def on_click_download_button(self, text_field, download_url, keyword):
        """"""
        if download_url.get():
            self.core_process.download_video(download_url.get())
        elif keyword.get():
            result = self.core_process.search_by_keywords(keyword.get())
            text_field.config(state=tk.NORMAL)
            text_field.delete(1.0, tk.END)
            for var in result:
                text_field.insert(tk.END, var + "\n")
            text_field.config(state=tk.DISABLED)
        else:
            title = "No data input"
            warning_msg = "You haven't enter neither URL nor keywords yet. Enter it please!"
            messagebox.showwarning(title=title, message=warning_msg)


def main():
    root = tk.Tk()
    my_app = YoutubeDownloaderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
