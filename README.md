# Macro Recorder

A tool that records your mouse clicks and keyboard actions, then replays them automatically — as many times as you want.

> **No GitHub account needed.** The project is public — anyone can download it.

---

## First-Time Setup

You only need to do this once.

### Step 1 — Open Terminal

On your Mac, press **Cmd+Space**, type **Terminal**, and press Enter.

### Step 2 — Install Git (if you don't have it)

Paste this into Terminal and press Enter:

```bash
git --version
```

- If you see something like `git version 2.x.x` — you already have it, skip to Step 3.
- If a pop-up appears asking you to install **Xcode Command Line Tools** — click **Install** and wait for it to finish (takes a few minutes), then continue.
- If nothing happens and you get an error, install Git manually by pasting this and pressing Enter:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

This installs Homebrew (a package manager for Mac). Once done, run:

```bash
brew install git
```

### Step 3 — Download the project

Paste these commands into Terminal one by one, pressing Enter after each:

```bash
mkdir ~/tools
cd ~/tools
git clone https://github.com/LordSereos/clicker clicker
cd clicker
```

What these do:
- `mkdir ~/tools` — creates a folder called `tools` in your home directory
- `cd ~/tools` — navigates into that folder
- `git clone ...` — downloads the project into a folder called `clicker`
- `cd clicker` — navigates into the project folder

### Step 4 — Install dependencies

```bash
bash prereq.sh
```

This installs everything the tool needs. You'll see some text scroll by — that's normal. Wait until you see `All dependencies installed.`

### Step 5 — Grant Accessibility permission (required)

The tool needs permission to control your mouse and keyboard.

1. Open **System Settings**
2. Go to **Privacy & Security** → **Accessibility**
3. Click the **+** button and add **Terminal** (or iTerm2, whichever app you use)
4. Make sure the toggle next to it is turned **on**

Without this step, the script will appear to do nothing when you press the hotkey.

---

## How to Use

Every time you want to use the tool, open Terminal and navigate to the project folder first:

```bash
cd ~/tools/clicker
```

### Recording a macro

A "macro" is a recording of your actions — every click, scroll, and keypress.

1. Start recording and give your macro a name:
   ```bash
   python3 macro.py record my_macro.json
   ```

2. The terminal will say:
   ```
   Press Cmd+0 to start recording...
   ```

3. Switch to your browser (or wherever you want to record).

4. Press **Cmd+0** to start recording. Perform the actions you want to automate — scrolling, clicking download buttons, approving dialogs, etc.

5. When done, press **Cmd+0** again to stop. You'll see:
   ```
   Recording stopped. N events saved to my_macro.json
   ```

---

### Playing back a macro

1. Run the playback command, replacing `100` with however many times you want it to repeat:
   ```bash
   python3 macro.py play my_macro.json -i 100
   ```

2. The terminal will say:
   ```
   Ready. Press Cmd+0 to begin playback of 'my_macro.json'...
   ```

3. Switch to your browser and make sure the window is in **exactly the same position** as when you recorded.

4. Press **Cmd+0** to start. The tool repeats your recorded actions the specified number of times and prints progress:
   ```
   Iteration 1/100...
   Iteration 2/100...
   ...
   ```

5. To stop early at any time, press **Cmd+Q** or **Escape**.

---

## Tips

- **Keep the browser window in the same position** as when you recorded. The tool uses exact screen coordinates — if the window moves, clicks will land in the wrong place.
- **Wait for pages to load** before clicking during recording — the playback replays your pauses too, so natural timing is preserved.
- **Test with `-i 1` first** to confirm the macro works correctly before running a large batch.
- You can have **multiple macro files** for different tasks:
  ```bash
  python3 macro.py record site_a.json
  python3 macro.py record site_b.json
  python3 macro.py play site_a.json -i 50
  ```
