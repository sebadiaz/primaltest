import csv,random,time
from datetime import datetime
from operator import itemgetter, attrgetter, methodcaller
import sklearn.preprocessing as preprocessing
import numpy as np
class Action:
        def __init__(self, idref, date, ouverture,haut,bas,fermeture,nbTitre):
                self.idref = idref
                self.date = date
                self.mktime = time.mktime(date.timetuple())
                self.sortKey = idref +"-" + str(self.mktime)
                self.ouverture = float(ouverture.replace(",", "."))
                self.haut = float(haut.replace(",", "."))
                self.bas = float(bas.replace(",", "."))
                self.fermeture=float(fermeture.replace(",", "."))
                self.nbTitre=nbTitre
        def __repr__(self):
                return repr((self.idref, self.date, self.ouverture,self.haut,self.bas,self.fermeture,self.nbTitre))

def getKey(custom):
      return custom.sortKey

student_tuples = []
with open('complete.csv', 'rb') as csvfile:
     spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')

     for row in spamreader:
         idref = row[0]
         datetime_object = datetime.strptime(row[1], '%d/%m/%y')
         ouverture=row[2]
         haut=row[3]
         bas=row[4]
         fermeture=row[5]
         nbTitre=row[6]
         student_tuples.append(Action(idref,datetime_object,ouverture,haut,bas,fermeture,nbTitre))
         if random.random() < 0.00001 :
                 print "."
         
print "sort alogo"
savedSorted=sorted(student_tuples, key=getKey)

with open('completeSorted.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=';',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in savedSorted:
            spamwriter.writerow([row.idref,row.date,row.mktime,row.ouverture,row.haut,row.bas,row.fermeture,row.nbTitre])


refidref=""
listValues=[]
nbValue=30
decay=1
ecart=10
ecart=5
with open('alignedSorted.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=';',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    head=["X{:02d}".format(x) for x in range(nbValue)]
    spamwriter.writerow(["id"]+head+["taux","score"])
    for row in savedSorted:
        if refidref=="":
                refidref=row.idref
        if refidref!=row.idref:
                arefer=nbValue+decay+ecart
                arefer=1
                for i in range(0,len(listValues)/nbValue,arefer):
                        if i+nbValue+decay+ecart<len(listValues):
                                norm =np.asarray(listValues[i:i+nbValue])
                                taux=(listValues[i+nbValue+decay+ecart]-listValues[i+nbValue+decay])/listValues[i+nbValue+decay]
                                score=0
                                
                                if taux > 0.05 :
                                        score =1
                                if taux > 0.1 :
                                        score =2                                        
                                spamwriter.writerow([refidref]+preprocessing.scale(norm).tolist() +[taux,score])                        
                refidref=row.idref               
        listValues.append(row.fermeture)
                
