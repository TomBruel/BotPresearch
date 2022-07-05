import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import random
import time
import xlrd
import datetime


ua = UserAgent()

# hour.. = hour , minutes
hourFR  = datetime.datetime.now().hour, datetime.datetime.now().minute
hourUK  = datetime.datetime.now().hour - 1, datetime.datetime.now().minute
hourUSA = datetime.datetime.now().hour - 7, datetime.datetime.now().minute
hourUA  = datetime.datetime.now().hour + 1,datetime.datetime.now().minute

proxies_France =[]
proxies_UK     =[]
proxies_USA    =[]
proxies_UA     =[]


def Mise_a_jour_heure():
  #### MISE A JOUR DE L'HEURE ACTUELLE POUR CHAQUE PAYS
  hourFR  = datetime.datetime.now().hour, datetime.datetime.now().minute
  hourUK  = datetime.datetime.now().hour - 1, datetime.datetime.now().minute
  hourUSA = datetime.datetime.now().hour - 7, datetime.datetime.now().minute
  hourUA  = datetime.datetime.now().hour + 1,datetime.datetime.now().minute
  return hourFR,hourUK,hourUSA,hourUA

def Affiche_nb_compte_pays(pays,registre):
#affiche le nombre de compte de la bdd du pays "pays"
  print("Personnal account found for " + pays + " : " + str(len(registre)))

def Affiche_nb_proxy_trouves():
#affiche le nombre de proxy trouvés de chaque pays
  print("proxy FR  : " + str(len(proxies_France)))
  print("proxy UA  : " + str(len(proxies_UA)))
  print("proxy UK  : " + str(len(proxies_UK)))
  print("proxy USA : " + str(len(proxies_USA)))
  print(" ")

def Verifie_disponibilite_proxy(ip,port,https,country):

    if https == 'yes' :
        proxies_replace = {
                'https': 'https://' +ip + ':' + port
                }
    else:
        proxies_replace = {
                'https': 'http://' + ip + ':' + port
                }
        
    try:
      r = requests.get('https://www.google.com/' , timeout = 3 ,proxies = proxies_replace ) ## TIME OUT A 3
    except Exception:
        pass
        print('Proxy Mort   : '  + country)
        return 0
    
    print('Proxy Vivant : ' + country)
    return 1
   
def Trouve_les_proxy():
  headers = {'User-Agent': ua.random}
  r = requests.Session()
  proxies_doc = r.get('https://free-proxy-list.net',headers = headers ).content
  soup = BeautifulSoup(proxies_doc, 'html.parser')

  proxies_table = soup.find(id='proxylisttable')

  # Save proxies in the array
  for row in proxies_table.tbody.find_all('tr'):
    
    #if row.find_all('td')[3].string == 'no':
      #  print('NON')
      
    if   (row.find_all('td')[2].string == 'FR') or (row.find_all('td')[2].string =='GB') or (row.find_all('td')[2].string =='US') or (row.find_all('td')[2].string =='UA'):
        if Verifie_disponibilite_proxy(ip = row.find_all('td')[0].string, port = row.find_all('td')[1].string, https = row.find_all('td')[3].string,country = row.find_all('td')[2].string) == 1: 
            if row.find_all('td')[2].string == 'FR':
                proxies_France.append({
                        'ip':   row.find_all('td')[0].string,
                        'port': row.find_all('td')[1].string,
                        'country' : row.find_all('td')[2].string,
                        'https' : row.find_all('td')[3].string
                        })
            
            elif row.find_all('td')[2].string == 'GB':
                proxies_UK.append({
                        'ip':   row.find_all('td')[0].string,
                        'port': row.find_all('td')[1].string,
                        'country' : row.find_all('td')[2].string,
                        'https' : row.find_all('td')[3].string
                        })
    
            elif row.find_all('td')[2].string == 'US':
                proxies_USA.append({
                        'ip':   row.find_all('td')[0].string,
                        'port': row.find_all('td')[1].string,
                        'country' : row.find_all('td')[2].string,
                        'https' : row.find_all('td')[3].string
                        })

            elif row.find_all('td')[2].string == 'UA':
                proxies_UA.append({
                        'ip':   row.find_all('td')[0].string,
                        'port': row.find_all('td')[1].string,
                        'country' : row.find_all('td')[2].string,
                        'https' : row.find_all('td')[3].string
                        })
    
