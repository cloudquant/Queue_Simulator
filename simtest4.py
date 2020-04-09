import time
import sys
import threading

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

#Genera un nombre definit de persones. En ser un generador, permet "cridar" a cada persona d'una en una
# per a simular l'arribada a una cua
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

# Cada periode entre 1 i x segons, entra un nou client a la fila d'espera
def fillCustomersLine(customersGenerator, line):
	while customersGenerator:
		try:
			line.append(next(customersGenerator))
			time.sleep(randint(1,5))
			print(str(len(line))+" customers waiting")
		except StopIteration:
			break

# Modelitza el procès d'atenció al client.
def customerAttention(mainThread,airLineCounter,customerLine):
	global flag
	
	while mainThread.isAlive() or len(customerLine)>0:
		if len(customerLine)>0 and flag==FREE:
			flag=BUSY
			p=customerLine.pop(0)
			flag=FREE
			print(p.name+" "+p.lastname+" being attended at counter: "+str(airLineCounter.getNumber()))
			time.sleep(randint(20,30))
		else:
			continue

def average_calculator():
	values=[]
	def calculator(new_value):
		values.append(new_value)
		total=sum(values)
		return total/len(values)
	return calculator



#Semàfor d'accès a la cua de clients, per a evitar col.lisions entre fils d'execució. LA cua pot estar disponible o 
# en funció de si està sent utilitzada per un altre fil per a extraure un client.
flag=FREE

#Crida al generador de persones. En sol.licita el numero desitjat per a la simulació
customers=peopleGenerator(50)

#Llista que contindrà els mostradors
airLineCounters=[]

#llista que conté els clients a la fila
customersLine=[]

filsexecucio=[]


#Creem els mostradors
for i in range(1,5):
	airLineCounters.append(Counter(i))


#Crea el fil d'execució que posa clients a la fila d'espera
peoplearriving=threading.Thread(target=fillCustomersLine, args=(customers,customersLine))

#Crea els fils d'execució per a fer funcionar els mostradors
#first=threading.Thread(target=customerAttention, args=(peoplearriving,airLineCounters[0],customersLine))
#second=threading.Thread(target=customerAttention, args=(peoplearriving,airLineCounters[1],customersLine))
for ctr in range(0,len(airLineCounters)):
	filsexecucio[ctr]=threading.Thread(target=customerAttention, args=(peoplearriving,airLineCounters[ctr], customersLine))
#Activa els fils
peoplearriving.start()
#first.start()
#second.start()
for i in range(len(filsexecucio)):
	filsexecucio[i].start()








