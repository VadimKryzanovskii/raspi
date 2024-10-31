for event in gamepad.read_loop():
    if event.type == ecodes.EV_ABS:
        absevent = categorize(event)
        if event.code == ecodes.ABS_X:  # Событие оси X левого стика
            print(f'Левый стик (ось X): {event.value}')
        elif event.code == ecodes.ABS_Y:  # Событие оси Y левого стика
            print(f'Левый стик (ось Y): {event.value}')
        elif event.code == ecodes.ABS_RX:  # Событие оси X правого стика
            print(f'Правый стик (ось X): {event.value}')
        elif event.code == ecodes.ABS_RY:  # Событие оси Y правого стика
            print(f'Правый стик (ось Y): {event.value}')