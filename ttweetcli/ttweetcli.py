import socket
import sys
from tkinter import *
from tkinter import ttk

#server ip & port
host = '127.0.0.1'
port = 8080

msg_original = ''
msg_list = []
msg = ''

################################################################################

#Defining scrollable frame (used for displaying the tweets)

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

################################################################################

#Trivial Twitter - New Account page
        
class Newaccount():
    def __init__(self):
        self.newacc_window = None

    def newacc(self):
        self.newacc_window = Tk()
        self.newacc_window.title('Trivial Twitter - New Account')
        self.newacc_window.configure(bg='#4863A0')
        self.newacc_window.rowconfigure([0,1,2,3,4,5,6], weight = 1, minsize = 50)
        self.newacc_window.columnconfigure([0,1,2,3,4], weight = 1, minsize = 50)
        
#Trivial Twitter logo
        nimage = PhotoImage(file='./ttlogo.png')
        nlbl1 = Label(master=self.newacc_window, image=nimage)
        nlbl1.grid(row=0, column=2)

        nlbl2 = Label(master=self.newacc_window, text='Happening now', bg='#4863A0', fg='white', font='arial 30 bold')
        nlbl2.grid(row=1, column=1, columnspan=3)

        nlbl3 = Label(master=self.newacc_window, text='Join Trivial Twitter today.', bg='#4863A0', fg='white', font='arial 22 bold')
        nlbl3.grid(row=2, column=1, columnspan=3)

#frame - holding labels & entry fields
        nfrm1 = Frame(master=self.newacc_window, width=550, height=550, bg='black')
        nfrm1.grid(row=3, column=1, columnspan=3)
        nfrm1.rowconfigure([0,1,2,3,4,5,6,7,8,9,10], weight=1, minsize=50)
        nfrm1.columnconfigure([0,1,2,3,4,5,6], weight=1, minsize=50)

        nlbl4 = Label(master=nfrm1, text='Username', bg='black', fg='white', font='arial 18 bold')
        nlbl4.grid(row=1, column=0, columnspan=2)

        nlbl5 = Label(master=nfrm1, text='Password', bg='black', fg='white', font='arial 18 bold')
        nlbl5.grid(row=3, column=0, columnspan=2)

        nlbl6 = Label(master=nfrm1, text='Re-type password', bg='black', fg='white', font='arial 18 bold')
        nlbl6.grid(row=5, column=0, columnspan=2)

        nent1 = Entry(master=nfrm1, bg='black', fg='white', highlightbackground='#1DA1F2', font='arial 16 bold')
        nent1.grid(row=1, column=3)
        
        nent2 = Entry(master=nfrm1, bg='black', fg='white', highlightbackground='#1DA1F2', font='arial 16 bold', show='*')
        nent2.grid(row=3, column=3)
        
        nent3 = Entry(master=nfrm1, bg='black', fg='white', highlightbackground='#1DA1F2', font='arial 16 bold', show='*')
        nent3.grid(row=5, column=3)
        
#feedback label
        nlbl7 = Label(master=nfrm1, text='', bg='black', fg='red', font='arial 18 bold')
        nlbl7.grid(row=9, column=1, columnspan=5)
        
#event (create button)
        def create1():
            new_username = nent1.get()      #entry field values
            npassword = nent2.get()
            re_pass = nent3.get()
            
            if len(new_username) < 6 or len(new_username) > 30:
                nlbl7['text'] = 'Username must be 6 to 30 characters.'

            elif len(npassword) < 8:
                nlbl7['text'] = 'Password must contain atleast 8 characters.'
                
            elif npassword != re_pass:      #comparing passwords
                nlbl7['text'] = "Password didn't match.Try again."

            else:
                nmsg = 'new '+ new_username+ ' '+ npassword         # "new username password"

                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ns:
                    ns.connect((host, port))
                    ns.sendall(nmsg.encode())       #sending username & password to server
                    recv_data = ns.recv(1024)
                    
                    if recv_data:       #feedback
                        nfeedback = recv_data.decode()
                        
                        if nfeedback[0] == '0':
                            nlbl7['fg'] = 'red'
                        else:
                            nlbl7['fg'] = '#16F529'

                        nlbl7['text'] = nfeedback[1:]

        nbtn1 = Button(master=nfrm1, width=15, text='Create', bg='white', fg='black', font='arial 16 bold', command = create1)
        nbtn1.grid(row=7, column=2, columnspan=2)

        self.newacc_window.mainloop()

################################################################################
        
#Trivial Twitter - Profile page
        
class Profilepage():
    def __init__(self, user_name = ''):
        self.profile_window = None
        self.user_name = user_name

    def profile(self):
        self.profile_window = Tk()
        self.profile_window.title('Trivial Twitter - Profile')
        self.profile_window.configure(bg='#4863A0')
        self.profile_window.rowconfigure([0, 1, 2], weight=1, minsize=50)
        self.profile_window.columnconfigure([0, 1, 2, 3, 4], weight=1, minsize=50)
        
