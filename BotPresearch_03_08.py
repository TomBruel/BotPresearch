import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import random
import time
import xlrd
import datetime


#60 recherches prennent environ 5min et 18s

##### VARIABLE GLOBAL #####
Registre_compte_FR=[]
Registre_compte_UA=[]
Registre_compte_UK=[]
Registre_compte_USA=[]
Registre_compte=[]
Registre_compte_world=[]

ua = UserAgent()

# hour.. = hour , minutes
hourFR  = datetime.datetime.now().hour + 2, datetime.datetime.now().minute
hourUK  = datetime.datetime.now().hour + 2 - 1, datetime.datetime.now().minute
hourUSA = datetime.datetime.now().hour + 2 +10, datetime.datetime.now().minute # +10 pour les test +2 pour caler l'heure du systeme linux a la notre
hourUA  = datetime.datetime.now().hour + 2 +10 + 1,datetime.datetime.now().minute

start_chrono=0

proxies_France =[]
proxies_UK     =[]
proxies_USA    =[]
proxies_UA     =[]

#### FONCTIONS #####

def Demarre_chrono():
  global start_chrono
  start_chrono=round(time.time())
  
def Lire_chrono():
  global start_chrono
  y=round(time.time())
  time_sec=y-start_chrono
  time_hour=int(time_sec/3600)
  time_sec=time_sec%3600
  time_min=int(time_sec/60)
  time_sec=time_sec%60
  print(str(time_hour).zfill(2)+':'+str(time_min).zfill(2)+':'+str(time_sec).zfill(2))

def Mise_a_jour_heure():
  #### MISE A JOUR DE L'HEURE ACTUELLE POUR CHAQUE PAYS
  # hour.. = hour , minutes
  hourFR  = datetime.datetime.now().hour + 2, datetime.datetime.now().minute
  hourUK  = datetime.datetime.now().hour + 2 - 1, datetime.datetime.now().minute
  hourUSA = datetime.datetime.now().hour + 2 + 10, datetime.datetime.now().minute
  hourUA  = datetime.datetime.now().hour + 2 + 10 + 1,datetime.datetime.now().minute
  return hourFR,hourUK,hourUSA,hourUA

def Affiche_heure():

  global hourFR,hourUA,hourUK,hourUSA
  print(' ')
  print("Hour FR  : " + str(hourFR))
  print("Hour UK  : " + str(hourUK))
  print("Hour USA : " + str(hourUSA))
  print("Hour UA  : " + str(hourUA))
  
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
   
