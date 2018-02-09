# Cipherpad

A cryptographically secure instant messenger utilizing RSA encryption over LAN-UDP/IP<sup> 1</sup>. **Cipherpad** utilizes time-stamps in order to change public and private keys for each new session initiated. User IP addresses are hard-coded into python, in order for multiparty verification of session owner. Any user IP address not hard-coded in, will make the program abandon all sessions. This is due to a break in the trust relationship between the session owner, session members and program verification mechanisms.

**Usage**

Step 1: Make sure that all recipients along with yourself are hardcoded into the directory dictionary. This is so the program can begin a trust relationship between all session members.

Step 2: Run **Cipherpad** py file on your machine

<sup>1</sup> A WLAN implementation is currently being developed. For now, **Cipherpad** works for machines on a networked environment where all machines have physical access to the public RSA keys (see TODO for more information).
