from transitions.extensions import GraphMachine

from utils import send_text_message

import random

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
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
    def is_going_to_state2(self, event):
        text = event.message.text
        return text.lower() == "go to state2"
    def is_going_back(self, event):
        text = event.message.text
        return text.lower() == "menu"
    def on_enter_option(self, event):
        print("I'm entering state1")
        option_str=(
            "請輸入以下關鍵字取得功能\n"+
            "我想聽音樂\n"+
            "go to state2"
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
            "6.Violin Concerto in D major by Tchaikovsky\n"
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
        reply_token = event.reply_token
        send_text_message(reply_token, music_str+"\n輸入menu回到主選單"+"\n輸入 我想聽音樂 回到音樂選單")
        
    def on_enter_random(self, event):
        print("I'm entering random")
        num=random.randint(1, 6)
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
        reply_token = event.reply_token
        send_text_message(reply_token, music_str+"\n輸入menu回到主選單"+"\n輸入 我想聽音樂 回到音樂選單")
    def on_enter_state2(self, event):
        print("I'm entering state2")

        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger state2")
        #self.go_back()
    
    #def on_exit_state2(self):
     #   print("Leaving state2")
