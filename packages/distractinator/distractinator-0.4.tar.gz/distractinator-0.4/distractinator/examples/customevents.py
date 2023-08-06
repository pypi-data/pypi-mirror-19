"""
Custom events file for The Distractinator(TM)!

You can re-assign the provided alert function to a different button

    alert(title="Some title", msg="Some message")

"""

from distractinator.events import alert 

def run_action_a():
    pass

def run_action_b():
    pass

def run_action_c():
    pass

def run_action_d():
    pass

def on_connect():
    alert(title="yay!", msg="USB Connected! :)")

def on_disconnect():
    alert(title="boo...", msg="USB Disconnected! :(")