def Affiche_les_proxy_dispo():
#######PROXY FR########
  print('Proxy France : ')
  if(len(proxies_France) > 0):
    for n in range(0,len(proxies_France)):
      proxy = proxies_France[n]
      print('Proxy ' + proxy['ip'] + ':' + proxy['port'] + ' country :' + proxy['country'] + ' https :' + proxy['https'] )
  else :
    print('Pas de proxy pour la france')

#######PROXY UK########
  print('Proxy UK : ')
  if len(proxies_UK) > 0 :
    for n in range(0,len(proxies_UK)):
      proxy = proxies_UK[n]
      print('Proxy ' + proxy['ip'] + ':' + proxy['port'] + ' country :' + proxy['country'] + ' https :' + proxy['https'] )
  else :
    print('Pas de proxy pour GB')

  #######PROXY US########
  print('Proxy US : ')
  if len(proxies_USA) > 1 :
    for n in range(0,len(proxies_USA)):
      proxy = proxies_USA[n]
      print('Proxy ' + proxy['ip'] + ':' + proxy['port'] + ' country :' + proxy['country'] + ' https :' + proxy['https'] )
  else :
    print('Pas de proxy pour les US')

#######PROXY UKRAINE########
  print('Proxy Ukraine : ')
  if len(proxies_UA) > 1 :
    for n in range(0,len(proxies_UA)):
      proxy = proxies_UA[n]
      print('Proxy ' + proxy['ip'] + ':' + proxy['port'] + ' country :' + proxy['country'] + ' https :' + proxy['https'] )
  else :
    print('Pas de proxy pour Ukraine')

def Envoyer_une_requete(compte):

  email = compte[0]
  password = compte[1]
  headers1 = {'User-Agent': compte[3]}
  proxies = {
    'https' : compte[8]
  }

  headers2 = {
    'User-Agent': compte[3],
  'Content-Type': 'application/x-www-form-urlencoded'
  }

  r = requests.Session()

  try :
      content = r.get("https://www.presearch.org",headers = headers1,proxies = proxies, timeout = 10).content
  except Exception:
    pass
    return

  print('IP Used : ' + str(proxies))


  soup = BeautifulSoup(content, 'html.parser')
  token = soup.find("input", {
    "name": "_token"
  })["value"]

  payload = "_token={}&login_form=1&email={}&password={}".format(token, email, password)
  login = r.post("https://www.presearch.org/api/auth/login", data = payload, headers = headers2, proxies = proxies)


  words = random.choice(["apple", "life", "hacker", "facebook", "abeyancies", "abeyancy", "abeyant", "abfarad", "abfarads", "abhenries", "abhenry", "abhenrys", "abhominable", "abhor", "abhorred", "abhorrence", "abhorrences", "abhorrencies", "abhorrency", "abhorrent", "abhorrently", "abhorrer", "abhorrers", "abhorring", "abhorrings", "abhors", "abid", "abidance", "abidances", "abidden", "abide", "abided", "abider", "abiders", "abides", "abiding", "abidingly", "abidings", "abies", "abietic", "abigail", "abigails", "abilities", "ability", "abiogeneses", "abiogenesis", "abiogenetic", "abiogenetically", "abiogenic", "abiogenically", "abiogenist", "abiogenists", "abiological", "abioses", "abiosis", "abiotic", "abiotically", "abiotrophic", "abiotrophies", "abiotrophy"])
  print('word choice : ' + words)
  payload = "term={}&provider_id=98&_token={}".format(words, token)
  r.post("https://www.presearch.org/search", data = payload, headers = headers2)
  print("Term:{} Search done!".format(words))

  try :
      r = r.get("https://www.presearch.org",headers = headers1,proxies = proxies,timeout = 10)
  except Exception:
    pass
    return

  print('IP Used : ' + str(proxies))

  soup = BeautifulSoup(r.content, 'html.parser')
  balance = soup.find("span", {
    "class": "number ajax balance"
  })

  print('Compte ' + str(email) + ' '  + ": Your Balance : {} PRE".format(balance.text))
  print(' ')

