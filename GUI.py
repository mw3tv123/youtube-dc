# .-------------------.
# |      imports      |
# '-------------------'
from __future__ import absolute_import
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter.constants import *
import threading

from lib.coreprocess import CoreProcess
from lib.ToolTip import Tooltip
from lib.ProgressInlineLabel import PercentageLabel
from lib.observable import register, unregister
from lib.observer import Observer
from VERSION import VERSION

# .---------------.
# |   constants   |
# '---------------'
ORANGE = "#f5be2e"
BRIGHT_GREEN = "#b7f731"
DARK_GREY = "#191919"
MID_GREY = "#323232"
LIGHT_GREY = "#c8c8c8"

# .---------------.
# |    classes    |
# '---------------'
# =====================================Main Window==================================================================== #


class MainFrame(ttk.Frame, Observer):
    """Frame in the main menu"""
    def __init__(self, original, core_process):
        """Constructor"""
        self.cp = core_process
        self.master = original
        ttk.Frame.__init__(self, self.master)

        # ------------ VARIABLES ------------- #
        option_choose = tk.BooleanVar()
        self.download_url_value = tk.StringVar()
        self.keyword_value = tk.StringVar()
        self.download_status_value = tk.StringVar()
        self.current_progress_value = tk.DoubleVar()

        # -------------- STYLE --------------- #
        self.progressbar_style = PercentageLabel()

        # -------------- LABEL --------------- #
        self.logo_title_lb = ttk.Label(self, text="A Python applicant")
        self.download_status_lb = ttk.Label(self, textvariable=self.download_status_value)

        # -------------- TEXT ---------------- #
        self.result_lf = ttk.Labelframe(self, text="Result")
        self.result_txt = scrolledtext.ScrolledText(self.result_lf, height=25, width=55, state=tk.DISABLED)

        # ----------- PROGRESSBAR ------------ #
        self.download_pb = ttk.Progressbar(self,
                                           orient=HORIZONTAL,
                                           length=300,
                                           style="text.Horizontal.TProgressbar",
                                           variable=self.current_progress_value,
                                           mode="determinate")

        # -------------- ENTRY --------------- #
        self.download_url_et = ttk.Entry(self,
                                         textvariable=self.download_url_value,
                                         width=30,
                                         state=DISABLED)
        self.download_url_et.bind("<Return>", lambda event: self.on_click_download)
        self.search_et = ttk.Entry(self, textvariable=self.keyword_value, width=30, state=DISABLED)
        self.search_et.bind("<Return>", lambda event: self.on_click_download)

        # ----------- RADIO BUTTON ----------- #
        self.option1_rb = tk.Radiobutton(self,
                                         text="Download from URL",
                                         command=lambda: self.on_change_option(self.option1_rb),
                                         variable=option_choose,
                                         value=0)
        self.option2_rb = tk.Radiobutton(self,
                                         text="Search YouTube",
                                         command=lambda: self.on_change_option(self.option2_rb),
                                         variable=option_choose,
                                         value=1)

        # -------------- BUTTON -------------- #
        self.open_file_location_bt = ttk.Button(self, text="Open download folder", command=self.on_open_file)
        self.search_and_download_bt = ttk.Button(self, text="Download/Search", command=self.on_click_download)

        # -------------- IMAGE --------------- #
        download_icon = tk.PhotoImage(file=self.cp.resize_image("Spinner.gif", 30, 30))
        self.download_indicate_icon = ttk.Label(self, image=download_icon)
        self.download_indicate_icon.photo = download_icon

        self.frame_layout()

    def frame_layout(self):
        """Manage components layout of the window"""
        # -------------- ENTRY --------------- #
        self.download_url_et.grid(row=1, column=1)
        self.search_et.grid(row=2, column=1)

        # ----------- RADIO BUTTON ----------- #
        self.option1_rb.grid(row=1, column=0, sticky=W, padx=10, pady=5)
        self.option2_rb.grid(row=2, column=0, sticky=W, padx=10, pady=5)

        # -------------- TEXT ---------------- #
        self.result_lf.grid(row=6, column=0, rowspan=10, columnspan=3)
        self.result_txt.pack()

        # -------------- BUTTON -------------- #
        self.search_and_download_bt.grid(row=1, column=3, sticky=NSEW)
        self.open_file_location_bt.grid(row=2, column=3, sticky=NSEW)

    def on_open_file(self):
        """Attempt to open a file path contains audio files"""
        result = self.cp.open_storage_file()
        if result is False:
            title = "Unable to open file"
            error_msg = "Folder not exist or wrong file path. Please check your configuration again!"
            messagebox.showerror(title=title, message=error_msg)

    @staticmethod
    def _check_url(url):
        """Check URL"""
        if not url.startswith("https://www.youtube.com/watch?v="):
            return False
        return True

    def _start_download_progress(self, uri):
        """Split downloader function into a separate thread to avoid interferes with tkinter"""
        global downloading_thread
        downloading_thread = threading.Thread(target=self.cp.download_video, args=[uri])
        downloading_thread.daemon = True
        self.download_status_value.set(0)
        self.download_indicate_icon.grid(row=2, column=0, columnspan=2)
        self.download_pb.grid(row=3, column=0, columnspan=2)
        self.download_status_lb.grid(row=4, column=0, columnspan=2)
        downloading_thread.start()

    def download_status(self, *args, **kwargs):
        """Implement from Observer Class to get event info from download progress"""
        try:
            self.download_pb.config(maximum=args[0]["total_bytes"])
            self.download_pb.step()
            self.current_progress_value.set(args[0]["downloaded_bytes"])
            self.download_status_value.set(args[0]["status"])
            current_percent = int((args[0]["downloaded_bytes"]/args[0]["total_bytes"])*100)
            self.progressbar_style.configure('text.Horizontal.TProgressbar', text='{:g} %'.format(current_percent))
            if args[0]["downloaded_bytes"] == args[0]["total_bytes"]:
                completed_icon = tk.PhotoImage(file=self.cp.resize_image("Ok_check.png", 25, 25))
                self.download_indicate_icon.config(image=completed_icon)
                self.download_indicate_icon.photo = completed_icon
                self.after(2000, self.after_download)
        except KeyError as e:
            self.cp.store_log(e)

    def after_download(self):
        """Hide progress bar and its components"""
        self.download_pb.grid_remove()
        self.download_indicate_icon.grid_remove()
        self.download_status_lb.grid_remove()

    def on_click_download(self):
        """Check which options does user choose: download an URL or search for keyword."""
        url = self.download_url_value.get()
        if "normal" in self.download_url_et.config()["state"] and url:
            if self._check_url(url) is False:
                title = "Can't download the URL video"
                error_msg = "The URL is not valid!"
                messagebox.showerror(title=title, message=error_msg)
                return
            self._start_download_progress(url)
        elif "normal" in self.search_et.config()["state"] and self.keyword_value.get():
            result = self.cp.search_by_keywords(self.keyword_value.get())
            self.result_txt.config(state=NORMAL)
            self.result_txt.delete(1.0, END)
            for var in result:
                self.result_txt.insert(END, var + "\n")
        else:
            title = "No data input"
            warning_msg = "You haven't enter neither URL nor keywords yet. Enter it please!"
            messagebox.showwarning(title=title, message=warning_msg)

    def on_change_option(self, radio_button):
        """Automate disabled Entry widget referent to the radio option user choose"""
        if radio_button["text"].startswith("Download"):
            self.download_url_et.config(state=NORMAL)
            self.search_et.config(state=DISABLED)
        if radio_button["text"].startswith("Search"):
            self.search_et.config(state=NORMAL)
            self.download_url_et.config(state=DISABLED)

    def warning(self, *args, **kwargs):
        """Get warning flag"""
        messagebox.showwarning(message=args[0])

    def error(self, *args, **kwargs):
        """Show error while downloading"""
        self.after_download()
        title = args[0][:5]
        msg = args[0][7:]
        messagebox.showerror(title=title, message=msg)

