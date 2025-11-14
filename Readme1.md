#  <ins>Implementare SNMP .Aplicație demonstrativă</ins>

## Proiect la disciplina Rețele de Calculatoare 
## Studenți : Aciocîrlănoaei Georgiana  & Dascălu  Ioana-Felicia - 1310 A 


   _Simple Network Management Protocol_ (SNMP, ro. : “Protocolul Simplu de Administrare a Rețelei “) este un protocol de administrare standardizat  Internet , conceput initial pentru gestionarea rețelelor TCP/IP .
  
  SNMP este un protocol implementat la nivel de aplicație ce folosește porturile _UDP 161(SNMP Manager- trimite request-uri către agent pe portul 161 – Get, GetNext, Set) și 162(SNMP Manager – pentru a primi traps sau inform messages de la agenți; agentul SNMP trimite Trap/Inform către manager pe portul 162)_ . Acesta este utilizat în cadrul monitorizării rețelelor , administrării echipamentelor de rețea ( routere, switch-uri, servere, imprimante etc.),  detectarea defecțiunilor de rețea , colectării informațiilor și configurarea dispozitivelor de la distanță.
      
  		Arhitectura SNMP
  
   Arhitectura SNMP se bazează pe un model Manager – Agent , împreună cu o bază de date numită MIB ( nu este o bază de date clasică ce stochează date, ci doar descrie ce variabile există, de tip au, cum se accesează și ce semnificații au ), și are la bază 3 elemente fundamentale:
  
**1.	SNMP MANAGER**

   Managerul SNMP , cunoscut și sub numele de NMS – Network Management Station ( Stație de Management a Rețelei ) , este o aplicație care generează cereri pentru informațiile din MIB , procesează răspunsurile primite și care rulează pe un PC sau Server. Un router care rulează programul de server SNMP este numit agent , în timp ce un sistem (host) care rulează programul client SNMP este numit manager.

**2.	SNMP AGENT**

  Agentul SNMP este un modul software de management ce rulează pe un dispozitiv administrat . Managerul accesează valorile stocate în baza de date, în timp ce agentul menține informațiile din acesta. De exemplu, pentu a verifica dacă un router este congestionat (are un trafic excesiv ) sau nu, maganerul poate examina variabilele relevante pe care routerul le stochează, cum ar fi numărul de pachete primite și transmise. 
  
  Un manager SNMP poate trimite cereri către un agent fie pentru a prelua informații din MIB-ul agentului (cerere SNMP Get), fie pentru a modifica informații din MIB (cerere SNMP Set). De asemenea, un agent SNMP poate trimite mesaje nesolicitate către managerul SNMP, numite SNMP traps.


  Fiecare stație de management sau agent dintr-o rețea administrată prin SNMP menține o bază de date locală cu informații relevante pentru administrarea rețelei, cunoscută sub numele de MIB. Caracteristicile administrabile ale resurselor, așa cum sunt definite într-un MIB compatibil cu SNMP, sunt numite obiecte administrate sau variabile de management .

  
**3. MIB (Management Information Base )** 

   MIB conține informații despre resursele care necesită administrate. Aceste informații sunt organizate ierarhic și constau din instanțele de obiecte, care sunt, în esență, variabile.  MIB-ul, sau colecția de date de sub management-ul managerului, este unică pentru fiecare agent. MIB este împărțită în opt categorii : System, Interface, Address Translation, IP, UDP,ICMP , TCP.
   
    
    STRUCTURA INFORMAȚIILOR DIN MIB 
	
  Structura informțiilor de management (SMI) este  un standard SNMP care  definește structura informațiilor din MIB si tipul de date premise. SMI identifică modul în care resursele din MIB sunt reprezentate și denumite. Specificația SNMP include un șablon, cunoscut sub numele de ASN1, care oferă modelul formal pentru definirea  obiectelor și a tabelelor de obiecte din MIB. Pentru a defini un MIB sunt folosite următoarele cuvinte cheie:
  
  
  _**	 Syntax**_ : definește o structură abstractă de date corespunzătoare tipului de obiecte;
 SMI restricționează construcțiile ASN1 în mod intenționat pentru a menține simplitatea ;
 
 _**	Access**_ : definește dacă valoarea obiectului poate fi doar citită,  dar nu modificată (read-only), sau dacă poate fi și modificată (read-write);
 
  _**	Description**_ : conține definiția tipului de obiect și oferă toate explicațiile semantice necesare pentru interpretare .  

    IDENTIFICATORII DE OBIECTE MIB (MIB Object Identifiers)
  Fiecare obiect din MIB are asociat un identificator de obiect – OID, pe care stația de management îl folosește pentru a solicita valoarea obiectului de la agent.  Un OID este o secvență de întregi care identifică în mod unic un obiect administrat, definind o cale către acel obiect printr-o structură ierarhică de tip arbore, numită arbore OID sau arbore de înregistrare. 
  
   În momentul în care un agent SNMP trebuie să acceseze un anumit obiect administrat, acesta parcurge arborele OID pentru a găsi obiectul. O viziune de ansamblu asupra acestui concept o putem observa în figura de mai jos :
