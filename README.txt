Macro Recorder
==============

SETUP
  bash prereq.sh
  System Settings -> Privacy & Security -> Accessibility -> add your terminal app (required)

RECORD
  python3 macro.py record <file>
  Cmd+0 to start, Cmd+0 to stop and save

PLAY
  python3 macro.py play <file> -i 100
  Cmd+0 to start, Cmd+Q or Escape to stop early

  -i N   number of iterations (default: 10)
  Example: python3 macro.py play download.json -i 50
