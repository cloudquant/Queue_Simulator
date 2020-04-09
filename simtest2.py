import time
import sys

from random import shuffle
from random import choice
from random import randint
from datetime import datetime

from datasets import names_DB
from datasets import lastnames_DB
from datasets import FREE
from datasets import BUSY

timer=time.clock if sys.platform[:3]=='win' else time.time

#Modelitza una persona qualsevol amb Nom, Cognom i Edat
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
		return self.res
	def talk(self):
		print("Hi! my name is:"+self.name+' '+self.lastname+" and I am "+str(self.age)+" years old")


#Modelitza un mostrador d'atenció a les persones. Esta lliure per defecte, però permet modificar el seu estat a ocupat.
#Aplicable a qualsevol activitat.
class Counter:
	def __init__(self,counterNumber):
		self.status=FREE
		self.counterNumber=counterNumber
	def changeStatus(self):
		if self.status==FREE:
			self.status=BUSY
		elif self.status==BUSY:
			self.status=FREE
	def getStatus(self):
		return self.status
	def getNumber(self):
		return self.counterNumber

#Genera un nombre definit de persones. Es poden fer servir una a una.
def peopleGenerator(quantity):
	generated=0
	while generated<quantity:
		p=Person()
		yield(p)
		generated+=1


#Calcula el tamany actual del generador. Permet calcular quants elements queden
def generatorSize(generator):
	nbr=sum(1 for item in generator)
	return nbr


#Crida al generador de persones. En sol.licita 5
customers=peopleGenerator(10)
#Llista que contindrà els mostradors
airLineCounters=[]

#Creem 4 mostradors
for i in range(0,4):
	airLineCounters.append(Counter(i))

while customers:
	try:
		next(customers).talk()	
		#generatorSize(customers)	
		for counter in airLineCounters:
			if counter.getStatus()==FREE:
				counter.changeStatus()
				break
			else:
				print("El mostrador "+ str(counter.getNumber())+" esta ocupat")
		time.sleep(2)
		
	except StopIteration:
		break

for item in airLineCounters:
	print(item.getStatus())






