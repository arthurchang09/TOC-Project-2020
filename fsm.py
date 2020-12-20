from transitions.extensions import GraphMachine
from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from utils import send_text_message,push_message

import random
import laughing
import music
import riddle

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.num=0
        self.riddle_num=0
        self.ans=("hi")
        self.delete_num=0
        self.new_music_name=""
        self.new_music_composer=""
        self.new_music_link=""
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
        if text.lower()=="menu":
            return False
        return int(text)==self.num 
    def is_going_to_wrong_large(self, event):
        text = event.message.text
        #if text.lower()=="menu":
        #    return False
        #return int(text)>self.num
        try:
            int(text)
            return int(text)>self.num
        except ValueError:
            return False
    def is_going_to_wrong_small(self, event):
        text = event.message.text
        #if text.lower()=="menu":
        #    return False
        #return int(text)<self.num
        try:
            int(text)
            return int(text)<self.num
        except ValueError:
            return False
    def is_going_to_riddle(self, event):
        text = event.message.text
        return text.lower() == "猜謎"
    def is_going_to_riddle_right(self, event):
        text = event.message.text
        if text.lower()=="menu":
            return False
        return text.lower() == self.ans 
    def is_going_to_riddle_wrong(self, event):
        text = event.message.text
        if text.lower()=="menu":
            return False
        elif text.lower()=="拜託給我答案":
            return False
        return text.lower() != self.ans
    def is_going_to_riddle_answer(self, event):
        text = event.message.text
        return text.lower() == "拜託給我答案"
    def is_going_to_laugh(self,event):
        text = event.message.text
        return text.lower() == "笑話"
    def is_going_to_laugh_manage(self,event):
        text = event.message.text
        return text.lower() == "笑話管理"
    def is_going_to_add_laugh(self,event):
        text = event.message.text
        return text.lower() == "新增"
    def is_going_to_add_success(self,event):
        text = event.message.text
        return text.lower() != "menu"
    def is_going_to_search_laugh(self,event):
        text = event.message.text
        return text.lower() == "search"
    def is_going_to_laugh_search_num(self,event):
        text = event.message.text
        try:
            int(text)
            return True
        except ValueError:
            return False
    def is_going_to_delete_laugh(self,event):
        text = event.message.text
        return text.lower() == "刪除"
    def is_going_to_confirm_delete(self,event):
        text = event.message.text
        try:
            int(text)
            if int(text)<len(laughing.laugh):
                self.delete_num=int(text)
                return True
            else:
                return False
        except ValueError:
            return False
    def is_going_to_finish_delete(self,event):
        text = event.message.text
        return text.lower() == "確認刪除"
    def is_going_to_music_manage(self, event):
        text = event.message.text
        return text.lower() == "音樂管理"
    def is_going_to_add_music(self, event):
        text = event.message.text
        return text.lower() == "新增"
    def is_going_to_add_music_name(self, event):
        text = event.message.text
        if text.lower() != "menu":
            self.new_music_name=text
        return text.lower() != "menu"
    def is_going_to_add_music_link(self, event):
        text = event.message.text
        if text.lower() != "menu":
            self.new_music_link=text
        return text.lower() != "menu"
    def is_going_to_add_music_composer(self, event):
        text = event.message.text
        if text.lower() != "menu":
            self.new_music_composer=text
        return text.lower() != "menu"
    def is_going_to_add_confirm(self, event):
        text = event.message.text
        return text.lower() == "確認"
    def is_going_back(self, event):
        text = event.message.text
        return text.lower() == "menu"
    def on_enter_option(self, event):
        print("I'm entering state1")
        option_str=(
            "請輸入以下關鍵字取得功能\n"+
            "1.我想聽音樂：來聽點音樂\n"+
            "2.guess number：猜數字遊戲\n"+
            "3.猜謎：來猜點謎語吧\n"+
            "4.笑話：看笑話放鬆一下(很冷警告)\n"+
            "5.笑話管理：新增、搜尋或刪除笑話"
            )
        reply_token = event.reply_token
        send_text_message(reply_token, option_str)

    def on_enter_music(self, event):
        print("I'm entering music")
        music_list=""
        push_message(event.source.user_id,"曲目如下：")
        for i in range(0,len(music.music_name)):
            #music_list.append(str(i+1)+music.music_name[i]+"\n")
            music_list+=str(i+1)+"."+music.music_name[i]+"\n"
        push_message(event.source.user_id,music_list)
        reply_token = event.reply_token
        send_text_message(reply_token,"選歌請輸入歌曲編號\n"+"隨機播放 請輸入「隨機」\n"+"輸入menu回到主選單")
        #self.go_back()
    def on_enter_play(self, event):
        print("I'm entering paly")
        text = event.message.text
        music_str=("wrong\n")
        music_str=music.music_link[int(text)-1]
        reply_token = event.reply_token
        send_text_message(reply_token, music_str+"\n輸入menu回到主選單"+"\n輸入「我想聽音樂」回到音樂選單")
        
    def on_enter_random(self, event):
        print("I'm entering random")
        num=random.randint(0, len(music.music_link)-1)
        music_str=("wrong\n")
        music_str=music.music_link[num]
        reply_token = event.reply_token
        send_text_message(reply_token, music_str+"\n輸入menu回到主選單"+"\n輸入「我想聽音樂」回到音樂選單")
    def on_enter_guest_num(self, event):
        print("I'm entering guest_num")
        self.num=random.randint(0, 10)
        reply_token = event.reply_token
        send_text_message(reply_token, "Guess number. Enter a integer.")
        #self.go_back()
    def on_enter_right(self, event):
        print("I'm entering right")
        reply_token = event.reply_token
        send_text_message(reply_token, "You are right! 輸入Menu回到主選單 輸入guess number在猜一次")
    def on_enter_wrong_large(self, event):
        print("I'm entering wrong_large")
        reply_token = event.reply_token
        send_text_message(reply_token, "You are wrong! 太大了，再猜一次。退出輸入Menu回到主選單")
    def on_enter_wrong_small(self, event):
        print("I'm entering wrong_large")
        reply_token = event.reply_token
        send_text_message(reply_token, "You are wrong! 太小了，再猜一次。退出輸入Menu回到主選單")
    def on_enter_riddle(self, event):
        print("I'm entering riddle")
        riddle_str=("")
        
        self.riddle_num=random.randint(0, len(riddle.ques)-1)
        riddle_str=riddle.ques[self.riddle_num]
        self.ans=riddle.answer[self.riddle_num]
        reply_token = event.reply_token
        
        send_text_message(reply_token, riddle_str)
    def on_enter_riddle_right(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "答對了 \n輸入Menu回到主選單 \n輸入「猜謎」再猜一次")
    def on_enter_riddle_wrong(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "答錯了 \n以卑微的語氣輸入 「拜託給我答案」取得答案\n你也可以繼續猜下去，祝你好運\n輸入Menu回到主選單 ")
        push_message(event.source.user_id, "笑你")
    def on_enter_riddle_answer(self, event):
        reply_token = event.reply_token
        send_text_message(reply_token, "答案是 「"+self.ans+"」，想不到吧！！！！\n輸入Menu回到主選單 \n輸入「猜謎」再猜另一題")
    def on_enter_laugh(self, event):
        reply_token = event.reply_token
        get_rand=random.randint(0,len(laughing.laugh)-1)
        laugh_text=laughing.laugh[get_rand]
        send_text_message(reply_token, laugh_text+"\n\n輸入Menu回到主選單 \n輸入「笑話」再看一則笑話")
    def on_enter_laugh_manage(self, event):
        reply_token = event.reply_token
        manage_list=(
            "輸入「新增」增加笑話\n"+
            "輸入「刪除」刪除笑話\n"+
            "輸入 search 查詢笑話"
        )
        send_text_message(reply_token, manage_list)
    def on_enter_add_laugh(self, event):
        reply_token = event.reply_token
        manage_list=(
            "輸入你的笑話增加笑話\n"+
            "輸入menu返回主選單"
        )
        send_text_message(reply_token, manage_list)
    def on_enter_add_success(self, event):
        reply_token = event.reply_token
        text = event.message.text
        laughing.laugh.append(text)
        send_text_message(reply_token,"新增笑話\n\n"+text+"\n\n輸入menu返回主選單")
    def on_enter_search_laugh(self, event):
        reply_token = event.reply_token
        laugh_len=len(laughing.laugh)-1
        send_text_message(reply_token,"輸入數字"+"0~"+str(laugh_len)+"搜尋笑話")
    def on_enter_laugh_search_num(self, event):
        reply_token = event.reply_token
        text = event.message.text
        laugh_content=laughing.laugh[int(text)]
        send_text_message(reply_token,"你的笑話"+":\n"+laugh_content+"\n\n\n輸入menu返回主選單\n輸入search再找一次")
    def on_enter_delete_laugh(self,event):
        reply_token = event.reply_token
        laugh_len=len(laughing.laugh)-1
        send_text_message(reply_token,"輸入數字"+"0~"+str(laugh_len)+"刪除笑話")
    def on_enter_confirm_delete(self,event):
        reply_token = event.reply_token
        laugh_content=laughing.laugh[self.delete_num]
        send_text_message(reply_token,"你要刪除的笑話"+":\n"+laugh_content+"\n\n\n輸入「確認刪除」刪除笑話\n輸入menu返回主選單")
    def on_enter_finish_delete(self, event):
        reply_token = event.reply_token
        laugh_content=laughing.laugh.pop(self.delete_num)
        send_text_message(reply_token,"你刪除了以下的笑話"+":\n"+laugh_content+"\n\n\n輸入menu返回主選單")
    def on_enter_music_manage(self, event):
        reply_token = event.reply_token
        manage_list=(
            "輸入「新增」增加音樂\n"+
            "輸入「刪除」刪除音樂\n"+
            "輸入「修改」修改音樂\n"+
            "輸入 search 查詢音樂"
        )
        send_text_message(reply_token, manage_list)
    def on_enter_add_music(self, event):
        reply_token = event.reply_token
        manage_list=(
            "輸入你的歌曲曲名\n"+
            "輸入menu返回主選單"
        )
        send_text_message(reply_token, manage_list)
    def on_enter_add_music_name(self,event):
        reply_token = event.reply_token
        manage_list=(
            "輸入你的歌曲連結\n"+
            "輸入menu返回主選單"
        )
        send_text_message(reply_token, manage_list)
    def on_enter_add_music_link(self,event):
        reply_token = event.reply_token
        manage_list=(
            "輸入你的歌曲作曲家或在哪部電影戲劇\n"+
            "輸入menu返回主選單"
        )
        send_text_message(reply_token, manage_list)
    def on_enter_add_music_composer(self,event):
        reply_token = event.reply_token
        manage_list=(
            "你要新增的曲目資訊如下："+
            "曲名："+self.new_music_name+"\n"+
            "連結："+self.new_music_link+"\n"+
            "作曲家、演唱家或所屬電影戲劇："+self.new_music_composer+"\n"+
            "輸入「確認」新增歌曲"
            "輸入menu返回主選單"
        )
        send_text_message(reply_token, manage_list)
    def on_enter_add_confirm(self, event):
        music.music_name.append(self.new_music_name)
        music.music_link.append(self.new_music_link)
        music.composer.append(self.new_music_composer)
        reply_token = event.reply_token
        send_text_message(reply_token, "新增成功\n輸入menu返回主選單")
    #def on_exit_state2(self):
     #   print("Leaving state2")
