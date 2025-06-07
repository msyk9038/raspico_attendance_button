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
3. `template_private.py` → `private.py` にリネームして設定:

```python
# Wi-Fi
ssid = "your-wifi"
password = "your-password"

# Slack
token = "xoxb-your-token"
channel_id = "your-channel-id"

# OpenAI
openai_api_key = "your-api-key"
```

## 使い方

電源入れて「Ready?」が表示されたらボタン押すだけ。ChatGPT がメッセージ生成して Slack に投稿します。
