# Swifty - Simple code editor for Swift langauge.

This is a task written as a part of JetBrains internship recruitment process. 

It's a simple GUI tool that allows users to enter a swift script, execute it and see its output side-by-side.

It's written in Python, and uses the PyQt5 framework for GUI.

## Features
* Editor pane and an output pane.
* Can run swift scripts. (using '/usr/bin/env swift \<script>.swift')
* Shows live output of the script as it's being executed. (Remember to flush the output)
* Shows errors in different color in the output pane.
* Can save and load scripts.
* Shows the exit code of the last ran script.
* Simple syntax highlighting.
* Currently running status is indicated by the disabled run button.

## How to use?
1. Download the repo.
2. Activate the virtual environment. (`source venv/bin/activate`)
3. Run the app. (`python3 swift.py`)