import iperf3
server = iperf3.Server()

server.bind_address = '10.10.10.10'
server.port = 44000
server.verbose = True
while True:
    server.run()

# import subprocess
# import os

# ser = "iperf3 -s -p 5022 -i 1"
# process = subprocess.Popen(ser, encoding = 'utf-8',
#             stdout=subprocess.PIPE)

# while True:
#         output = process.stdout.readline()
#         print(output)