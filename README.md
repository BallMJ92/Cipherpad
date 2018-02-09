# Cipherpad

A cryptographically secure instant messenger utilizing RSA encryption over LAN-UDP/IP<sup>1</sup>. Cipherpad utilizes time-stamps in order to change public and private keys for each new session initiated. User IP addresses are hard-coded into python, in order for multiparty verification of session owner. Any user IP address not hard-coded in, will make the program abandon all sessions. This is due to a break in the trust relationship between the session owner, session members and program verification mechanisms.

**Usage**
Make sure that all recipients along with yourself are hardcoded into the directory dictionary. This is so the program can begin a trust relationship between all session members.

Run *Cipherpad* py file on your machine
