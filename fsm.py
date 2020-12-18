from transitions.extensions import GraphMachine

from utils import send_text_message


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_music(self, event):
        text = event.message.text
        return text.lower() == "我想聽音樂"

    def is_going_to_state2(self, event):
        text = event.message.text
        return text.lower() == "go to state2"
    def is_going_back(self, event):
        text = event.message.text
        return text.lower() == "menu"
    def on_enter_option(self, event):
        print("I'm entering state1")
        option_str=(
            "two\n"+
            "我想聽音樂\n"+
            "go to state2\n"
            )
        reply_token = event.reply_token
        send_text_message(reply_token, option_str)

    def on_enter_music(self, event):
        print("I'm entering music")
        music_list=(
            "music list\n"+
            "https://www.youtube.com/watch?v=-7mntyrW3HU"+
            "\n2."
        )
        reply_token = event.reply_token
        send_text_message(reply_token, music_list)
        #self.go_back()

   # def on_exit_state1(self):
    #    print("Leaving state1")

    def on_enter_state2(self, event):
        print("I'm entering state2")

        reply_token = event.reply_token
        send_text_message(reply_token, "Trigger state2")
        #self.go_back()
    
    #def on_exit_state2(self):
     #   print("Leaving state2")
