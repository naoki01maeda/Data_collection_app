import tkinter as tk
from PIL import Image, ImageTk
import json
import os
import re

ori_data_path = "./data/ori_data/"

class App(tk.Frame):
    
    """
    
    データ収集アプリの表示画面、内部処理の関数を保持したクラス
    
    Attributes
    ---------------
    
    image_id : list
        読み込んだ画像ファイルのIDが格納される
    rect_list : list
        作成された矩形の情報が格納される
    check_list : list
        "危険"と書かれたチェックボックスの情報が格納される
    button_list : list
        "取り消し"と書かれたボタンの情報が格納される
    check_var_list : list
        "危険"と書かれたチェックボックスのチェック可否の情報が格納される
    txt_var_list : list
        テキストボックスに打ち込んだ文字情報が格納される
    box_start_list : list
        矩形の左上の座標を格納
    box_end_list : list
        矩形の右下の座標を格納
    region_json_data : list
        アプリ開始時にすでに保存されているjsonファイルの領域データが格納され、新規データ取得時、順次格納
    image_json_data : list
        アプリ開始時にすでに保存されているjsonファイルの画像データが格納され、新規データ取得時、順次格納
    
    counter_box : int
        領域が作成されるたび、+1される
        次の画像へ推移時、初期化される
    counter_img : int
        画像を読み込むためのIDの役割
        画像推移時、+1される
    region_id : int
        領域を作成するたび、+1される
    
    
    """
    
    image_id = []
    
    rect_list = []
    txt_list = []
    check_list = []
    button_list = []
    
    check_var_list = []
    txt_var_list = []
    
    box_start_list = []
    box_end_list = []
    
    region_json_data = []
    image_json_data = []
    
    counter_box = -1
    counter_img = 0
    region_id = 0
   
    if os.path.exists(ori_data_path + 'region_descriptions.json') and os.path.exists(ori_data_path + 'image_data.json'):#データファイルがすでに存在する場合

        region_json_open = open(ori_data_path + 'region_descriptions.json', 'r')
        image_json_open = open(ori_data_path + 'image_data.json', 'r')
        region_json_load = json.load(region_json_open)
        image_json_load = json.load(image_json_open)
        
        for i,one_region_data in enumerate(region_json_load):
                region_json_data.append(one_region_data)
                if i == len(region_json_load)-1:#最後のデータの画像IDと領域IDを取得
                    counter_img = region_json_data[-1]["id"]
                    region_id = region_json_data[-1]["regions"][-1]['region_id']
                    
                    
        for i,one_image_data in enumerate(image_json_load):
            image_json_data.append(one_image_data)
            
        assert counter_img == image_json_data[-1]["image_id"]
    
    def __init__(self, frame):
        
        """
        
        ウィンドウを表示させる設定を定義するコンストラクタ
        
        args
        ---------------
        
        frame : class
            フレームの情報を持つクラス
        
        
        Methods
        ---------------
        
        _createVariables()
            フレームの更新をする関数
        _createCanvas()
            ウィンドウの各種設定及び、表示する関数
        _createCanvasBinding()
            マウスクリックなどのイベントを識別して、イベントに応じた関数を呼び出す関数
        
        """
        
        tk.Frame.__init__(self, frame)
        self._createVariables(frame)
        self._createCanvas()
        self._createCanvasBinding()
        
        
    def save_json(self, s_rect, e_rect, text, risk_degree, img_id): 
        
        """
        
        btn_click_next()関数から呼び出され、入力されたデータを加工しjsonファイルとして保存する
        
        args
        ---------------
        
        s_rect : list
            各ボックスの左上の座標が格納されたリスト
        e_rect : list
            各ボックスの右下の座標が格納されたリスト
        text : list
            各ボックスのテキストバックスに打ち込まれた文字列に関するオブジェクトが格納されたリスト
        risk_degree : list
            各ボックスに保持されているチェックボックスのチェック可否の情報が含まれるオブジェクトが格納されたリスト
        img_id : int
            画面に表示されている画像の画像ID
        
        """
        
        self.one_region_data = {"regions":[]}
        
        
        record_s_rect_data = list(filter(None, s_rect))
        record_e_rect_data = list(filter(None, e_rect))
        record_txt_data = list(filter(None, text))
        record_risk_data = list(filter(None, risk_degree))
        
        for i in range(len(record_txt_data)):
            record_txt_data[i] = record_txt_data[i].get()
            record_risk_data[i] = record_risk_data[i].get()

        for i in range(len(record_s_rect_data)):
            self.region_id += 1
            self.one_region_data["regions"].append({"region_id": self.region_id, "width": int(record_e_rect_data[i][0] - record_s_rect_data[i][0]), "height": int(record_e_rect_data[i][1] - record_s_rect_data[i][1]), 
                                                   "image_id": int(img_id), "phrase": record_txt_data[i], "y": int(record_s_rect_data[i][1]), "x": int(record_s_rect_data[i][0]), "risk":1 if record_risk_data[i] == True else 0})
        self.one_region_data["id"] = int(img_id)
        
        self.region_json_data.append(self.one_region_data)
        
        self.image_json_data.append({"width": self.img_width, "url": "ori_data/{}.jpg".format(img_id), "height": self.img_height, "image_id": int(img_id)})
        
        with open(ori_data_path + 'region_descriptions.json', 'w') as fp:
            json.dump(self.region_json_data, fp, ensure_ascii=False)
            
        with open(ori_data_path + 'image_data.json', 'w') as fp:
            json.dump(self.image_json_data, fp, ensure_ascii=False)
            
            
    def save_json_split(self,img_id_list):
        
        """
        
        保存されたjsonファイルの画像IDデータを (訓練データ、検証データ、テストデータ) に分割し、保存する
        
        args
        ---------------
        
        img_id_list : list
            保存されたjsonファイルの各データの画像IDが格納されたリスト
        
        ---------------
        
        """
        
        train_rate = 0.8
        val_rate = 0.1
        test_rate = 0.1
        train_rate_data = int(len(img_id_list)*train_rate)
        val_rate_data = train_rate_data + int(len(img_id_list)*val_rate)+1
        test_rate_data = val_rate_data + int(len(img_id_list)*test_rate)+1
        split_data = {"test": img_id_list[val_rate_data : test_rate_data], "train": img_id_list[0 : train_rate_data], "val": img_id_list[train_rate_data : val_rate_data]}
        with open('./info/split_data.json', 'w') as fp:
            json.dump(split_data, fp, ensure_ascii=False)
    
    def _createVariables(self, frame):
        
        """
        
        フレームを更新するための関数
        
        args
        ---------------
        frame : class
            tk.Tk()クラスを保持(フレーム情報を保持するクラスと考えればよい)
        ---------------
        
        """
        
        self.frame = frame
        

    def _createCanvas(self):
        
        """
        
        ウィンドウの各種設定および表示
        
        """
        
        self.files = os.listdir(ori_data_path + 'drama_image')
        
        self.files = sorted(self.files, key=lambda s: int(re.search('\d+', s).group()))
        
        self.img_list = []
        
        
        self.img = Image.open(ori_data_path + 'drama_image/{}'.format(self.files[self.counter_img]))
        self.tk_img = ImageTk.PhotoImage(self.img)
        self.img_width, self.img_height = self.img.size
        self.canvas = tk.Canvas(self.frame, width = self.img_width, height = self.img_height)
        self.item = self.canvas.create_image(0, 0 , anchor = tk.NW, image=self.tk_img)
        self.canvas.grid(row=0, column=0, sticky='nsew')
        self.button = tk.Button(width=7,text='NEXT', command=self.btn_click_next)
        self.button.place(x=self.img_width*0.9, y=self.img_height*0.9)

    def _createCanvasBinding(self):
        
        """
        
        マウスクリックなどのイベントを識別して、イベントに応じた関数を呼び出す
        
        """
        
        self.canvas.bind( "<Button-1>", self.startRect )
        self.canvas.bind( "<ButtonRelease-1>", self.stopRect )
        self.canvas.bind( "<B1-Motion>", self.movingRect )
        
    def startRect(self, event):
        
        """
        
        マウスを左クリックされたときに呼び出される関数
        
        args
        ---------------
        
        event : class
            左クリックしたイベントの情報が保持されたクラス
            event.x はクリックされたx座標
            event.y はクリックされたy座標
        
        """
        
        self.counter_box += 1
        
        self.rectx0 = self.canvas.canvasx(event.x)
        self.recty0 = self.canvas.canvasy(event.y) 
        
        self.rectid = self.canvas.create_rectangle(
            self.rectx0, self.recty0, self.rectx0, self.recty0, outline = 'red', width = 5, tag="rect_{}".format(self.counter_img))
        
        self.rect_list.append(self.rectid)
        
        
    def btn_click_next(self):
        
        """
        
        画面上の "NEXT" ボタンが押されたときに呼び出される関数
        
        """
        
        self.image_id = self.files[self.counter_img].split(".")[0]
        
        test_list = list(filter(None, self.box_start_list))
        
        if test_list != []:
            self.save_json(self.box_start_list, self.box_end_list, self.txt_var_list, self.check_var_list, self.image_id)#jsonファイルに記録
            image_id_list = [self.image_json_data[i]["image_id"] for i in range(len(self.image_json_data))]
            self.save_json_split(image_id_list)
        
        self.counter_img += 1
        self.change_img = Image.open(ori_data_path + 'drama_image/{}'.format(self.files[self.counter_img]))
        self.tk_img = ImageTk.PhotoImage(self.change_img)
        self.item = self.canvas.itemconfig(self.item,image=self.tk_img)
        self.item = self.canvas.create_image(0, 0 , anchor = tk.NW, image=self.tk_img)
        
        for i in range(self.counter_box + 1):
            
            if self.rect_list[i] == None:
                pass
            else:
                self.canvas.delete(self.rect_list[i])
                self.check_list[i].destroy()
                self.txt_list[i].destroy()
                self.button_list[i].destroy()

        self.counter_box = -1
        self.rect_list = []
        self.txt_list = []
        self.check_list = []
        self.button_list = []
        self.check_var_list = []
        self.txt_var_list = []
        
        self.box_start_list = []
        self.box_end_list = []
        
        
    def btn_click(self, create_numbers):
        
        """
        
        ボックスに付与されている "取り消し" ボタンが押されたときの処理
        
        args
        ---------------
        
        create_numbers
            何番目に作成されたボックスかを表すID
        
        """
        
        def x():
            
            self.canvas.delete(self.rect_list[create_numbers])
            self.rect_list[create_numbers] = None
            self.check_list[create_numbers].destroy()
            self.check_list[create_numbers] = None
            self.txt_list[create_numbers].destroy()
            self.txt_list[create_numbers] = None
            self.button_list[create_numbers].destroy()
            self.button_list[create_numbers] = None
            
            self.box_start_list[create_numbers] = None
            self.box_end_list[create_numbers] = None
            
            self.check_var_list[create_numbers] = None
            self.txt_var_list[create_numbers] = None
            
        return x
        
        
    def movingRect(self, event):
        
        """
        
        マウスが左クリックされた状態でのドラッグ動作の情報を取得し、情報をウィンドウに表示する。
        
        args
        ---------------
        
        event : class
            ドラッグ状態の情報が保持されたクラス
            event.x は現在のx座標
            event.y は現在のy座標
        
        """
        
        self.rectx1 = self.canvas.canvasx(event.x)
        self.recty1 = self.canvas.canvasy(event.y)
        
        self.canvas.coords(self.rectid, self.rectx0, self.recty0,
                      self.rectx1, self.recty1)

    def stopRect(self, event):
        
        """
        
        左クリックが離されたときの情報を取得し、各種処理を行う関数
        
        args
        ---------------
        
        event : class
            左クリックを離すというイベントの情報が保持されたクラス
            event.x は左クリックが離されたときのx座標
            event.y は左クリックが離されたときのy座標
        
        """
        
        self.rectx1 = self.canvas.canvasx(event.x)
        self.recty1 = self.canvas.canvasy(event.y)
        
        self.canvas.coords(self.rectid, self.rectx0, self.recty0,
                      self.rectx1, self.recty1)
        
        self.box_start_list.append([self.rectx0, self.recty0])
        self.box_end_list.append([self.rectx1, self.recty1])
        
        self.check_var_list.append(tk.BooleanVar())
        self.check_var_list[self.counter_box].set(False)
        self.txt_var_list.append(tk.StringVar())
        self.txt_var_list[self.counter_box].set("")
        
        self.txt_list.append(tk.Entry(width=30,textvariable = self.txt_var_list[self.counter_box]))
        self.txt_list[self.counter_box].place(x=self.rectx0, y=self.recty0 + 30)
        self.check_list.append(tk.Checkbutton(text='危険',variable = self.check_var_list[self.counter_box]))
        self.check_list[self.counter_box].place(x=self.rectx0, y=self.recty0 + 50)
        self.button_list.append(tk.Button(width=7,text='取り消し', command=self.btn_click(self.counter_box)))
        self.button_list[self.counter_box].place(x=self.rectx0, y=self.recty0)
        
        
if __name__ == "__main__":
    root = tk.Tk()#ウィンドウを作成
    root.title("データ収集")#ウィンドウのタイトルを設定
    app = App(root)#作成されたウィンドウのインスタンスをAppクラスに入力しAppのインスタンスを生成
    root.mainloop()#アプリが終了するまでループ
    
    