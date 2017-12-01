#rejtveny
# Copyleft() M.O.
T=[]
# ebben lesz a rejtvény

for sor in open("rejtveny.txt"):
	R=sor.strip().split()
	for i in range(len(R)):
		if R[i]==".":R[i]="."
		else:
			if R[i].isnumeric():R[i]=int(R[i])
	T.append(R)



def Tki(T):
	sordb=oszlopdb=0
	print("--",end="")
	for i in range(len(T[0])):
		print(oszlopdb%10 , end=" ")
		oszlopdb+=1
	print()
	for sor in T:
		print(sordb%10,end=" ")
		for x in sor:
			print(x,end=" ")
		print()
		sordb+=1

# T körbevétele x-szel
for sor in T:
	sor.insert(0,"x")
	sor.append("x")
sorx=list("x"*len(T[0]))
T.insert(0,sorx)
T.append(sorx)

Tki(T)

TORNYOK=[]  # a világítótornyok helyének és értékének kimentése
for sor in range(len(T)):          
	for oszlop in range(len(T[0])):
		if type(T[sor][oszlop]) is int:
			TORNYOK.append([sor,oszlop,T[sor][oszlop]])
print(TORNYOK)



#  tiltott helyek megkeresése + érvénytelen helyek
def tilt(s,o):
	mentett=T[s][o]
	for i in range(s-1,s+2):
		for j in range(o-1,o+2):
			T[i][j]="x"
	T[s][o]=mentett

def soraban_oszlopaban(sor,oszlop): 
	# az adott hely sorában és oszlopában hány torony van, és ezeknek mennyi az összértéke
	db=0
	for o in range(len(T[0])):
		if type(T[sor][o]) is  int:
			db+=T[sor][o]
	for s in range(len(T)):
		if type(T[s][oszlop]) is  int:
			db+=T[s][oszlop]
	return db

def tiltasok():
	for sor in range(1,len(T)-1):
		for oszlop in range(1,len(T[0])-1):
			if type(T[sor][oszlop]) is int or T[sor][oszlop]=="H":
				tilt(sor,oszlop)
	# szélére "x"
	for sor in range(len(T)):
		T[sor][0]=T[sor][-1]="x"
	#aljára,tetejére "x"
	for oszlop in range(len(T[0])):
		T[0][oszlop]=T[-1][oszlop]="x"
	for sor in range(len(T)):           # azokra a helyekre "x" kerül, amelynek a sorában+oszlopában nincs torony
		for oszlop in range(len(T[0])):
			if soraban_oszlopaban(sor,oszlop)==0 and T[sor][oszlop]==".":
				T[sor][oszlop]="x"
	# A 0-ás tornyot tartalmazó sorok és oszlopok tiltása
	for sor in range(len(T)):           
		for oszlop in range(len(T[0])):
			if  T[sor][oszlop]==0:
				for o in range(len(T[0])):
					if T[sor][o]==".":
						T[sor][o]="x"
				for s in range(len(T)):
					if T[s][oszlop]==".":
						T[s][oszlop]="x"
			
			
def felszabadit(): # az x-ek helyére . kerül
	for sor in range(len(T)):
		for oszlop in range(len(T[0])):
			if T[sor][oszlop]=="x":
				T[sor][oszlop]="."

print("\n")
tiltasok()
Tki(T)


def letesz(s,o):
	if T[s][o]==".":
		T[s][o]="H"
		for sor in range(len(T)):
			if type(T[sor][o]) is int :
				T[sor][o]-=1
		for oszlop in range(len(T[0])):
			if type(T[s][oszlop]) is int :
				T[s][oszlop]-=1
	else:print(" *************  Ide nem lehet tenni!!! ----------->  ",s,o)



def felvesz(s,o):
	if T[s][o]=="H":
		T[s][o]="."
		for sor in range(len(T)):
			if type(T[sor][o]) is int :
				T[sor][o]+=1
		for oszlop in range(len(T[0])):
			if type(T[s][oszlop]) is int :
				T[s][oszlop]+=1
	else:print(" *************  Itt nem volt hajó!!! ------------->  ",s,o)


def Osszeg():
	db=0
	for sor in range(len(T)):          
		for oszlop in range(len(T[0])):
			if type(T[sor][oszlop]) is int:
				db+=T[sor][oszlop]
	return db

# Ötlet: Arra a helyre tegyük, amely a legtöbb toronyból látszik
def helykereses():
	HELYSORREND=[]
	for sor in range(len(T)):          
		for oszlop in range(len(T[0])):
			if T[sor][oszlop]==".":
				HELYSORREND.append([soraban_oszlopaban(sor,oszlop),sor,oszlop])
	HELYSORREND.sort()
	#print("TESZT:",HELYSORREND)
	return HELYSORREND[-1][1:]

def szabadhelyekszama():
	db=0
	for sor in range(len(T)):          
		for oszlop in range(len(T[0])):
			if T[sor][oszlop]==".":
				db+=1
	return db


LF="L"
while LF.upper()!="M" and Osszeg()>0 and szabadhelyekszama()>0:
	print("Összeg:",Osszeg())
	print("***  Javaslat:",helykereses())
	#LF=input("Letesz (L) vagy  Felvesz (F) vagy   Ment_és_kilép (M) :") 
	if LF.upper()=="M":
		g=open("rejtveny_M.txt","w")
		for sor in range(1,len(T)-1):
			for oszlop in range(1,len(T[0])-1):
				print(T[sor][oszlop],end=" ",file=g)
			print("",file=g)
		g.close() 
		print("az aktuális állást mentettem a 'rejtveny_M.txt' fájlba.")
	else:
		#hsor=int(input("sor="))
		#hoszlop=int(input("oszlop="))
		hsor,hoszlop=helykereses()
		if LF.upper()=="L":
			letesz(hsor,hoszlop)
			felszabadit()
			tiltasok()
		if LF.upper()=="F":
			felvesz(hsor,hoszlop)
			felszabadit()
			tiltasok()
	Tki(T)




# kilépés itt ----------------


print("Vééége")
if Osszeg()>0 and szabadhelyekszama()==0:
	print("\n ******************** ERRE NINCS MEGOLDÁSOM !!! ****************** \n")
for x in TORNYOK:          # A tornyok eredeti értékének visszaírása
	T[x[0]][x[1]]=x[2]
hajoszam=0                 # Egy kis statisztika a végére
toronyszam=0
toronyertek=0
for sor in range(1,len(T)-1):
	for oszlop in range(1,len(T[0])-1):
		if T[sor][oszlop]=="x":T[sor][oszlop]="."
		if T[sor][oszlop]=="H":hajoszam+=1
		if type(T[sor][oszlop]) is int:
			toronyszam+=1
			toronyertek+=T[sor][oszlop]
Tki(T)
print("\n * A hajók száma:",hajoszam,"\n * A tornyok száma:",toronyszam,"\n * A tornyok összértéke:",toronyertek)

