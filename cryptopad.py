from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import socket
from time import gmtime, strftime

class messenger:

    def currentTime(self):
        dateTime = strftime("%d-%m-%Y %H:%M:%S", gmtime())
        return dateTime

    def generateRSAKeys(self, keyLength):
        private = RSA.generate(keyLength)
        public = private.publickey()
        privateKey = private.exportKey()
        publicKey = public.exportKey()
        
        # Writing Public Key to file
        with open('pubkey.der', 'wb') as puKeyFile:
            puKeyFile.write(publicKey)
        puKeyFile.close()

        # Writing Private Key to file
        with open('privkey.der', 'wb') as prKeyFile:
            prKeyFile.write(privateKey)
        prKeyFile.close()

    def rsaPublicEncrypt(self, data):
        # Importing and reading Public Key from file and assigning value to key variable
        publicKey = RSA.importKey(open('pubkey.der').read())
        cipher = PKCS1_OAEP.new(publicKey)
        
        # Encrypting plaintext data using Public Key
        self.ciphertext = cipher.encrypt(data)
        
        # Returning Cipher-text
        return self.ciphertext

    def rsaPrivateDecrypt(self, ciphertext):
        # Importing and reading Private Key from file and assigning value to key variable
        privateKey = RSA.importKey(open('privkey.der').read())
        cipher = PKCS1_OAEP.new(privateKey)
        
        # Decrypting cipher-text and assigning plaintext to message variable
        message = cipher.decrypt(ciphertext)
        return message

    def portSender(self, message):
        # Defining IP address and Port to send cipher-text to
        IP = '172.19.2.1'
        PORT = 5001
        
        # Opening port and binding in order to send cipher-text
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((IP, PORT))
        self.sock.sendto(message, (IP, PORT))

    def portListen(self):
        IP = ''
        PORT = 5001

        # Defining max data length
        data, addr = self.sock.recvfrom(64024)
        cipher = self.ciphertext

        # Decrypting received ciphertext using rsaPrivateDecrypt function
        plain = self.rsaPrivateDecrypt(data)

        # Printing current time along with plaintext decrypted from ciphertext
        print(self.currentTime(), plain.decode("utf-8"))

    def main(self):
        # Variable for RSA key length to be used in session
        keyLength = self.generateRSAKeys(1024)
        name = "Matt: "

        # Block for active session
        while True:
            print(self.currentTime(), end='')
            inputMessage = (input(" - ")).encode()

            # Turning input into bytes for encryption
            byteString = (b""+inputMessage)

            # Encrypting text input and sending it to IP address
            self.portSender(self.rsaPublicEncrypt(byteString))

            # Listening on port and printing decoded message received
            self.portListen()


if __name__ == '__main__':
   message = messenger()
   message.main()
