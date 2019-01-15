import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext
from PIL import Image

from sources.coreprocess import CoreProcess
from lib.ToolTip import Tooltip


def resize_image(path, width, height):
    """Resize image"""
    temp_path = path.split("/")
    name, extension = temp_path[len(temp_path)-1].split(".")
    image = Image.open(path)
    image = image.resize((width, height), Image.ANTIALIAS)
    path = "../images/_" + name + "." + extension
    image.save(path, extension)
    return path


class AdvanceFrame(tk.Frame):
    """An extended frame contains program setting"""
    def __init__(self, original, core_process):
        """Constructor"""
        tk.Frame.__init__(self, original)
        self.cp = core_process

        # ------------ VARIABLES ------------- #
        self.format_value = tk.StringVar()
        self.extension_value = tk.StringVar()
        self.folder_path_value = tk.StringVar()
        self.quality_value = tk.StringVar()
        self.restricted_value = tk.IntVar()
        self.format_value.set(self.get_format_setting())
        self.extension_value.set(self.cp.options["postprocessors"][0]["preferredcodec"])
        self.folder_path_value.set(self.cp.get_absolute_path(self.cp.options["outtmpl"]))
        self.quality_value.set("192")
        self.restricted_value.set(0)

        # -------------- LABEL --------------- #
        self.setting_lf = ttk.Labelframe(self, text="Setting", labelanchor=tk.N)
        self.format_lb = ttk.Label(self.setting_lf, text="Format")
        self.post_processor_lf = ttk.Labelframe(self.setting_lf, text="Post Processor")
        self.extension_lb = ttk.Label(self.post_processor_lf, text="File Extension")
        self.quality_lb = ttk.Label(self.post_processor_lf, text="Preferred Quality")
        self.storage_lb = ttk.Label(self.setting_lf, text="Save file location")
        self.restricted_file_name_lb = ttk.Label(self.setting_lf, text="Restrict file name", anchor=tk.CENTER)

        # -------------- ENTRY --------------- #
        self.path_entry = ttk.Entry(self.setting_lf, textvariable=self.folder_path_value, state="readonly")

        # ------------- COMBOBOX ------------- #
        self.format_cb = ttk.Combobox(self.setting_lf,
                                      textvariable=self.format_value,
                                      values=["Best Audio", "Worst Audio"],
                                      state="readonly")
        self.get_format_setting()
        self.format_cb.bind("<<ComboboxSelected>>", lambda event: self.on_change_value(event, "fm"))
        self.extension_cb = ttk.Combobox(self.post_processor_lf,
                                         textvariable=self.extension_value,
                                         values=["aac", "m4a", "mp3", "wav", "webm"],
                                         state="readonly")
        self.extension_cb.bind("<<ComboboxSelected>>", lambda event: self.on_change_value(event, "ext"))
        self.quality_cb = ttk.Combobox(self.post_processor_lf,
                                       textvariable=self.quality_value,
                                       values=["192"],
                                       state="readonly")

        # ------------- CHECKBOX ------------- #
        self.restricted_chb = ttk.Checkbutton(self.setting_lf,
                                              variable=self.restricted_value,
                                              command=self.on_check_box)

        # -------------- BUTTON -------------- #
        self.brow_bt = ttk.Button(self.setting_lf, text="Brow...", command=self.on_select_folder)
        self.close_bt = ttk.Button(self.setting_lf, text="Close", command=self.on_close)

        # -------------- ICON ---------------- #
        info_image = tk.PhotoImage(file=resize_image("../images/information-icon.png", 15, 15))
        self.info_icon = ttk.Label(self.post_processor_lf, image=info_image)
        self.info_icon.photo = info_image

        # ------------- TOOLTIP -------------- #
        Tooltip(self.info_icon, text="Currently support only 192", wrap_length=200)

        self.frame_layout()

    def frame_layout(self):
        """Manager frame layout"""
        # -------------- LABEL --------------- #
        self.setting_lf.pack(padx=5, pady=5)
        self.format_lb.grid(row=0, column=0, padx=5)
        self.post_processor_lf.grid(row=1, column=0, rowspan=2, columnspan=2, padx=5)
        self.extension_lb.grid(row=0, column=0, padx=2, pady=2)
        self.quality_lb.grid(row=1, column=0, padx=5, pady=5)
        self.storage_lb.grid(row=0, column=3, padx=5)
        self.restricted_file_name_lb.grid(row=1, column=3)

        # -------------- ENTRY --------------- #
        self.path_entry.grid(row=0, column=4)

        # ----------- OPTION MENU ------------ #
        self.format_cb.grid(row=0, column=1, padx=2)
        self.extension_cb.grid(row=0, column=1, padx=5, pady=5, sticky=tk.N)
        self.quality_cb.grid(row=1, column=1, padx=5, pady=5)

        # ------------- CHECKBOX ------------- #
        self.restricted_chb.grid(row=1, column=4, sticky=tk.W, padx=5)

        # -------------- BUTTON -------------- #
        self.brow_bt.grid(row=0, column=5, padx=5)
        self.close_bt.grid(columnspan=6, pady=5)

        # -------------- ICON ---------------- #
        self.info_icon.grid(row=1, column=3, padx=5)

    def on_change_value(self, event, name=""):
        """Change value of the setting based on input"""
        event.widget.selection_clear()
        if name == "fm":
            if self.format_value.get() == "Best Audio":
                self.cp.options["format"] = "bestaudio"
                return
            if self.format_value.get() == "Worst Audio":
                self.cp.options["format"] = "worstaudio"
                return
        if name == "ext":
            self.cp.options["postprocessors"][0]["preferredcodec"] = self.extension_value.get()

    def on_check_box(self):
        if self.restricted_value.get() == 0:
            self.cp.options["restrictfilenames"] = False
        else:
            self.cp.options["restrictfilenames"] = True

    def on_select_folder(self):
        """Open a dialog for user to choose a path"""
        self.folder_path_value.set(filedialog.askdirectory() + "/")

    def get_format_setting(self):
        """Set default format setting"""
        if self.cp.options["format"] == "bestaudio":
            return "Best Audio"
        if self.cp.options["format"] == "worstaudio":
            return "Worst Audio"

    def on_close(self):
        """Hide the frame"""
        self.grid_remove()