#holding profile pic, username, pfrm2, pfrm6
        pfrm1 = Frame(master=self.profile_window, width=1000, height=300, bg='black')
        pfrm1.grid(row=0, column=1, columnspan=3, sticky='n')
        pfrm1.rowconfigure([0, 1], weight=1, minsize=100)
        pfrm1.columnconfigure([0, 1, 2, 3, 4], weight=1, minsize=150)
    
#default profile picture
        pimage = PhotoImage(file='./profilepic.png')
        plbl1 = Label(master=pfrm1, image=pimage)
        plbl1.grid(row=0, column=0, sticky='e')

        plbl2 = Label(master=pfrm1, text='@'+ self.user_name, bg='black', fg='#FFA500', font='arial 16 bold')
        plbl2.grid(row=1, column=0, sticky='ne')
    
#feedback label
        plbl3 = Label(master=self.profile_window, text='', bg='#4863A0', fg='#16F529', font='arial 16 bold')
        plbl3.grid(row=2, column=1, columnspan=3)
    
#pfrm2 - holding tweet, timeline buttons
        pfrm2 = Frame(master=pfrm1, width=100, height=30, bg='black')
        pfrm2.grid(row=1, column=0, sticky='se', columnspan=2)
        pfrm2.rowconfigure([0,1, 2, 3, 4], weight=1, minsize=6)
        pfrm2.columnconfigure([0,1, 2, 3, 4], weight=1, minsize=20)

#pfrm6 - holding logout button
        pfrm6 = Frame(master=pfrm1, width=50, height=30, bg='black')
        pfrm6.grid(row=1, column=3, sticky='se', columnspan=2)
    
#event (logout button)
        def logout():
            msg = 'logout '+ self.user_name         # "logout username"
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                s.sendall(msg.encode())
                recv_data = s.recv(1024)
                if recv_data.decode() == 'Logged out.':
                    print(recv_data.decode())
                    self.profile_window.destroy()

#logout button
        pbtn6 = Button(master=pfrm6, text='Log out', width=10, height=2, fg='red', bg='white', font='arial 14 bold', command = logout)
        pbtn6.grid()
    
#TWEET event START
        def tweet():
            pfrm3 = Frame(master=self.profile_window, width=600, height=250, bg='black')
            pfrm3.grid(row=1, column=1, rowspan=2, columnspan=3, sticky='n')
            pfrm3.rowconfigure([0,1,2,3,4], weight=1, minsize=50)
            pfrm3.columnconfigure([0,1,2,3,4], weight=1, minsize=120)

            txt1 = Text(master=pfrm3, width=60, height=10, bg='white', fg='black', highlightbackground='#1DA1F2', font='arial 18 bold', wrap = WORD)
            txt1.grid(row = 1, column = 1, rowspan = 2, columnspan = 3)

#event (post button)
            def post():
                msg_original = 'tweet '+ txt1.get('1.0', 'end')
                msg_list = list(msg_original.split(' '))
                msg_list.append(self.user_name)
                msg = ' '.join(msg_list)        # "tweet 'message' username"

                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((host, port))
                    s.sendall(msg.encode())
                    recv_data = s.recv(1024)
                
                    if recv_data:
                        plbl3['fg'] = '#16F529' ##
                        plbl3['text'] = recv_data.decode()
                    
#post button
            pbtn3 = Button(master=pfrm3, text='Post', width=10, height=2, bg='white', fg='#00008B', font='arial 14 bold', command = post)
            pbtn3.grid(row=3, column=3, sticky='se')

#event (close button)
            def x():
                pfrm3.destroy()
                plbl3['text'] = ''
            
#close button
            pbtn4 = Button(master=pfrm3, text='x', fg='red', bg='white', command = x)
            pbtn4.grid(row=0, column=0, sticky='nw')
        
#TWEET event END
        pbtn1 = Button(master=pfrm2, text='Tweet', width=10, height=2, bg='white', fg='#00008B', font='arial 14 bold', command = tweet)
        pbtn1.grid(row=2, column=1, sticky='s')


#TIMELINE event START
        def timeline():
            frame1 = ScrollableFrame(container = self.profile_window, width = 750, height = 600) #scrollable frame
            frame1.grid(row = 1, column = 1, rowspan = 2, columnspan = 3, sticky = 'n')
        
            frame2 = Frame(master= frame1.scrollable_frame, width = 600, height = 20, bg = 'black')
            frame2.pack(pady = 10)

            #event (close button)
            def x1():
                frame1.destroy()
                plbl3['text'] = ''
                
    #close button
            pbtn5 = Button(master=frame1, text='x', bg = 'white', fg='red', command = x1) #
            pbtn5.pack()
            
            msg_original = 'timeline'
            msg_list = list(msg_original.split(' '))
            msg_list.append(self.user_name)
            msg = ' '.join(msg_list) # "timeline username"
            
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                s.sendall(msg.encode())
                recv_data = s.recv(1024)
                
                if recv_data:
                    feedback = recv_data.decode()
                    if feedback == 'No new messages.':
                        plbl3['fg'] = 'black'
                        plbl3['text'] = feedback

                    else:
                        tweet_list = list(feedback.split('\n\n'))
                        tweet_list.pop() ##
                        #print(tweet_list)

                        for t in tweet_list:
                            #tweet = t
                            t_list = list(t.split(' '))
                            sender = t_list[2]
                            sender = sender.replace(':', '')
                            a = t.split(':')
                            tweet1 = a[1]
                            tweet1.strip()
                            tweet = '@'+ sender+ '\n\n'+ tweet1

