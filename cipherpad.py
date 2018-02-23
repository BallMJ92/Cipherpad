from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from colorama import init
from termcolor import cprint
from pyfiglet import figlet_format
import socket, os, sys
from time import gmtime, strftime

class messenger:

    # Setting current directory path to work from
    os.chdir("")

    def logo(self):
        init(strip=not sys.stdout.isatty())
        cprint(figlet_format("cipherpad", font="small"))
        
    def commands(self, com):
        bool = False
        if com == "help()":
            bool = True
            print("-COMMANDS:\n"
                  "-exit()\n"
                  "v - pubkey: Prints out public key being used in session for verification\n")
        elif com == "exit()":
            sys.exit()
        elif com == "v - pubkey" or com == "v-pubkey":
            bool = True
            with open('pubkey.der', 'r') as puKeyFile:
                for i in puKeyFile:
                    print(i)
            puKeyFile.close()
        elif com == "v - privkey" or com == "v-privkey":
            bool = True
            with open('privkey.der', 'r') as prKeyFile:
                for i in prKeyFile:
                    print(i)
                prKeyFile.close()

        return bool

    def timeStamp(self):
        # Creates a time stamp of session for program to generate new keys on next session
        with open("lastSession.txt", "w") as ls:
            ls.write("m"+self.currentTime())
            #ls.write("Initiated by: ")
        ls.close()

    def timeStampVerification(self):
        # Reading time stamp file
        previousSession = str()
        with open("lastSession.txt", "r") as ls:
            for i in ls:
                previousSession += i
        ls.close()

        return previousSession

    def keyFileModificationTime(self, filename):
        return strftime("%d-%m-%Y %H:%M:%S", gmtime(os.path.getmtime(filename)))

    def currentTime(self):
        dateTime = strftime("%d-%m-%Y %H:%M:%S", gmtime())
        return dateTime

    def addressBook(self):
        # Dictionary to hold IP addresses and corresponding users
        self.directory = {'172.19.2.1': 'UserOne: ', '172.19.2.5': 'UserTwo: '}
        return self.directory

    def generateRSAKeys(self, keyLength):
        private = RSA.generate(keyLength)
        public = private.publickey()
        privateKey = private.exportKey()
        publicKey = public.exportKey()

        # Writing Public Key to file
        if os.path.isfile("pubkey.der") == True:
            # Checking time stamp of last session against current session
            if self.timeStampVerification() != self.currentTime():
                # Generate new public key if time is different between previous and current session
                with open('pubkey.der', 'wb') as puKeyFile:
                    puKeyFile.write(publicKey)
                puKeyFile.close()
            else:
                pass
            pass
        else:
            with open('pubkey.der', 'wb') as puKeyFile:
                puKeyFile.write(publicKey)
            puKeyFile.close()

        # Writing Private Key to file
        if os.path.isfile("privkey.der") == True:
            # Checking time stamp of previous session. If time stamp is different from current time create new keys
            if self.timeStampVerification()[1:] != self.currentTime():
                if self.timeStampVerification()[0] == "a":
                    pass
                with open('privkey.der', 'wb') as prKeyFile:
                    prKeyFile.write(privateKey)
                    prKeyFile.close()
            else:
                pass
            pass
        else:
            with open('privkey.der', 'wb') as prKeyFile:
                prKeyFile.write(privateKey)
            prKeyFile.close()

        # Making a time stamp for this session of key generation
        self.timeStamp()

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
        for key, value in self.directory.items():
            try:
                if key == addr[0]:
                    user = value
            except Exception:
                user = "Unknown User: "

        # variable to capture ciphertext value from rsaPublicEncrypt function to show proof of concept (POC)
        cipher = self.ciphertext

        # Decrypting received ciphertext using rsaPrivateDecrypt function
        plain = self.rsaPrivateDecrypt(data)

        # Printing current time along with plaintext decrypted from ciphertext. Add cipher variable to print statement for RSA encryption POC
        print(self.currentTime(), user, plain.decode("utf-8"))

    def main(self):
        self.logo()
        """validation = input("Please enter IP address for validation: ")
        for key, value in self.addressBook().items():
            try:
                if key == validation:
                    print("validated")
            except Exception as e:
                sys.exit()"""
        # Variable for RSA key length to be used in session
        keyLength = self.generateRSAKeys(2048)

        # Code block for active session
        while True:
            # Formatting messenger to display time for each message sent and received
            print(self.currentTime(), end='')
            inputMessage = (input(" - ")).encode()

            """detectCommand = inputMessage.decode()
            command = self.commands(detectCommand)
            if command == False:
                pass"""

            # Encoding message input into bytes for encryption
            byteString = (b""+inputMessage)

            # Encrypting text input and sending it to IP address
            self.portSender(self.rsaPublicEncrypt(byteString))

            # Listening on port and printing decoded message received
            self.portListen()


if __name__ == '__main__':
   message = messenger()
   message.main()