# ===================================Setting Frame==================================================================== #


class SettingFrame(tk.Frame):
    """Frame contains all configuration"""
    def __init__(self, original, core_process):
        """Constructor"""
        self.cp = core_process
        self.master = original
        tk.Frame.__init__(self, self.master)

        # ------------ VARIABLES ------------- #
        self.format_value = tk.StringVar()
        self.extension_value = tk.StringVar()
        self.folder_path_value = tk.StringVar()
        self.quality_value = tk.StringVar()
        self.restricted_value = tk.BooleanVar()
        self.debug_mode_value = tk.BooleanVar()
        self.format_value.set(self.get_format_setting())
        self.extension_value.set(self.cp.options["postprocessors"][0]["preferredcodec"])
        self.folder_path_value.set(self.cp.default_storage_directory)
        self.quality_value.set("192")
        self.restricted_value.set(self.cp.options["restrictfilenames"])
        self.debug_mode_value.set(self.cp.options["debug_printtraffic"])

        # -------------- LABEL --------------- #
        self.setting_lf = ttk.Labelframe(self, text="Setting", labelanchor=tk.N)
        self.format_lb = ttk.Label(self.setting_lf, text="Format")
        self.post_processor_lf = ttk.Labelframe(self.setting_lf, text="Post Processor")
        self.extension_lb = ttk.Label(self.post_processor_lf, text="File Extension")
        self.quality_lb = ttk.Label(self.post_processor_lf, text="Preferred Quality")
        self.storage_lb = ttk.Label(self.setting_lf, text="Save file location")
        self.restricted_file_name_lb = ttk.Label(self.setting_lf, text="Restrict file name", anchor=tk.CENTER)
        self.debug_mode_lb = ttk.Label(self.setting_lf, text="Debug Mode")

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
                                              command=lambda: self.on_check_box("restrict"))
        self.debug_mode_chb = ttk.Checkbutton(self.setting_lf,
                                              variable=self.debug_mode_value,
                                              command=lambda: self.on_check_box("debug"))

        # -------------- BUTTON -------------- #
        self.brow_bt = ttk.Button(self.setting_lf, text="Brow...", command=self.on_select_folder)

        # -------------- ICON ---------------- #
        info_image = tk.PhotoImage(file=self.cp.resize_image("information-icon.png", 15, 15))
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
        self.debug_mode_lb.grid(row=2, column=3)

        # -------------- ENTRY --------------- #
        self.path_entry.grid(row=0, column=4)

        # ----------- OPTION MENU ------------ #
        self.format_cb.grid(row=0, column=1, padx=2)
        self.extension_cb.grid(row=0, column=1, padx=5, pady=5, sticky=tk.N)
        self.quality_cb.grid(row=1, column=1, padx=5, pady=5)

        # ------------- CHECKBOX ------------- #
        self.restricted_chb.grid(row=1, column=4, sticky=tk.W, padx=5)
        self.debug_mode_chb.grid(row=2, column=4, sticky=tk.W, padx=5)

        # -------------- BUTTON -------------- #
        self.brow_bt.grid(row=0, column=5, padx=5)

        # -------------- ICON ---------------- #
        self.info_icon.grid(row=1, column=3, padx=5)

    def on_change_value(self, event, name=""):
        """Change value of the setting based on input"""
        event.widget.selection_clear()
        if name == "fm":
            if self.format_value.get() == "Best Audio":
                self.cp.options["format"] = "bestaudio"
            if self.format_value.get() == "Worst Audio":
                self.cp.options["format"] = "worstaudio"
        if name == "ext":
            self.cp.options["postprocessors"][0]["preferredcodec"] = self.extension_value.get()

    def on_check_box(self, checkbox_id):
        """"""
        if checkbox_id == "restrict":
            self.cp.options["restrictfilenames"] = self.restricted_value.get()
        if checkbox_id == "debug":
            self.cp.options["debug_printtraffic"] = self.debug_mode_value.get()

    def on_select_folder(self):
        """Open a dialog for user to choose a path"""
        self.folder_path_value.set(filedialog.askdirectory() + "/")

    def get_format_setting(self):
        """Set default format setting"""
        if self.cp.options["format"] == "bestaudio":
            return "Best Audio"
        if self.cp.options["format"] == "worstaudio":
            return "Worst Audio"