def Trouve_les_proxy():#Registre_compte_FR,Registre_compte_UA,Registre_compte_UK):
  
  global Registre_compte,Registre_compte_FR,Registre_compte_UA,Registre_compte_UK,Registre_compte_USA
  global proxies_France,proxies_UA,proxies_UK,proxies_USA

  print("Trouve les proxy")
  cpt_proxy_FR=0
  cpt_proxy_GB=0
  cpt_proxy_US=0
  cpt_proxy_UA=0
  
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
                cpt_proxy_FR=cpt_proxy_FR+1
                proxies_France.append({
                        'ip':   row.find_all('td')[0].string,
                        'port': row.find_all('td')[1].string,
                        'country' : row.find_all('td')[2].string,
                        'https' : row.find_all('td')[3].string
                        })
            
            elif row.find_all('td')[2].string == 'GB':
                cpt_proxy_GB=cpt_proxy_GB+1
                proxies_UK.append({
                        'ip':   row.find_all('td')[0].string,
                        'port': row.find_all('td')[1].string,
                        'country' : row.find_all('td')[2].string,
                        'https' : row.find_all('td')[3].string
                        })
    
            elif row.find_all('td')[2].string == 'US':
                cpt_proxy_US=cpt_proxy_US+1
                proxies_USA.append({
                        'ip':   row.find_all('td')[0].string,
                        'port': row.find_all('td')[1].string,
                        'country' : row.find_all('td')[2].string,
                        'https' : row.find_all('td')[3].string
                        })

            elif row.find_all('td')[2].string == 'UA':
                cpt_proxy_UA=cpt_proxy_UA+1
                proxies_UA.append({
                        'ip':   row.find_all('td')[0].string,
                        'port': row.find_all('td')[1].string,
                        'country' : row.find_all('td')[2].string,
                        'https' : row.find_all('td')[3].string
                        })
    #print("len(Registre_compte_FR)="+str(len(Registre_compte_FR)))
    #print("cpt_proxy_FR="+str(cpt_proxy_FR))
    if((cpt_proxy_UA>=len(Registre_compte_UA))and(cpt_proxy_GB>=len(Registre_compte_UK))and(cpt_proxy_UA>=len(Registre_compte_UK))):#pas de compte USA
      break
   
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
########## ERREUR -2 INDEXERROR OUT OF RANGE #########
 
 try:
    email = compte[0]
    password = compte[1]
    headers1 = {'User-Agent': compte[3]}
    proxies = {
      'https' : compte[8]
    }
    
 except Exception:
    pass
    return
   
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
 print('Pays : ' + str(compte[2]))


 soup = BeautifulSoup(content, 'html.parser')
 token = soup.find("input", {
    "name": "_token"
 })["value"]

 payload = "_token={}&login_form=1&email={}&password={}".format(token, email, password)
 login = r.post("https://www.presearch.org/api/auth/login", data = payload, headers = headers2, proxies = proxies)

 words = random.choice(["facebook","fb","facebook","fb","facebook","fb","facebook","fb","facebook","fb","facebook","fb","facebook","fb","facebook","fb","facebook","fb","facebook","fb","facebook","fb","facebook","fb","facebook","fb","facebook","fb","facebook","fb","facebook","fb","facebook","fb","youtube","mail","mail","mail","mail","mail","mail","mail","mail","mail","mail","mail","mail","mail","mail","youtube","youtube","youtube","youtube","youtube","youtube","youtube","youtube","youtube","youtube","youtube","youtube","youtube","news","outlook","outlok","gmail","gmal","calendar","twitter","binance connect","binance","air drop","youporn","amazone","amazon","amzon","google","ebay","netflix","spotify","deezer","deezr","spotfy","crack office", "crack photoshop", "crack photoshop CS6","red dead redemption","blizzcom 2018","blizzcom","strike airplane","google maps","btc usd","bts/usd", "ripple","crypto","eth","weather","pornhub","pronhub","hotmail","calculator","instagram","messenger","xvideos","airbnb","translate","traductor","tradctor","traductor english spanish","traductor english","icloud", "streaming","stream","streaming Games of throne","games of throne","breaking bad","series","cinema release","wish","present","gift","discount code amazon","coinbase","coinex","coinmarket cap","coinmarket cal","coinmarkt","coingecko","learn guitar","ed sheeran","playlist jazz","playlist techno","playlist pop","jeyz z","Rihanna","Beyonce","rihanna","beyonce","beatles","playlist old school","pewdiepie","trump","obama","obama speech","speech trump","simpson","southpark","result world cup","world cup replay","buy shooes", "buy pants","buy jeans","buy jacket","buy shirt","nike","adidas","weather tomorrow","i9","samsung","apple","mouse","keyboard","headphone","horoscope","reddit","funny story","world wide news","BBC","CNN","EURONEWS","Brexit news","actuallity economic","economic news","crypto and economic","gaming forum","reddit finance", "GTA 6 news","PUBG Ptr","pubg new weapon","pubg new vehicule","pubg new map","fortnite new patch","fortnite new gun","fortnine new skins","get free Vbucks","Vbucks crack","GTA 5 New patch", "GTA 5 patch","connect","bose buy","beats by dre","justin sun","Ripple investment","Presearch cryptomarketcap","orange is the new black","oitnb","netflix free account","picky little blinder","picky litl binder","picky little blinder streaming","orange is the new black streaming","casa de papel","case de bapel","casa de papel streaming","remix online","soundcloud","no working day 2018","hollidays 2019","online comparator","compare price","priceminister","ikea buy online","help excel","help word","help photoshop","help powerpoint","guide excel","guide photoshop","guide word","guide powerpoint","guide office","crack office 2018 new version", "which crypto to mine","buy summer cloth online", "buy cloth online", "buy for summer","rent a car for summer", "rent car","spacex news","space x news","HSBC news","KPMG news","job in my location", "find a job","youtube to mp3","speed test","olymmpics","olympics","free game","mortgage calculator","youtube music","music","star wars","harry potter","deadpool","deadpool streaming","deadpol","deadpol streaming","youtube downloader","youtube downlaoder","nfl","dictionary","dictionry","dictionaty","sex","nba","fifa","christmas","mothers day","fathers day","yahoo","yahoomail","freeporn","ali express","aliexpress","ali expres","ali expre","sport","skype","restaurant","fast food","piratebay","pirate bay","office 365","office 3652","wikipedia","anti virus","trip advisor","how to make pancakes","ATM","what is the weather today","weapons","weapons store","weopon store"])

 print('word choice : ' + words)
 payload = "term={}&provider_id=98&_token={}".format(words, token)
 r.post("https://www.presearch.org/search", data = payload, headers = headers2)
 print("Term:{} Search done!".format(words))

 try :
      r = r.get("https://www.presearch.org",headers = headers1,proxies = proxies,timeout = 10)
 except Exception:
    pass
    return


