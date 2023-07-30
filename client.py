import socket
from threading import Thread
from tkinter import *
# nickname = input("Enter Name: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = '127.0.0.1'
port = 8000
client.connect((ip,port))

class GUI:
  def __init__(self):
    self.Window = Tk()
    self.Window.withdraw()

    self.login = Toplevel()
    self.login.title("Login")
    self.login.resizable(width=False, height=False)
    self.login.configure(width=500, height=500)

    self.titleLabel = Label(
      self.login, 
      text="Login Screen", 
      bd=4, fg="#2f3436", 
      font="Helvetica 16 bold", 
      justify=CENTER)
    self.titleLabel.place(x=180, y=50)

    self.nameLabel = Label(
      self.login, 
      text="Username:", 
      bd=4, fg="#2f3436", 
      font="Helvetica 12 bold", 
      justify=CENTER)
    self.nameLabel.place(x=100, y=100)
    self.nameEntry = Entry(self.login, font="Helvetica 12 bold")
    self.nameEntry.place(x=220, y=100)

    self.go = Button(
      self.login, 
      text="Login", 
      background="#6e818a", 
      bd=4, fg="#e8e8e8", 
      font="Helvetica 14 bold", 
      justify=CENTER, 
      command=lambda: self.goAhead(self.nameEntry.get()))
    self.go.place(x=210, y=150)

    self.Window.mainloop()

  def layout(self,name):
    self.name = name
    self.Window.deiconify()
    self.Window.title("CHATROOM")
    self.Window.resizable(width=False, height=False)
    self.Window.configure(width=470, height=550, bg="#17202A")

    self.labelHead = Label(self.Window, text=self.name, bg="#17202A", fg="#EAECEE", font="Helvetica 14 bold", pady=5)
    self.labelHead.place(relwidth=1)
    self.line = Label(self.Window, width=450, bg="#ABB2B9")
    self.line.place(relwidth=1, rely=0.07, relheight=0.012)

    self.textCons = Text(self.Window, width=20, height=2, bg="#17202A", fg="#EAECEE", font="Helvetica 14", padx=5, pady=5)
    self.textCons.place(relheight=0.745, relwidth=1, rely=0.08)
    self.textCons.config(cursor="arrow")
    self.textCons.config(state=DISABLED)

    self.scrollBar = Scrollbar(self.textCons)
    self.scrollBar.place(relheight=1, relx=0.974)
    self.scrollBar.config(command=self.textCons.yview)

    self.labelBottom = Label(self.Window, bg="#ABB2B9", height=80)
    self.labelBottom.place(relwidth=1, rely=0.825)

    self.entryMsg = Entry(self.labelBottom, bg="#2C3E50", fg="#EAECEE", font="Helvetica 13")
    self.entryMsg.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.11)
    self.entryMsg.focus()

    self.buttonMessage = Button(self.labelBottom, text="SEND", font="Helvetica 10 bold", width=20, bg="#ABB2B9", command=lambda:self.sendButton(self.entryMsg.get()))
    self.buttonMessage.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)

  def goAhead(self, name):
    self.login.destroy()
    #self.name = name
    self.layout(name)
    rcv = Thread(target=self.recieve)
    rcv.start()

  def sendButton(self,msg):
    self.textCons.config(state=DISABLED)
    self.msg = msg
    self.entryMsg.delete(0,END)
    snd = Thread(target=self.write)
    snd.start()

  def showMsg(self, message):
    self.textCons.config(state=NORMAL)
    self.textCons.insert(END, message+"\n\n")
    self.textCons.config(state=DISABLED)
    self.textCons.see(END)

  def write(self):
    self.textCons.config(state=DISABLED)
    while True:
      message = (f"{self.name}: {self.msg}")
      client.send(message.encode('utf-8'))
      self.showMsg(message)
      break
  
  def recieve(self):
    while True:
      try:
        message = client.recv(2048).decode("utf-8")
        if message == "NICKNAME":
          client.send(self.name.encode("utf-8"))
        else:
          self.showMsg(message)
      except:
        print("An error occured!")
        client.close()
        break



g = GUI()

# def write():
#   while True:
#     message = "{}:{}".format(nickname,input(""))
#     client.send(message.encode("utf-8"))

# recvThread = Thread(target=recieve)
# recvThread.start()

# writeThread = Thread(target=write)
# writeThread.start()