# =====================================Main Window==================================================================== #


class YoutubeDownloader(object):
    """This sector handle GUI, and inherited from CoreProcess to process data."""
    def __init__(self):
        """Constructor"""
        register(self)
        self.core_process = CoreProcess()
        self.root = tk.Tk()
        self.root.title("YouTube downloader/converter")
        self.root.resizable(width=False, height=False)
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)

        # -------------- STYLE --------------- #
        self.style = ttk.Style()
        self.set_app_style()

        # ------------ MENU BAR -------------- #
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        menu_bar = tk.Menu(self.menu)
        self.menu.add_cascade(label="Options", menu=menu_bar)
        menu_bar.add_command(label="About", command=self.about)
        menu_bar.add_command(label="Exit", command=self.on_exit)

        # -------------- FRAME --------------- #
        self.window_frame = ttk.Frame(self.root)
        self.tab_nb = ttk.Notebook(self.window_frame)
        self.main_frame = MainFrame(self.tab_nb, self.core_process)
        self.setting_frame = SettingFrame(self.tab_nb, self.core_process)
        self.tab_nb.add(self.main_frame, text="Main")
        self.tab_nb.add(self.setting_frame, text="Setting")
        self.tab_nb.hide(self.setting_frame)
        self.tab_nb.hide(self.main_frame)

        # -------------- LABEL --------------- #
        self.logo_title_lb = ttk.Label(self.window_frame, text="A Python applicant")

        # -------------- IMAGE --------------- #
        logo_image = tk.PhotoImage(file=self.core_process.resize_image("python_logo.png", 140, 140))
        self.logo_icon = ttk.Label(self.window_frame, image=logo_image)
        self.logo_icon.photo = logo_image

        # -------------- BUTTON -------------- #
        self.main_bt = ttk.Button(self.window_frame, text="Main", command=lambda: self.switch_tab("main"))
        self.setting_bt = ttk.Button(self.window_frame, text="Setting", command=lambda: self.switch_tab("setting"))

        self.window_layout()

    def set_app_style(self):
        """Define the Application style"""
        self.style.theme_create("st_app", parent="alt", settings={
            ".": {"configure": {"background": DARK_GREY,
                                "foreground": LIGHT_GREY,
                                "relief": "flat",
                                "highlightcolor": BRIGHT_GREEN}},

            "TLabel": {"configure": {"foreground": BRIGHT_GREEN,
                                     "padding": 10,
                                     "font": ("Calibri", 12)}},

            "TNotebook": {"configure": {"padding": 5}},
            "TNotebook.Tab": {"configure": {"padding": [25, 5],
                                            "foreground": "white"},
                              "map": {"background": [("selected", MID_GREY)],
                                      "expand": [("selected", [1, 1, 1, 0])]}},

            "TCombobox": {"configure": {"font": ("Calibri", 13, "bold"),
                                        "selectbackground": DARK_GREY,
                                        "fieldbackground": "white",
                                        "background": LIGHT_GREY,
                                        "foreground": "black"}},

            "TButton": {"configure": {"font": ("Calibri", 13, 'bold'),
                                      "background": "black",
                                      "foreground": BRIGHT_GREEN},
                        "map": {"background": [("active", BRIGHT_GREEN)],
                                "foreground": [("active", "black")]}},

            "TEntry": {"configure": {"foreground": "black"}},
            "Horizontal.TProgressbar": {"configure": {"background": MID_GREY}}
        })
        self.style.theme_use("st_app")

    def window_layout(self):
        """Manage components layout of the window"""
        # -------------- FRAME --------------- #
        self.window_frame.pack()
        self.tab_nb.grid(row=0, column=1, rowspan=15)

        # -------------- LABEL --------------- #
        self.logo_title_lb.grid(row=1, column=0)

        # -------------- IMAGE --------------- #
        self.logo_icon.grid(row=0, column=0, padx=15, pady=15)

        # -------------- BUTTON -------------- #
        self.main_bt.grid(row=2, column=0, sticky=NSEW)
        self.setting_bt.grid(row=3, column=0, sticky=NSEW)

    @staticmethod
    def about():
        """Show program info"""
        title = "About"
        info_msg = "YouTube Downloader/Converter\nVersion " + VERSION
        messagebox.showinfo(title=title, message=info_msg)

    def switch_tab(self, clicked_button):
        if clicked_button == "main":
            # self.tab_nb.add(self.main_frame)
            self.tab_nb.select(0)
            self.tab_nb.hide(self.setting_frame)
        else:
            # self.tab_nb.add(self.setting_frame)
            self.tab_nb.select(1)
            self.tab_nb.hide(self.main_frame)

    def on_exit(self):
        """Exit the programs"""
        title = "Confirm messages"
        confirm_msg = "Really want to exit the program?"
        if messagebox.askyesno(title=title, message=confirm_msg) is True:
            unregister(self)
            self.core_process.save_setting()
            self.root.quit()


if __name__ == "__main__":
    """Start the application"""
    my_app = YoutubeDownloader()
    my_app.root.mainloop()

# https://www.youtube.com/watch?v=a9I2Wwm11pg