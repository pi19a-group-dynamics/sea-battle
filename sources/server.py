import socket
from threading import Thread


class Server(Thread):
    def __init__(self, server_field):
        Thread.__init__(self)
        self.socket = socket.socket()
        self.socket.bind(('0.0.0.0', 4747))
        self.socket.listen(1)
        self.field = [['0' for i in range(12)] for i in range(12)]
        self.server_field = server_field
        self.player_connected = False
        self.conn = None
        self.do_run = True
        self.x = 0
        self.y = 0
        self.shot = False
        self.turn = True
    

    def run(self):
        try:
            self.conn, self.addr = self.socket.accept()
        except: self.do_run = False

        while self.do_run:
            operation = None

            try:
                operation = self.conn.recv(1).decode()
            except: self.do_run = False
            
            if not operation: break

            # player connection
            if operation == '+':
                # receive client field
                for i in range(12):
                    for j in range(12):
                        cell = self.conn.recv(2).decode()
                        if cell[1] == ' ':
                            cell = cell.strip()
                        self.field[i][j] = cell
                
                # send server field
                self.conn.send(str.encode('+'))
                for i in range(12):
                    for j in range(12):
                        cell = self.server_field[i][j]
                        if len(cell) == 1:
                            cell += ' '
                        self.conn.send(str.encode(cell))

                self.player_connected = True

            # hit receive
            elif operation == '*':
                self.x = int(self.conn.recv(2).decode())
                self.y = int(self.conn.recv(2).decode())
                self.shot = True
        
        if self.conn:
            self.conn.close()
        self.socket.close()
    

    def do_shot(self, x, y):
        # send shot
        x = str(x)
        y = str(y)
        if int(x) < 10:
            x += ' '
        if int(y) < 10:
            y += ' '
        self.conn.send(str.encode('*'))
        self.conn.send(str.encode(x))
        self.conn.send(str.encode(y))