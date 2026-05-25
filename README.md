# Macro Recorder

A tool that records your mouse clicks and keyboard actions, then replays them automatically — as many times as you want.

---

## First-Time Setup

You only need to do this once.

### Step 1 — Open Terminal

On your Mac, press **Cmd+Space**, type **Terminal**, and press Enter.

### Step 2 — Create a folder and download the project

Copy and paste these commands into Terminal one by one, pressing Enter after each:

```bash
mkdir ~/tools
cd ~/tools
git clone <repository-url> clicker
cd clicker
```

> If you don't have git installed, your Mac will prompt you to install it automatically. Click Install and wait for it to finish, then run the commands again.

### Step 3 — Install dependencies

```bash
bash prereq.sh
```

This installs everything the tool needs. You'll see some text scroll by — that's normal.

### Step 4 — Grant Accessibility permission (required)

The tool needs permission to control your mouse and keyboard.

1. Open **System Settings**
2. Go to **Privacy & Security** → **Accessibility**
3. Click the **+** button and add **Terminal** (or whichever terminal app you use)

Without this step, the script will appear to do nothing.

---

## How to Use

### Recording a macro

A "macro" is a recording of your actions — every click, scroll, and keypress.

1. In Terminal, navigate to your clicker folder:
   ```bash
   cd ~/tools/clicker
   ```

2. Start recording and give your macro a name:
   ```bash
   python3 macro.py record my_macro.json
   ```

3. The terminal will say:
   ```
   Press Cmd+0 to start recording...
   ```

4. Switch to your browser (or wherever you want to record actions).

5. Press **Cmd+0** to start recording. Perform the actions you want to automate — scrolling, clicking download buttons, approving dialogs, etc.

6. When done, press **Cmd+0** again to stop. The recording is saved to `my_macro.json`.

---

### Playing back a macro

1. Run the playback command, replacing `100` with however many times you want it to repeat:
   ```bash
   python3 macro.py play my_macro.json -i 100
   ```

2. The terminal will say:
   ```
   Ready. Press Cmd+0 to begin playback...
   ```

3. Switch to your browser and make sure it's positioned exactly where it was when you recorded.

4. Press **Cmd+0** to start. The tool will repeat your recorded actions the specified number of times, printing progress in the terminal.

5. To stop early at any time, press **Cmd+Q** or **Escape**.

---

## Tips

- **Keep the browser window in the same position** as when you recorded. The tool uses exact screen coordinates, so if the window moves, clicks will land in the wrong place.
- **Wait for pages to load** before clicking during recording — the playback will replay your pauses too, so natural timing is captured.
- **Test with `-i 1` first** to make sure the macro works correctly before running a large batch.
- You can have **multiple macro files** for different tasks:
  ```bash
  python3 macro.py record site_a.json
  python3 macro.py record site_b.json
  python3 macro.py play site_a.json -i 50
  ```
