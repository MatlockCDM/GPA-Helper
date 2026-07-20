import os
import platform
import queue
import re
import subprocess
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk


APP_NAME = "GPA Helper"
REVIEW_INTERVALS = (1, 3, 5, 10, 20, 40, 105, 365)
LEGACY_CONFIG_FILE = Path(__file__).resolve().with_name("config.txt")

COLORS = {
    "background": "#F4F7FB",
    "surface": "#FFFFFF",
    "navy": "#172A46",
    "muted": "#65758B",
    "blue": "#2563EB",
    "blue_hover": "#1D4ED8",
    "teal": "#0F9F8F",
    "teal_hover": "#0B8276",
    "gold": "#F5B942",
    "border": "#DCE3EC",
}


def config_file_path():
    """Return a user-writable, platform-appropriate settings path."""
    system = platform.system()
    if system == "Windows":
        root = Path(os.environ.get("APPDATA", Path.home()))
    elif system == "Darwin":
        root = Path.home() / "Library" / "Application Support"
    else:
        root = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    return root / "GPA Helper" / "config.txt"


def resource_path(relative_path):
    """Resolve bundled resources in development and PyInstaller builds."""
    bundle_root = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    return bundle_root / relative_path


def numbered_folders(base_directory):
    """Map each leading lesson number to its folder path."""
    folders = {}
    for root, dirs, _ in os.walk(base_directory):
        dirs.sort(key=str.casefold)
        for folder in dirs:
            match = re.match(r"^(\d+)", folder)
            if match:
                number = int(match.group(1))
                # Prefer the first, shallowest deterministic match for duplicates.
                folders.setdefault(number, os.path.join(root, folder))
    return folders


def review_folders(folder_numbers):
    """Select the newest lesson and available spaced-review lessons."""
    if not folder_numbers:
        return []
    newest = max(folder_numbers)
    selected = [newest]
    selected.extend(
        newest - interval
        for interval in REVIEW_INTERVALS
        if newest - interval in folder_numbers
    )
    return [(number, folder_numbers[number]) for number in selected]


class FolderBrowserApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("980x640")
        self.root.minsize(760, 500)
        self.root.configure(bg=COLORS["background"])
        icon_path = resource_path("assets/icon.png")
        if icon_path.exists():
            try:
                self.window_icon = tk.PhotoImage(file=icon_path)
                self.root.iconphoto(True, self.window_icon)
            except tk.TclError:
                pass

        self.base_directory = self.load_last_directory()
        self.folder_map = {}
        self.folder_buttons = {}
        self.opened_folders = set()
        self.result_paths = []
        self.search_generation = 0
        self.search_results = queue.Queue()

        self._configure_styles()
        self._build_ui()

        if self.base_directory:
            self.search_folders(show_empty_message=False)
        else:
            self._show_folder_placeholder("Choose your lessons folder to get started.")

    def _configure_styles(self):
        style = ttk.Style(self.root)
        if "clam" in style.theme_names():
            style.theme_use("clam")

        style.configure("App.TFrame", background=COLORS["background"])
        style.configure("Surface.TFrame", background=COLORS["surface"])
        style.configure(
            "Header.TLabel", background=COLORS["background"],
            foreground=COLORS["navy"], font=("Helvetica", 25, "bold")
        )
        style.configure(
            "Subtitle.TLabel", background=COLORS["background"],
            foreground=COLORS["muted"], font=("Helvetica", 11)
        )
        style.configure(
            "Section.TLabel", background=COLORS["surface"],
            foreground=COLORS["navy"], font=("Helvetica", 14, "bold")
        )
        style.configure(
            "Muted.TLabel", background=COLORS["surface"],
            foreground=COLORS["muted"], font=("Helvetica", 10)
        )
        style.configure(
            "Primary.TButton", font=("Helvetica", 10, "bold"),
            foreground="white", background=COLORS["blue"], padding=(14, 9),
            borderwidth=0, focusthickness=0
        )
        style.map("Primary.TButton", background=[("active", COLORS["blue_hover"])])
        style.configure(
            "Lesson.TButton", font=("Helvetica", 11, "bold"),
            foreground="white", background=COLORS["teal"], padding=(14, 12),
            borderwidth=0, anchor="w"
        )
        style.map("Lesson.TButton", background=[("active", COLORS["teal_hover"])])
        style.configure(
            "Opened.TButton", font=("Helvetica", 11, "bold"),
            foreground=COLORS["navy"], background=COLORS["gold"],
            padding=(14, 12), borderwidth=0, anchor="w"
        )
        style.map("Opened.TButton", background=[("active", "#E3A82F")])
        style.configure(
            "Search.Treeview", background=COLORS["surface"],
            fieldbackground=COLORS["surface"], foreground=COLORS["navy"],
            rowheight=34, borderwidth=0, font=("Helvetica", 10)
        )
        style.configure(
            "Search.Treeview.Heading", background="#EAF0F8",
            foreground=COLORS["navy"], font=("Helvetica", 10, "bold"),
            relief="flat", padding=6
        )
        style.map("Search.Treeview", background=[("selected", "#DCE9FF")],
                  foreground=[("selected", COLORS["navy"])])

    def _build_ui(self):
        outer = ttk.Frame(self.root, style="App.TFrame", padding=(28, 22, 28, 24))
        outer.pack(fill="both", expand=True)

        header = ttk.Frame(outer, style="App.TFrame")
        header.pack(fill="x", pady=(0, 18))
        title_box = ttk.Frame(header, style="App.TFrame")
        title_box.pack(side="left", fill="x", expand=True)
        ttk.Label(title_box, text=APP_NAME, style="Header.TLabel").pack(anchor="w")
        ttk.Label(
            title_box, text="Your spaced-review lesson dashboard",
            style="Subtitle.TLabel"
        ).pack(anchor="w", pady=(2, 0))
        ttk.Button(
            header, text="Choose folder", style="Primary.TButton",
            command=self.select_base_directory
        ).pack(side="right")

        self.path_label = ttk.Label(
            outer, text=self._path_text(), style="Subtitle.TLabel", anchor="w"
        )
        self.path_label.pack(fill="x", pady=(0, 14))

        panes = ttk.Panedwindow(outer, orient="horizontal")
        panes.pack(fill="both", expand=True)

        lessons_panel = ttk.Frame(panes, style="Surface.TFrame", padding=18)
        search_panel = ttk.Frame(panes, style="Surface.TFrame", padding=18)
        panes.add(lessons_panel, weight=2)
        panes.add(search_panel, weight=3)

        ttk.Label(lessons_panel, text="Review queue", style="Section.TLabel").pack(anchor="w")
        ttk.Label(
            lessons_panel, text="Newest lesson and spaced-review intervals",
            style="Muted.TLabel"
        ).pack(anchor="w", pady=(2, 12))

        folder_host = ttk.Frame(lessons_panel, style="Surface.TFrame")
        folder_host.pack(fill="both", expand=True)
        self.folder_canvas = tk.Canvas(
            folder_host, bg=COLORS["surface"], highlightthickness=0
        )
        folder_scroll = ttk.Scrollbar(
            folder_host, orient="vertical", command=self.folder_canvas.yview
        )
        self.folder_canvas.configure(yscrollcommand=folder_scroll.set)
        self.folder_frame = ttk.Frame(self.folder_canvas, style="Surface.TFrame")
        self.folder_window = self.folder_canvas.create_window(
            (0, 0), window=self.folder_frame, anchor="nw"
        )
        self.folder_frame.bind("<Configure>", self._update_folder_scrollregion)
        self.folder_canvas.bind("<Configure>", self._resize_folder_window)
        self.folder_canvas.pack(side="left", fill="both", expand=True)
        folder_scroll.pack(side="right", fill="y")

        ttk.Label(search_panel, text="Search notes", style="Section.TLabel").pack(anchor="w")
        ttk.Label(
            search_panel, text="Find text inside every .txt file in this folder",
            style="Muted.TLabel"
        ).pack(anchor="w", pady=(2, 12))

        search_row = ttk.Frame(search_panel, style="Surface.TFrame")
        search_row.pack(fill="x", pady=(0, 12))
        self.search_entry = ttk.Entry(search_row, font=("Helvetica", 11))
        self.search_entry.pack(side="left", fill="x", expand=True, ipady=7)
        self.search_entry.bind("<Return>", lambda _event: self.search_text_files())
        self.search_button = ttk.Button(
            search_row, text="Search", style="Primary.TButton",
            command=self.search_text_files
        )
        self.search_button.pack(side="left", padx=(8, 0))

        results_host = ttk.Frame(search_panel, style="Surface.TFrame")
        results_host.pack(fill="both", expand=True)
        self.results_tree = ttk.Treeview(
            results_host, columns=("file", "folder"), show="headings",
            style="Search.Treeview", selectmode="browse"
        )
        self.results_tree.heading("file", text="File")
        self.results_tree.heading("folder", text="Folder")
        self.results_tree.column("file", width=170, minwidth=100)
        self.results_tree.column("folder", width=260, minwidth=120)
        results_scroll = ttk.Scrollbar(
            results_host, orient="vertical", command=self.results_tree.yview
        )
        self.results_tree.configure(yscrollcommand=results_scroll.set)
        self.results_tree.pack(side="left", fill="both", expand=True)
        results_scroll.pack(side="right", fill="y")
        self.results_tree.bind("<Double-1>", self._open_selected_result)
        self.results_tree.bind("<Return>", self._open_selected_result)

        self.status_label = ttk.Label(
            search_panel, text="Enter a word or phrase to search.", style="Muted.TLabel"
        )
        self.status_label.pack(fill="x", pady=(10, 0))

    def _path_text(self):
        return f"Current folder: {self.base_directory}" if self.base_directory else "No folder selected"

    def _update_folder_scrollregion(self, _event=None):
        self.folder_canvas.configure(scrollregion=self.folder_canvas.bbox("all"))

    def _resize_folder_window(self, event):
        self.folder_canvas.itemconfigure(self.folder_window, width=event.width)

    def _show_folder_placeholder(self, text):
        for widget in self.folder_frame.winfo_children():
            widget.destroy()
        ttk.Label(
            self.folder_frame, text=text, style="Muted.TLabel",
            anchor="center", justify="center", wraplength=250
        ).pack(fill="x", pady=50, padx=10)

    def select_base_directory(self):
        directory = filedialog.askdirectory(
            title="Select your lessons folder", initialdir=self.base_directory or str(Path.home())
        )
        if directory:
            self.search_generation += 1
            self.base_directory = directory
            self.path_label.configure(text=self._path_text())
            self.search_button.state(["!disabled"])
            self._display_results([])
            self.status_label.configure(text="Enter a word or phrase to search.")
            self.save_last_directory(directory)
            self.search_folders()

    def search_folders(self, show_empty_message=True):
        self.folder_map.clear()
        self.folder_buttons.clear()

        if not self.base_directory or not os.path.isdir(self.base_directory):
            self._show_folder_placeholder("Choose a valid lessons folder to continue.")
            return

        try:
            selected = review_folders(numbered_folders(self.base_directory))
        except OSError as error:
            messagebox.showerror("Folder error", f"Could not scan this folder:\n{error}")
            return

        if not selected:
            self._show_folder_placeholder("No folders beginning with a number were found.")
            if show_empty_message:
                messagebox.showinfo("No lessons found", "No folders beginning with a number were found.")
            return

        for widget in self.folder_frame.winfo_children():
            widget.destroy()

        newest = selected[0][0]
        for number, path in selected:
            folder_name = os.path.basename(path)
            key = path
            self.folder_map[key] = path
            interval = newest - number
            suffix = "Newest lesson" if interval == 0 else f"{interval} lesson{'s' if interval != 1 else ''} ago"
            button = ttk.Button(
                self.folder_frame, text=f"{folder_name}\n{suffix}",
                style="Opened.TButton" if key in self.opened_folders else "Lesson.TButton",
                command=lambda folder_key=key: self.open_selected_folder(folder_key)
            )
            button.pack(fill="x", pady=(0, 8))
            self.folder_buttons[key] = button

    def search_text_files(self):
        search_text = self.search_entry.get().strip()
        if not search_text:
            messagebox.showwarning("Search", "Enter a word or phrase to search for.")
            self.search_entry.focus_set()
            return
        if not self.base_directory or not os.path.isdir(self.base_directory):
            messagebox.showwarning("Search", "Choose a valid lessons folder first.")
            return

        self.search_button.state(["disabled"])
        self.status_label.configure(text="Searching…")
        self.search_generation += 1
        generation = self.search_generation
        threading.Thread(
            target=self._scan_text_files,
            args=(self.base_directory, search_text.casefold(), generation),
            daemon=True,
        ).start()
        self.root.after(50, self._poll_search_results)

    def _scan_text_files(self, base_directory, needle, generation):
        matches = []
        unreadable = 0

        def count_walk_error(_error):
            nonlocal unreadable
            unreadable += 1

        for root, _, files in os.walk(base_directory, onerror=count_walk_error):
            for filename in files:
                if not filename.lower().endswith(".txt"):
                    continue
                path = os.path.join(root, filename)
                try:
                    with open(path, "r", encoding="utf-8", errors="replace") as file:
                        if any(needle in line.casefold() for line in file):
                            matches.append(path)
                except OSError:
                    unreadable += 1

        self.search_results.put((generation, matches, unreadable))

    def _poll_search_results(self):
        try:
            generation, matches, unreadable = self.search_results.get_nowait()
        except queue.Empty:
            self.root.after(50, self._poll_search_results)
            return
        self._finish_search(generation, matches, unreadable)

    def _finish_search(self, generation, matches, unreadable):
        if generation != self.search_generation:
            return
        self.search_button.state(["!disabled"])
        self._display_results(matches)
        count = len(matches)
        status = f"{count} matching file{'s' if count != 1 else ''}. Double-click to open."
        if unreadable:
            status += f" {unreadable} unreadable file{'s' if unreadable != 1 else ''} skipped."
        self.status_label.configure(text=status)

    def _display_results(self, paths):
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        self.result_paths = sorted(paths, key=str.casefold)
        for index, path in enumerate(self.result_paths):
            relative_parent = os.path.relpath(os.path.dirname(path), self.base_directory)
            if relative_parent == ".":
                relative_parent = "Base folder"
            self.results_tree.insert(
                "", "end", iid=str(index), values=(os.path.basename(path), relative_parent)
            )

    def _open_selected_result(self, _event=None):
        selection = self.results_tree.selection()
        if selection:
            self.open_path(self.result_paths[int(selection[0])], "file")

    def open_text_file(self, file_path):
        self.open_path(file_path, "file")

    def open_selected_folder(self, folder_key):
        folder_path = self.folder_map.get(folder_key)
        if folder_path and self.open_path(folder_path, "folder"):
            self.opened_folders.add(folder_key)
            self.folder_buttons[folder_key].configure(style="Opened.TButton")

    def open_path(self, path, kind):
        if not os.path.exists(path):
            messagebox.showerror("Missing item", f"This {kind} no longer exists:\n{path}")
            return False
        try:
            system = platform.system()
            if system == "Windows":
                os.startfile(path)
            elif system == "Darwin":
                subprocess.Popen(["open", path])
            else:
                subprocess.Popen(["xdg-open", path])
            return True
        except (OSError, subprocess.SubprocessError) as error:
            messagebox.showerror("Open error", f"Could not open this {kind}:\n{error}")
            return False

    def save_last_directory(self, directory):
        try:
            path = config_file_path()
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(directory, encoding="utf-8")
        except OSError as error:
            messagebox.showerror("Settings error", f"Could not remember this folder:\n{error}")

    def load_last_directory(self):
        for path in (config_file_path(), LEGACY_CONFIG_FILE):
            try:
                directory = path.read_text(encoding="utf-8").strip()
            except OSError:
                continue
            if os.path.isdir(directory):
                return directory
        return ""


if __name__ == "__main__":
    root = tk.Tk()
    FolderBrowserApp(root)
    root.mainloop()
