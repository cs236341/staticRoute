from mininet.node import Switch
from mininet.log import lg, info, setLogLevel
from mininet.link import Intf

from time import sleep

class Router (Switch):
    "A Node with IP forwarding enabled."

    def config( self, **params ):
        super( Router, self).config( **params )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( Router, self ).terminate()


    def __init__( self, name, **params ):
        params['inNamespace'] = True
        super( Router, self ).__init__(name, **params)


    @staticmethod
    def setup():
        return

    def start(self, controllers):
        pass

    def stop(self):
        self.deleteIntfs()

    def log(self, s, col="magenta"):
        print T.colored(s, col)



    def initZebra( self , conffile ):
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )
        self.waitOutput()
        sleep(3)

        self.cmd("/usr/lib/quagga/zebra -f %s -d -i /tmp/zebra-%s.pid &> ./logs/zebra-%s.out " % (conffile, self.name, self.name))
        self.waitOutput()

    def initRipd( self , conffile ):
        self.cmd("/usr/lib/quagga/ripd -f %s -d -i /tmp/ripd-%s.pid &> ./logs/ripd-%s.out " % (conffile, self.name, self.name), shell=True)
        self.waitOutput()

    def initBgpd( self , conffile ):
        self.cmd("/usr/lib/quagga/bgpd -f %s -d -i /tmp/bgpd-%s.pid &> ./logs/bgpd-%s.out " % (conffile, self.name, self.name), shell=True)
        self.waitOutput()

#    def defaultIntf ( self ):
    
