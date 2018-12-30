# TNW
TNW is Not WeChat

An instant messaging app for 2018 Computer Networks Homework.

Author: tandf
2018.12.30

## Usage
### Windows
Run `Executable/Windows/TNW.exe`

### Other platform
Run `python3 TNW.py`

#### Dependency
Python is needed.

Install necessary modules using pip.

`pip3 install pyqt5`
`pip3 install sounddevice`
`pip3 install soundfile`
`pip3 install numpy`

## Protocol
- use json
- source
- target
- time stamp
- type
    - TEXT
    - FILE
    - RECORDING
- data
    - text packet: msg
    - file packet: file name
    - recording packet: recording name (generated using hash funciton)

If file or recording, get file after get packet.

## Directory Structure
- login.py (log in/out, query)
- msg.py (send and receive message)
- TNW.py (ui and main function)
- data/
    - [ID]/
        - contact
        - [msg file, name generated using hash function)
        - files/ (files received)
        - recordings/ (recordings received)
    - recv (temp dir for receiving files and recordings)

## Threads
- UI (main thread)
- receive msg
    - server thread, always loop
    - socket thread, threads to deal with incoming tcp link
- send msg (open thread at incoming connect)

## To be improved
- Show the percentage when sending files.
- Show the time when recording.
