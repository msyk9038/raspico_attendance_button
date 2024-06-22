from machine import Pin, I2C  # 入出力モジュール
import ssd1306                # 液晶表示器用ライブラリ
import math                   # 数学関数
from misakifont import MisakiFont # 日本語表示用のライブラリ
import time

def show_bitmap(oled, fd, x, y, color, size):
    """
    美咲フォントのビットマップ表示
    """
    for row in range(0, 7):
        for col in range(0, 7):
            if (0x80 >> col) & fd[row]:
                oled.fill_rect(int(x + col * size), int(y + row * size), size, size, color)
    oled.show()

def show_message(message: str, size: int = 1) -> None:

    # I2C設定 (I2C識別ID 0or1, SDA, SCL)
    i2c = I2C(0, sda=Pin(16), scl=Pin(17) )

    # 使用するSSD1306のアドレス取得表示（通常は0x3C）
    addr = i2c.scan()
    # print( "OLED I2C Address :" + hex(addr[0]) )

    # ディスプレイ設定（幅, 高さ, 通信仕様）
    oled = ssd1306.SSD1306_I2C(128, 64, i2c)

    mf = MisakiFont()
    color = 1

    x = 0
    y = 0
    for c in message:
        d = mf.font(ord(c))
        show_bitmap(oled, d, x, y, color, size)
        x += 8 * size
        if x >= 128:
            x = 0
            y += 8 * size
        if y >= 64:
            y = 0
        time.sleep(0.02)
        
    return

if __name__ == "__main__":
    show_message('はろーわーるど！', size=2)