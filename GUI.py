import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
from coreprocess import CoreProcess


class YoutubeDownloaderApp(object):
    """This sector handle GUI, and inherited from CoreProcess to process data."""

    def __init__(self, parent):
        """Constructor"""
        self.core_process = CoreProcess()
        self.LOGO_PATH = "/home/tqhung1/Works/github/CompletedPY/youtube-dl/python_logo.png"
        self.root = parent
        self.root.title("YouTube downloader/converter")
        self.root.resizable(width=False, height=False)
        self.root.protocol("WM_DELETE_WINDOW", self.exit_messages_box)
        self.frame = tk.Frame(parent)
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        self.frame.pack()

        # ------------ VARIABLES ------------- #
        option_choose = tk.BooleanVar()
        download_url_value = tk.StringVar()
        keyword_value = tk.StringVar()

        # ------------ MENU BAR -------------- #
        menu_bar = tk.Menu(self.menu)
        self.menu.add_cascade(label="File", menu=menu_bar)
        menu_bar.add_command(label="About", command=self.about)
        menu_bar.add_command(label="Exit", command=self.exit_messages_box)

        # ------------ LOGO -------------- #
        image = tk.PhotoImage(file=self.LOGO_PATH)
        canvas_width = canvas_height = 200
        self.canvas = tk.Canvas(self.frame, width=canvas_width, height=canvas_height)
        self.canvas.create_image(30, 30, anchor=tk.NW, image=image)

        # ------------ LABEL -------------- #
        self.download_from_url_label = tk.Label(self.frame, text="Direct download from URL:")
        self.search_label = tk.Label(self.frame, text="Search YouTube by keywords:")
        self.logo_title_label = tk.Label(self.frame, text="A Python applicant")

        # ------------ TEXT --------------- #
        self.result_text = scrolledtext.ScrolledText(self.frame, bd=2, height=20, width=40, state=tk.DISABLED)

        # ------------ ENTRY -------------- #
        self.download_url_entry = tk.Entry(self.frame, textvariable=download_url_value)
        self.search_entry = tk.Entry(self.frame, textvariable=keyword_value, state=tk.DISABLED)

        # ------------ RADIO BUTTON -------------- #
        self.option1_rb = tk.Radiobutton(self.frame,
                                         text="Download from URL",
                                         command=lambda: self.change_radio_option(self.option1_rb),
                                         variable=option_choose,
                                         value=0
                                         )
        self.option2_rb = tk.Radiobutton(self.frame,
                                         text="Search YouTube",
                                         command=lambda: self.change_radio_option(self.option2_rb),
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
                                                    command=lambda: self.download_button(self.download_url_entry,
                                                                                         self.search_entry,
                                                                                         self.result_text,
                                                                                         download_url_value,
                                                                                         keyword_value
                                                                                         )
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
        self.download_url_entry.grid(row=1, column=1)
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
        result = self.core_process.open_storage_file()
        if result is False:
            title = "Unable to open file"
            error_msg = "Folder not exist or wrong file path. Please check your configuration again!"
            messagebox.showerror(title=title, message=error_msg)

    def download_button(self, download_entry_state, keyword_entry_state, text_field, download_url, keyword):
        """
        Check which options does user choose: download an URL or search for keyword.

        :param Entry download_entry_state: The download url Entry Object.
        :param Entry keyword_entry_state: The search Entry Object.
        :param Text text_field: The result Text where all search result show.
        :param Object download_url: The tk Object which store the download entry value.
        :param Object keyword: The tk Object which store the search entry value.
        """
        if "normal" in download_entry_state.config()["state"] and download_url.get():
            self.core_process.download_video(download_url.get())
        elif "normal" in keyword_entry_state.config()["state"] and keyword.get():
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

    def change_radio_option(self, radio_button):
        """Automate disabled Entry widget referent to the radio option user choose"""
        if radio_button["text"].startswith("Download"):
            self.download_url_entry.config(state=tk.NORMAL)
            self.search_entry.config(state=tk.DISABLED)
        elif radio_button["text"].startswith("Search"):
            self.search_entry.config(state=tk.NORMAL)
            self.download_url_entry.config(state=tk.DISABLED)


def main():
    """Start the application"""
    root = tk.Tk()
    my_app = YoutubeDownloaderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
