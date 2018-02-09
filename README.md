# Cipherpad

A cryptographically secure instant messenger utilizing RSA encryption over UDP/IP. Cipherpad utilizes time-stamps in order to change public and private keys for each new session initiated. User IP addresses are hard-coded into python, in order for multiparty verification of session owner. Any user IP address not hard-coded in, will make the program abandon all sessions. This is due to a break in the trust relationship between the session owner, session members and program verification mechanisms.
