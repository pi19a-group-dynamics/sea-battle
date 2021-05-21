import socket
from threading import Thread


class Client(Thread):
    def __init__(self, ip, client_field):
        Thread.__init__(self)
        
        try: 
            self.socket = socket.socket()
            self.socket.connect((ip, 4747))
        except:
            self.socket = None
            return
        
        self.field = [['0' for i in range(12)] for i in range(12)]
        self.player_connected = False
        self.do_run = True
        self.x = 0
        self.y = 0
        self.shot = False
        self.turn = False

        # send client field
        self.socket.send(str.encode('+'))
        for i in range(12):
            for j in range(12):
                cell = client_field[i][j]
                if len(cell) == 1:
                    cell += ' '
                self.socket.send(str.encode(cell))
    

    def run(self):
        while self.do_run:
            operation = None

            try:
                operation = self.socket.recv(1).decode()
            except: self.do_run = False
            
            if not operation: break

            # receive server field
            if operation == '+':
                for i in range(12):
                    for j in range(12):
                        cell = self.socket.recv(2).decode()
                        if cell[1] == ' ':
                            cell = cell.strip()
                        self.field[i][j] = cell
                self.player_connected = True

            # hit receive
            if operation == '*':
                self.x = int(self.socket.recv(2).decode())
                self.y = int(self.socket.recv(2).decode())
                self.shot = True
        
        self.socket.close()


    def do_shot(self, x, y):
        # send shot
        x = str(x)
        y = str(y)
        if int(x) < 10:
            x += ' '
        if int(y) < 10:
            y += ' '
        self.socket.send(str.encode('*'))
        self.socket.send(str.encode(x))
        self.socket.send(str.encode(y))