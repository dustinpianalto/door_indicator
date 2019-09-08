#!/usr/bin/env python

import time
import socket
import tkinter

host = 'bedroom-door.djpianalto.com'
port = 22222
socksize = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

root = tkinter.Tk()

current_state = 'red'


class MyButton(tkinter.Button):
    def __init__(self, *args, width=20, height=10, **kwargs):
        super().__init__(*args, width=width, height=height, command=self.toggle, **kwargs)
        self.current_state = 'green'
        self.previous_state = self.current_state
        self.alert = False
        self.able_to_update = True
        self.process()
        self.timer()

    def process(self):
        s.send(self.current_state.encode('utf-8'))
        self.able_to_update = True
        self.update_state()

    def toggle(self):
        if self.alert:
            self.able_to_update = False
            s.send(b'clear button')
            self.current_state = self.previous_state
            time.sleep(0.5)
        else:
            if self.current_state == 'red':
                self.current_state = 'green'
            elif self.current_state == 'green':
                self.current_state = 'red'

        self.process()

    def timer(self):
        self.update_state()
        self.after(100, self.timer)

    def update_state(self):
        if not self.able_to_update:
            return
        s.send(b'state')
        state = s.recv(socksize).decode('utf-8')
        if '|alert' in state:
            self.previous_state = self.current_state
            self.current_state = state.split('|')[0]
            self.alert = True
        else:
            self.current_state = state
            self.alert = False

        if self.current_state == 'red':
            self.configure(bg="#ff0000")
            self.configure(activebackground="#ff0000")
        elif self.current_state == 'green':
            self.configure(bg='#00ff00', activebackground='#00ff00')
        elif self.current_state == 'None':
            self.configure(bg='#000000')
            self.configure(activebackground='#000000')


def on_close():
    s.send(b'clear lights')
    root.destroy()
    s.close()


def main():
    frame = tkinter.Frame()
    frame.pack()
    b = MyButton(frame)
    b.pack()
    root.protocol('WM_DELETE_WINDOW', on_close)
    root.mainloop()


if __name__ == '__main__':
    main()
