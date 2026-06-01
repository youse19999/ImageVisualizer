from PIL import Image, ImageTk
import tkinter as tk

class IV_ImageViewer:
    """画像の読み込み・リサイズ・tkinter用変換を担当"""

    MAX_WIDTH = 800
    MAX_HEIGHT = 600

    def __init__(self, canvas: tk.Canvas):
        self.canvas = canvas
        self._photo = None
        self._image_ref = None

    def display(self, image_path: str):
        """画像をキャンバスに表示（アスペクト比維持、キャンバスにフィット）"""
        pil_img = Image.open(image_path)
        pil_img = self._fit_to_canvas(pil_img)
        self._photo = ImageTk.PhotoImage(pil_img)
        self.canvas.delete("all")
        self._image_ref = self.canvas.create_image(
            self.canvas.winfo_width() // 2,
            self.canvas.winfo_height() // 2,
            image=self._photo,
            anchor=tk.CENTER
        )

    def clear(self):
        """キャンバスをクリア"""
        self.canvas.delete("all")
        self._photo = None
        self._image_ref = None

    def _fit_to_canvas(self, img: Image.Image) -> Image.Image:
        """画像をキャンバスサイズに収める（アスペクト比維持）"""
        cw = self.canvas.winfo_width()
        ch = self.canvas.winfo_height()
        if cw < 10 or ch < 10:
            cw, ch = self.MAX_WIDTH, self.MAX_HEIGHT
        img_w, img_h = img.size
        ratio = min(cw / img_w, ch / img_h, 1.0)
        if ratio < 1.0:
            new_w = int(img_w * ratio)
            new_h = int(img_h * ratio)
            img = img.resize((new_w, new_h), Image.LANCZOS)
        return img
