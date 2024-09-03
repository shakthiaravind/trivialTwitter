# trivialTwitter

## Overview

In the age of information, people have an ever-growing need to share their experiences instantly. Social networking platforms like Facebook and Twitter facilitate this interaction with scalable infrastructure that reliably handles large volumes of information exchange.

Trivial Twitter is a simplified version of such social networking platforms. It mimics the fundamental aspects of social networking by implementing a client-server architecture that allows multiple clients to communicate instantaneously. This project utilizes a non-blocking server to orchestrate the exchange of text messages among users.

## Features

- **Inter-Process Communication**: Leveraging socket programming to establish communication between the server and clients.
- **User Authentication**: Server authenticates users with a password to ensure credibility.
- **Tweet Management**: Clients can tweet or view their timeline. Tweets are stored on the server and the timeline displays unread tweets from online users.
- **GUI Interface**: Built using Tkinter for a user-friendly experience.

The project is developed in Python 3.9.6 and uses TCP sockets for client-server communication. The server can handle multiple clients concurrently using `select()` from the `selectors` module.

## Usage

1. Clone the Repository:
   ```
   git clone https://github.com/shakthiaravind/trivialTwitter.git
   ```
2. Running the server
   ```
   $ cd trivialTwitter/ttweetsrv
   $ python3 ttweetsrv.py
   ```
3. Running the client
   ```
   $ cd ../ttweetcli
   $ python3 ttweetcli.py
   ```


