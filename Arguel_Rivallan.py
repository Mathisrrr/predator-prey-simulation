from tkiteasy import *
import random
import time
import matplotlib.pyplot as pyplt


#Taille du plateau
Taille=45
#Taille des cases:
Tcases=10
#Fréquence d'apparition des lapins
FNLAP=10
#Nombre de vie des lapins
DVLAP=8
#Age reproduction des lapins
ARLAP=2
#Fréquence d'apparition des renards
FREN=3
#Nombre de vie des renards
DVREN=14
#Nombre d'énergie des renards 
ENREN=5
#niveau d'énergie gagné lorsqu'un renard mange un lapin
MIAM=2
#indique la distance maximale à laquelle un renard peut sentir un lapin
FLAIR=5
#Age de reproduction des renards
ARREN=1
#niveau d'energie pour que un renard se reproduise
NEREN=4

#Tableau des cases voisines
pos=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

class foret():
    
    def __init__(self):
        #Nombre initial de lapin
        INITLAP=15
        #Nombre initial de renards
        INITREN=4
        
        self.poslapins=[]
        self.posrenards=[]
        
        #Initialisation des positions uniques des premiers lapins et renards
        for i in range (INITLAP+INITREN):
            
            #On vérifie que le plateau n'est pas plein
            if len(self.poslapins)+len(self.posrenards)<Taille**2:
                b,c=random.randint(0, Taille-1),random.randint(0, Taille-1)
                
                if i<INITLAP:
                    while (b,c) in self.poslapins:
                        b,c=random.randint(0, Taille-1),random.randint(0, Taille-1)   
                    self.poslapins.append((b,c))
                
                #Une fois toute les positions des lapins trouvées, on trouve les positions des renards
                else:    
                    
                    while (b,c) in self.poslapins or (b,c) in self.posrenards:
                        b,c=random.randint(0, Taille-1),random.randint(0, Taille-1)                   
                    self.posrenards.append((b,c))
        
        #self.poslapins=[(0,0)]
        #self.posrenards=[(29,29)]
        #Initialisation des listes associées aux lapins
        self.reprolapins=[0 for i in range(len(self.poslapins))]
        self.agelapins=[DVLAP for i in range (len(self.poslapins))]
        
        #Initialisation des listes associées aux renards
        self.agerenards=[DVREN for i in range (len(self.posrenards))]
        self.energierenards=[ENREN for i in range (len(self.posrenards))]
        self.reprorenards=[0 for i in range (len(self.posrenards))]
        
        #Création du plateau
        self.plateau=[[0 for i in range (Taille)] for i in range (Taille)]
      
        #On remplace les cases du tableau occupées par des lapins par des 1 et par des renards par des 2       
        for i in range (len(self.poslapins)):
            x1,x2=self.poslapins[i]
            self.plateau[x2][x1]=1
        
        for i in range(len(self.posrenards)):
           x1,x2=self.posrenards[i]           
           self.plateau[x2][x1]=2
  
    
    def AffichePlateau(self):                   #Affiche le plateau de jeu correctement mais non utilisé dans l'éxécution du programme
                                                #(permet de corriger les erreurs et mieux visualiser pendant l'écriture du code)       
        for ligne in range (Taille):
            print(self.plateau[ligne])
        print()
    
    def pos2gfx(self,a):                #Permet de passer des coordonnées du plateau aux coordonnées graphiques
        
        a=a*Tcases    
        return a
    
    def verif_taille(self,x1,x2,j,pos):                         #vérifie si les coordonées de la case voisine est dans le plateau
        if x2+pos[j][1]>=0 and x2+pos[j][1]<=Taille-1 and x1+pos[j][0] >= 0 and x1+pos[j][0] <=Taille-1:
            return True
        else:
            return False
            
    def initgraphique(self):        #Ouvre la fenêtre graphique et fais apparaitre les premiers éléments
        self.tdisque=(Tcases*8)/20
        n=self.pos2gfx(Taille)        
        self.gfx=ouvrirFenetre(n,(105/100)*n)
                                    
        #Création du tableau contenant les lapins graphiques et affichage des premiers lapins
        self.objetlapins=[]
        for i in range(len(self.poslapins)):
            self.objetlapins.append(self.gfx.dessinerDisque(self.pos2gfx(self.poslapins[i][0])+(Tcases/2),self.pos2gfx(self.poslapins[i][1])+(Tcases/2),self.tdisque,"green"))
        
        #Création du tableau contenant les renards graphiques et affichage des premiers renards    
        self.objetrenards=[]
        for i in range (len(self.posrenards)):
            self.objetrenards.append(self.gfx.dessinerDisque(self.pos2gfx(self.posrenards[i][0])+(Tcases/2),self.pos2gfx(self.posrenards[i][1])+(Tcases/2),self.tdisque,"red"))
    
    def age_lapin(self):    #Enlève de la vie au lapins   
        
        for i in range(len(self.agelapins)):        
            self.agelapins[i]-=1
        
    #Gère l'apparition des nouvaux lapins    
    def new_lapin(self):
        
        a=len(self.poslapins)
        for i in range (FNLAP):
            if len(self.poslapins)+len(self.posrenards)<Taille**2:                
                b,c=random.randint(0, Taille-1),random.randint(0, Taille-1)
                                
                while (b,c) in self.poslapins or (b,c) in self.posrenards:
                    b,c=random.randint(0, Taille-1),random.randint(0, Taille-1)                   

                self.poslapins.append((b,c))
         
        #Ajout des nouveaux lapins et de leurs informations                        
        for i in range (a,len(self.poslapins)):
            x1,x2=self.poslapins[i]
            self.plateau[x2][x1]=1
            self.objetlapins.append(self.gfx.dessinerDisque(self.pos2gfx(self.poslapins[i][0])+(Tcases/2),self.pos2gfx(self.poslapins[i][1])+(Tcases/2),self.tdisque,"green"))
            self.agelapins.append(DVLAP)
            self.reprolapins.append(1)
    
    #Suppression des lapins morts
    def actu_lapin(self):
        a=0
        #On supprime les éléments des lapins dont le nombre de vie est égal a 0
        while a<len(self.agelapins):
            if self.agelapins[a]==0:
                x1,x2=self.poslapins[a]                
                self.plateau[x2][x1]=0
                del self.reprolapins[a],self.agelapins[a],self.poslapins[a]
              
                #On supprime le lapin de l'interface graphique avant de le supprimé dans le tableau d'objet où il est stocké
                self.gfx.supprimer(self.objetlapins[a])
                del self.objetlapins[a]
                
            else:
                a+=1            #Si age du lapin>0, on continue de parcourir le tableau
               
    def deplacement_lapin(self):                #Déplace tout les lapins si possible
  
        for y in range(len(self.poslapins)):
                
            random.shuffle(pos)                 #On mélange la liste des déplacements pour avoir un déplacement aléatoire du lapin
            x1,x2=self.poslapins[y]
            
            #On parcourt le tableau des déplacements jusqu'à ce qu'on trouve une case libre
            for j in range(len(pos)):
                if self.verif_taille(x1,x2,j,pos) and self.plateau[x2+pos[j][1]][x1+pos[j][0]]== 0:
                    self.plateau[self.poslapins[y][1]][self.poslapins[y][0]]=0
                    self.plateau[x2+pos[j][1]][x1+pos[j][0]]=1
                    self.gfx.deplacer(self.objetlapins[y],self.pos2gfx(pos[j][0]),self.pos2gfx(pos[j][1]))
                    self.poslapins[y]=(x1+pos[j][0],x2+pos[j][1])
                    break
                              
    def capacite_reproduction_lapin(self):          #Attribue aux lapins leur capacité de reproduction
        
        for i in range (len(self.reprolapins)):
            self.reprolapins[i]=0     
            if self.agelapins[i] > (DVLAP-ARLAP):           #On vérifie si le lapin à l'âge de se reproduire
                self.reprolapins[i]=1
               
    def reproduction_lapin(self):               #fonction de reproduction des lapins
        
        for y in range(len(self.poslapins)):        
            
            if self.reprolapins[y]==0:          #On vérifie si le lapin à l'âge de se reproduire                
                x1,x2=self.poslapins[y]
            
                random.shuffle(pos)             #On mélange les déplacements
                
                for j in range (len(pos)):
                    
                    #On vérifie que la case voisine est un lapin
                    if self.verif_taille(x1,x2,j,pos) and self.plateau[x2+pos[j][1]][x1+pos[j][0]]== 1:
                        #On cherche l'indice du lapin séléctionné afin de connaitre ses informations
                        indice=self.poslapins.index((x1+pos[j][0],x2+pos[j][1]))
                        memoire=len(self.poslapins)                                 
                        
                        if self.reprolapins[indice]==0:     #On vérifie si le lapin sélectionné peut se reproduire
                            self.recherche_place_new_lapin(x1, x2, indice, y)       #On cherche une place autour du lapin 1
                            
                            #On regarde si un nouveau a été ajouté a la liste des positions
                            #Si pas de nouveau lapin, on cherche une place autour du lapin 2
                            if len(self.poslapins)==memoire:
                                self.recherche_place_new_lapin(x1+pos[j][0], x2+pos[j][1], indice, y)
                            else:
                                break
                       
    #x1,x2=Coordonées du premier lapin,y=index du premier lapin et indice =index du lapin 2        
    def recherche_place_new_lapin(self,x1,x2,indice,y):         #Recherche une place libre parmi les cases voisines des deux lapins

            for i in range (len(pos)):
            
                if self.verif_taille(x1,x2,i,pos) and self.plateau[x2+pos[i][1]][x1+pos[i][0]]== 0:     #On vérifie que la case voisine est vide
                    
                    #Ajout du nouveau lapin et de ses informations
                    self.poslapins.append((x1+pos[i][0],x2+pos[i][1]))   
                    self.objetlapins.append(self.gfx.dessinerDisque(self.pos2gfx(x1+pos[i][0])+(Tcases/2),self.pos2gfx(x2+pos[i][1])+(Tcases/2),self.tdisque,"green"))
                    self.plateau[x2+pos[i][1]][x1+pos[i][0]]=1
                    self.reprolapins.append(1)
                    self.agelapins.append(DVLAP)
                    #Une fois que les deux lapins se sont reproduit, ils ne peuvent plus se reproduire
                    self.reprolapins[y]=1
                    self.reprolapins[indice]=1
                    break
                                
    def age_renard(self):               #diminue l'âge des renards
        
        for i in range(len(self.agerenards)):
            self.agerenards[i]-=1
            
    def new_renard(self):           #fait apparaitre les nouveux renards
        
        a=len(self.posrenards)
        for i in range (FREN):
            
            if len(self.poslapins)+len(self.posrenards)<Taille**2:
                
                b,c=random.randint(0, Taille-1),random.randint(0, Taille-1)
                
                while (b,c) in self.poslapins or (b,c) in self.posrenards:
                    b,c=random.randint(0, Taille-1),random.randint(0, Taille-1)
                    
                self.posrenards.append((b,c))
                
        #Ajout des nouveaux renards et de leurs informations            
        for i in range (a,len(self.posrenards)):
            x1,x2=self.posrenards[i]
            self.plateau[x2][x1]=2
            self.objetrenards.append(self.gfx.dessinerDisque(self.pos2gfx(self.posrenards[i][0])+(Tcases/2),self.pos2gfx(self.posrenards[i][1])+(Tcases/2),self.tdisque,"red"))
            self.agerenards.append(DVREN)
            self.energierenards.append(ENREN)
            self.reprorenards.append(1)
 
    def chasse_renard(self):                #Algorithme de chasse des renards
        
        for y in range(len(self.posrenards)):
            
            x1,x2 =self.posrenards[y]
            random.shuffle(pos)
                         
         
            distance=0      #Distance correspond au voisinage qu'on regarde, 0 étant les cases voisines du renard 
          
            while distance < FLAIR:             #On cherche le lapin dans le périmètre du FLAIR du renard
                
                if distance==0:     #On cherche un lapin à manger sur les cases voisines du renards
                
                    for i in range(len(pos)):
                        if self.verif_taille(x1,x2,i,pos) and self.plateau[x2+pos[i][1]][x1+pos[i][0]]==1:   #On vérifie si un lapin est dans les cases voisines
                            indice=self.poslapins.index((x1+pos[i][0],x2+pos[i][1]))                     #On cherche l'indice du lapin
                            #On supprime toutes les informations sur le lapin mangé
                            del self.agelapins[indice],self.poslapins[indice],self.reprolapins[indice] 
                            #On supprime le lapin de l'interface graphique
                            self.gfx.supprimer(self.objetlapins[indice])
                            del self.objetlapins[indice]
                            #On met à jour le plateau et les informations du renard
                            self.plateau[x2+pos[i][1]][x1+pos[i][0]]=2
                            self.plateau[x2][x1]=0
                            self.gfx.deplacer(self.objetrenards[y], self.pos2gfx(pos[i][0]), self.pos2gfx(pos[i][1]))
                            self.posrenards[y]=((x1+pos[i][0],x2+pos[i][1]))
                            self.energierenards[y]+=MIAM
                            #On arrête de chercher car le renard à déjà mangé un lapin
                            distance=FLAIR
                            break
              
                    distance+=1         #On augmente le rayon du voisinage qu'on regarde
                   
                else:
                    pos2=[(0,-1),(-1,0),(0,1),(1,0)]        #On utilise ce tableau pour pouvoir tourner dans le sens trigonométrique 
                    memoire=(x1+distance+1,x2+distance+1) #On se place dans la diagonale du perimetre que l'on etudie
                    
                    #comme python commence en 0, on ajoute 1 à la distance  pour avoir la distance reelle 
                    z=0
                    
                    while z < 4:    #Cette boucle permet de faire les quatres déplacements pour realiser la spirale: 
                        for i in range((2*(distance+1))):      # Pour chaque action, cette boucle enleve n-fois le déplacement aux cordonnées précedentes 
        
                            #Si il y a un lapin, on cherche le meilleur deplacement pour le renard 
                            if self.verif_taille(memoire[0],memoire[1],z,pos2) and self.plateau[memoire[1]+pos2[z][1]][memoire[0]+pos2[z][0]]==1:
                                coorlapinx,coorlapiny=memoire[0]+pos2[z][0],memoire[1]+pos2[z][1]                                
                                coorrenardx,coorrenardy=x1,x2
                                #On utilise le théorème de Pythagore pour calculer la distance entre la case du renard et le lapin
                                longueur=((coorlapinx-x1)**2+(coorlapiny-x2)**2)**0.5 
                                dx,dy=0,0
                              
                                for i in range(len(pos)):
                                    #On calcul cette distance pour toutes les autres possibilités de déplacements
                                    #cette boucle teste toutes les possibilités de déplacements et garde a chaque fois les cordonnées dont la distance est la plus petite (distance entre le lapin et la futur place du renard)
                                    if self.verif_taille(x1,x2,i,pos) and longueur > ((coorlapinx-(x1+pos[i][0]))**2+(coorlapiny-(x2+pos[i][1]))**2)**0.5 and self.plateau[x2+pos[i][1]][x1+pos[i][0]]==0:
                                        
                                        longueur=((coorlapinx-(x1+pos[i][0]))**2+(coorlapiny-(x2+pos[i][1]))**2)**0.5                                         
                                        coorrenardx,coorrenardy=x1+pos[i][0],x2+pos[i][1]                       
                                        dx,dy=pos[i]
                                        
                                #On actualise les informations du renard après son déplacement
                                self.plateau[x2][x1]=0
                                self.plateau[coorrenardy][coorrenardx]=2
                                self.posrenards[y]=(coorrenardx,coorrenardy)
                                self.gfx.deplacer(self.objetrenards[y], self.pos2gfx(dx), self.pos2gfx(dy))
                                
                                #On arrête de chercher car le renard s'est déjà déplacé
                                distance=FLAIR
                                z=4
                                break
                         
                            else:                   
                                memoire=(memoire[0]+pos2[z][0],memoire[1]+pos2[z][1])
                                #on actualise les cordonnées 
                              
                         
                        z+=1 # on ajoute un pour changer de déplacement
                    
                    distance+=1    #On augmente la taille du rayon du voisinage
           
    def energie_renard(self):       #Enlève de l'énergie au renard
        
        for i in range(len(self.energierenards)):
            self.energierenards[i]-=1
            
    def actu_renard(self):                  #Supprime les renards qui n'ont plus de vie ou d'énergie
        a=0
        
        while a < len(self.agerenards):
           
           
            if self.agerenards[a]==0 or self.energierenards[a]==0:          #On supprime tout les renards dont la vie ou l'énergie est descendue à 0
                
                x1,x2=self.posrenards[a]
                #On supprime les informations du renard
                self.plateau[x2][x1]=0
                del self.reprorenards[a],self.agerenards[a],self.posrenards[a],self.energierenards[a]
                #On supprime le renard de l'interface graphique avant de le supprimé dans le tableau d'objet où il est stocké
                self.gfx.supprimer(self.objetrenards[a])
                del self.objetrenards[a]
                
            else:
                a+=1            #Si âge du renard>0, on continue de parcourir le tableau
                
    def capacite_reproduction_renard(self):         #Attribue à chaque renard leur possibilité de reproduction
        
        for i in range(len(self.reprorenards)):
            self.reprorenards[i]=0
            #On vérifie si le renard a l'âge et le niveau d'énergie nécessaire afin de se reproduire
            if self.agerenards[i] > (DVREN-ARREN) or self.energierenards[i] <= NEREN:
                self.reprorenards[i]=1
               
    def reproduction_renard(self):          #Reproduction des renards
        
        for y in range(len(self.posrenards)):
            
            if len(self.poslapins)+len(self.posrenards) < Taille**2:    #On verifie que le plateau n'est pas plein
     
                if self.reprorenards[y]==0:         #On vérifie que le renard puisse se reproduire
                    
                    x1,x2=self.posrenards[y]
                    random.shuffle(pos)
                    
                    for j in range (len(pos)):                     
                       
                        if self.verif_taille(x1,x2,j,pos) and self.plateau[x2+pos[j][1]][x1+pos[j][0]]==2:          #On regarde si un renard est présent dans une case voisine
                           
                            indice=self.posrenards.index((x1+pos[j][0],x2+pos[j][1]))           #On cherche l'indice du renard2
                            
                            if self.reprorenards[indice]==0:        #On regarde si le renard2 peut se reproduire
                                b,c=random.randint(0, Taille-1),random.randint(0, Taille-1)
                                
                                while (b,c) in self.posrenards or (b,c) in self.poslapins:          #On cherche une case libre sur le plateau pour placer le nouveau renard
                                    b,c=random.randint(0, Taille-1),random.randint(0, Taille-1)
                                                                
                                #On ajoute le renard et ses informations 
                                self.posrenards.append((b,c))
                                self.agerenards.append(DVREN)                                
                                self.energierenards.append(ENREN)
                                self.reprorenards.append(1)
                                self.plateau[c][b]=2
                                self.objetrenards.append(self.gfx.dessinerDisque(self.pos2gfx(b)+(Tcases/2),self.pos2gfx(c)+(Tcases/2),self.tdisque,"red"))
                                #On actualise les informations des renards qui viennent de se reproduire
                                self.reprorenards[y]=1
                                self.reprorenards[indice]=1
                                
                                break
                        
