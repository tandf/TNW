# TNW
An instant messaging app for 2018 Computer Networks Homework.

Author: tandf

TNW is Not WeChat

## Protocol
- use json
- source
- time stamp
- target
- type
    - TEXT
    - WTDW
    - FILE
    - GROU
- data
    - text packet: msg
    - withdraw packet: sourceId and timestamp
    - file packet: file name

## Directory Structure
- login.py (log in/out, query)
- msg.py (send and receive message)
- TNW.py (ui and main function)
- data/
    - contact
    - msg
- recv_files/

## Threads
- UI
- receive msg (always loop)
- send msg (open thread at incoming connect)

## TODO list
- [x] design directory structure
- [x] test socket coding
- functions
    - [] one to one
    - [] group talk
    - [] save history msgs
    - [] file(10M) sending with socket
    - [] log in and log out
- Additional functions
    - [] msg withdraw
        - estimate RTT using coming msg time stamp and receving time
            - average with older one
        - receving time and RTT decide weither to withdraw a certain msg(text or file)
        - delete file or text and then update window
- with gui
    - [] input in a qt window
    - [] qss
    - [] test in windows and linux
- pyinstaller

