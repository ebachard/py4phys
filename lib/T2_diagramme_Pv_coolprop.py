# coding: latin1

# Sauf mention explicite du contraire par la suite, ce travail a �t� fait par 
# Jean-Julien Fleck, professeur de physique/IPT en PCSI1 au lyc�e Kl�ber. 
# Vous �tes libres de le r�utiliser et de le modifier selon vos besoins.
# 
# Si l'encodage vous pose probl�me, vous pouvez r�encoder le fichier � l'aide 
# de la commande
# 
# recode l1..utf8 monfichier.py
# 
# Il faudra alors modifier la premi�re ligne en # coding: utf8
# pour que Python s'y retrouve.



import numpy as np               # Les outils math�matiques
import CoolProp.CoolProp as CP   # Les outils thermodynamiques
import matplotlib.pyplot as plt  # Les outils graphiques

""" 
Fabrication d'un diagramme (P,v) avec CoolProp, ce qui n'est pas possible 
en natif car ils travaillent en masse volumique et non en volume massique par 
d�faut.
"""

def diagramme_Pv(fluide,dico={}):
    """ Dessine le diagramme Pv pour le fluide demand� avec des 
    choix par d�faut qui peuvent �tre "overridden" en sp�cifiant ceux � 
    changer dans le dictionnaire 'dico'. Les options disponibles sont:
    * 'vmin' et 'vmax' pour d�finir les limites des �chantillonnages en volume 
    massique. Par d�faut vtripleL et vtripleG * 10
    * 'Prange' pour l'intervalle de pression affich�
    * 'T': une liste des temp�ratures pour lesquelles il faut tracer 
    l'isotherme. (d�faut � None)
    * 'x': une liste des titres en vapeur pour lesquels il faut tracer la 
    courbe isotitre (d�faut � np.linspace(0,1,11))
    * 'titre': le titre (textuel, hein...) � donner au graphique.
    * 'fichier': le nom du fichier dans lequel enregistrer la figure.
    * 'logx': Bool�en indiquant si on veut un axe logarithmique en abscisse
    * 'logy': Bool�en indiquant si on veut un axe logarithmique en ordonn�e
    * 'legend': Bool�en indiquant si on veut rajouter les l�gendes
    * 'saturation': Bool�en indiquant si on veut rajouter la courbe de 
    saturation au trac� (d�faut � True)
    """
    Pcritique = CP.PropsSI(fluide,'pcrit')  # Pression
    Tcritique = CP.PropsSI(fluide,'Tcrit')  # et temp�rature critique
    Ptriple = CP.PropsSI(fluide,'ptriple')  # Pression 
    Ttriple = CP.PropsSI(fluide,'Ttriple')  # et temp�rature au point triple
    # On r�cup�re les volumes massiques via les 'densit�s' (ie masses 
    # volumiques) donn�es par CoolProp
    vtripleL = 1/CP.PropsSI('D','P',Ptriple,'Q',0,fluide)
    vtripleG = 1/CP.PropsSI('D','P',Ptriple,'Q',1,fluide)
    vcritique= 1/CP.PropsSI('D','P',Pcritique,'T',Tcritique,fluide)
    P_sat= np.linspace(Ptriple,Pcritique,1000)
    # L'ensemble des valeurs par d�faut.
    DEFAUTS = {'vmin':vtripleL, 'vmax':vtripleG*10, 
       'Prange': None, 
       'T': None, 'x': np.linspace(0,1,11),
       'titre': "Diagramme $(P,v)$ pour le fluide {}".format(fluide),
       'fichier': 'PNG/T2_diagramme_Pv_coolprop_{}.png'.format(fluide),
       'logx': True, 'logy': True, 'legend': False,
       'saturation': False}
    DEFAUTS.update(dico)      # Mise � jour des valeurs par d�faut via 'dico' 
    # L'�chantillonnage sera diff�rent
    if DEFAUTS['logx']:       # si l'axe est logarithmique
       v=np.logspace(np.log10(DEFAUTS['vmin']),np.log10(DEFAUTS['vmax']),1000)
    else:                     # ou simplement lin�aire
       v=np.linspace(DEFAUTS['vmin'],DEFAUTS['vmax'],1000)
    if DEFAUTS['T'] != None:
        for Ti in DEFAUTS['T']:   # Trac� des diff�rentes isothermes
            P = CP.PropsSI('P','T',Ti,'D',1/v,fluide)
            plt.plot(v,P,label='$T={}$'.format(Ti))
    if DEFAUTS['x'] != None:
        for xi in DEFAUTS['x']:   # Trac� des courbes isotitre
            vxi = 1/CP.PropsSI('D','P',P_sat,'Q',xi,fluide)
            plt.plot(vxi,P_sat,'k',label='$x={}$'.format(xi))
    if DEFAUTS['saturation']: # Trac� de la courbe de saturation
        v_eb   = 1/CP.PropsSI('D','P',P_sat,'Q',0,fluide)
        v_rosee= 1/CP.PropsSI('D','P',P_sat,'Q',1,fluide)
        plt.plot(v_eb,P_sat,'k',linewidth=4.0)
        plt.plot(v_rosee,P_sat,'k',linewidth=4.0)
    if DEFAUTS['Prange']: plt.ylim(DEFAUTS['Prange']) # Intervalle vertical
    plt.xlim((DEFAUTS['vmin'],DEFAUTS['vmax']))       # Intervalle horizontal
    if DEFAUTS['logx']: plt.xscale('log')             # Echelle log en x
    if DEFAUTS['logy']: plt.yscale('log')             # Echelle log en y
    if DEFAUTS['legend']: plt.legend()                # Rajout des l�gendes
    plt.xlabel('Volume massique $v$ en m$^3/$kg')     # L�gende en abscisse
    plt.ylabel('Pression en Pa')                      # L�gende en ordonn�e
    plt.title(DEFAUTS['titre'])                       # Titre
    plt.savefig(DEFAUTS['fichier'])                   # Enregistrement
    plt.clf()                                         # Nettoyage

# Le fluide � �tudier (� choisir parmi ceux donn�s par CP.FluidsList())
fluide = 'Water'

# Le diagramme "par d�faut"
diagramme_Pv(fluide)

# Les valeurs suivantes ont �t� choisies suite � l'observation du diagramme 
# par d�faut. Il faudra certainement changer les valeurs si vous modifiez le 
# fluide
dico = {'Prange':(1e7,3e7),
        'fichier':'PNG/T2_diagramme_Pv_coolprop_{}_lin.png'.format(fluide),
        'logx':False, 'logy': False,
        'vmin': 1e-3, 'vmax':1e-2}
diagramme_Pv(fluide,dico)


