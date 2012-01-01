import stomp
import sys
from comms import *
from config import *
global conn


def start():
    run = True
    global conn
    conn = GumstixCLI(host_ip, host_port, '', '')
    try:
        while True:
            line = raw_input("\r> ")
            if not line or line.lstrip().rstrip() == '':
                continue
            line = line.lstrip().rstrip()
            if line.startswith('quit') or line.startswith('disconnect'):
                break
            split = line.split()
            command = split[0]
            if not command.startswith("on_") and hasattr(conn, command):
                getattr(conn, command)(split)
            else:
                print 'unrecognised command'
    finally:
        print "broke"

  
    
    
class GumstixCLI(stomp.ConnectionListener):
    def __init__(self, host='192.168.1.11', port=61613, user='', passcode=''):
        self.c = stomp.Connection([(host, port)], user, passcode)
        self.c.set_listener('', self)
        self.c.start()
        self.c.connect(wait=True)
        
    def __print_async(self, frame_type, headers, body):
        print "\r  \r>",
        print frame_type
        for header_key in headers.keys():
            print '%s: %s' % (header_key, headers[header_key])
        print
        print body
        print '> ',
        sys.stdout.flush()

    def on_connecting(self, host_and_port):
        print 'connection %s %s' % host_and_port
        

    def on_connected(self, headers, body):
        #Send message to laptop
        print 'connected'
        

    def on_disconnected(self):
        pass

    def on_message(self, headers, body):
        pass       
        

    def on_receipt(self, headers, body):
        pass

    def on_error(self, headers, body):
        print "Error: %s" %body
        pass
        

    def on_send(self, headers, body):
        print "Message Sent:"
        
    def send(self, message):
        '''
        Usage:
            send <message>
        
        parameters:
            message - message class
        
        Description:
            Used to send and pickle the message class 
            Called by other functions85 
        '''
        body = message.serialize()
        self.c.send(body, destination=queue_commands)

    
    def move(self, args):
        '''
        Usage:
            move [angle] [speed]
        
        Parameters:
            angle - Rover move angle from -50 to 50 degrees
            speed = Rover speed from -100 to 100 percent
        
        Description:
            Sends a move command to the Gumstix
        '''
        if len(args) > 2:
            self.angle = int(args[1])
            self.speed = int(args[2])
            if (self.angle > 100) or (self.angle < -100):
                print "Incorrect Angle, \r Expected: 50 <> -50"
            elif (self.speed > 100) or (self.speed < -100):
                print "Incorrect Speed, \r Expected: 100 <> -100"
            else:
                message = message_controls('move', [self.angle, self.speed])
                self.send(message)
        else:
            print "Expected: move <angle> <speed>"
        pass
    
    def sensor(self, args):
        '''
        NOT IN USE
        Usage:
            sensor <params>
        
        Parameters:
            param1 - Sensor No
            
        Description:
            Used to update sensors
        '''
        pass
    
    def help(self, args):
        '''
        Usage:
            help [command]
            
        Description:
            Returns information on chosen command
        '''
        if len(args) == 1:
            print 'Usage: help <command>, where command is one of the following:'
            print '    '
            for f in dir(self):
                if f.startswith('_') or f.startswith('on_') or f == 'c':
                    continue
                else:
                    print '%s ' % f,
            print ''
            return
        elif not hasattr(self, args[1]):
            print 'There is no command "%s"' % args[1]
            return

        func = getattr(self, args[1])
        if hasattr(func, '__doc__') and getattr(func, '__doc__') is not None:
            print func.__doc__
        else:
            print 'There is no help for command "%s"' % args[1]
        pass


if __name__ == '__main__':
    start()