######## ERROR -1 ATTRIBUTE ERROR ########
 try:
  soup = BeautifulSoup(r.content, 'html.parser')
  balance = soup.find("span", {
    "class": "number ajax balance"
  })

  print('Compte ' + str(email) + ' '  + ": Your Balance : {} PRE".format(balance.text))
  print(' ')
  
  f.write('\n\nCompte ' + str(email) + ' '  + ": Your Balance : {} PRE".format(balance.text))


 except Exception:
   print ('\n\n ########## COMPTE INTROUVABLE ########## \n\n')
   pass
   return

def Lecture_fichier(nom_du_fichier):

  global Registre_compte
  wb = xlrd.open_workbook(nom_du_fichier)
  for s in wb.sheets():
    Registre_compte=[]                                                  # Creation d'une liste de lignes
    for ligne in range(1,s.nrows):
      Registre_compte.append([])                                        # Creation d'une liste par ligne pour les colonnes : table[ligne][colonne]
      for col in range(s.ncols):
        Registre_compte[ligne-1].append(s.cell(ligne,col).value)
      Registre_compte[ligne-1].append(ua.random)                        # [3] Machine différente pour chaque email
      Registre_compte[ligne-1].append(random.randint(29,45))            # [4] nb de recherche à faire sur le compte (29,45)
      Registre_compte[ligne-1].append(0)                                # [5] nombre de recherche fait
      Registre_compte[ligne-1].append(random.randint(8,10))             # [6] Heure différente pour chaque email
      Registre_compte[ligne-1].append(random.randint(0,59))             # [7] Minute différente pour chaque email
  
def Affichage_comptes_utilises():

  global Registre_compte
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

def Tri_compte_par_pays():

  global Registre_compte,Registre_compte_FR,Registre_compte_UA,Registre_compte_UK,Registre_compte_USA
  #registre[0]:          email                     PW        pays                                                        machine                                           nombre de recherche           nb de recherche deja fait             heure du debut des recherches        minutes du début des recherches              adresse IP du proxy (est rajouté plus tard dans le code)
  #registre[0]:          [0][0]                  [0][1]     [0][2]                                                       [0][3]                                                  [0][4]                           [0][5]                                 [0][6]                               [0][7]                                            [0][8]                                          
  #registre[0]: ['thithilherlher@gmail.com', 'Regensburg07', 'UA', 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1500.55 Safari/537.36','34',                            '0'                                    '9',                                  '54']
  #enregistre dans Registre_compte_FR tous les comptes (une ligne de la base de donnée) qui appartient au pays FR
  Registre_compte_FR = Registre_par_pays('FR')
  #affiche le nombre de comptes de la bdd qui appartiennent au pays FR
  Affiche_nb_compte_pays('FR',Registre_compte_FR)
  #enregistre dans Registre_compte_UA tous les comptes (une ligne de la base de donnée) qui appartient au pays UA
  Registre_compte_UA = Registre_par_pays('UA')
  #affiche le nombre de comptes de la bdd qui appartiennent au pays UA
  Affiche_nb_compte_pays('UA',Registre_compte_UA)
  #enregistre dans Registre_compte_UK tous les comptes (une ligne de la base de donnée) qui appartient au pays UK
  Registre_compte_UK = Registre_par_pays('UK')
  #affiche le nombre de comptes de la bdd qui appartiennent au pays UK
  Affiche_nb_compte_pays('UK',Registre_compte_UK)
  #enregistre dans Registre_compte_USA tous les comptes (une ligne de la base de donnée) qui appartient au pays USA
  Registre_compte_USA = Registre_par_pays('USA')
  #affiche le nombre de comptes de la bdd qui appartiennent au pays USA
  Affiche_nb_compte_pays('USA',Registre_compte_USA)
  print(' ')
  
