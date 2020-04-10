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

#Modelitza una persona qualsevol amb Nom, Cognom i Edat. Es pot adaptar a diferents necessitats ampliant amb 
# nous mètodes o eliminant mètodes existents.
class Person:
	def __init__(self):
		shuffle(names_DB)
		shuffle(lastnames_DB)
		self.name=choice(names_DB)
		self.lastname=choice(lastnames_DB)
		self.age=randint(18,85)
	def start_process_time(self):
		self.start_time=timer()
	def stop_process_time(self):
		self.stop_time=timer()
	def elapsed_time(self):
		return self.stop_time-self.start_time
	def current_time(self):
		self.res=''
		self.now=datetime.now()
		self.res+=str(self.now.hour)+":"+str(self.now.minute)+":"+str(self.now.second)
		return self.res
	def talk(self):
		print("Hi! my name is:"+self.name+' '+self.lastname+" and I am "+str(self.age)+" years old")


#Modelitza un mostrador d'atenció a les persones. Esta lliure per defecte, però permet modificar el seu estat a ocupat.
#Aplicable a qualsevol activitat.
class Counter:
	def __init__(self,counter_number):
		self.status=FREE
		self.counter_number=counter_number
	def change_status(self):
		if self.status==FREE:
			self.status=BUSY
		elif self.status==BUSY:
			self.status=FREE
	def get_status(self):
		return self.status
	def get_number(self):
		return self.counter_number

#Genera un nombre definit de persones. En ser un generador, permet "cridar" a cada persona d'una en una
# amb el mètode next() per a simular l'arribada a una cua d'un en un.
def people_generator(quantity):
	generated=0
	while generated<quantity:
		p=Person()
		yield(p)
		generated+=1

#Funcio per anar calculant la mitjana dels temps d'espera dels clients una vegada entren a la cua
# fins que surten. El que calcula, en aquest cas, és la mitjana dels valors retornats pel mètode
# elapsedTime() de la classe Person, que és la diferència entre el temps d'arribada (en aquest cas, a la fila)
# i el temps de sortida del procès, quan el client ja ha estat atès.
def average_calculator():
	values=[]
	def calculator(new_value):
		values.append(new_value)
		total=sum(values)
		return total/len(values)
	return calculator

#Calcula el tamany actual del generador. Permet calcular quants elements queden. No s'utilitza a aquest programa. Es deixa
# per a properes necessitats.
def generator_size(generator):
	nbr=sum(1 for item in generator)
	return nbr

# Cada periode entre x i y segons, entra un nou client a la fila d'espera
def fill_customers_line(customers_generator, line):
	# Mentre el generador de persones generi noves persones....
	while customers_generator:
		try:
			# "Crida" al segûent client/passatger/persona... etc.. nc= next customer
			nc=next(customers_generator)
			# l'incorpora a la fila d'espera
			line.append(nc)
			# comença el càlcul del temps que la persona romandrà a la fila
			nc.start_process_time()
			# L'atenció dura entre x i y segons
			time.sleep(randint(10,20))
			# informa del nombre de persones que encara esperen a la fila
			print(str(len(line))+" customers waiting")
		except StopIteration:
			break

# Modelitza el procès d'atenció al client.
def customer_attention(main_thread,simulation_counter,customer_line):
	global flag
	global total_mean_time
	global averager
	
	# Mentre el generador de persones es trobi en execució, o bé, si aquest ha acabat, però encara queden persones 
	# per a ser ateses a la fila d'espera...
	while main_thread.isAlive() or len(customer_line)>0:
		# Si hi ha persones a la llista d'espera i el semàfor d'accès dona via lliure...
		if len(customer_line)>0 and flag==FREE:
			# Semàfor en vermell per a que cap altre fil d'execució accedeixi a la fila d'espera
			flag=BUSY
			# extrau el client que es troba en primer lloc a la fila
			p=customer_line.pop(0)
			# Allibera la fila d'espera per a que d'altres fils tinguin accès
			flag=FREE
			# Informació de l'usuari que està sent atès i a quin mostrador
			print(p.name+" "+p.lastname+" being attended at counter: "+str(simulation_counter.get_number()))
			# el temps d'atenció dura entre x i y segons. Es simula parant l'execució del fil
			time.sleep(randint(15,30))
			# Quan acaba el temps d'atenció, el client surt. Es para el temps que ha estat dins del procès: espera+atenció
			p.stop_process_time()
			# s'envien les dades de temps al calculador de temps mitjàcl
			total_mean_time=averager(p.elapsed_time())
		else:
			continue

# Retorna False si tots els fils d'execució han acabat. En cas contrari, retorna True.
def threads_running(*args):
	result=False
	for thread in args:
		# Alguns arguments poden ser una fila, com per exemple filsexecució. En aquest cas
		# examina els elements de la fila (fils) individualment
		if isinstance(thread,list):
			for element in thread:
				if element.isAlive():
					result=True
		else:
			if thread.isAlive():
				result=True
	return result


#Semàfor d'accès a la cua de clients, per a evitar col.lisions entre fils d'execució. La cua pot estar disponible o 
# no,en funció de si està sent utilitzada per un altre fil per a extraure un client.
flag=FREE

#Total de la mitana dels temps d'atenció al conjunt de clients generats pel simulador
total_mean_time=0

#Variable que controla el calculador de valors mitjans
averager=average_calculator()

#Crida al generador de persones. En sol.licita el numero desitjat per a la simulació
customers=people_generator(5)

# llista que contindrà els mostradors
simulation_counters=[]

#llista que conté els clients a la fila
customers_line=[]

#Matriu per als fils d'execució en paralel
exec_threads=[]


#Creem els mostradors
for i in range(1,5):
	simulation_counters.append(Counter(i))


#Crea el fil d'execució que posa clients a la fila d'espera
people_arriving=threading.Thread(target=fill_customers_line, args=(customers,customers_line))

#Crea els fils d'execució per a fer funcionar els mostradors
for ctr in range(0,len(simulation_counters)):
	fil=threading.Thread(target=customer_attention, args=(people_arriving, simulation_counters[ctr], customers_line))
	exec_threads.append(fil)

#Activa els fils
def main():
	# Inicialització del generador de persones a la fila d'espera
	people_arriving.start()
	#Inicilització dels mostrador d'atenció a les persones
	for i in range(len(exec_threads)):
		exec_threads[i].start()
	#Bucle d'execució mentre hi hagi fils d'execució treballant.
	#Quan acaben, mostra el temps mitjà d'espera de les persones a les files +mostradors d'atenció
	while True:
		if threads_running(people_arriving,exec_threads):
			continue
		else:
			print("Temps mitja de permanencia: "+ str(total_mean_time))
			break
	



if __name__=='__main__':
    main()






