import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext
from coreprocess import CoreProcess


class AdvanceFrame(tk.Frame):
    """"""
    def __init__(self, original):
        """Constructor"""
        tk.Frame.__init__(self, original)

        # ------------ VARIABLES ------------- #
        option_value = tk.StringVar()
        extension_value = tk.StringVar()
        folder_path_value = tk.StringVar()

        # -------------- LABEL --------------- #
        self.setting_lf = ttk.Labelframe(self, text="Setting", labelanchor=tk.N)
        self.format_lb = ttk.Label(self.setting_lf, text="Format")
        self.post_processor_lf = ttk.Labelframe(self.setting_lf, text="Post Processor")
        self.extension_lb = ttk.Label(self.post_processor_lf, text="File Extension")
        self.storage_lb = ttk.Label(self.setting_lf, text="Save file location")

        # -------------- ENTRY --------------- #
        self.path_entry = ttk.Entry(self.setting_lf, textvariable=folder_path_value, state=tk.DISABLED)

        # ------------- COMBOBOX ------------- #
        self.format_cb = ttk.Combobox(self.setting_lf, textvariable=option_value, state="readonly")
        self.format_cb["value"] = ("Best Audio", "Worst Audio")
        self.format_cb.bind("<<ComboboxSelected>>", self.onChangeValue)
        self.extension_cb = ttk.Combobox(self.post_processor_lf, textvariable=extension_value, state="readonly")
        self.extension_cb["value"] = ("aac", "m4a", "mp3", "wav", "webm")
        self.extension_cb.bind("<<ComboboxSelected>>", self.onChangeValue)

        # -------------- BUTTON -------------- #
        self.brow_bt = ttk.Button(self.setting_lf,
                                  text="Brow...",
                                  command=lambda: self.onSelectFolder(folder_path_value))
        self.close_bt = ttk.Button(self.setting_lf, text="Close", command=self.onClose)

        self.frame_layout()

    def frame_layout(self):
        """"""
        # -------------- LABEL --------------- #
        self.setting_lf.pack()
        self.format_lb.grid(row=0, column=0)
        self.post_processor_lf.grid(row=1, column=0, columnspan=2)
        self.extension_lb.grid(row=0, column=0)
        self.storage_lb.grid(row=0, column=3)

        # -------------- ENTRY --------------- #
        self.path_entry.grid(row=0, column=4)

        # ----------- OPTION MENU ------------ #
        self.format_cb.grid(row=0, column=1)
        self.extension_cb.grid(row=0, column=1)

        # -------------- BUTTON -------------- #
        self.brow_bt.grid(row=0, column=5)
        self.close_bt.grid(columnspan=6)

    def onClose(self):
        """"""
        self.grid_remove()

    def onChangeValue(self, event):
        """"""
        event.widget.selection_clear()

    def onSelectFolder(self, folder_path):
        folder_path.set(filedialog.askdirectory())


