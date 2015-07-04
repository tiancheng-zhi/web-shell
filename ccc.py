from wrap import *
p = Popen('bash', stdin=PIPE, stdout=PIPE)
send_all(p,"")
recv_some(p)
