from machine import Pin
from wifi import connectWiFi
import slack
import private
import time
import chatgpt
import oled
import getJSTstr

def post_to_slack(slack_notifier, is_working: bool = False) -> str:
    oled.show_message('Generating...', size=2)
    posted_time = getJSTstr.getJSTstr()
    # chatGPTで文章の生成
    if is_working:
        sub_message1 = 'おはようございます'
        sub_message2 = '開始'
    else:
        sub_message1 = 'お疲れ様でした'
        sub_message2 = '終了'
    message = f'{sub_message1}, 月島勤務{sub_message2}します。'
    prompt = f'次のmessageをほんの少しだけローラ風の文章に変換してください。message:{message}'
    message = chatgpt.get_chat_response(openai_api_key, prompt)
    # oledに表示
    oled.show_message(message)
    # slackに投稿
    slack_notifier.post_new_message(message)    
    return posted_time
    
def switch_led(is_working: bool) -> None:
    working_led.value(is_working)
    off_duty_led.value(not is_working)
    return

if __name__ == "__main__":

    # GPIOの初期化
    builtin_led = Pin("LED", Pin.OUT)
    builtin_led.value(0)
    working_button = Pin(2, Pin.IN, pull=Pin.PULL_UP)
    working_led = Pin(15, Pin.OUT)
    working_led.value(0)
    off_duty_button = Pin(0, Pin.IN, pull=Pin.PULL_UP)
    off_duty_led = Pin(14, Pin.OUT)
    off_duty_led.value(1)

    # WiFiに接続
    ssid = private.ssid
    password = private.password
    result = connectWiFi(ssid, password)
    builtin_led.value(result) # WiFiに繋がったら光る

    # chatGPT の apikey取得
    openai_api_key = private.openai_api_key

    # slackで投稿
    token = private.token
    channel_id = private.channel_id
    slack_notifier = slack.SlackNotifier(token, channel_id)

    is_working = False
    oled.show_message('Ready?', size=2)

    while True:
        if working_button.value() == 0:
            if is_working: continue # すでに出勤状態なら出勤ボタンが押されてももう一度投稿しない
            is_working = True
            # メッセージの生成とSlackへの投稿
            posted_time = post_to_slack(slack_notifier, is_working) 
            # LED の切り替え
            switch_led(is_working)
            # 10病後に投稿時刻を表示
            time.sleep(10)
            oled.show_message(posted_time)
        if off_duty_button.value() == 0:
            if not is_working: continue # すでに退勤状態なら退勤ボタンが押されてももう一度投稿しない
            is_working = False
            # メッセージの生成とSlackへの投稿
            posted_time = post_to_slack(slack_notifier, is_working)       
            # LED の切り替え
            switch_led(is_working)
            # 10病後に投稿時刻を表示
            time.sleep(10)
            oled.show_message(posted_time)
