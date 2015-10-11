# Import modules
import socket, os, atexit

def quit():
	print "Error 13: unexpected dc"
	s.send("Error 13: unexpected dc")
	s.close  

atexit.register(quit)

# Initialize and wait for connection
s = socket.socket()         
#host = socket.gethostname() 
host = '172.17.192.115'
port = 5000            
bufsize = 4096

s.connect((host, port))

print s.recv(1024)
print "Welcome to the server :)"

while True:
	# Get inputted command
	userInput = raw_input()

	if userInput.split(" ")[0] == "ls":
		# Send command and print recieved output
	    print "inputed ls"
	    s.send(userInput)
	    print s.recv(1024)

	elif userInput.split(" ")[0] == "get":
		# Send command and initialize data
		print "inputed get"
		s.send(userInput)
		fName = os.path.basename(userInput.split(" ")[1])
		data = "" 

		while True:
			# Loop to recieve all buffered data until end message recieved
			if (":endT:" in data or ":errorT:" in data): break
			data += s.recv(bufsize)
			print 'writing file ....'

		# Open and write data to new file excluding end message  
		if data == ":errorT:":
			print "File does not exist"
		else:
			myfile = open(fName, 'w')
			myfile.write(data[:-6])
			# Close file and send success message
			myfile.close()
			s.send('success')

	elif userInput.split(" ")[0] == "put":
		# Send command and print recieved output
		print "inputed put"
		fName = os.path.basename(userInput.split(" ")[1])
		if os.path.isfile(fName):
			s.send(userInput)

			bytes = open(fName).read()
			s.send(bytes)
			s.send(":endT:")
			print s.recv(1024)
		else:
			print "File does not exist"

	elif userInput.split(" ")[0] == "cd":
		# Send command and print recieved status message
		print "inputed cd"
		s.send(userInput)
		print s.recv(1024)

	elif userInput.split(" ")[0] == "mkdir":
		# Send command and print recieved status message
		print "inputed mkdir"
   		s.send(userInput)
   		print s.recv(1024)

# Close the socket when done
s.close                    