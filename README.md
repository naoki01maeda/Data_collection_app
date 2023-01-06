# Data_collection_app

# 環境

- python 3.7.0
- tkinter 8.6.12
- PIL 9.2.0
- json 2.0.9

# 概要

- 物体検出などのデータ作成に使えるデータ収集アプリ

![sample](https://user-images.githubusercontent.com/98692841/209474513-56e13081-b5d3-4142-a0d6-0e6156258754.png)

# 手順

- 左クリックホールドでボックスの描画開始
- 左クリックを離すことでボックスの描画終了
- テキストボックスが表示されるので、目的に合わせてテキストを入力
- NEXTボタンを押すことでjsonファイルとして保存され、次の画像に推移
- 繰り返す
- 終了はウィンドウの右上の×ボタンをクリック

# 保存形式
```save_json
[
    {
        "regions": [
            {
                "region_id": 1,
                "width": 55,
                "height": 121,
                "image_id": 1,
                "phrase": "Contact with a red sign on the left shoulder that says 'No Parking'",
                "y": 474,
                "x": 260,
                "risk": 0
            },
            {
                "region_id": 2,
                "width": 290,
                "height": 500,
                "image_id": 1,
                "phrase": "Contact with a white van parked on the right shoulder",
                "y": 236,
                "x": 706,
                "risk": 0
            }
        ],
        "id": 1
    }
```
