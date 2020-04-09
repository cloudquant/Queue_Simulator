import time
import sys

from random import shuffle
from random import choice
from random import randint
from datetime import datetime

from datasets import names_DB
from datasets import lastnames_DB

timer=time.clock if sys.platform[:3]=='win' else time.time

class Person:
	def __init__(self):
		shuffle(names_DB)
		shuffle(lastnames_DB)
		self.name=choice(names_DB)
		self.lastname=choice(lastnames_DB)
		self.age=randint(18,85)
	def startProcessTime(self):
		self.starttime=timer()
	def stopProcessTime(self):
		self.stoptime=timer()
	def elapsedTime(self):
		return self.stoptime-self.starttime
	def currentTime(self):
		self.res=''
		self.now=datetime.now()
		self.res+=str(self.now.hour)+":"+str(self.now.minute)+":"+str(self.now.second)
		return self.resprint(str(generatorSize(customers)))
	def talk(self):
		print("Hi! my name is:"+self.name+' '+self.lastname+" and I am "+str(self.age)+" years old")

def peopleGenerator(quantity):
	generated=0
	while generated<quantity:
		p=Person()
		yield(p)
		generated+=1


customerline=peopleGenerator(25)

for el in customerline:
	el.talk()
