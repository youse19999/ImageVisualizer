import tkinter as tk
from tkinter import filedialog, messagebox
import os

from src.directory_reader import IV_Dirs
from src.image_viewer import IV_ImageViewer


class IV_GUI:
    """メインGUIウィンドウ — 左にファイル一覧、右に画像プレビュー"""

    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 700
    LISTBOX_WIDTH = 30

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Image Visualizer")
        self.root.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        self.root.minsize(800, 500)

        self._current_dir = None
        self._current_index = -1
        self._image_files = []

        self._build_ui()
        self._bind_events()

    # ── UI構築 ──────────────────────────────────

    def _build_ui(self):
        """全体のレイアウトを構築"""
        # メニューバー
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="フォルダを開く...", command=self._open_folder)
        file_menu.add_separator()
        file_menu.add_command(label="終了", command=self.root.quit)
        menubar.add_cascade(label="ファイル", menu=file_menu)
        self.root.config(menu=menubar)

        # メインフレーム（左: リスト / 右: 画像）
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 左側 — ファイルリスト
        list_frame = tk.Frame(main_frame, width=250)
        list_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        list_frame.pack_propagate(False)

        self._listbox = tk.Listbox(list_frame)
        scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self._listbox.yview)
        self._listbox.config(yscrollcommand=scrollbar.set)
        self._listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 右側 — 画像表示キャンバス
        canvas_frame = tk.Frame(main_frame)
        canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self._canvas = tk.Canvas(canvas_frame, bg="#2b2b2b", highlightthickness=0)
        self._canvas.pack(fill=tk.BOTH, expand=True)

        # ステータスバー
        self._status_var = tk.StringVar(value="フォルダを開いてください")
        status_bar = tk.Label(
            self.root, textvariable=self._status_var,
            bd=1, relief=tk.SUNKEN, anchor=tk.W
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # コアコンポーネント
        self._viewer = IV_ImageViewer(self._canvas)

    def _bind_events(self):
        """イベントバインディング"""
        self._listbox.bind("<<ListboxSelect>>", self._on_select)
        self._canvas.bind("<Configure>", self._on_canvas_resize)

    # ── フォルダ操作 ────────────────────────────

    def _open_folder(self):
        """フォルダ選択ダイアログを表示し、画像一覧を読み込む"""
        folder = filedialog.askdirectory(title="画像フォルダを選択")
        if not folder:
            return
        self._current_dir = folder
        dirs = IV_Dirs(folder)
        dirs.get_img_files()
        all_files = dirs.get_files()
        if all_files is None:
            messagebox.showerror("エラー", "フォルダの読み込みに失敗しました")
            return

        ext_whitelist = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".webp", ".ico"}
        self._image_files = [
            f for f in all_files
            if os.path.splitext(f)[1].lower() in ext_whitelist
        ]
        self._image_files.sort()

        self._listbox.delete(0, tk.END)
        for fname in self._image_files:
            self._listbox.insert(tk.END, fname)

        self._current_index = -1
        self._viewer.clear()
        self._status_var.set(f"{folder}  —  {len(self._image_files)} 個の画像")

    # ── 画像選択 ────────────────────────────────

    def _on_select(self, event):
        """リスト選択時の処理"""
        selection = self._listbox.curselection()
        if not selection:
            return
        idx = selection[0]
        self._current_index = idx
        fname = self._image_files[idx]
        full_path = os.path.join(self._current_dir, fname)
        try:
            self._viewer.display(full_path)
            self._status_var.set(
                f"{idx + 1} / {len(self._image_files)}  —  {fname}"
            )
        except Exception as e:
            messagebox.showerror("画像エラー", f"{fname} を開けませんでした:\n{e}")

    def _on_canvas_resize(self, event):
        """キャンバスリサイズ時に画像を再表示"""
        if self._current_index >= 0 and self._current_dir:
            fname = self._image_files[self._current_index]
            full_path = os.path.join(self._current_dir, fname)
            try:
                self._viewer.display(full_path)
            except Exception:
                pass

    # ── スクリーンショット ────────────────────────────

    def screen_shot(self, save_dir: str = "screenshot") -> str | None:
        """現在の画面全体のスクリーンショットを撮り、PNGとして保存（Linux/Windows/macOS対応）"""
        import datetime

        os.makedirs(save_dir, exist_ok=True)
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(save_dir, f"screenshot_{ts}.png")
        try:
            # mss: クロスプラットフォーム（Linux/Windows/macOSで動作）
            import mss
            with mss.mss() as sct:
                sct.shot(output=path)
            self._status_var.set(f"スクリーンショット保存: {path}")
            return path
        except ImportError:
            # mss 未インストール時 → PIL.ImageGrab でフォールバック
            try:
                from PIL import ImageGrab
                img = ImageGrab.grab()
                img.save(path)
                self._status_var.set(f"スクリーンショット保存: {path}")
                return path
            except Exception as e:
                self._status_var.set(f"スクリーンショット失敗: {e}")
                return None
        except Exception as e:
            self._status_var.set(f"スクリーンショット失敗: {e}")
            return None

    # ── 起動 ────────────────────────────────────

    def run(self):
        self.root.mainloop()