def Registre_par_pays(pays):
  #enregistre dans "registre" toutes les lignes (adresse mail, mdp, pays de la bdd) qui sont du pays "pays"
  global Registre_compte
  registre = []
  for i in range(0,len(Registre_compte)):
    if Registre_compte[i][2] == pays:
      registre.append(Registre_compte[i])

  return registre

def Affectation_email_proxy(proxy,registre_pays):
  print("Debut Affectation_email_proxy")
  # Si il n'y a pas assez de proxy alors on attribue plusieurs comptes a un proxy
  if len(proxy) < len(registre_pays) and len(proxy)>0:
    for i in range(0,len(registre_pays)) :
        if proxy[i%len(proxy)]['https'] == 'yes' :
            registre_pays[i].append('https://' + proxy[i%len(proxy)]['ip'] + ':' + proxy[i%len(proxy)]['port'])
        else :
            registre_pays[i].append('http://' + proxy[i%len(proxy)]['ip'] + ':' + proxy[i%len(proxy)]['port'])
        registre_pays[i].append(False) # ajoute un boolean a chaque comtpe qui temoigne si le compte a fait toutes les recher
            
  elif len(proxy) > len(registre_pays) and len(registre_pays)>0:
    for i in range(0,len(registre_pays)) :
        if proxy[i]['https'] == 'yes' :
            registre_pays[i].append('https://' + proxy[i]['ip'] + ':' + proxy[i]['port'])
        else :
            registre_pays[i].append('http://' + proxy[i]['ip'] + ':' + proxy[i]['port'])
        registre_pays[i].append(False)

  elif len(proxy) == len(registre_pays) and len(registre_pays)>0:
    for i in range(0,len(proxy)) :
        if proxy[i]['https'] == 'yes' :
            registre_pays[i].append('https://' + proxy[i]['ip'] + ':' + proxy[i]['port'])
        else :
            registre_pays[i].append('http://' + proxy[i]['ip'] + ':' + proxy[i]['port'])
        registre_pays[i].append(False)
        
  print("Fin Affectation_email_proxy")
  return registre_pays

def Lancer_recherche_UK():
  global Registre_compte_UK
  global hourUK
  print(' ')
  print('UK account : '+ str(len(Registre_compte_UK)))
  print(' ')
  FLAG_TOUS_LES_COMPTES_ONT_FAIT_TOUTES_LES_RECHERCHES_UK = False
  while(FLAG_TOUS_LES_COMPTES_ONT_FAIT_TOUTES_LES_RECHERCHES_UK == False):
    FLAG_TOUS_LES_COMPTES_ONT_FAIT_TOUTES_LES_RECHERCHES_UK=True
    for i in range(0,len(Registre_compte_UK)):
      if(hourUK>(Registre_compte_UK[i][6],Registre_compte_UK[i][7]) and Registre_compte_UK[i][5]<Registre_compte_UK[i][4]):
        print("compte " + str(i+1) +'/'+str(len(Registre_compte_UK)))
        print("recherche : "+str(Registre_compte_UK[i][5]+1)+'/'+str(Registre_compte_UK[i][4]))
        x=round(random.uniform(0,0.2),2)                                                # tir un nombre aleatoire en 0 et 0.2s pour faire une pause entre chaque requete de comtpe(round permet d'arrondir le nombre floatant)
        time.sleep(x)
        Envoyer_une_requete(Registre_compte_UK[i])
        Registre_compte_UK[i][5]=Registre_compte_UK[i][5]+1
        FLAG_TOUS_LES_COMPTES_ONT_FAIT_TOUTES_LES_RECHERCHES_UK=False
    time.sleep(random.randint(2,5))
    
