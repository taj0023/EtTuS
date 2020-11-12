#!/usr/bin/env python3
import socket
import time
import concurrent.futures
import sys

if len(sys.argv) == 1:
	print(f'Usage: "python3 ettuip.py <IP>"\n(Use "-h" option for more info)')
	sys.exit()
if '-h' in sys.argv or '--help' in sys.argv:
	print('''
Example usage: python3 ettuip.py 192.168.123.123 -p 1-1000 

-h                     To show this message
-p(optional)           The range of ports to scan. (default: 1-65535)''')
	sys.exit()
min_range, max_range = 1, 65536

ip = sys.argv[1]
if '-p' in sys.argv:
	min_range, max_range = sys.argv[sys.argv.index('-p')+1].split('-')

def scanner(port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(0.05)
	try:
		s.connect((ip, port))
		print(f"Port \033[1;32m{str(port).ljust(4)}\033[0m     OPEN         {socket.getservbyport(port, 'tcp')}")
	except socket.timeout:
		s.close()

def main():
	print("──────────────────────────────────")
	print(f"\033[94mScanning {str(int(max_range)+1-int(min_range))} ports....\033[0m")
	print("──────────────────────────────────")
	print("\033[4mPORT\033[0m          \033[4mSTATE\033[0m        \033[4mSERVICE\033[0m")
	start = time.perf_counter()
	with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
		results = [executor.submit(scanner, i) for i in range(int(min_range), int(max_range)+1)]
		for f in concurrent.futures.as_completed(results):
			f.result()
	end = time.perf_counter()

	print("──────────────────────────────────")
	print(f"Took \033[94m{round(end-start, 2)}s\033[0m")

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		sys.exit()		