![manager_agent](https://github.com/user-attachments/assets/a97064b1-b4a4-4360-9bb8-329a3607876d)



	MIB-ul este scris în notația ASN.1 ( Abstract Syntax Notation 1) 

   ASN.1 este o notație standard întreținută de ISO (Organizația Internațională pentru Standardizare) și utilizată în domenii variate, de la World Wide Web până la sisteme de control al aviației. Toată comunicația SNMP depinde de faptul că toate dispozitivele trebuie să înțeleagă mesajele SNMP, ceea ce ridică câteva probleme tehnice.

   Prima problemă apare deoarece diferitele limbaje de programare au seturi ușor diferite de tipuri de date (numere întregi, șiruri de caractere, octeți, caractere etc.).De exemplu, un manager SNMP care trimite un mesaj cu tipuri de date specifice Java poate să nu fie înțeles de un agent SNMP scris în C.
Soluția: SNMP folosește ASN.1 (Abstract Syntax Notation One) pentru a defini tipurile de date utilizate în mesajele SNMP. Deoarece ASN.1 este independent de orice limbaj de programare, agenții și managerii SNMP pot fi scriși în orice limbaj.	

   ASN.1 este un limbaj utilizat pentru a descrie structura logică a mesajelor SNMP și tipurile de date suportate. Aceasta nu este o metoda de codificare specifică, ci este tradusă sub forma unei scheme care definește : tipurile de date utilizate, structura PDU-urilor ( Get, Set, Trap ), forma perechilor OID+valoare. 
   
   SNMP este definit, la nivelul ASN1-ului, ca fiind o structură de tip SEQUENCE ce conține următoarele câmpuri : enterprise (OID-ul stabilit de persoana ce creează aplicația, agent-addr ( adresa IP a agentului ), generic-trap (codul standard al evenimentului), specific-trap( identificator pentru alertele definite de utilizator ), time-stamp, variable-bindings (lista cu OID-urile și valorile trasnmise).
   
   După cum am precizat, pentru  a construi un mesaj SNMP, programatorul sau cel ce construiește aplicația trebuie să înțeleagă tipurile de date ASN.1, care se împart în două categorii:
   
1.	Tipuri primitive:
	o	Integer (număr întreg)
	
	o	Octet String (șir de octeți/caractere)
	
	o	Null
	
	o	Boolean

	o	Object Identifier (OID) – central pentru SNMP, deoarece OID identifică parametrul adresat în agent.
	
	
	2.Tipuri complexe:
	   
	  ASN.1 permite gruparea tipurilor primitive în tipuri complexe, pentru organizarea datelor.
	   
	   Exemple:
	   
	   o Sequence: o listă de câmpuri, fiecare cu tip diferit.
		
	   o PDU (Protocol Data Unit): tipuri complexe specifice SNMP, care conțin corpul mesajului SNMP. Exemple: GetRequest și SetRequest, pentru citirea și scrierea parametrilor.

	
	  BER ( Basic Encoding Rules) reprezintă metoda de transformare a structurilor definite in ASN1 în format binar pentru a putea fi transmise mai departe prin rețea. Rolurile BER-ului la nivelul SNMP-ului :  asigură o codificare standard pentru toate tipurile ASN1, permit interpretarea în mod corect a mesajelor, atât de către agent, cât și de manager, mențin compatibilitatea între diferite echipamente. În contextul proiectului dezvoltat, trebuie să avem în vedere faptul că SNMP utilizează BER pentru reprezentarea internă a mesajelor.

	
	_Relație ASN1 – BER- MIB_

1.	MIB-ul : definește ce resurse pot fi monitorizate (prin OID);
	
2.	ASN1 : definește structura mesajelor și tipurile de date ;

3.	BER : definește cum sunt reprezentate în mod binar aceste structuri.
   

       Scopul principal al unui mesaj SNMP este de a controla (set) sau de a monitoriza (get) parametrii unui agent SNMP. În SNMP, un parametru reprezintă o instanță a unui obiect definit într-un mod general în cadrul MIB-ului (Management Information Base). Un obiect SNMP poate avea una sau mai multe instanțe, în funcție de structura și tipul resursei monitorizate. Managerul SNMP poate obține sau modifica valoarea fiecărei instanțe gestionate de agent.

	
	   În cadrul unui agent SNMP, obiectele și parametrii monitorizați sunt organizați sub forma unui arbore ierarhic. Pentru identificarea exactă a fiecărui element din acest arbore, SNMP folosește Object Identifier-uri (OID-uri).



		OBJECT IDENTIFIER  (OID)
	   Un Object Identifier (OID) este o secvență numerică ce indică în mod unic poziția unui obiect sau a unei instanțe din arborele MIB. Structura sa este ierarhică, iar fiecare nivel al secvenței reprezintă o ramură în arbore.

	
	_Structura ierarhică a OID-urilor_

	Arborele OID este organizat pe nivele ierarhice, pornind de la rădăcina globală. În mod uzual, ramura utilizată de SNMP pentru obiectele de management este:1.3.6.1 care corespunde lanțului: iso → org → dod → internet.


Sub această ramură se găsesc:


   •.2.1 – OID-uri standard (MIB-II);
	
   •.4.1 – OID-uri pentru companii și implementări specific.


Prin această ierarhie, este asigurată:
•	unicitatea globală a fiecărui parametru monitorizat;

•	compatibilitatea între sisteme diferite;

•	extensibilitatea pentru implementări personalizate.



		OID – urile absolute 
		
	Specifică o cale către un atribut începândde la rădăcina arborelui OID;

	Numele OID absolute încep întotdeauna cu un punct (.) și trebuie să specifice fiecare nod al arborelui, de la nodul de sus până la obiectul administrat, de exemplu, : .1.3.6.1.2.1.1.1;


		OID – urile relative 
		
	Specifică o cale către atribut relativ la un anumit nod din arbore; 

	De exemplu, 2.1.1.1 specifică obiectul sysDescr din grupul system, relativ la nodul Internet din arborele OID;


		Specificarea OID – urilor 
		
   Pe lângă notația “punct-punct” ( o serie de numere separate prin puncte pentru a descrie OID-urile), putem utiliza simboluri textuale în locul numerelor pentru a reprezenta nodurile din calea către obiect sau utilizând o combinație între cele două. 

   
   Un OID simbolic folosește cuvinte mnemonice pentru a specifica obiectul administrat; de exemplu : mgmt.mib-2.system.sysContact  2.1.1.7 (echivalentul numeric – OID relativ), demonstrând ca un OID  poate combina atât reprezentări simbolice, cât și numerice ale nodurilor individuale din arbore .



	Rolul OID-urilor în SNMP

   În orice operație SNMP (GetRequest, GetNextRequest, SetRequest sau Trap), OID-ul identifică obiectul vizat de manager. În loc să transmită un nume textual, managerul folosește OID-ul numeric, garantând interpretarea corectă de către agent. 

   
   De exemplu, pentru a solicita o anumită informație sistemică de la agent, manager-ul transmite un OID specific, iar agentul returnează valoarea asociată obiectului respectiv. Astfel, OID-ul reprezintă elementul fundamental prin care SNMP asigură o adresare standardizată și precisă a obiectelor monitorizate sau controlate într-un sistem gestionat la distanță.

   

			Mod de funcționare al SNMP 
			
   Agenții software SNMP de pe dispozitivele și serviciile de rețea comunică cu un NMS ( Network Management System) pentru a trasnmite informații despre starea sistemului și modificările de configurare ). NMS-ul oferă o interfață unică prin care administratorii pot trimite comenzi și primi alerte automate. 

   
   SNMP se bazează pe conceptul de MIB ( Management Information Base ) pentru a determina modul în care sunt transmise și schimbate informațiile despre metricele dispozitivelor . MIB-ul reprezintă o descriere formală a componentelor unui dispozitiv de rețea și a informațiilor sale de stare . MIB-urile pot fi create pentru orice dispozitiv din rețeaua Internet of Things ( IoT), inclusiv pentru camere  video IP, vehicule, echipamente industrial sau medicale .

   
   SNMP utilizează o combinație de comunicații de tip pull și push între dispozitivele de rețea și NMS . Agentul SNMP, care se află împreună cu MIB-ul pe un dispozitiv de rețea, colectează în mod continuu informații despre stare . Totuși, el transmite informații către NMS doar la cerere sau atunci când un anumit parametru al rețelei depășește un prag predefinit, cunoscut sun numele de trap. Mesajele trap sunt, de obicei, trimise către serverul de administrare atunci cand apare un eveniment semnificativ, cum ar fi o eroare critică .

   
   SNMP include și un tip de mesaj numit inform , care permite unui instrument de monitorizare a rețelei să confirme primirea unui mesaj de la un dispozitiv. Mesajele inform  îi permit agentului să reseteze o alertă declanșată .

   
   Instrumentele de administrare a rețelei pot folosi un mesaj de tip set pentru a modifica un dispozitiv de rețea prin intermediul agentului SNMP. Aceste mesaje predefinite permit, de asemenea, administratorului să schimbe configurațiile dispozitivelor ca răspuns la evenimente noi din rețea.

   
   În majoritatea cazurilor, SNMP funcționează într-un model sincron: managerul SNMP inițiază comunicarea, iar agentul răspunde. De obicei, SNMP folosește User Datagram Protocol (UDP) ca protocol de transport. Porturile UDP bine cunoscute pentru traficul SNMP sunt 161 (SNMP) și 162 (SNMPTRAP). Aceste două porturi sunt valori implicite standard, identice în toate versiunile SNMP.

   
   SNMP este denumit „simplu” datorită naturii sale necomplicate. El poate executa comenzi de citire/scriere, cum ar fi resetarea unei parole sau modificarea unei setări de configurare, și poate raporta cantitatea de lățime de bandă, putere de procesare și memorie utilizată.Fiind unul dintre cele mai utilizate protocoale, SNMP este compatibil cu o gamă largă de echipamente hardware — de la echipamente tradiționale de rețea (routere, switch-uri, puncte de acces wireless) până la dispozitive finale, cum ar fi imprimante, scanere și dispozitive IoT.
   

		Versiunile SNMP 
		
  _ 1.SNMPv1 (cea pe care o vom dezvolta în cadrul proiectului propus)_
   
->Această versiunile se concentrează pe ușurința utilizării și pe o configurație simplă;

->Totuși, în comparație cu versiunile ulterioare, a avut capacități și mecanisme de securitate limitate;

->Schimbul de date între dispozitivele conectate și sistemul central de management era autentificat doar cu o parolă necriptată, cunoscută sub numele de community string, iar orice persoană cu acces la rețea o putea vedea ;


   _2.SNMPv2_
   
->Acesta a oferit mai multe funcționalități decât versiunea 1, însă a păstrat același mecanism slab de autenfiticare;

->Pe partea pozitivă, SNMPv2c poate  trimite cantități mai mari de date mai rapid și a introdus un nou tip de comunicare numit inform;

-> În timp ce mesajele trap informau sistemul de management despre o eroare sau o problemă, mesajele inform permiteau managerului SNMP să confirme primirea mesajului trimis de agent. Agentul continua să retrimită mesajul inform până când primea un răspuns de la manager;


   _3.SNMPv3_
   
-> Oferă cel mai ridicat nivel de securitate, având mecanisme îmbunătățite care se asigură că doar utilizatorii autorizați pot vizualiza mesajele SNMP;

->Versiunea 3 oferă și criptare, prin care mesajele SNMP sunt „amestecate”, astfel încât utilizatorii neautorizați să nu le poată citi ;

->Această versiune necesită o configurare mai complexă pentru a activa măsurile suplimentare de securitate. De asemenea, are nevoie de mai multe resurse, crescând utilizarea de procesare și memorie.





			COMENZI SNMP
   SNMP poate efectua o varietate de funcții, folosind o combinație de comunicații de tip „push” și „pull” între dispozitivele de rețea și sistemul de administrare. Aceste funcții includ trimiterea de comenzi de citire/scriere și furnizarea de informații actualizate despre lățimea de bandă, puterea de procesare , utilizarea memoriei etc.. 

   _GET request_: Managerul SNMP generează și trimite această comandă către un agent pentru a obține valoarea unei variabile, identificată prin OID-ul său dintr-un MIB.

   _GETNEXT request_: Managerul SNMP trimite această comandă către agent pentru a prelua valorile următorului OID din ierarhia MIB-ului.

   _INFORM request_: Este o alertă asincronă, similară cu un mesaj trap, dar necesită confirmarea primirii de către SNMP.

   _RESPONSE_: Agentul trimite această comandă către managerul SNMP ca răspuns la un GET request, GETNEXT request sau SET request. Conține valorile variabilelor solicitate.

   _SET request_: Managerul SNMP trimite această comandă către agent pentru a efectua configurări sau comenzi.

   _TRAP_: Agentul trimite această comandă către manager ca alertă asincronă, indicând că a avut loc un eveniment semnificativ, cum ar fi o eroare sau o defecțiune.





						PROIECTAREA APLICAȚIEI 

			1.	Introducere 
		
   Proiectul  realizat își propune să demonstreze principiile de funcționare ale protocolului SNMPv1 (Simple Network Management Protocol) prin implementarea unei aplicații complete, formată dintr-un agent SNMP și un manager SNMP, utilizând exclusiv modulul socket pentru comunicația în rețea:
   
   _Agent SNMP_ – rulează pe sistemul monitorizat, colectează informații despre resurse și le expune printr-un MIB intern;
	
   _Manager SNMP_ – rulează pe un alt sistem din rețea și interacționează cu unul sau mai mulți agenți SNMP, afișând informațiile preluate și gestionând notificările de tip Trap.
	
   _Scopul proiectului_ este de a evidenția modul în care poate fi realizată monitorizarea și administrarea resurselor unui sistem de calcul utilizând mecanismele standardizate ale protocolului SNMP, implementate de la zero prin intermediul modulului socket, fără a apela la biblioteci externe dedicate SNMP.
	
   _Programarea cu sockets_ este esențială pentru comunicațiile de rețea, permițând schimbul de date între diferite dispositive, fiind o metodă de a conecta două noduri într-o rețea pentru a comunica între ele .



	
   În Python, **_socket_**-urile permit comunicarea între procese (IPC) prin rețele.
   
Acest modul  oferă un ghid complet pentru:

•	Crearea de servere și clienți socket ;

•	Gestionarea conexiunilor multiple ;

•	Manipularea erorilor folosind modulul socket din Python.

   Un socket (nod) ascultă pe un anumit port la o adresă IP, în timp ce celălalt socket inițiază conexiunea către acesta.

•	Serverul creează socket-ul care ascultă (listener) ;

•	Clientul se conectează la server pentru a stabili legătura ;

Programarea cu socket-uri începe prin importarea bibliotecii socket și crearea unui socket simplu.





			2.	Motivația proiectului 
			
   Monitorizarea sistemelor și gestionarea eficientă a resurselor reprezintă elemente esențiale în administrarea rețelelor . SNMP este unul dintre cele mai utilizate protocoale în acest domeniu, fiind implementat în routere, servere, switch-uri, echipamente de telecomunicații și multe alte dispozitive inteligente.
   

Proiectul nostru urmărește familiarizarea cu funcționarea concretă a SNMP prin dezvoltarea unei aplicații de la zero, pentru înțelegerea următoarelor elemente :

-	Codificarea și transmiterea  pachetelor SNMP prin rețea ;
  
-	Structurarea MIB-urilor, OID-urilor ;
  
-	Rolul mesajelor specifice SNMPv1 (Get, GetNext, Set, Response, Trap);
  
-	Interacțiunea dintre un manager și mai mulți agenți .
  

			3.Obiectivele proiectului
 	
   Proiectul nostru își propune realizarea unei aplicații demonstrative SNMP funcționale  formată dintr-un agent SNMP și un manager SNMP , care evidențiază modul de monitorizare și administrare a resurselor unui sistem într-o rețea locală. 
   
   Pentru a ilustra practic funcționarea protocolului, demonstrarea proiectului va fi realizată pe două laptopuri conectate în aceeași rețea, unul acționând ca manager, dar și ca agent,  și celălalt ca agent .
   

		 Agent SNMP ( script Python )
		 
	Monitorizează cel puțin cinci resurse ale sistemului (ex: utilizare CPU, memorie, temperatură, spațiu pe disc etc.);

	Expune aceste resurse prin intermediul unor intrări MIB ce pot fi accesate de manager;

	Permite selectarea unităților de măsură pentru anumite resurse (ex: raportarea temperaturii în °C, °F sau K);

	Oferă posibilitatea configurării unor praguri de alertă pentru resursele monitorizate;

	La atingerea pragurilor configurate, agentul generează și transmite mesaje de tip Trap către manager.



		 Manager SNMP ( script Python )
		 
	Poate comunica simultan cu cel puțin două instanțe de agenți, fiecare rulând pe sisteme diferite, aflate în aceeași rețea locală;

	Responsabil de interogarea și administrarea agentului ;

	Inițiază comunicarea și trimite cereri (GetRequest, SetRequest);

	Trimite pachete SNMP către agent, solicitând una dintre resursele expuse în MIB; 

Cererea include OID-ul obiectului și versiunea protocolului ;

	Permite interogarea manuală și setarea valorilor din MIB prin mesaje SNMP;

	Afișează notificări în timp real pentru pachetele Trap primite;

	Include opțiuni pentru modificarea unităților de măsură utilizate de agenți în raportarea datelor ( această funcționalitate este utilizată doar pentru intrarea MIB temperatureUnit);

	Primește răspunsurile (GetRequest) și afișează valorile sistemului în interfață ;

	Ascultă  pe un port dedicat mesajele Trap generate de agent la depășirea unor praguri prestabilite de noi (aceste evenimente sunt afișate imediat pe interfață pentru a alerta utilizatorul/administratorul programului) ;


		Generarea Trap-urilor 
   Agentul implementat la nivelul proiectului nostru SNMP include un mecanism de monitorizare continuă, precisă și detecție a depășirii unor praguri critice. În astfel de situații care pot apărea, agentul generează și trimite manager-ului un mesaj SNMP Trap, conform SNMPv1.
   
   Pragurile stabilite pentru realizarea demonstrației sunt următoarele :
	
1.	CPU Load > 85% (sistem suprasolicitat);
   
2.	Memory usage > 80% ( apare riscul de resurse RAM lipsă);
   
3.	Disk usage > 90% (spațiu insuficient pe disc);
	
4.	Temperature > limita admisă : 65 grade Celsius (apare riscul de supraîncălzire a sistemului );
	
5.	Network  Load > 90% (rețeaua este congestionată).
   

       **Rolul Trap-urilor** :
  	
	Permite notifucarea managerului fără ca acesta să interogheze explicit agentul ;

	Detectare rapidă a situațiilor critice ;

	Simulează un sistem real de monitorizare de rețea .



			Structura Trap-urilor 
   Trap-urile de analiză sunt asociate cu ramura enterprise  1.3.6.1.4.1.2.6.258 . Această ramură reprezintă enterprise-ul privat sub care sunt definite tipurile de alerte trimise de către agent. Toate aceste trap-uri ce sunt trimise din cauza depășirii unor praguri  folosesc acest prefix in OID-ul lor . De asemenea, fiecare variabilă transmisă într-un trap folosește acest OID ca prefix al numelui variabilei.

   
   Un mesaj SNMPv1-Trap este alcătuit din următoarele câmpuri :
   
   _1.Enterprise_ ( OID ce descrie aplicația, indică baza ierarhică a Trap-ului ,permite definirea de alerte specifice – 1.3.6.1.4.1.2.6.258- ramură enterprise privată – pentru definirea alertelor definite de utilizator);
   
   _2.Agent-addr_ ( conține adresa IP a agentului care a generat trap-ul – ajută la identificarea dispozitivului de pe care provine evenimentul – format IPv4 – 4 octeți );


   _3.Generic-trap_ (cod numeric între 0 și 6 care descrie tipul general al evenimentului – pentru evenimente definite de utilizator, se folosește întotdeauna valoarea 6 ) : generic-trap = 6 (enterpriseSpecific)
Sub această categorie sunt incluse Trap-urile definite în ramura: 
1.3.6.1.4.1.2.6.258.0.x

	
   _4.Specific-trap_ ( devine relevant doar atunci când generic-trap =6)   - este un număr de tip întreg ce diferențiază evenimentele proprii definite , de exemplu :
   
	1- > depășire prag temperatură

	2 -> utilizare CPU peste pragul admis , etc.

	6 -> evenimente corelate.




			Trap-urile din  cadrul proiectului  : vom defini 5 trap-uri specifice, în funcție de resursele monitorizate :
			
		Specific- trap :
	1 – depășirea pragului de temperatură;
	2 – depășirea pragului pentru CPU;
	3 – consum ridicat de memorie;
	4 – spațiu insuficient pe disc;
	5 – rată de pachete pierdute – peste prag .


		
**Structură conceptuală ASN1 pentru Traps**
 
![trap_structure](https://github.com/user-attachments/assets/0c93e63f-7e22-4f74-8a70-5b8762a91799)






		**Resurse monitorizate și intrările MIB definite în agentul SNMP **
		
   În aplicația demonstrativă realizată, agentul SNMP implementat monitorizează cel puțin 5 resurse ale sistemului de calcul și le expune manager-ului prin intermediul unor intrări MIB, construite în cadrul unui arbore OID propriu .
   
   Resursele monitorizate în cadrul proiectului nostru sunt :
   
_1.	CPU Load (Încărcarea procesorului)_
   
-	Este o valoare exprimată în procente (0-100%) ce semnifică nivelul de utilizare al procesorului ;
	
_2.	Memory usage (Memoria utilizată)_
 	
-	Procentul RAM utilizat în momentul preluării;

_3.	Disk Usage (Spațiul utilizat pe disc)_
 	
-	Este o valoare exprimată în procente ce indică gradul de ocupare al discului ;
	
_4.	NetworkLoad (Traficul/Încărcarea rețelei)_
 	
-	Este o valoare exprimată în procente ce reflectă activitatea interfeței într-un interval scurt ;

_5.	System Temperature (Temperatura sistemului)_
 	
-	Poate fi raportată în 3 unități de măsură : °C, °F sau °K, conform opțiunii selectate printr-o intrare suplimentară în MIB.



	**_Intrări suplimentare în MIB pentru unitățile de măsură_**
	   Așa cum indică și unul dintre task-urile pe care trebuie să le realizăm în cadrul proiectului propus, pentru resursele a căror valoare poate fi exprimată în mai multe unități de măsură, agentul SNMP trebuie să include intrări suplimentare în MIB care permit manager-ului să selecteze unitatea de măsură dorită . În cadrul proiectului, această cerință se aplică asupra resursei : Temperatura sistemului . Așadar, trebuie să definim doua tipuri de intrări în MIB :
 	
 _a)Intrare în MIB pentru valoarea temperaturii_

– returnează temperatura convertită în unitatea de măsură selectată;

- are următorul format :1.3.6.1.4.1.9999.1.3.0 – systemTemperature ;


_b) Intrare în MIB pentru unitatea de măsură_
  
