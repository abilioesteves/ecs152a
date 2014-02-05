from socket import *
import time as t
import datetime as dt

# standard configurations for the client
serverName = 'localhost'
serverPort = 19239
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)
for i in range(9):
    # create the objects of time needed to print the date as is asked for
    timeSent = dt.datetime.now()
    timeSentUTC = t.gmtime()

    # ping message
    message = "Ping " + str(i+1) + " "
    message += str(timeSentUTC[0]) + "-" + str(timeSentUTC[1]) + "-" + str(timeSentUTC[2]) + " T " + str(timeSentUTC[3]) + ":" + str(timeSentUTC[4]) + " UTC"

    #output
    print "\n" + message

    # ping
    clientSocket.sendto(message, (serverName, serverPort));
    try:
        # try to receive response
        modifiedMessage, serverAddress = clientSocket.recvfrom(1024)
        timeReceived = dt.datetime.now()
    except Exception:
        print "Request timed out"
        continue

    # output
    print modifiedMessage
    print "RTT: " + str(round((float(timeReceived.strftime('%s.%f')) - float(timeSent.strftime('%s.%f')))*1000, 3)) + "\n"
clientSocket.close()