from mininet.topo import Topo
class CustomTopo(Topo):
	def __init__(self, **opts):
		Topo.__init__(self, **opts)
		
		s1 = self.addSwitch('s1')
		s2 = self.addSwitch('s2')
		s3 = self.addSwitch('s3')
		s4 = self.addSwitch('s4')
		s5 = self.addSwitch('s5')
		
		h1 = self.addHost('h1')
		h2 = self.addHost('h2')
				
		linkopts = dict(delay='0ms', loss=0)
		linkopts_a = dict(delay='10ms', loss=0)
		linkopts_b = dict(delay='20ms', loss=0)
		linkopts_c = dict(delay='30ms', loss=0)
		linkopts_d = dict(delay='40ms', loss=0)
		linkopts_e = dict(delay='50ms', loss=0) 
		
		self.addLink(s1, h1, **linkopts)
		self.addLink(s5, h2, **linkopts)
		
		self.addLink(s1, s2, **linkopts_a)
		self.addLink(s1, s3, **linkopts_b)
		self.addLink(s2, s4, **linkopts_c)
		self.addLink(s4, s5, **linkopts_d)
		self.addLink(s3, s5, **linkopts_e)
		
topos = {'custom': (lambda: CustomTopo())}		


