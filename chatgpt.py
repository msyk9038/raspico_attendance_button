import json
import urequests as requests

# Chatbotの応答を取得する関数
def get_chat_response(openai_api_key:str, prompt:str) -> str:
    """
    OpenAI APIを使用してチャット応答を取得する関数

    Args:
        openai_api_key (str): OpenAI APIキー
        prompt (str): ユーザーからのプロンプト

    Returns:
        str: OpenAI APIからの応答メッセージ
    """
    endpoint = 'https://api.openai.com/v1/chat/completions'
    # APIリクエストヘッダーを設定
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Authorization': 'Bearer ' + openai_api_key
    }
    
    # APIリクエストデータを設定
    data = {
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'user', 'content': prompt }]
    }
    
    # APIリクエストを送信
    json_data = json.dumps(data)
    encoded_data = bytes(json_data, 'utf-8')
    response = requests.post(endpoint, headers=headers, data=encoded_data)
    
    # API応答を解析
    response_json = json.loads(response.text)
    message = response_json['choices'][0]['message']['content'].strip()
    return message

if __name__ == "__main__":
    import private
    from wifi import connectWiFi

    # WiFiへ接続
    ssid = private.ssid
    password = private.password
    res = connectWiFi(ssid, password)
    
    # chatGPTに聞いてみる
    openai_api_key = private.openai_api_key
    message = 'こんにちわ。これはテスト投稿です。'
    prompt = f'次のmessageを90年代女子高生風な文章に変換してください。message:{message}'
    response = get_chat_response(openai_api_key, prompt)
    print(response)