def Recuperation_des_comptes_presearch() :

  ####################LECTURE DU FICHIER DE DONNEES###########################
  
  wb = xlrd.open_workbook('databaseTom.xlsx')
  for s in wb.sheets():
    Registre_compte =[]                                                 # Creation d'une liste de lignes
    for ligne in range(1,s.nrows):
      Registre_compte.append([])                                        # Creation d'une liste par ligne pour les colonnes : table[ligne][colonne]
      for col in range(s.ncols):
        Registre_compte[ligne-1].append(s.cell(ligne,col).value)
      Registre_compte[ligne-1].append(ua.random)                        # [3] Machine différente pour chaque email
      Registre_compte[ligne-1].append(random.randint(4,4))              # [4] nb de recherche à faire sur le compte (29,52)
      Registre_compte[ligne-1].append(0)                                # [5] nombre de recherche fait
      Registre_compte[ligne-1].append(random.randint(8,10))             # [6] Heure différente pour chaque email
      Registre_compte[ligne-1].append(random.randint(0,59))             # [7] Minute différente pour chaque email

  ####################AFFICHAGE DES COMPTES UTILISES###########################   
  
  print(' ')
  print(' ')
  print('######## Compte ########')
  for i in range(0,len(Registre_compte)):
    print('email : ' + Registre_compte[i][0] + '    ' + 'password : ' + Registre_compte[i][1] + '    ' + 'country : ' + Registre_compte[i][2] )
    print('Machine : ' + Registre_compte[i][3])
    print('Recherche à faire : ' +  str(Registre_compte[i][4]))
    print('Heure : ' + str(Registre_compte[i][6]) + '    ' + 'Minute : ' + str(Registre_compte[i][7]))
    print(' ')
  print('########################')
  print(' ')
  print(' ')
  
  ####################TRI DES COMPTES PAS PAYS###########################
  
  #registre[0]:          email                     PW        pays                                                        machine                                           nombre de recherche           nb de recherche deja fait             heure du debut des recherches        minutes du début des recherches              adresse IP du proxy (est rajouté plus tard dans le code)
  #registre[0]:          [0][0]                  [0][1]     [0][2]                                                       [0][3]                                                  [0][4]                           [0][5]                                 [0][6]                               [0][7]                                            [0][8]
  #registre[0]: ['thithilherlher@gmail.com', 'Regensburg07', 'UA', 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1500.55 Safari/537.36','34',                            '0'                                    '9',                                  '54']
  #enregistre dans Registre_compte_FR tous les comptes (une ligne de la base de donnée) qui appartient au pays FR
  Registre_compte_FR = Registre_par_pays('FR',Registre_compte)
  #affiche le nombre de comptes de la bdd qui appartiennent au pays FR
  Affiche_nb_compte_pays('FR',Registre_compte_FR)
  #enregistre dans Registre_compte_UA tous les comptes (une ligne de la base de donnée) qui appartient au pays UA
  Registre_compte_UA = Registre_par_pays('UA',Registre_compte)
  #affiche le nombre de comptes de la bdd qui appartiennent au pays UA
  Affiche_nb_compte_pays('UA',Registre_compte_UA)
  #enregistre dans Registre_compte_UK tous les comptes (une ligne de la base de donnée) qui appartient au pays UK
  Registre_compte_UK = Registre_par_pays('UK',Registre_compte)
  #affiche le nombre de comptes de la bdd qui appartiennent au pays UK
  Affiche_nb_compte_pays('UK',Registre_compte_UK)
  print(' ')
  
  ####################CHERCHE ET AFFICHE DES PROXIES###########################
  
  Trouve_les_proxy()
  Affiche_nb_proxy_trouves()

  #Verifie_disponibilite_proxy(myproxy = proxies_France)
  #Verifie_disponibilite_proxy(myproxy = proxies_UA)
  #Verifie_disponibilite_proxy(myproxy = proxies_UK)
  
  ####################AFFECTE A CHAQUE COMPTE UN PROXY###########################
  
  Registre_compte_FR = Affectation_email_proxy(proxies_France,Registre_compte_FR)
  Registre_compte_UA = Affectation_email_proxy(proxies_UA,Registre_compte_UA)
  Registre_compte_UK = Affectation_email_proxy(proxies_UK,Registre_compte_UK)

  print(len(Registre_compte_UK))

  ####################VERIFIER L'HEURE AVANT DE FAIRE DES RECHERCHES SUR INTERNET###########################
  
  hourFR,hourUK,hourUSA,hourUA  = Mise_a_jour_heure()
  print(' ')
  print("Hour FR  : " + str(hourFR))
  print("Hour UK  : " + str(hourUK))
  print("Hour USA : " + str(hourUSA))
  print("Hour UA  : " + str(hourUA))
  
  ####################DEBUT DES RECHERCHES SUR PRESEARCH########################### 

  ####################FR ACCOUNT########################### 
  
  print(' ')
  print('FR account : '+ str(len(Registre_compte_FR)))
  for i in range(0,len(Registre_compte_FR)):
    if(hourFR>(Registre_compte_FR[i][6],Registre_compte_FR[i][7])):                   #Compare si l'heure actuelle est supérieur à l'heure choisie pour le début des recherches (propre au compte)
      for x in range (0,Registre_compte_FR[i][4]):                                    #Fait x recherches 
        Envoyer_une_requete(compte = Registre_compte_FR[i])
      print("time sleep between each request")
      print(" ")
      time.sleep(random.randint(2,10))
        
  ####################UK ACCOUNT###########################
  
  print(' ')
  print('UK account : '+ str(len(Registre_compte_UK)))
  for i in range(0,len(Registre_compte_UK)):
    # print(' ')
    # print('Heure UK     : ' + str(hourUK))
    # print('Heure compte : ' + str(Registre_compte_UK[i][6]) + ':' + str(Registre_compte_UK[i][7]))
    # print(' ') 
    # print('email : ' + Registre_compte_UK[i][0] + '    ' + 'password : ' + Registre_compte_UK[i][1] + '    ' + 'country : ' + Registre_compte_UK[i][2] )
    # print('Machine : ' + Registre_compte_UK[i][3])
    # print('Recherche : ' +  str(Registre_compte_UK[i][4]))
    # print('Heure : ' + str(Registre_compte_UK[i][6]) + '    ' + 'Minute : ' + str(Registre_compte_UK[i][7]))
    # print(' ')
    if(hourUK>(Registre_compte_UK[i][6],Registre_compte_UK[i][7])):                   #Compare si l'heure actuelle est supérieur à l'heure choisie pour le début des recherches (propre au compte) 
      for x in range (0,Registre_compte_UK[i][4]):                                    #Fait x recherches
        print("number of research : " + str(x+1) + '/' + str(Registre_compte_UK[i][4]))
        Envoyer_une_requete(compte = Registre_compte_UK[i])
        print("time sleep between each request")
        print(" ")
        time.sleep(random.randint(2,10))

  ####################UA ACCOUNT########################### 
  
  FLAG_TOUS_LES_COMPTES_ONT_FAIT_TOUTES_LES_RECHERCHES = False
  while(FLAG_TOUS_LES_COMPTES_ONT_FAIT_TOUTES_LES_RECHERCHES == False):
    FLAG_TOUS_LES_COMPTES_ONT_FAIT_TOUTES_LES_RECHERCHES=True
    for i in range(0,len(Registre_compte_UA)):
      x=round(random.uniform(0,0.2),2)                                                # tir un nombre aleatoire en 0 et 0.2s pour faire une pause entre chaque requete de comtpe(round permet d'arrondir le nombre floatant)
      time.sleep(x)
      Envoyer_une_requete(Registre_compte_UA[i])
      registre_cpt_UA[i][5]=registre_cpt_UA[i][5]+1;
    if Registre_compte_UA[i][4]!=registre_cpt_UA[i][5]:
      FLAG_TOUS_LES_COMPTES_ONT_FAIT_TOUTES_LES_RECHERCHES=False
    time.sleep(random.randint(2,10))
    
      
    
  
  
  
  # print(' ')
  # print('UA account : '+ str(len(Registre_compte_UA)))
  # for i in range(0,len(Registre_compte_UA)):
    # if(hourUA>(Registre_compte_UA[i][6],Registre_compte_UA[i][7])):                  #Compare si l'heure actuelle est supérieur à l'heure choisie pour le début des recherches (propre au compte) 
      # #print("l'heure est bonne")
      # for x in range (0,Registre_compte_UA[i][4]):                                   #Fait x recherches 
        # #print("j'envoi une requete")
        # #print("Registre_compte_UA[" + str(i) + "] : " + str(Registre_compte_UA[i]))
        # Envoyer_une_requete(compte = Registre_compte_UA[i])
        # print("time sleep between each request")
        # print(" ")
        # time.sleep(random.randint(2,10))
      
