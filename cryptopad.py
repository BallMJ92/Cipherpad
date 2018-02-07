from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import socket, os
from time import gmtime, strftime

class messenger:

    # Setting current directory path to work from
    os.chdir("//degas/home/Py/K/e/y/")

    def currentTime(self):
        dateTime = strftime("%d-%m-%Y %H:%M:%S", gmtime())
        return dateTime

    def addressBook(self):
        # Dictionary to hold IP addresses and corresponding users
        directory = {'IP': 'USER: ', 'IP': 'USER: '}
        return directory

    def generateRSAKeys(self, keyLength):
        private = RSA.generate(keyLength)
        public = private.publickey()
        privateKey = private.exportKey()
        publicKey = public.exportKey()

        # Writing Public Key to file
        if os.path.isfile("pubkey.der") == True:
            pass
        else:
            with open('pubkey.der', 'wb') as puKeyFile:
                puKeyFile.write(publicKey)
            puKeyFile.close()

        # Writing Private Key to file
        if os.path.isfile("privkey.der") == True:
            pass
        else:
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

        # Variable to hold username corresponding to IP address in the addressbook
        user = ""

        # Importing user addressBook
        directory = self.addressBook()

        # Assigning username to user variable if corresponding IP address is in data received in addr variable
        # addr[0] == IP, addr[1] == PORT
        for key, value in directory.items():
            try:
                if key == addr[0]:
                    user = value
            except Exception as e:
                user = "Unknown User: "

        # variable to capture ciphertext value from rsaPublicEncrypt function to show proof of concept (POC)
        cipher = self.ciphertext

        # Decrypting received ciphertext using rsaPrivateDecrypt function
        plain = self.rsaPrivateDecrypt(data)

        # Printing current time along with plaintext decrypted from ciphertext. Add cipher variable to print statement for RSA encryption POC
        print(self.currentTime(), user, plain.decode("utf-8"))

    def main(self):
        # Variable for RSA key length to be used in session
        keyLength = self.generateRSAKeys(2048)

        # Code block for active session
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