– permite managerului să trimită un mesaj SNMP Set pentru a modifica unitatea : 1.3.6.1.4.1.9999.1.3.1 – temperatureUnit;

- pentru cele 3 unități de măsură, avem 3 sufixe diferite la nivelul MIB-ului
  
	1.3.6.1.4.1.9999.1.3.1 – grade Celsius
  
	1.3.6.1.4.1.9999.1.3.2 – grade Fahrenheit
  
	1.3.6.1.4.1.9999.1.3.3 – grade Kelvin
  





				Structura MIB-ului pentru resursele monitorizate 
	 Arborele MIB utilizat în cadrul proiectului nostru este construit  începând cu ramura principală, și continuând cu ramura privată : 1.3.6.1(aparțin ramurii principale).4.1.9999(aparțin ramurii private ).În partea de jos a acestei ramuri , 1.3.6.1.4.1.9999, sunt conținute valorile MIB-urilor pentru resursele monitorizate :
  
		1.3.6.1.4.1.9999.1.1	-> cpuUsage
		
		1.3.6.1.4.1.9999.1.2	-> memoryUsage
		
		1.3.6.1.4.1.9999.1.3.0 -> systemTemperature 
		
		1.3.6.1.4.1.9999.1.3.1 -> temperatureUnit
		
		1.3.6.1.4.1.9999.1.4 -> diskUsage 
		
		1.3.6.1.4.1.9999.1.5 -> networkLoad

  