#Fonction pour faire tourner le jeux:
        
    def deplacement(self):
        self.deplacement_lapin()
        self.chasse_renard()
        
    def reproduction(self):
        self.capacite_reproduction_renard()
        self.capacite_reproduction_lapin()
        self.reproduction_renard()
        self.reproduction_lapin()
        
    def new_animals(self):
        self.new_renard()
        self.new_lapin()
        
        
    def actu_tour(self):
        
        self.age_lapin()
        self.age_renard()
        self.energie_renard()
        self.actu_lapin()
        self.actu_renard()
        
#Fonction de tour

    def tour(self):
        
        self.deplacement()
        self.reproduction()
        self.actu_tour()
        self.new_animals()
        self.gfx.actualiser()
        print(f"nombre de lapins:{len(self.poslapins)}, nombre de renards:{len(self.posrenards)}")
        
        self.eflap.append(len(self.poslapins))
        self.efren.append(len(self.posrenards))
        
    #Cette fonction permet plus de lisibilté    
    def jeu(self,a):
        self.eflap=[]
        self.efren=[]
        self.ly=[i for i in range (a)]
        
        self.initgraphique()
        self.gfx.actualiser()
        time.sleep(0.5)
        compteurlapins=len(self.poslapins)
        compteurrenards=len(self.posrenards)
        rabs=self.gfx.afficherTexte(f"Nombre de lapins: {compteurlapins}", self.pos2gfx(Taille)/5.5 ,self.pos2gfx(Taille) +self.pos2gfx(Taille)*(1/50),"green",int(self.pos2gfx(Taille)*(1/30)))
        foxs=self.gfx.afficherTexte(f"Nombres de renards: {compteurrenards}", self.pos2gfx(Taille)/1.78, self.pos2gfx(Taille) +self.pos2gfx(Taille)*(1/50), "red",int(self.pos2gfx(Taille)*(1/30)))
        n=[]
        for i in range(a):
            #time.sleep(0.03)
            compteurlapins=len(self.poslapins)
            compteurrenards=len(self.posrenards)
            self.gfx.changerTexte(rabs,f"Nombre de lapins: {compteurlapins}")
            self.gfx.changerTexte(foxs, f"Nombre de renards: {compteurrenards}")
            pourcentagelapins=len(self.poslapins)/(Taille**2)
            pourcentagerenards=len(self.posrenards)/(Taille**2)
            pourcentagevide=1-(pourcentagelapins+pourcentagerenards)
            
            self.gfx.dessinerRectangle(self.pos2gfx(Taille)/1.25,self.pos2gfx(Taille)+self.pos2gfx(Taille)*(1/75),pourcentagelapins*100 , self.pos2gfx(Taille)*(1/45), "green")
            self.gfx.dessinerRectangle(self.pos2gfx(Taille)/1.25+pourcentagelapins*100,self.pos2gfx(Taille)+self.pos2gfx(Taille)*(1/75),pourcentagerenards*100, self.pos2gfx(Taille)*(1/45), "red")
            self.gfx.dessinerRectangle(self.pos2gfx(Taille)/1.25+pourcentagelapins*100+pourcentagerenards*100,self.pos2gfx(Taille)+self.pos2gfx(Taille)*(1/75),pourcentagevide*100, self.pos2gfx(Taille)*(1/45), "white")
           
            self.tour()
        
        self.gfx.fermerFenetre()
        
        
        self.graph()
        
    def graph(self):
        pyplt.plot(self.ly,self.eflap)
        pyplt.plot(self.ly,self.efren)
        pyplt.show()
        

a=foret()
a.jeu(300)