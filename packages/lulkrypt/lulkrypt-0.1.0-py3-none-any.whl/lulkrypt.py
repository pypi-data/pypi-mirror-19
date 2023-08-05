import sys
import argparse
import datetime

parser = argparse.ArgumentParser(description="encrypts or decrypts a given ASCII string")
parser.add_argument("string",
					help = "string to be encrypted/decrypted")
parser.add_argument("-k","--key",
					dest = "key",
					type = int,
					help = "key used to decrypt the string")
parser.add_argument("-f", "--file",
					help = "file to write the result to",
					required = False,
					dest = "file",
					type = argparse.FileType('w')
					)


					
args = parser.parse_args()

if args.key and (args.key < 0 or args.key > 9999):
	parser.print_help()
	sys.exit(1)

def decrypt():
	ints = [ord(c) for c in args.string]
	for index, val in enumerate(ints):
		ints[index] = 33 + (val - 33 - args.key - index) % 94
	if args.file:
		for i in ints:
			args.file.write(chr(i))
	else:
		for i in ints:
			out = [chr(i) for i in ints]
		print(''.join(out))
	
def encrypt():
	now = datetime.datetime.now()
	day = now.day % 10
	hour = now.hour % 10
	minute = now.minute % 10
	second = now.second // 10
	key = second + minute * 10 + hour * 100 + day * 1000
	ints = [ord(c) for c in args.string]
	for index, int in enumerate(ints):
		ints[index] = 33 + (int - 33 + key + index) % 94
	if args.file:
		for i in ints:
			args.file.write(chr(i))
		args.file.write('\r\n{}'.format(now))
	else:
		for i in ints:
			out = [chr(i) for i in ints]
		print(''.join(out))
		print(now)
	
def main():
	if args.key:
		decrypt()
	else:
		encrypt()



if __name__ == "__main__":
	main()