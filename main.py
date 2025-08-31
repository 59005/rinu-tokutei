import re
import requests
import urllib.parse

def get_param(name: str, url: str) -> str | None:
    parsed = urllib.parse.urlparse(url)
    params = urllib.parse.parse_qs(parsed.query)
    return params.get(name, [None])[0]

def check(url: str):
    ## 正規表現はここからパクりました https://github.com/e6nlaq/rinucf-checker/blob/master/index.js#L32
    rinu_regex = re.compile(r"^https?://rinu\.(cf|jp)/[\w/:%#\$&\?\(\)~\.=\+\-]+$")

    if not rinu_regex.match(url):
        print("rinu.jp のURLを入力してください。")
        return

    url_code = url.split("rinu.jp/")[-1] if "rinu.jp/" in url else url.split("rinu.cf/")[-1]

    api_url = f"https://api.activetk.jp/urlmin/get?code={url_code}"
    try:
        dat = requests.get(api_url).json()
    except Exception as e:
        print("API取得失敗:", e)
        return

    if dat.get("status") != "OK":
        print("エラー:", dat.get("type"))
        if dat.get("type") == 404:
            print("URLが存在しません。(404)")
        else:
            print("予期せぬエラーが発生しました。")
        return

    go_url = dat["LinkURL"]
    if rinu_regex.match(go_url):
        go_url = get_param("url", go_url)
    else:
        print("逆探知完了")

    creator_ip = dat["CreatorInfo"]["IPAddress"]
    ipinfo = requests.get(f"https://ipinfo.io/{creator_ip}/json").json()

    last_use_ip = dat["LastUsed"][11:]

    print("\n===== 情報 =====")
    print(f"作成者のIPアドレス: {creator_ip}")
    print(f"作成者のタイムゾーン: {dat['CreatorInfo']['TimeZone']}")
    print(f"IPからわかる住所: {dat['CreatorInfo']['Location']}")
    print(f"IPからわかる郵便番号: {ipinfo.get('postal')}")
    print(f"最後に使用したユーザーのIP: {last_use_ip}")
    print("")

def main():
    url = input("作者を特定したいURLを入力してください (例: https://rinu.jp/UNKOMANEZ1234): ")
    check(url)

if __name__ == "__main__":
    main()
