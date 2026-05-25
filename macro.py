import argparse
import json
import os
import time
import threading
from pynput import mouse, keyboard
from pynput.keyboard import Key, KeyCode

RECORD_HOTKEY = "<cmd>+0"
STOP_HOTKEY = "<cmd>+q"


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Record and replay keyboard/mouse macros."
    )
    subparsers = parser.add_subparsers(dest="mode", required=True)

    rec = subparsers.add_parser("record", help="Record a macro to a file")
    rec.add_argument("filename", help="Output file path (e.g. download.json)")

    play = subparsers.add_parser("play", help="Play back a recorded macro")
    play.add_argument("filename", help="Macro file to play (e.g. download.json)")
    play.add_argument("-i", "--iterations", type=int, default=10, help="Number of times to repeat (default: 10)")

    return parser.parse_args(argv)


def save_events(events, filename):
    with open(filename, "w") as f:
        json.dump(events, f, indent=2)


def load_events(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Macro file not found: {filename}")
    with open(filename) as f:
        return json.load(f)


def record(filename):
    events = []
    recording = False
    start_time = None
    done = threading.Event()
    cmd_held = threading.Event()

    def on_move(x, y):
        if recording:
            events.append({"type": "move", "x": x, "y": y,
                           "time": round(time.time() - start_time, 4)})

    def on_click(x, y, button, pressed):
        if recording:
            events.append({
                "type": "click", "x": x, "y": y,
                "button": button.name, "pressed": pressed,
                "time": round(time.time() - start_time, 4),
            })

    def on_scroll(x, y, dx, dy):
        if recording:
            events.append({"type": "scroll", "x": x, "y": y, "dx": dx, "dy": dy,
                           "time": round(time.time() - start_time, 4)})

    def on_press(key):
        nonlocal recording, start_time
        if key in (Key.cmd, Key.cmd_l, Key.cmd_r):
            cmd_held.set()
        elif key == KeyCode.from_char("0") and cmd_held.is_set():
            if not recording:
                recording = True
                start_time = time.time()
                print("Recording started. Press Cmd+0 to stop.")
            else:
                recording = False
                save_events(events, filename)
                print(f"Recording stopped. {len(events)} events saved to {filename}")
                done.set()
        elif recording:
            key_str = key.char if hasattr(key, "char") and key.char else str(key)
            events.append({"type": "key", "key": key_str, "pressed": True,
                           "time": round(time.time() - start_time, 4)})

    def on_release(key):
        if key in (Key.cmd, Key.cmd_l, Key.cmd_r):
            cmd_held.clear()
        elif recording and not (key == KeyCode.from_char("0") and cmd_held.is_set()):
            key_str = key.char if hasattr(key, "char") and key.char else str(key)
            events.append({"type": "key", "key": key_str, "pressed": False,
                           "time": round(time.time() - start_time, 4)})

    mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
    kb_listener = keyboard.Listener(on_press=on_press, on_release=on_release)

    print("Press Cmd+0 to start recording...")
    mouse_listener.start()
    kb_listener.start()
    done.wait()
    mouse_listener.stop()
    kb_listener.stop()


def play(filename, iterations=10):
    events = load_events(filename)
    stop_flag = threading.Event()
    start_flag = threading.Event()
    cmd_held = threading.Event()

    mouse_ctrl = mouse.Controller()
    keyboard_ctrl = keyboard.Controller()

    def on_press(key):
        if key in (Key.cmd, Key.cmd_l, Key.cmd_r):
            cmd_held.set()
        elif key == KeyCode.from_char("0") and cmd_held.is_set():
            start_flag.set()
        elif key == Key.esc or (key == KeyCode.from_char("q") and cmd_held.is_set()):
            stop_flag.set()

    def on_release(key):
        if key in (Key.cmd, Key.cmd_l, Key.cmd_r):
            cmd_held.clear()

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    print(f"Ready. Press Cmd+0 to begin playback of '{filename}'...")
    start_flag.wait()
    print(f"Playing {iterations} iteration(s). Press Cmd+Q or Escape to stop.")

    for i in range(iterations):
        if stop_flag.is_set():
            break
        print(f"Iteration {i + 1}/{iterations}...")
        prev_time = events[0]["time"] if events else 0

        for event in events:
            if stop_flag.is_set():
                break
            delay = event["time"] - prev_time
            if delay > 0:
                time.sleep(delay)
            prev_time = event["time"]

            if event["type"] == "move":
                mouse_ctrl.position = (event["x"], event["y"])
            elif event["type"] == "click":
                btn = mouse.Button.left if event["button"] == "left" else mouse.Button.right
                mouse_ctrl.position = (event["x"], event["y"])
                if event["pressed"]:
                    mouse_ctrl.press(btn)
                else:
                    mouse_ctrl.release(btn)
            elif event["type"] == "scroll":
                mouse_ctrl.position = (event["x"], event["y"])
                mouse_ctrl.scroll(event["dx"], event["dy"])
            elif event["type"] == "key":
                try:
                    k = event["key"]
                    if len(k) == 1:
                        key_obj = KeyCode.from_char(k)
                    else:
                        key_name = k.replace("Key.", "")
                        key_obj = getattr(Key, key_name, None)
                    if key_obj:
                        if event["pressed"]:
                            keyboard_ctrl.press(key_obj)
                        else:
                            keyboard_ctrl.release(key_obj)
                except Exception:
                    pass

    listener.stop()
    if stop_flag.is_set():
        print("Playback stopped by user.")
    else:
        print("Playback complete.")


def main():
    args = parse_args()
    if args.mode == "record":
        record(args.filename)
    elif args.mode == "play":
        play(args.filename, args.iterations)


if __name__ == "__main__":
    main()
