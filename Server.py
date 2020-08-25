'''pybluez wird hier als bibliothek benutzt'''
import bluetooth
from MotorManagement import *
import threading
import time
'''uuid des services'''
uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

'''Legt einen Socket an'''
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
'''bindet diesen socket an einen port'''
server_sock.bind(("", bluetooth.PORT_ANY))
'''Wartet auf verbindung an diesem port'''
server_sock.listen(1)
'''Holt sich den port an dem der Service anliegt (bis hier her ist dieser dem programm unbekannt)'''
port = server_sock.getsockname()[1]

'''der service wird wird nach außenhin sichtbar gemacht'''
bluetooth.advertise_service(server_sock, "Camera", service_id=uuid,
                            service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                            profiles=[bluetooth.SERIAL_PORT_PROFILE]
                            )

print("Waiting for connection on RFCOMM channel", port)
'''informationen des clients werden abgerufen und die verbindung wird bestätigt'''
client_sock, client_info = server_sock.accept()
print("Accepted connection from", client_info)

try:
    while True:
        '''die daten kommen hier als byte array an. für die spätere verwendung caste ich sie hier gleich auf str'''
        data = str(client_sock.recv(1024))
        if not data:
            break
        data = data.split("\\n", 2)
        for i in range(len(data)-1):
            '''hier wird jeder einzelne teil des strings an der stelle ": " geteilt. So steht im zweiten Teil nur noch die Zahl'''
            data[i]=int(data[i].split(": ")[1])
        '''Da der 4te teil des Datensatzes leer ist und nicht gebraucht wird wird er gelöscht.'''
        data.pop(2)
        try:
            cameraWorker = threading.Thread(target=execute, args=(data[0],data[1],))
            cameraWorker.start()
            print("Started Camera Worker.")
            while cameraWorker.isAlive():
                client_sock.send(bytes("1", 'utf-8'))
                time.sleep(1)
            cameraWorker.join()
            client_sock.send(bytes("0", 'utf-8'))
        except:
            print("Thread Problem")
        '''Der ganze obige prozess muss darauf angepasst werden, was der client sendet, die jetztige form ist nur vorläufig'''
        
except OSError:
    pass


print("Sever is terminating.")



'''Nachdem sich der client trennt wird die verbindung geschlossen.'''
client_sock.close()
'''Nachdem die sitzung mit dem client getrennt wurde wird der socket geschlossen. Dieser und obiger schritt ist nur vorläufig.'''
server_sock.close()
print("Server terminated.")