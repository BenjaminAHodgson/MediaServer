import paramiko
import socket
import tkinter as tk
import tkinter.filedialog as tkft
import subprocess
import sys
import time
import os


class UserInterface(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.connectionEstablished = False
        self.ssh_client = paramiko.SSHClient()

        # WINDOW COMPONENTS (INITIAL STATE)
        self.title("Connect to your Server")
        self.minsize(width=200, height=200)
        self.resizable(False, False)
        self.ssh = tk.Button(self, text="Connect", command=self.sshConnect, padx= 50)
        self.passwordEntry = tk.Entry(self, show='*')
        self.hostEntry = tk.Entry(self)
        self.usernameEntry = tk.Entry(self)
        self.labelUsername = tk.Label(self, text="Username")
        self.labelPassword = tk.Label(self, text="Password")
        self.labelHost = tk.Label(self, text="Host Name or Local Address")

        # CONDITIONAL COMPONENTS
        self.finalize = tk.Button(self, text="Continue", command=self.sftpConnect, padx= 50)
        self.status = tk.Label(self, text="Status: Please fill all fields.")

        # POSITIONING (INITIAL STATE)
        self.ssh.grid(row=5, column=2)
        self.labelHost.grid(row=2, column=1)
        self.hostEntry.grid(row=2, column=2)
        self.labelUsername.grid(row=3, column=1)
        self.usernameEntry.grid(row=3, column=2)
        self.labelPassword.grid(row=4, column=1)
        self.passwordEntry.grid(row=4, column=2)
        self.status.grid(row=1, column=1)

        ## Raspberry Pi IP Print

        ## LOOK FOR RASPBERRY PI Address on Windows, and then MAC ##
    
        raspiIPWindows = subprocess.getoutput('arp -a | findstr b8-27-eb')
        raspiIPMac = subprocess.getoutput('arp -na | grep -i b8:27:eb')
        
        raspiIPMac = str(raspiIPMac)
        raspiIPWindows = str(raspiIPWindows)

        if raspiIPMac == '':
            raspiIPMac = 'Not Found'
        if raspiIPWindows == '/bin/sh: findstr: command not found':
            raspiIPWindows = '10.0.0.1 to 10.0.0.9'

        labelString = 'Potential Host Address: ' + raspiIPWindows + ' OR ' + raspiIPMac

        ## Print Address to GUI
        self.potentialIP = tk.Message(self, text=labelString, font=('Courier', 10))
        self.potentialIP.config(width = 250)
        self.potentialIP.grid(row = 6, column= 1)

    def fileTransferState(self):

        ## List and destroy previous UI grid.
        list = self.grid_slaves()

        for i in list:
            i.destroy()

        # WINDOW COMPONENTS (TRANSFER STATE)
        self.title("Media Server")
        self.minsize(width=200, height=200)
        self.resizable(False, False)
        self.sendFileOption = tk.Button(self, text="Choose File", command=self.chooseFile, pady=50, padx= 50)

        # CONDITIONAL COMPONENTS (TRANSFER STATE)
        pictures = "Pictures"
        video = "Videos"
        music = "Music"
        document = "Documents"
        self.music = tk.Button(self, text="Music", bg='green', command=lambda: self.sendFile(music))
        self.video = tk.Button(self, text="Videos", bg='green', command=lambda: self.sendFile(video))
        self.picture = tk.Button(self, text="Pictures", bg='green', command=lambda: self.sendFile(pictures))
        self.document = tk.Button(self, text="Documents", bg='green', command=lambda: self.sendFile(document))
        self.dialog = tk.Label(self, text="Which folder?")

        self.transferFailure = tk.Label(self, text="Transfer Failed")
        self.transfer = tk.Label(self, text="Transferring...")
        self.transferSuccess = tk.Label(self, text="Transfer Success")

        # POSITIONING (TRANSFER STATE)
        self.sendFileOption.pack()

    ## User credentials entry + SSH connection
    def sshConnect(self):



        self.username = self.usernameEntry.get()
        self.password = self.passwordEntry.get()
        self.host = self.hostEntry.get()

        if self.username is "" or self.password is "" or self.host is "":
            self.status.destroy()
            self.status = tk.Label(self, text="Status: Fill all fields.")
            self.status.grid(row=1, column=1)
            return

        try:
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(hostname=self.host, username=self.username, password=self.password)
            self.status.destroy()
            self.status = tk.Label(self, text="Status: Connected")
            self.status.grid(row=1, column=1)
            self.connectionEstablished = True
            self.ssh.destroy()
            self.finalize.grid(row=5, column=2)
            return

        except paramiko.AuthenticationException:
            self.status.destroy()
            self.status = tk.Label(self, text="Status: Connection Failed.")
            self.status.grid(row=1, column=1)
            self.ssh_client.close()
            return

        except socket.error:
            self.status.destroy()
            self.status = tk.Label(self, text="Status: Connection Failed.")
            self.status.grid(row=1, column=1)
            self.ssh_client.close()
            return

    ## Convert SSH to SFTP
    def sftpConnect(self):
        try:
            self.sftp_client = self.ssh_client.open_sftp()
            self.fileTransferState()
        except paramiko.AuthenticationException:
            self.sftp_client.close()
        except socket.error:
            self.sftp_client.close()

    ## Select file in File Browser
    def chooseFile(self):
        self.file = tkft.askopenfile(parent=self)
        print(str(self.file))
        self.fileName = os.path.basename(self.file.name)
        print(str(self.fileName))
        self.fileDir = self.file.name

        self.dialog.pack()
        self.document.pack()
        self.music.pack()
        self.video.pack()
        self.picture.pack()

    ## Finalize and PUT file.
    def sendFile(self, string):
        
        remoteDir = "/home/pi/" + string + '/' + self.fileName
        print(remoteDir)

        try:           
            self.sftp_client.put(self.fileDir, remoteDir)
            self.transfer.destroy()
            self.transferSuccess.pack()
            time.sleep(1)
            self.transfer.destroy()

        except paramiko.SFTPError:
            self.transferFailure.pack()

def main():

    try:
        UI = UserInterface()
        UI.mainloop()

    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)


if __name__ == "__main__":
    main()
