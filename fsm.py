from transitions.extensions import GraphMachine

from utils import send_text_message

import random

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.num=0
        self.riddle_num=0
        self.ans=("hi")
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_music(self, event):
        text = event.message.text
        return text.lower() == "我想聽音樂"
    def is_going_to_play(self, event):
        text = event.message.text
        return text.isdigit()
    def is_going_to_random(self, event):
        text = event.message.text
        return text.lower() == "隨機"
    def is_going_to_guest_num(self, event):
        text = event.message.text
        return text.lower() == "guess number"
    def is_going_to_right(self, event):
        text = event.message.text
        if text=="menu":
            return False
        return int(text)==self.num 
    def is_going_to_wrong_large(self, event):
        text = event.message.text
        if text=="menu":
            return False
        return int(text)>self.num 
    def is_going_to_wrong_small(self, event):
        text = event.message.text
        if text=="menu":
            return False
        return int(text)<self.num 
    def is_going_to_riddle(self, event):
        text = event.message.text
        return text.lower() == "猜謎"
    def is_going_to_riddle_right(self, event):
        text = event.message.text
        return text.lower() == self.ans 
    def is_going_to_riddle_wrong(self, event):
        text = event.message.text
        return text.lower() != self.ans 
    def is_going_back(self, event):
        text = event.message.text
        return text.lower() == "menu"
    def on_enter_option(self, event):
        print("I'm entering state1")
        option_str=(
            "請輸入以下關鍵字取得功能\n"+
            "我想聽音樂\n"+
            "guess number\n"+
            "猜謎"
            )
        reply_token = event.reply_token
        send_text_message(reply_token, option_str)

    def on_enter_music(self, event):
        print("I'm entering music")
        music_list=(
            "曲單:\n"+
            "1.op48 no 1 by Chopin\n"+
            "2.Symphony no.6 by Tchaikovsky\n"+
            "3.BWV565 by Bach\n"+
            "4.Chaconne by Bach\n"+
            "5.Le Temps des cathedrales\n"+
            "6.Violin Concerto in D major by Tchaikovsky\n"+
            "7.op 55 no.1 by Chopin \n"+
            "8.Der Erlkönig violin version\n"
            "選歌 請輸入 編號\n"+
            "隨機播放 請輸入 隨機\n"+
            "輸入menu回到主選單"
        )
        reply_token = event.reply_token
        send_text_message(reply_token, music_list)
        #self.go_back()
    def on_enter_play(self, event):
        print("I'm entering paly")
        text = event.message.text
        music_str=("wrong\n")
        if int(text)==1:
             music_str=("https://www.youtube.com/watch?v=-7mntyrW3HU")
        elif int(text)==2:
             music_str=("https://www.youtube.com/watch?v=zIJiPlbJjs8")
        elif int(text)==3:
             music_str=("https://www.youtube.com/watch?v=Nnuq9PXbywA")
        elif int(text)==4:
             music_str=("https://www.youtube.com/watch?v=ngjEVKxQCWs")
        elif int(text)==5:
             music_str=("https://www.youtube.com/watch?v=qT6Mpkj9Y8Q")
        elif int(text)==6:
             music_str=("https://www.youtube.com/watch?v=CTE08SS8fNk")
        elif int(text)==7:
             music_str=("https://www.youtube.com/watch?v=e3yrEEM5j_s")
        elif int(text)==8:
             music_str=("https://www.youtube.com/watch?v=UWNCbpwC-PQ")
        reply_token = event.reply_token
        send_text_message(reply_token, music_str+"\n輸入menu回到主選單"+"\n輸入 我想聽音樂 回到音樂選單")
        
    def on_enter_random(self, event):
        print("I'm entering random")
        num=random.randint(1, 8)
        music_str=("wrong\n")
        if num==1:
             music_str=("https://www.youtube.com/watch?v=-7mntyrW3HU")
        elif num==2:
             music_str=("https://www.youtube.com/watch?v=zIJiPlbJjs8")
        elif num==3:
             music_str=("https://www.youtube.com/watch?v=Nnuq9PXbywA")
        elif num==4:
             music_str=("https://www.youtube.com/watch?v=ngjEVKxQCWs")
        elif num==5:
             music_str=("https://www.youtube.com/watch?v=qT6Mpkj9Y8Q")
        elif num==6:
             music_str=("https://www.youtube.com/watch?v=CTE08SS8fNk")
        elif num==7:
             music_str=("https://www.youtube.com/watch?v=e3yrEEM5j_s")
        elif num==8:
             music_str=("https://www.youtube.com/watch?v=UWNCbpwC-PQ")
        reply_token = event.reply_token
        send_text_message(reply_token, music_str+"\n輸入menu回到主選單"+"\n輸入 我想聽音樂 回到音樂選單")
    def on_enter_guest_num(self, event):
        print("I'm entering guest_num")
        self.num=random.randint(0, 10)
        reply_token = event.reply_token
        send_text_message(reply_token, "guess number,Enter a integer.")
        #self.go_back()
    def on_enter_right(self, event):
        print("I'm entering right")
        reply_token = event.reply_token
        send_text_message(reply_token, "You are right! 輸入Menu回到主選單")
    def on_enter_wrong_large(self, event):
        print("I'm entering wrong_large")
        reply_token = event.reply_token
        send_text_message(reply_token, "You are wrong! 太大了，再猜一次")
    def on_enter_wrong_small(self, event):
        print("I'm entering wrong_large")
        reply_token = event.reply_token
        send_text_message(reply_token, "You are wrong! 太小了，再猜一次")
    def on_enter_riddle(self, event):
        print("I'm entering riddle")
        riddle_str=("")
        self.riddle_num=random.randint(1, 4)
        reply_token = event.reply_token
        if self.riddle_num==1:
            riddle_str=("芷草飛花落，重峰望北塵 (猜一字)")
            self.ans=("紫")
        elif self.riddle_num==2:
            riddle_str=("紅芍半掩向西南 (猜一字)")
            self.ans=("約")
        elif self.riddle_num==3:
            riddle_str=("上八不像八,下八才是八,十字當中站,生命需靠它 (猜一字)")
            self.ans=("米")
        elif self.riddle_num==4:
            riddle_str=("一邊發綠,一邊發紅;一邊喜雨,一邊怕風;一邊怕水,一邊怕蟲 (猜一字)")
            self.ans=("秋")
        elif self.riddle_num==4:
            riddle_str=("悟道乘舟去，張弓射遠空 (猜二字)")
            self.ans=("首長")
        send_text_message(reply_token, riddle_str)
    def on_enter_riddle_right(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "答對了 輸入Menu回到主選單")
    def on_enter_riddle_wrong(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "答錯了 輸入Menu回到主選單 ")
    #def on_exit_state2(self):
     #   print("Leaving state2")
