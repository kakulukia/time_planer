#!/bin/bash

# Get the project name from the current directory
project_name=$(basename "$PWD")

# Create the log directory if it doesn't exist
log_path="$PWD/log"
if [ ! -d "$log_path" ]; then
    mkdir "$log_path"
fi

# Get the current shell's PATH
path=$(printenv PATH)

# Create the plist file
plist_file="$HOME/Library/LaunchAgents/$project_name.plist"
echo '<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.'$project_name'</string>
    <key>ProgramArguments</key>
    <array>
        <string>'$PWD'/.venv/bin/python</string>
        <string>'$PWD'/manage.py</string>
        <string>runserver</string>
        <string>0.0.0.0:8000</string>
    </array>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>'$path'</string>
    </dict>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardErrorPath</key>
    <string>'$log_path'/'$project_name'.err</string>
    <key>StandardOutPath</key>
    <string>'$log_path'/'$project_name'.log</string>
</dict>
</plist>' > "$plist_file"

# Load the plist file
launchctl load -w "$plist_file"

echo $plist_file
