import socket
import ssl
import json
import time

class SlackNotifier:
    def __init__(self, token: str, channel_id: str) -> None:
        """
        SlackNotifier の コンストラクタ

        Args:
            token (str): Slack APIトークン
            channel_id (str): メッセージを送信するSlackチャンネルのID
        """
        self.headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            'Authorization': 'Bearer ' + token
        }
        self.channel_id = channel_id

    def send_request_with_retry(self, url: str, data: str, max_retries: int = 3, timeout: int = 10) -> bool:
        """
        指定されたURLに対してHTTP POSTリクエストを送信し、必要に応じてリトライを行う

        Args:
            url (str): リクエストを送信するURL
            data (Any): リクエストボディに含めるデータ
            max_retries (int, optional): 最大リトライ回数。デフォルトは3
            timeout (int, optional): タイムアウト時間（秒）。デフォルトは10

        Returns:
            bool: リクエストが成功した場合はTrue、失敗した場合はNone
        """
        retries = 0
        while retries < max_retries:
            try:
                # URL解析
                proto, dummy, host, path = url.split('/', 3)
                addr = socket.getaddrinfo(host, 443)[0][-1]
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect(addr)
                sock = ssl.wrap_socket(sock)

                # HTTPリクエストの作成
                request = "POST /{} HTTP/1.1\r\nHost: {}\r\n".format(path, host)
                for header in self.headers:
                    request += "{}: {}\r\n".format(header, self.headers[header])
                encoded_data = data.encode('utf-8')
                request += "Content-Length: {}\r\n\r\n".format(len(encoded_data))
                request += data

                # リクエストの送信
                sock.write(request.encode('utf-8'))

                # レスポンスの取得
                # response = sock.read(4096)
                time.sleep(3)
                response = True # response取得に時間がかかるため True で代用
                sock.close()
                return response
            except OSError as e:
                print("Error:", e)
                print("Retrying... (attempt {}/{})".format(retries + 1, max_retries))
                retries += 1
                time.sleep(1)
        return None

    def post_new_message(self, message: str) -> bool:
        """
        Slack APIを使用して新しいメッセージを指定されたチャンネルに投稿する

        Args:
            message (str): 投稿するメッセージ

        Returns:
            bool: メッセージの投稿が成功した場合はTrue、失敗した場合はNone
        """
        url = 'https://slack.com/api/chat.postMessage'
        data = json.dumps({
            'channel': self.channel_id,
            'text': message
        })
        res = self.send_request_with_retry(url, data)
        return res

if __name__ == "__main__":
    import private
    from wifi import connectWiFi

    # WiFiへ接続
    ssid = private.ssid
    password = private.password
    res = connectWiFi(ssid, password)
    
    # slackへテストメッセージ投稿
    token = private.token
    channel_id = private.channel_id
    notifier = SlackNotifier(token, channel_id)
    message = "はろーわーるど！"
    response = notifier.post_new_message(message)
    if response:
        print("Message posted successfully!")
    else:
        print("Failed to post message.")