| **OID numeric**           |**Obiect**           | **Tip ASN**1 | **Acces**    | **Descriere**                                     |
|------------------------|-------------------|----------|-----------|------------------------------------------------|
| 1.3.6.1.4.1.9999.1.1   | cpuUsage          | Integer  | read-only | Utilizare procesor (%)                         |
| 1.3.6.1.4.1.9999.1.2   | memoryUsage       | Integer  | read-only | Utilizare memorie (%)                          |
| 1.3.6.1.4.1.9999.1.3.0 | systemTemperature | Integer  | read-only | Temperatura convertită în u.m. selectată       |
| 1.3.6.1.4.1.9999.1.3.1 | temperatureUnit   | Integer  | read-write| Unitatea de măsură (1= °C, 2= °F, 3= °K)       |
| 1.3.6.1.4.1.9999.1.4   | diskUsage         | Integer  | read-only | Spațiul de pe disc utilizat (%)                |
| 1.3.6.1.4.1.9999.1.5   | networkLoad       | Integer  | read-only | Traficul de rețea (%)                          |





		Imaginile de mai jos ne oferă o viziune pe ansamblu a protocolului studiat numit SNMP 

![snmp_arhitecture](https://github.com/user-attachments/assets/169ff203-127c-470c-b2c1-f9c835a8c90b)
![snmp_overwiew](https://github.com/user-attachments/assets/0aa60e3d-d5e4-4306-b7c8-d5d43da09970)
![snmp_elements](https://github.com/user-attachments/assets/9ab6ca7f-f010-4ca5-9b97-fe4d3eee2ea4)
![snmp_manager_agent](https://github.com/user-attachments/assets/899aa921-64a9-47cb-a053-ba81d9e99440)






			Resurse bibliografice
	https://docs.oracle.com/cd/E13203_01/tuxedo/tux91/snmpmref/1tmib.htm#1030143
	https://www.ibm.com/docs/en/oala/1.3.7?topic=events-snmp-trap-structure
	https://www.12000.org/my_notes/snmp/index.html
	https://www.geeksforgeeks.org/computer-networks/simple-network-management-protocol-snmp/
	https://www.ibm.com/docs/en/csfdcd/7.1.0?topic=protocol-introduction-snmp
	https://realpython.com/python-sockets/
	https://www.geeksforgeeks.org/python/socket-programming-python/
	https://www.ranecommercial.com/legacy/note161.html
	https://www.techtarget.com/searchnetworking/definition/SNMP
		
		Pentru imagini :
	https://www.youtube.com/watch?v=swwZO7wWwNY