#holding tweets
                            pfrm4 = Frame(master = frame1.scrollable_frame, width = 600, height = 150, bg = 'black')
                            pfrm4.pack(pady = 10)
                            pfrm4.rowconfigure([0,1,2], weight=1, minsize = 50)
                            pfrm4.columnconfigure([0,1,2], weight = 1, minsize = 200)
                            
#holding like, retweet buttons
                            pfrm5 = Frame(master=pfrm4, width=100, height=30, bg='black')
                            pfrm5.grid(row=2, column=0, sticky='sw', columnspan=2)
                            pfrm5.rowconfigure([0,1, 2, 3, 4], weight=1, minsize=6)
                            pfrm5.columnconfigure([0,1, 2, 3, 4], weight=1, minsize=20)
                            
#tweets
                            plbl4 = Label(master=pfrm4, text=tweet, bg='black', fg='#93FFE8', font='arial 16 bold', wraplength=280)
                            plbl4.grid(row=0, column=0, sticky='nw', rowspan=2, columnspan=5)
                            
#like button
                            pcbtn1 = Checkbutton(master=pfrm5, text='\U0001F44D')
                            pcbtn1.grid(row=2, column=1, sticky='s')

#retweet button
                            pcbtn2 = Checkbutton(master=pfrm5, text='\U0001F503')
                            pcbtn2.grid(row=2, column=3, sticky='s')
                                               
    #TIMELINE event END
        pbtn2 = Button(master=pfrm2, text='Timeline', width=10,height=2, bg = 'white', fg='#00008B', font = 'arial 14 bold', command = timeline)
        pbtn2.grid(row=2, column=3, sticky='s')
        
        self.profile_window.mainloop()


################################################################################
        
#Trivial Twitter (login page)
        
window = Tk()
window.title('Trivial Twitter')
window.configure(bg='#4863A0')
window.rowconfigure([0,1,2], weight=1, minsize=50)
window.columnconfigure([0,1,2], weight=1, minsize=50)

frm1 = Frame(master=window, width=550, height=550, bg='black')
frm1.grid(row=1, column=1)
frm1.rowconfigure([0,1,2,3,4,5,6,7,8,9,10], weight=1, minsize=50)
frm1.columnconfigure([0,1,2,3,4,5,6], weight=1, minsize=50)

image = PhotoImage(file='./ttlogo.png')
lbl1 = Label(master=window, image=image)
lbl1.grid(row=0, column=1)

lbl2 = Label(master=frm1, text='Sign in to Trivial Twitter', bg='black', fg='white', font='arial 28 bold')
lbl2.grid(row=1, column=1, sticky='nsew', columnspan=5)

#username
ent1 =Entry(master=frm1, width=25, bg='black', fg='white', highlightbackground='#1DA1F2', font='arial 16 bold')
ent1.grid(row=3, column=2, columnspan=3)

#password
ent2 =Entry(master=frm1, width=25, bg='black', fg='white', highlightbackground='#1DA1F2', font='arial 16 bold', show='*')
ent2.grid(row=5, column=2, columnspan=3)

#feedback label
lbl3 = Label(master=frm1, text='', bg='black', fg='red', font='arial 20')
lbl3.grid(row=8, column=1,columnspan=5)

#event (log in button)
def login():
    user_name = ent1.get()
    password = ent2.get()
    msg = user_name+ ' '+ password      # "username password"

    if not user_name.isalnum():
        lbl3['text'] = 'Illegal username'
        
    else:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(msg.encode())         #sending username & password to server
            recv_data = s.recv(1024)
            
            if recv_data:       #feedback
                feedback = recv_data.decode()
                if feedback[0] == '0':
                    lbl3['text'] = feedback[1:]
                    print(feedback[1:])
                    sys.exit()
                    
#REDIRECTING to PROFILE page
                elif feedback[0] == '1':
                    lbl3['text'] = feedback[1:]
                    window.destroy()
                    page = Profilepage(user_name)
                    page.profile()

                else:
                    lbl3['text'] = feedback
                    
#event (create button)
#REDIRECTING to NEW ACCOUNT page
def create():
    window.destroy()
    page1 = Newaccount()
    page1.newacc()
    
#login button
btn1 = Button(master=frm1, width=15, text='Log in', bg='white', fg='black', font='arial 16 bold', command = login)
btn1.grid(row=7, column=3)

#create button
btn2 = Button(master=frm1, width=20, text='Create Account', bg='white', fg='black', font='arial 16 bold', command = create)
btn2.grid(row=9, column=3)

lbl4 = Label(master=window, text='(c) 2022 Trivial Twitter, Inc [v2.5]', bg='#4863A0', fg='black', font='arial 16 bold')
lbl4.grid(row=2, column=1)

window.mainloop()
