# Import modules
import socket, os, subprocess, time         

# Initialize and wait for connection
s = socket.socket()         
host = socket.gethostname() 
port = 5000                
bufsize = 4096
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))       

s.listen(5)
def run():
  while True:
    # Establish connection with client.
    c, addr = s.accept()    
    print 'Got connection from', addr
    c.send('Thank you for connecting')

    while True:
      # Get and check user input
      userInput = c.recv(1024)
      if userInput == "Error 13: unexpected dc":
        c.shutdown(socket.SHUT_RDWR)
        c.close()
        print "lost connection"
        #time.sleep( 20 )
        run()
        break

      if userInput.split(" ")[0] == "ls":
        # Run ls command on server and send results to client
        print "inputed ls"
        output = subprocess.check_output(userInput, shell=True)
        c.send(output)

      elif userInput.split(" ")[0] == "get":
        # Get filename from input 
        print "inputed get"
        somefile = userInput.split(" ")[1]

        if os.path.isfile(somefile):
          # Send all bytes of file and end message
          bytes = open(somefile).read()
          c.send(bytes)
          c.send(":endT:")
          print c.recv(1024)
        else:
          c.send(":errorT:")

      elif userInput.split(" ")[0] == "put":
        # Get filename and initialize data
        print "inputed put"
        fName = os.path.basename(userInput.split(" ")[1])
        data = "" 

        while True:
          # Loop to recieve all buffered data until end message recieved
          if (":endT:" in data): break
          data += c.recv(bufsize)
          print 'writing file ...'

        # Open and write data to new file excluding end message  
        myfile = open(fName, 'w')
        myfile.write(data[:-6])
        # Close file and send success message
        myfile.close()
        c.send('success')

      elif userInput.split(" ")[0] == "cd":
        # Verify running command causes no errors
        print "inputed cd"
        try:
          # Run command and send success message
          os.chdir(userInput.split(" ")[1])
          c.send('success')
        except OSError as e:
          # Send client the error
          c.send(e.strerror)      

      elif userInput.split(" ")[0] == "mkdir":
        # Verify running command causes no errors
        print "inputed mkdir"
        try:
          # Run command and send success message
          os.system(userInput)
          c.send('success')
        except OSError as e:
          # Send client the error
          c.send(e.strerror) 

run()

# Close the connection
c.close()
