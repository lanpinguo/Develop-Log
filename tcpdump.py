import os
import signal
import subprocess

# The os.setsid() is passed in the argument preexec_fn so
# it's run after the fork() and before  exec() to run the shell.
cmd = cmd1 = ['tcpdump', '-i', 'eth1', '-n','-B', '4096','-s', '0', '-w', 'tcpdump.pcap'] 
pro = subprocess.Popen(cmd,shell=False, preexec_fn=os.setsid) 


while True:
    cmd = raw_input('cmd:')
    #print(cmd)
    if cmd == 'exit':
        break                        
                       
os.killpg(os.getpgid(pro.pid), signal.SIGTERM)  # Send the signal to all the process groups