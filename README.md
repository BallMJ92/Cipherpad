# cryptpad

A cryptographically secure instant messenger utilizing RSA encryption over IP. Cryptpad utilizes time-stamps in order to change public and private keys for each new session initiated. User IP addresses are hard-coded into python, in order for multiparty verification of session owner. Any user IP address not hard-coded in, will make the program abandon all sessions.
