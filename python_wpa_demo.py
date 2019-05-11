
from wpa_supplicant.core import WpaSupplicantDriver
from twisted.internet.selectreactor import SelectReactor
import threading
import time

# Start a simple Twisted SelectReactor
reactor = SelectReactor()
recThread = threading.Thread(target=reactor.run, kwargs={'installSignalHandlers': 0})
recThread.start()
time.sleep(0.1)  # let reactor start

# Start Driver
driver = WpaSupplicantDriver(reactor)

# Connect to the supplicant, which returns the "root" D-Bus object for wpa_supplicant
supplicant = driver.connect()

# Register an interface w/ the supplicant, this can raise an error if the supplicant
# already knows about this interface
interface = supplicant.create_interface('wlx001d43100027')

# Issue the scan
print("Issue the scan:")
scan_results = interface.scan(block=True)
for bss in scan_results:
    print bss.get_ssid()

    
desired_network = interface.add_network({'ssid': 'iHome', 'psk': 'beijingjiaotongdaxue'})
props = desired_network.get_properties()    
print(props)

interface.select_network(desired_network.get_path())

current_network = interface.get_current_network()
print(current_network)
state = current_network.get_enabled()
print(state)


while True:
    input = raw_input(">")
    if 'state' in input:
        print(supplicant.get_interfaces())    
    if input == 'exit':
        break
        
print("start clean")  

#remove network
result = interface.remove_network(desired_network.get_path())
print(result)
for if_path in supplicant.get_interfaces():
    rv = supplicant.remove_interface(if_path) 
    print rv
    
reactor.disconnectAll()
reactor.sigTerm()
recThread.join()
    
print("Done")