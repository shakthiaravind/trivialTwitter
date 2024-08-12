import socket
import selectors
import types
import csv

#function for getting new socket object and registering with selector
def accept_wrapper(sock):
    conn, addr = sock.accept()
    print('\naccepted connection from', addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)
    
#function for processing all the commands (contains everything to operate on the socket)
def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)

        if recv_data:
            msg = recv_data.decode()
            msg_list = msg.split(' ')

#TWEET
# "tweet 'message' username
            if msg_list[0] == 'tweet':
                msg_list.pop(0)
                user = msg_list.pop()
                user.strip()
                msg_original = ' '.join(msg_list)
                if(len(msg_original)==0):
                    data.outb = b'Length of tweet should be greater than 0'
                else:
                    message = user+ ': '+ msg_original+ '\n'
#adding message to other user's mailbox
                    for user_ in from_mailbox:
                        if user_ != user:
                            from_mailbox[user_] += [message]
                            from_mailbox[user_][0] +=1      #updating total messages
                            #print(user_, from_mailbox[user_]) ##
                    data.outb = b'Message posted.'
                    
                sock.send(data.outb)

#TIMELINE
# "timeline username"
            elif msg_list[0] == 'timeline':
                n= 0
                msg_list.pop(0)
                user = msg_list.pop()
                for user_ in from_mailbox:
                    if user == user_:       #identifying the mailbox
                        if from_mailbox[user_][1] < from_mailbox[user_][0]:         #checking if unread < total messages
                            for i in range(from_mailbox[user_][1], from_mailbox[user_][0]):
                                reply = user_+ ' from '+ from_mailbox[user_][i]
                                data.outb = reply.encode()
                                n += 1
                                sock.send(data.outb)
                            from_mailbox[user_][1] += n         #updating unread

                        else:
                            data.outb = b'No new messages.'
                            sock.send(data.outb)

#NEW - CREATING NEW ACCOUNT
# "new username password"
            elif msg_list[0] == 'new':
                flag = True
                msg_list.pop(0)
                new_username = msg_list[0]
                password = msg_list[1]
##                outfile = open('TTaccounts.csv', 'a')
##                outfile.close()
                
#account with given username already exits, choose new username
                with open('TTaccounts.csv', newline='') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if new_username == row[0]:
                            data.outb = b'0Username already exits.'
                            flag = False
                            
#Registering new account
                if flag == True:
                    with open('TTaccounts.csv', 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerows([[new_username, password]])
                        data.outb = b'1Account created successfully!'
                        
                sock.send(data.outb)
                
#LOGOUT
# "logout username"
            elif msg_list[0] == 'logout':
                user1 = msg_list.pop()
                from_mailbox.pop(user1)
                data.outb = b'Logged out.'
                
                sock.send(data.outb)

#LOGIN
# "username password" (login)
            else:
                new_user = msg_list[0]
                new_user.strip()
                password = msg_list[1]
##                outfile = open('TTaccounts.csv', 'a')
##                outfile.close()

## data.outb = b"Couldn't find Trivial Twitter account."
                
#account with given user name does not exist
                with open('TTaccounts.csv', newline='') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        #print(row)
                        if new_user != row[0]:
                            data.outb = b"Couldn't find Trivial Twitter account."
                            
#username & password correct but user already logged in
                        elif new_user == row[0]:
                            if password == row[1]:
                                if new_user in from_mailbox:
                                    data.outb = b'0User already login, shutdown client.'
                                    
#username & password correct logging in
                                else:
                                    from_mailbox[new_user] = [2,2]
                                    #tweet pointers [0] -> total, [1] ->read, [2...] ->tweets
                                    data.outb = b'1Connection established'
                                    break

#username correct, password incorrect
                            else:
                                data.outb = b'Incorrect password.'
                                break
                sock.send(data.outb)

#unregistering socket and closing connection
    else:
        print('\nclosing connection to', data.addr)
        sel.unregister(sock)
        sock.close()



########################################################################


host = '127.0.0.1'
port = 8080

with open('TTaccounts.csv', 'a', newline='') as file:
    writer = csv.writer(file)
    writer.writerows([['USERNAME', 'PASSWORD']])

msg = ''
msg_list = []
user = ''
msg_original = ''
#mailbox = []
from_mailbox = {}

sel = selectors.DefaultSelector()

#listening socket
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print('\nlistening on', (host, port))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

#event loop
while True:
    events = sel.select(timeout=None)
    for key, mask in events:
        if key.data is None:
            accept_wrapper(key.fileobj)
        else:
            service_connection(key, mask)