class YoutubeDownloaderApp(object):
    """This sector handle GUI, and inherited from CoreProcess to process data."""

    def __init__(self):
        """Constructor"""
        self.core_process = CoreProcess()
        self.root = tk.Tk()
        self.root.title("YouTube downloader/converter")
        self.root.resizable(width=False, height=False)
        self.root.protocol("WM_DELETE_WINDOW", self.onExit)

        # -------------- FRAME --------------- #
        self.main_frame = tk.Frame(self.root)
        self.setting_frame = AdvanceFrame(self.root)

        # ------------ VARIABLES ------------- #
        option_choose = tk.BooleanVar()
        download_url_value = tk.StringVar()
        keyword_value = tk.StringVar()
        logo_path = "./python_logo.png"

        # ------------ MENU BAR -------------- #
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        menu_bar = tk.Menu(self.menu)
        self.menu.add_cascade(label="File", menu=menu_bar)
        menu_bar.add_command(label="About", command=self.about)
        menu_bar.add_command(label="Exit", command=self.onExit)

        # -------------- LOGO ---------------- #
        image = tk.PhotoImage(file=logo_path)
        canvas_width = canvas_height = 200
        self.canvas = tk.Canvas(self.main_frame, width=canvas_width, height=canvas_height)
        self.canvas.create_image(30, 30, anchor=tk.NW, image=image)

        # -------------- LABEL --------------- #
        self.logo_title_label = tk.Label(self.main_frame, text="A Python applicant")

        # -------------- TEXT ---------------- #
        self.result_labelframe = ttk.Labelframe(self.main_frame, text="Result")
        self.result_text = scrolledtext.ScrolledText(self.result_labelframe, height=25, width=55, state=tk.DISABLED)

        # -------------- ENTRY --------------- #
        self.download_url_entry = tk.Entry(self.main_frame,
                                           textvariable=download_url_value,
                                           width=30,
                                           state=tk.DISABLED)
        self.search_entry = tk.Entry(self.main_frame,
                                     textvariable=keyword_value,
                                     width=30,
                                     state=tk.DISABLED)

        # ----------- RADIO BUTTON ----------- #
        self.option1_rb = tk.Radiobutton(self.main_frame,
                                         text="Download from URL",
                                         command=lambda: self.onChangeOption(self.option1_rb),
                                         variable=option_choose,
                                         value=0)
        self.option2_rb = tk.Radiobutton(self.main_frame,
                                         text="Search YouTube",
                                         command=lambda: self.onChangeOption(self.option2_rb),
                                         variable=option_choose,
                                         value=1)

        # -------------- BUTTON -------------- #
        self.open_file_location_button = tk.Button(self.main_frame,
                                                   text="Open download folder",
                                                   command=self.onOpenFile)
        self.search_and_download_button = tk.Button(self.main_frame,
                                                    text="Download/Search",
                                                    command=lambda: self.onClickDownload(self.download_url_entry,
                                                                                         self.search_entry,
                                                                                         self.result_text,
                                                                                         download_url_value,
                                                                                         keyword_value))
        self.exit_button = tk.Button(self.main_frame, text="Exit", command=self.onExit)
        self.setting_button = tk.Button(self.main_frame, text="Setting", command=self.onOpenSetting)

        self.window_layout()

    def window_layout(self):
        """Manage components layout of the window"""
        # -------------- FRAME --------------- #
        self.main_frame.grid()

        # -------------- LABEL --------------- #
        self.logo_title_label.grid(row=5, column=3)

        # -------------- LOGO ---------------- #
        self.canvas.grid(row=0, column=3, rowspan=5)

        # -------------- ENTRY --------------- #
        self.download_url_entry.grid(row=0, column=1)
        self.search_entry.grid(row=2, column=1)

        # ----------- RADIO BUTTON ----------- #
        self.option1_rb.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.option2_rb.grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)

        # -------------- TEXT ---------------- #
        self.result_labelframe.grid(row=3, column=0, rowspan=8, columnspan=3)
        self.result_text.pack()

        # -------------- BUTTON -------------- #
        self.open_file_location_button.grid(row=8, column=3)
        self.search_and_download_button.grid(row=9, column=3)
        self.exit_button.grid(row=10, column=3)
        self.setting_button.grid(row=7, column=3)

    @staticmethod
    def about():
        """"""
        title = "About"
        info_msg = "YouTube Downloader/Converter\nVersion0.10.2412"
        messagebox.showinfo(title=title, message=info_msg)

    def onExit(self):
        """"""
        title = "Confirm messages"
        confirm_msg = "Really want to exit the program?"
        if messagebox.askyesno(title=title, message=confirm_msg) is True:
            self.root.quit()

    def onOpenFile(self):
        """"""
        result = self.core_process.open_storage_file()
        if result is False:
            title = "Unable to open file"
            error_msg = "Folder not exist or wrong file path. Please check your configuration again!"
            messagebox.showerror(title=title, message=error_msg)

    def onClickDownload(self, download_entry_state, keyword_entry_state, text_field, download_url, keyword):
        """
        Check which options does user choose: download an URL or search for keyword.

        :param Entry download_entry_state: The download url Entry Object.
        :param Entry keyword_entry_state: The search Entry Object.
        :param Text text_field: The result Text where all search result show.
        :param Object download_url: The tk Object which store the download entry value.
        :param Object keyword: The tk Object which store the search entry value.
        """
        if "normal" in download_entry_state.config()["state"] and download_url.get():
            result = self.core_process.download_video(download_url.get())
            if result is False:
                title = "Can't download the URL video"
                error_msg = "The URL is not valid!"
                messagebox.showerror(title=title, message=error_msg)
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

    def onChangeOption(self, radio_button):
        """Automate disabled Entry widget referent to the radio option user choose"""
        if radio_button["text"].startswith("Download"):
            self.download_url_entry.config(state=tk.NORMAL)
            self.search_entry.config(state=tk.DISABLED)
        elif radio_button["text"].startswith("Search"):
            self.search_entry.config(state=tk.NORMAL)
            self.download_url_entry.config(state=tk.DISABLED)

    def onOpenSetting(self):
        """"""
        self.setting_frame.grid()


def main():
    """Start the application"""
    my_app = YoutubeDownloaderApp()
    my_app.root.mainloop()


if __name__ == "__main__":
    main()
