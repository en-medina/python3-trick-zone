#!/usr/bin/python3.8

from threading import Lock
from random import randint, uniform
from time import sleep
import concurrent.futures

class SingletonByArg(type):
	_instances = {}
	lock = Lock()

	def __call__(cls, *args, **kwargs):
		if (cls, args, tuple(kwargs)) not in cls._instances:
			with cls.lock:
				if (cls, args, tuple(kwargs)) not in cls._instances:
					cls._instances[(cls, args, tuple(kwargs))] = super(SingletonByArg, cls).__call__(*args, **kwargs)
		return cls._instances[(cls, args, tuple(kwargs))]

class FileManager(metaclass=SingletonByArg):

	def __init__(self, filename):
		self.filename = filename
		self.lock = Lock()

		#Delete and create the file if does not exist
		open(filename,'w').close()

	def txt2str(self):
		with self.lock:
			with open(self.filename) as rawInfo:
				lines = rawInfo.readlines()
				return ''.join(lines)

	def str2txt(self, data, mode='a'):
		with self.lock:
			with open(self.filename, mode) as rawFile:
				rawFile.write(f'\n{data}')

def task_maker_thread(filename, name):
	myFile = FileManager(filename)
	for i in range(3):
		num = randint(1, 99)
		myFile.str2txt(f'Hi I am thread #{name:02d} and I generate the number {num:02d} in my {i:02d} iteration')
		sleep(uniform(0.1, 0.5))

if __name__ == '__main__':
	filenames = ['a.txt','b.txt']
	threadAmount = 10

	with concurrent.futures.ThreadPoolExecutor() as executor:
		futuresAnswers = {executor.submit(task_maker_thread, 
			filenames[i % len(filenames)], i) for i in range(threadAmount)} 

		concurrent.futures.wait(futuresAnswers)

	for filename in filenames:
		temporalFile = FileManager(filename)
		print(temporalFile.txt2str())
		print('\n' + '-' * 67)