class YoutubeDownloader(object):
    """This sector handle GUI, and inherited from CoreProcess to process data."""

    def __init__(self):
        """Constructor"""
        self.core_process = CoreProcess()
        self.root = tk.Tk()
        self.root.title("YouTube downloader/converter")
        self.root.resizable(width=False, height=False)
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)

        # ------------ VARIABLES ------------- #
        option_choose = tk.BooleanVar()
        download_url_value = tk.StringVar()
        keyword_value = tk.StringVar()

        # ------------ MENU BAR -------------- #
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        menu_bar = tk.Menu(self.menu)
        self.menu.add_cascade(label="File", menu=menu_bar)
        menu_bar.add_command(label="About", command=self.about)
        menu_bar.add_command(label="Exit", command=self.on_exit)

        # -------------- FRAME --------------- #
        self.main_frame = tk.Frame(self.root)
        self.setting_frame = AdvanceFrame(self.root, self.core_process)

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
                                         command=lambda: self.on_change_option(self.option1_rb),
                                         variable=option_choose,
                                         value=0)
        self.option2_rb = tk.Radiobutton(self.main_frame,
                                         text="Search YouTube",
                                         command=lambda: self.on_change_option(self.option2_rb),
                                         variable=option_choose,
                                         value=1)

        # -------------- BUTTON -------------- #
        self.open_file_location_button = tk.Button(self.main_frame,
                                                   text="Open download folder",
                                                   command=self.on_open_file)
        self.search_and_download_button = tk.Button(self.main_frame,
                                                    text="Download/Search",
                                                    command=lambda: self.on_click_download(self.download_url_entry,
                                                                                           self.search_entry,
                                                                                           self.result_text,
                                                                                           download_url_value,
                                                                                           keyword_value))
        self.exit_button = tk.Button(self.main_frame, text="Exit", command=self.on_exit)
        self.setting_button = tk.Button(self.main_frame, text="Setting", command=self.on_open_setting)

        # -------------- LOGO ---------------- #
        logo_image = tk.PhotoImage(file=resize_image("../images/python_logo.png", 140, 140))
        self.logo_icon = ttk.Label(self.main_frame, image=logo_image)
        self.logo_icon.photo = logo_image

        self.window_layout()

    def window_layout(self):
        """Manage components layout of the window"""
        # -------------- FRAME --------------- #
        self.main_frame.grid()

        # -------------- LABEL --------------- #
        self.logo_title_label.grid(row=5, column=3)

        # -------------- LOGO ---------------- #
        self.logo_icon.grid(row=0, column=3, rowspan=5)

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
        """Show program info"""
        title = "About"
        info_msg = "YouTube Downloader/Converter\nVersion0.10.2412"
        messagebox.showinfo(title=title, message=info_msg)

    def on_exit(self):
        """Exit the programs"""
        title = "Confirm messages"
        confirm_msg = "Really want to exit the program?"
        if messagebox.askyesno(title=title, message=confirm_msg) is True:
            self.core_process.save_setting()
            self.root.quit()

    def on_open_file(self):
        """Attempt to open a file path contains audio files"""
        result = self.core_process.open_storage_file()
        if result is False:
            title = "Unable to open file"
            error_msg = "Folder not exist or wrong file path. Please check your configuration again!"
            messagebox.showerror(title=title, message=error_msg)

    def on_click_download(self, download_entry_state, keyword_entry_state, text_field, download_url, keyword):
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

    def on_change_option(self, radio_button):
        """Automate disabled Entry widget referent to the radio option user choose"""
        if radio_button["text"].startswith("Download"):
            self.download_url_entry.config(state=tk.NORMAL)
            self.search_entry.config(state=tk.DISABLED)
            return
        if radio_button["text"].startswith("Search"):
            self.search_entry.config(state=tk.NORMAL)
            self.download_url_entry.config(state=tk.DISABLED)

    def on_open_setting(self):
        """Open an extension of setting frame"""
        self.setting_frame.grid()
        # print(self.root.winfo_height(), self.root.winfo_width())


def main():
    """Start the application"""
    my_app = YoutubeDownloader()
    my_app.root.mainloop()


if __name__ == "__main__":
    main()