def Lancer_recherche_FR():
  global Registre_compte_FR
  global hourFR
  print(' ')
  print('FR account : '+ str(len(Registre_compte_FR)))
  print(' ')
  FLAG_TOUS_LES_COMPTES_ONT_FAIT_TOUTES_LES_RECHERCHES_FR = False
  while(FLAG_TOUS_LES_COMPTES_ONT_FAIT_TOUTES_LES_RECHERCHES_FR == False):
    FLAG_TOUS_LES_COMPTES_ONT_FAIT_TOUTES_LES_RECHERCHES_FR=True
    for i in range(0,len(Registre_compte_FR)):
      if(hourFR>(Registre_compte_FR[i][6],Registre_compte_FR[i][7]) and Registre_compte_FR[i][5]<Registre_compte_FR[i][4]):
        print("compte " + str(i+1) +'/'+str(len(Registre_compte_FR)))
        print("recherche : "+str(Registre_compte_FR[i][5]+1)+'/'+str(Registre_compte_FR[i][4]))
        x=round(random.uniform(0,0.2),2)                                                # tir un nombre aleatoire en 0 et 0.2s pour faire une pause entre chaque requete de comtpe(round permet d'arrondir le nombre floatant)
        time.sleep(x)
        Envoyer_une_requete(Registre_compte_FR[i])
        Registre_compte_FR[i][5]=Registre_compte_FR[i][5]+1
        FLAG_TOUS_LES_COMPTES_ONT_FAIT_TOUTES_LES_RECHERCHES_FR=False
    time.sleep(random.randint(2,5))
    
def Lancer_recherche_UA():
  global Registre_compte_UA
  global hourUA
  print(' ')
  print('UA account : '+ str(len(Registre_compte_UA)))
  print(' ')
  FLAG_TOUS_LES_COMPTES_ONT_FAIT_TOUTES_LES_RECHERCHES_UA = False
  while(FLAG_TOUS_LES_COMPTES_ONT_FAIT_TOUTES_LES_RECHERCHES_UA == False):
    FLAG_TOUS_LES_COMPTES_ONT_FAIT_TOUTES_LES_RECHERCHES_UA=True
    for i in range(0,len(Registre_compte_UA)):
      if(hourUA>(Registre_compte_UA[i][6],Registre_compte_UA[i][7]) and Registre_compte_UA[i][5]<Registre_compte_UA[i][4]):
        print("compte " + str(i+1) +'/'+str(len(Registre_compte_UA)))
        print("recherche : "+str(Registre_compte_UA[i][5]+1)+'/'+str(Registre_compte_UA[i][4]))
        x=round(random.uniform(0,0.2),2)                                                # tir un nombre aleatoire en 0 et 0.2s pour faire une pause entre chaque requete de comtpe(round permet d'arrondir le nombre floatant)
        time.sleep(x)
        Envoyer_une_requete(Registre_compte_UA[i])
        Registre_compte_UA[i][5]=Registre_compte_UA[i][5]+1
        FLAG_TOUS_LES_COMPTES_ONT_FAIT_TOUTES_LES_RECHERCHES_UA=False
    time.sleep(random.randint(2,5))
    
