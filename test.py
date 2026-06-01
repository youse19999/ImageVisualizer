# ++AIの書き込み [2026-06-01 12:30] [is_windows / screen_shot 実装] [patch + write_file] [deepseek-v4-flash]
# 機能:
#   - is_windows(): 現在のOSがWindowsかを返す
#   - check_windows(): スレッドでGUIを起動し、3秒後にscreen_shot()を実行、5秒後に終了
# --AIの書き込み [2026-06-01 12:30]

import platform
import threading
import time
import main
from src.gui import IV_GUI
from rich.console import Console
from rich.text import Text

console = Console()


def check():
    """GUIを起動 → スクリーンショット撮影 → 終了（Windows/Linux/macOS対応）"""
    app = IV_GUI()

    def _delayed_screenshot():
        time.sleep(3)
        result = app.screen_shot()
        if result:
            console.print(f"[green]スクリーンショット保存: {result}[/green]")
        else:
            console.print("[red]スクリーンショットに失敗[/red]")
        time.sleep(2)
        app.root.quit()

    threading.Thread(target=_delayed_screenshot, daemon=True).start()
    app.run()


if __name__ == "__main__":
    console.print(f"[cyan]OS: {platform.system()} / {platform.release()}[/cyan]")
    console.print("[green]GUI + スクリーンショットテスト開始[/green]")
    check()
    console.print("[green]スクリーンショットテスト完了[/green]")
