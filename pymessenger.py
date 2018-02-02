from Crypto.Cipher import AES
from Crypto import Random
import socket
from time import gmtime, strftime
import time

class messenger:

    encryptionKey = ""
    decryptionKey = ""

    def currentTime(self):
        dateTime = strftime("%d-%m-%Y %H:%M:%S", gmtime())
        return dateTime

    def p(self, s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)
    
    # Needs work
    def encrypt(self, message, key_size=256):
        key = b'\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18'
        message = self.p(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(message)

    # Needs work
    def decrypt(self, ciphertext):
        key = b'\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18'
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.rstrip(b"\0")

    def portSender(self, message):
        IP = '172.19.2.1'
        PORT = 5001
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((IP, PORT))
        self.sock.sendto(message.encode(), (IP, PORT))

    def portListen(self):
        IP = ''
        PORT = 5001
        data, self.addr = self.sock.recvfrom(64024)
        plain = self.decrypt(data.decode())
        print(self.currentTime(), plain)

    # Needs work
    def main(self):
        name = "Matt: "

        while True:
            print(self.currentTime(), end='')
            text = (str(input(" - ")))
            m = text.encode('utf-8')
            self.portSender(name+str(self.encrypt(m)))
            self.portListen()


if __name__ == '__main__':
   message = messenger()
   message.main()