def Lancer_recherche_USA():
  global Registre_compte_USA
  global hourUSA
  print(' ')
  print('USA account : '+ str(len(Registre_compte_USA)))
  print(' ')
  FLAG_TOUS_LES_COMPTES_ONT_FAIT_TOUTES_LES_RECHERCHES_USA = False
  while(FLAG_TOUS_LES_COMPTES_ONT_FAIT_TOUTES_LES_RECHERCHES_USA == False):
    FLAG_TOUS_LES_COMPTES_ONT_FAIT_TOUTES_LES_RECHERCHES_USA=True
    for i in range(0,len(Registre_compte_USA)):
      if(hourUSA>(Registre_compte_USA[i][6],Registre_compte_USA[i][7]) and Registre_compte_USA[i][5]<Registre_compte_USA[i][4]):
        print("compte " + str(i+1) +'/'+str(len(Registre_compte_USA)))
        print("recherche : "+str(Registre_compte_USA[i][5]+1)+'/'+str(Registre_compte_USA[i][4]))
        x=round(random.uniform(0,0.2),2)                                                # tir un nombre aleatoire en 0 et 0.2s pour faire une pause entre chaque requete de comtpe(round permet d'arrondir le nombre floatant)
        time.sleep(x)
        Envoyer_une_requete(Registre_compte_USA[i])
        Registre_compte_USA[i][5]=Registre_compte_USA[i][5]+1
        FLAG_TOUS_LES_COMPTES_ONT_FAIT_TOUTES_LES_RECHERCHES_USA=False
    time.sleep(random.randint(2,5))
    
def Lancer_recherche():
  global Registre_compte_world
  global hourUSA,hourFR,hourUK,hourUA
  dernier_compte=[]

  
  print(' ')
  print('All account : '+ str(len(Registre_compte_world)))
  print(' ')
  while(len(Registre_compte_world)>0):
    i=random.randint(0,len(Registre_compte_world)-1)
    if(dernier_compte==Registre_compte_world):
      time.sleep(random.randint(2,5))
    Lire_chrono()
    if(Registre_compte_world[i][2]=='UK'):
      if(hourUK>(Registre_compte_world[i][6],Registre_compte_world[i][7])):
        if(Registre_compte_world[i][5]<Registre_compte_world[i][4]):
          print("compte " + str(i+1) +'/'+str(len(Registre_compte_world)))
          print("recherche : "+str(Registre_compte_world[i][5]+1)+'/'+str(Registre_compte_world[i][4]))
          x=round(random.uniform(0,0.2),2)                                                # tir un nombre aleatoire en 0 et 0.2s pour faire une pause entre chaque requete de comtpe(round permet d'arrondir le nombre floatant)
          time.sleep(x)
          Envoyer_une_requete(Registre_compte_world[i])
          Registre_compte_world[i][5]=Registre_compte_world[i][5]+1
          dernier_compte=Registre_compte_world[i]
        
    elif(Registre_compte_world[i][2]=='FR'):
      if(hourFR>(Registre_compte_world[i][6],Registre_compte_world[i][7])):
        if(Registre_compte_world[i][5]<Registre_compte_world[i][4]):
          print("compte " + str(i+1) +'/'+str(len(Registre_compte_world)))
          print("recherche : "+str(Registre_compte_world[i][5]+1)+'/'+str(Registre_compte_world[i][4]))
          x=round(random.uniform(0,0.2),2)                                                # tir un nombre aleatoire en 0 et 0.2s pour faire une pause entre chaque requete de comtpe(round permet d'arrondir le nombre floatant)
          time.sleep(x)
          Envoyer_une_requete(Registre_compte_world[i])
          Registre_compte_world[i][5]=Registre_compte_world[i][5]+1
          dernier_compte=Registre_compte_world[i]
        
    elif(Registre_compte_world[i][2]=='UA'):
      if(hourUA>(Registre_compte_world[i][6],Registre_compte_world[i][7])):
        if(Registre_compte_world[i][5]<Registre_compte_world[i][4]):
          print("compte " + str(i+1) +'/'+str(len(Registre_compte_world)))
          print("recherche : "+str(Registre_compte_world[i][5]+1)+'/'+str(Registre_compte_world[i][4]))
          x=round(random.uniform(0,0.2),2)                                                # tir un nombre aleatoire en 0 et 0.2s pour faire une pause entre chaque requete de comtpe(round permet d'arrondir le nombre floatant)
          time.sleep(x)
          Envoyer_une_requete(Registre_compte_world[i])
          Registre_compte_world[i][5]=Registre_compte_world[i][5]+1
          dernier_compte=Registre_compte_world[i]
          
    elif(Registre_compte_world[i][2]=='USA'):
      if(hourUSA>(Registre_compte_world[i][6],Registre_compte_world[i][7])):
        if(Registre_compte_world[i][5]<Registre_compte_world[i][4]):
          print("compte " + str(i+1) +'/'+str(len(Registre_compte_world)))
          print("recherche : "+str(Registre_compte_world[i][5]+1)+'/'+str(Registre_compte_world[i][4]))
          x=round(random.uniform(0,0.2),2)                                                # tir un nombre aleatoire en 0 et 0.2s pour faire une pause entre chaque requete de comtpe(round permet d'arrondir le nombre floatant)
          time.sleep(x)
          Envoyer_une_requete(Registre_compte_world[i])
          Registre_compte_world[i][5]=Registre_compte_world[i][5]+1
          dernier_compte=Registre_compte_world[i]
          
    if(Registre_compte_world[i][5]==Registre_compte_world[i][4]):
      del(Registre_compte_world[i])
    
