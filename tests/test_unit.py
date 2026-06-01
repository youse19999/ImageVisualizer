# ++AIの書き込み [2026-06-01 12:30] [ユニットテスト作成] [write_file] [deepseek-v4-flash]
# --AIの書き込み [2026-06-01 12:30]

# ++AIの書き込み [2026-06-01 12:30] [screen_shot 実装] [patch] [deepseek-v4-flash]
# --AIの書き込み [2026-06-01 12:30]

"""
ImageVisualizer ユニットテスト
（全OS対応 — CIでlinux/macos/windows全て実行可能）
"""

import os
import sys
import platform

# プロジェクトルートをPYTHONPATHに追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.directory_reader import IV_Dirs
from src.image_loader import IV_Image


# ── is_windows (test.py) ──────────────────────────────

class TestIsWindows:
    def test_is_windows_returns_bool(self):
        """is_windows が bool を返すことを確認"""
        from test import is_windows
        result = is_windows()
        assert isinstance(result, bool)

    def test_is_windows_consistency(self):
        """is_windows が platform.system() と一致することを確認"""
        from test import is_windows
        assert is_windows() == (platform.system() == "Windows")


# ── IV_Dirs ──────────────────────────────────────────

class TestIVDirs:
    def test_get_img_files(self, tmp_path):
        """画像ファイルのみをリストする"""
        # テスト用ファイル作成
        (tmp_path / "a.png").write_text("dummy")
        (tmp_path / "b.jpg").write_text("dummy")
        (tmp_path / "c.txt").write_text("dummy")
        (tmp_path / "d.webp").write_text("dummy")

        dirs = IV_Dirs(str(tmp_path))
        dirs.get_img_files()
        all_files = dirs.get_files()

        # sort() で main.py 側と同じ順序になるよう注意
        assert all_files is not None
        assert "a.png" in all_files
        assert "b.jpg" in all_files
        assert "c.txt" in all_files  # directory_reader はフィルタしない
        assert "d.webp" in all_files

    def test_empty_folder(self, tmp_path):
        """空フォルダでエラーなく動く"""
        dirs = IV_Dirs(str(tmp_path))
        dirs.get_img_files()
        assert dirs.get_files() == []

    def test_nonexistent_path(self):
        """存在しないパス → OSError"""
        dirs = IV_Dirs("/nonexistent_path_xyz")
        import pytest
        with pytest.raises(OSError):
            dirs.get_img_files()

    def test_get_files_calls_get_img_files(self, tmp_path):
        """get_files() が自動的に get_img_files() を呼ぶ"""
        dirs = IV_Dirs(str(tmp_path))
        # get_img_files() を呼ばずに get_files()
        assert dirs.get_files() == []


# ── IV_Image ─────────────────────────────────────────

class TestIVImage:
    def test_image_properties(self, tmp_path):
        """画像のフォーマット・サイズ・モードを取得"""
        from PIL import Image
        img_path = os.path.join(tmp_path, "test.png")
        img = Image.new("RGB", (100, 50), color="red")
        img.save(img_path)

        obj = IV_Image(img_path)
        assert obj.get_format() == "PNG"
        assert obj.get_size() == (100, 50)
        assert obj.get_mode() == "RGB"

    def test_image_not_found(self):
        """存在しない画像 → FileNotFoundError"""
        import pytest
        with pytest.raises(FileNotFoundError):
            IV_Image("/nonexistent/image.png")
