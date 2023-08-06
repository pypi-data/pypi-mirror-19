import subprocess

def alert(title, msg):
    rc = subprocess.call(["/usr/bin/notify-send", title, msg])
    return rc

def run_action_a(usermodule=None, log=None):
    if not usermodule: 
        return

    try:
        usermodule.run_action_a()
    except Exception as e:
        log.error('There was an error trying to run action A.')
        log.error(e)

def run_action_b(usermodule=None, log=None):
    if not usermodule:
        return

    try:
        usermodule.run_action_b()
    except Exception as e:
        log.error('There was an error trying to run action B.')
        log.error(e)

def run_action_c(usermodule=None, log=None):
    if not usermodule:
        return

    try:
        usermodule.run_action_c()
    except Exception as e:
        log.error('There was an error trying to run action C.')
        log.error(e)

def run_action_d(usermodule=None, log=None):
    if not usermodule:
        return

    try:
        usermodule.run_action_d()
    except Exception as e:
        log.error('There was an error trying to run action D.')
        log.error(e)

def on_connect(usermodule=None, log=None):
    if not usermodule:
        return

    try:
        usermodule.on_connect()
    except Exception as e:
        log.error('There was an error trying to run the custom on_connect action.')
        log.error(e)

def on_disconnect(usermodule=None, log=None):
    if not usermodule:
        return 

    try:
        usermodule.on_disconnect()
    except Exception as e:
        log.error('There was an error trying to run the custom on_connect action.')
        log.error(e)
        pass