#### MAIN ####
  
def main() :

  global Registre_compte,Registre_compte_FR,Registre_compte_UA,Registre_compte_UK,Registre_compte_USA, Registre_compte_world
  global proxies_France,proxies_UA,proxies_UK,proxies_USA
  global hourFR,hourUA,hourUK,hourUSA
  
  ####################LANCE LE CHRONOMETRE###########################
  Mise_a_jour_heure()
  Affiche_heure()
  Demarre_chrono()
  
  ####################LECTURE DU FICHIER DE DONNEES###########################
  
  Lecture_fichier('databaseTomComplete.xlsx')

  ####################AFFICHAGE DES COMPTES UTILISES###########################   

  Affichage_comptes_utilises()
  
  ####################TRI DES COMPTES PAS PAYS###########################
  
  Tri_compte_par_pays()
  
  ####################CHERCHE ET AFFICHE DES PROXIES###########################
  
  Trouve_les_proxy()#Registre_compte_FR,Registre_compte_UA,Registre_compte_UK)
  Affiche_nb_proxy_trouves()

  #Verifie_disponibilite_proxy(myproxy = proxies_France)
  #Verifie_disponibilite_proxy(myproxy = proxies_UA)
  #Verifie_disponibilite_proxy(myproxy = proxies_UK)
  
  ####################AFFECTE A CHAQUE COMPTE UN PROXY ET AJOUTE UN BOOLEEN A CHAQUE COMPTE QUI TEMOIGNE SI LE COMPTE A FAIT TOUTES SES RECHERCHES ###########################
  
  Registre_compte_FR = Affectation_email_proxy(proxies_France,Registre_compte_FR)
  Registre_compte_UA = Affectation_email_proxy(proxies_UA,Registre_compte_UA)
  Registre_compte_UK = Affectation_email_proxy(proxies_UK,Registre_compte_UK)
  Registre_compte_USA = Affectation_email_proxy(proxies_USA,Registre_compte_USA)
  
  ####################AFFECTE TOUS LES REGISTRES DANS UN SEUL####################
  
  Registre_compte_world = Registre_compte_FR + Registre_compte_UA + Registre_compte_UK + Registre_compte_USA
  
  ####################VERIFIER L'HEURE AVANT DE FAIRE DES RECHERCHES SUR INTERNET###########################
  
  hourFR,hourUK,hourUSA,hourUA  = Mise_a_jour_heure()
  Affiche_heure()
  
  ####################DEBUT DES RECHERCHES SUR PRESEARCH########################### 

  Lancer_recherche()
  
  ####################UK ACCOUNT###########################
  
  #Lancer_recherche_UK()
  
  ####################FR ACCOUNT########################### 
  
  #Lancer_recherche_FR()
    
  ####################UA ACCOUNT########################### 

  #Lancer_recherche_UA()  
    
  ####################USA ACCOUNT########################### 

  #Lancer_recherche_USA()
      
#############################################################################################################


if __name__ == '__main__':

  f = open('log.txt','w')
  main()
  f.close()
