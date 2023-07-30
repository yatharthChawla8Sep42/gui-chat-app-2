import socket
from threading import Thread
import random

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ip = '127.0.0.1'
port = 8000
server.bind((ip, port))

server.listen()

clients = []
nicknames = []
questions = [
  "What's 9 + 10? \n a) 1 \n b) 19 \n c) 21 \n d) 90",
  "What is Obama's last name? \n a) Barack \n b) Johnnythan \n c) John2 \n d) Obama",
  "How many letters are in The Alphabet? \n a) 26 \n b) 11 \n c) 8 \n d) 27"
]
answers = ["c","d","b"]
numOfQ = len(questions)

def getRandomQuestion(conn):
  randomIndex = random.randint(0, len(questions)-1)
  randomQuestion = questions[randomIndex]
  randomAnswer = answers[randomIndex]
  conn.send(randomQuestion.encode("utf-8"))
  return randomIndex, randomQuestion, randomAnswer


def clientThread(conn, addr):
  score = 0
  conn.send("Welcome to the Quiz Game!".encode("utf-8"))
  conn.send("Answer each question with a, b, c, or d.".encode("utf-8"))
  conn.send("Good Luck! \n\n".encode("utf-8"))
  index, question, answer = getRandomQuestion(conn)

  while True:
    try:
      message = conn.recv(2048).decode("utf-8").split(":")[1]
      if message:
        if message.lower() == " " + answer:
          score += 1
          conn.send(f"Correct! Your score is {score}\n\n".encode("utf-8"))
        else:
          conn.send(f"Incorrect! Your score is still {score}\n\n".encode("utf-8"))
        removeQuestion(index)
        index, question, answer = getRandomQuestion(conn)
      else:
        remove(conn)
    except:
      continue

def removeQuestion(index):
  questions.pop(index)
  answers.pop(index)
        
def remove(conn):
  if conn in clients:
    clients.remove(conn)

while True:
  conn, addr = server.accept()
  conn.send('NICKNAME'.encode("utf-8"))
  nickname = conn.recv(2048).decode("utf-8")
  clients.append(conn)
  nicknames.append(nickname)

  message = '{} entered the quiz'.format(nickname)
  print(message)

  newThread = Thread(target=clientThread, args=(conn,addr))
  newThread.start()
  