def Registre_par_pays(pays,registre_general):
  #enregistre dans "registre" toutes les lignes (adresse mail, mdp, pays de la bdd) qui sont du pays "pays"
  registre = []
  for i in range(0,len(registre_general)):
    if registre_general[i][2] == pays:
      registre.append(registre_general[i])

  return registre

def Affectation_email_proxy(proxy,registre_pays):

  if len(proxy) < len(registre_pays) :
    for i in range(0,len(proxy)) :
        if proxy[i]['https'] == 'yes' :
            registre_pays[i].append('https://' + proxy[i]['ip'] + ':' + proxy[i]['port'])
        else :
            registre_pays[i].append('http://' + proxy[i]['ip'] + ':' + proxy[i]['port'])
            
  elif len(proxy) > len(registre_pays) :
    for i in range(0,len(registre_pays)) :
        if proxy[i]['https'] == 'yes' :
            registre_pays[i].append('https://' + proxy[i]['ip'] + ':' + proxy[i]['port'])
        else :
            registre_pays[i].append('http://' + proxy[i]['ip'] + ':' + proxy[i]['port'])

  elif len(proxy) == len(registre_pays) :
    for i in range(0,len(proxy)) :
        if proxy[i]['https'] == 'yes' :
            registre_pays[i].append('https://' + proxy[i]['ip'] + ':' + proxy[i]['port'])
        else :
            registre_pays[i].append('http://' + proxy[i]['ip'] + ':' + proxy[i]['port'])

  return registre_pays

############################################
    
# Main function
def main():
  
  Recuperation_des_comptes_presearch()
  #Trouve_les_proxy() # Trouve les proxy et ils sont classés dans des tableaux, un tableau = un pays
  #Affiche_les_proxy_dispo()
  #Verifie_disponibilite_proxy(myproxy = proxies_UA)
  #Verifie_disponibilite_proxy(myproxy = proxies_France)
  #Verifie_disponibilite_proxy(myproxy = proxies_UK)
  #Verifie_disponibilite_proxy(myproxy = proxies_USA)
  #Affiche_les_proxy_dispo()


  #if ( Verifie_disponibilite_proxy(myproxy = proxies_UA) == 1):
  #  proxy = proxies_UA[0]
  #  proxy_reformat = {
  #    'https': 'http://' + proxy['ip'] + ':' + proxy['port']
  #  }
    #Envoyer_une_requete(headers = , proxies = proxy_reformat, email = email_UA, password = password_compte)
  #else:
  #  print('Pas de proxy disponible pour le compte UA')
  # Retrieve latest proxies
  

###################################################
  










if __name__ == '__main__':
  main()
