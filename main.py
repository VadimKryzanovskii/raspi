for event in gamepad.read_loop():
    if event.type == ecodes.EV_ABS:
        if event.code == ecodes.ABS_X:
            print("Левый стик X:", event.value)
