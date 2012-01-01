import logging
logging.basicConfig()
import stomp
from config import *
from comms import *
global conn


def start():
    conn = stomp.Connection([(host_ip, host_port)])
    conn.set_listener('', Listener())
    conn.start()
    conn.connect(wait=True)
    conn.subscribe(destination='/topic/log', ack='auto')
    conn.subscribe(destination='/topic/sense', ack='auto')
    while True:
        pass
    
class Listener(stomp.ConnectionListener):

    def on_connecting(self, host_and_port):
        print 'connection %s %s' % host_and_port
        

    def on_connected(self, headers, body):
        #Send message to laptop
        print 'connected'
        

    def on_disconnected(self):
        pass

    def on_message(self, headers, body):
        if str(headers['destination']) == '/topic/sense':
            print 'Processed sensor data:'
            message = message_controls.unserialize(body)
            if message.getFunctionName() == 'sensor_data':
                params = message.getParams()
                for x in params:
                    name = x[0]
                    data = ''
                    for y in x:
                        if y != name:
                            zn = 0
                            for z in y:
                                zn = zn+1
                                if z == False:
                                    #sensor is off
                                    data = 'off'
                                elif zn != len(y):
                                    data += str(z) + ', '
                                else:
                                    data += str(z)
                    print '\n \t' + str(name) + ' - \t' + str(data)
                                
                        
            else:
                print 'This is not sensor data \n \t' + message.getParams
        else:
            print body
        

    def on_receipt(self, headers, body):
        pass

    def on_error(self, headers, body):
        pass
        

    def on_send(self, headers, body):
        pass


if __name__ == '__main__':
    start()