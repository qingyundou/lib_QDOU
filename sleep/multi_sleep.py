import time
import os
import sys
import pdb
def sleep(path):
	print('hi, checking path:' + str(path))
	while True:
		time.sleep(60*2) # 2 minute --- check if the file is still there
# 		time.sleep(5); print('still there')
		if not os.path.isfile(path): break
	print('byebye')

def main():
	if len(sys.argv) != 2:
		print("Usage: python multi_sleep.py fname")
		return

	fname = sys.argv[1]
	path = "/home/dawna/tts/qd212/lib_QDOU/sleep/temp/{}".format(fname)
	sleep(path)

if __name__ == "__main__":
	main()
