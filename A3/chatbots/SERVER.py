from tkinter import Frame, Label, Entry, Button, Text
import socket
import threading

class GUI:
    client_socket = None
    last_received_message = None
    def __init__(self, master):
        self.root = master
        self.name_widget = None
        self.join_button = None
        self.enter_text_widget = None
        self.chat_area = None
        self.initialize_socket()
        self.initialize_gui()
        self.listen_for_incoming_messages_in_a_thread()

    def initialize_socket(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_ip = '127.0.0.1'
        remote_port = 10319
        self.client_socket.connect((remote_ip, remote_port))


    def initialize_gui(self):
        self.root.title("Talk to Mahmoud") #window title
        self.root.resizable(0,0)
        self.display_name_section()
        self.chat_box()
        self.chat_entry_box()

    def listen_for_incoming_messages_in_a_thread(self):
        thread = threading.Thread(target=self.receive_messages_from_server, args=(self.client_socket,))
        thread.start()

    def receive_messages_from_server(self,so):
        while True:
            buffer = so.recv(256)
            if not buffer:
                break
            message = buffer.decode('utf-8')
            if "joined" in message:
                user= message.split(":")[1]
                message = user + " has joined"
                self.chat_area.insert('end', message + '\n')
                self.chat_area.yview(END)
            else:
                self.chat_area.insert('end', message + '\n')
                self.chat_area.yview(END)
        so.close()


    def display_name_section(self):
        frame = Frame()
        Label(frame, text = "Mahmoud Chat Box:" , fonts = ("Serif", 12)).pack(side ='top', anchor = 'w')
        self.name_widget = Entry(frame, width = 50, borderwidth =2)
        self.name_widget.pack(side='left', anchor = 'e')
        self.join_button = Button(frame, text = 'Join', width =10, command = self.on_join).pack(sides='left')
        frame.pack(sides = 'top', anchor = 'w')

    def chat_box(self):
        frame = Frame()
        Label(frame, text = 'Mahmoud: ', font =('Serif', 12)).pack(side='top, anchor='w')
        self.chat_area = Text(frame, width = 60, height = 10, font=("Serif",12))
        scrollbar = Scrollbar(frame, command= self.chat_area.yview, orient=VERTICAL)
        self.chat_area.bind('<KeyPress>', lambda e:'break')
        self.chat_area.pack(side='left', padx =10)
        scrollbar.pack(side='right', fill ='y')
        frame.pack(side='top')


    def chat_entry_box(self):
        frame = Frame()
        Label(frame, text = "Enter Message:" , fonts = ("Serif", 12)).pack(side ='top', anchor = 'w')
        self.enter_text_widget = Text(frame, width = 60, height =3, font = ("Serif", 12))
        self.enter_text_widget.pack(side='left' ,pady =15)
        self.enter_text_widget.bind('<Return>', self.on_enter_key_pressed)
        frame.pack(side = 'top')

    def on_join(self):
        if len(self.name_widget.get())==0:
            messagebox.showerror("Enter your name", "Enter your name to send message")
            return
        self.name_widget.config(state= 'disabled')

    def on_enter_key_pressed(self):
        if len(self.name_widget.get())==0:
            messagebox.showerror("Enter your name","Enter your name to send message")
            return
        self.send_chat()
        self.clear_text()

    def send_chat(self):
        senders_name = self.name_widget.get().strip()+": "
        data = self.enter_text_widget.get(1.0,'end').strip()
        message = (senders_name + data).encode('utf-8')
        self.chat_area.insert('end', message.decode('utf-8')+'\n')
        self.chat_area.yview(END)
        self.client_socket.send(message)
        self.enter_text_widget.delete(1.0, 'end')
        return 'break'

    def clear_text(self):
        self.enter_text_widget.delete(1.0,'end')
    
    def on_close_window(self):
        if messagebox.askokcancel("Quit", "Do you want to exit?"):
            self.root.destroy()
            self.client_socket.close()
            exit(0)

if __name__ =='main':
    root = Tk()
    gui = GUI(root)
    root.protocol('WM_DELETE_WINDOW', gui.on_close_window)
    root.mainloop()