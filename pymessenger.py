from Crypto.Cipher import AES
from Crypto import Random
import socket
from time import gmtime, strftime

class messenger:

    def currentTime(self):
        dateTime = strftime("%d-%m-%Y %H:%M:%S", gmtime())
        return dateTime

    def encrypt(self, message):

        obj = AES.new('3spOrAEplGNbYLQT6SfUO', AES.MODE_CBC, '61886891308545195383516181521626211')
        ciphertext = obj.encrypt(m)
        return ciphertext


    def decrypt(self, ciphertext):
        objd = AES.new('3spOrAEplGNbYLQT6SfUO', AES.MODE_CBC, '61886891308545195383516181521626211')
        plaintext = objd.decrypt(ciphertext)
        return plaintext

    def portSender(self, message):
        IP = '172.19.2.1'
        PORT = 5000
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((IP, PORT))
        self.sock.sendto(message.encode(), (IP, PORT))

    def portListen(self):
        IP = ''
        PORT = 5000
        data, self.addr = self.sock.recvfrom(64024)
        print(self.currentTime(), data.decode())

    def main(self):
        name = "Matt: "
        while True:
            print(self.currentTime(), end='')
            text = (str(input(" - ")))
            m = text.encode('utf-8')
            self.portSender(name+text)
            self.portListen()


if __name__ == '__main__':
   message = messenger()
   message.main()

