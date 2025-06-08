# 出席ボタン

Raspberry Pi Pico W でボタン押すだけで Slack に出退勤通知。ChatGPT がローラ風メッセージ生成します。

## ハードウェア

- Raspberry Pi Pico W
- ボタン 2個、LED 2個
- OLED ディスプレイ (SSD1306)

## 配線

```
GP0: 退勤ボタン   GP14: 退勤LED
GP2: 出勤ボタン   GP15: 出勤LED
GP16/17: OLED (SDA/SCL)
```

## セットアップ

1. MicroPython インストール
2. 全ファイルを Pico に転送
3. 設定ファイル作成:

**方法1: .env ファイル使用（推奨）**
```bash
cp .env.example .env
# .env ファイルを編集して実際の値を設定
```

**方法2: private.py ファイル使用**
```bash
cp template_private.py private.py
# private.py ファイルを編集して実際の値を設定
```

⚠️ **重要**: 実際の API キーやトークンは絶対にコミットしないでください

## 使い方

電源入れて「Ready?」が表示されたらボタン押すだけ。ChatGPT がメッセージ生成して Slack に投稿します。
