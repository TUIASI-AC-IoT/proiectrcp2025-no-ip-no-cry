
[SNMP-doc.pdf](https://github.com/user-attachments/files/23440129/SNMP-doc.pdf)

Implementare SNMP .Aplicație demonstrativă
Proiect la disciplina Rețele de Calculatoare
Studenți : Aciocîrlănoaei Georgiana (1310A)
Dascălu Ioana-Felicia (1310A)


Simple Network Management Protocol (SNMP, ro. : “Protocolul Simplu de Administrare a Rețelei “) este un protocol de administrare standardizat Internet , conceput initial pentru gestionarea rețelelor TCP/IP .
SNMP este un protocol implementat la nivel de aplicație ce folosește porturile UDP 161(SNMP Manager) și 162(SNMP Agent) . Acesta este utilizat în cadrul monitorizării rețelelor , administrării echipamentelor de rețea ( routere, switch-uri, servere, imprimante etc.), detectarea defecțiunilor de rețea , colectării informațiilor și configurarea dispozitivelor de la distanță .


  Arhitectura SNMP
Arhitectura SNMP se bazează pe un model Manager – Agent , împreună cu o bază de date numită MIB, și are la bază 3 elemente fundamentale :
  1. SNMP MANAGER
Managerul SNMP , cunoscut și sub numele de NMS – Network Management Station ( Stație de Management a Rețelei ) , este o aplicație care generează cereri pentru informațiile din MIB , procesează răspunsurile primite și care rulează pe un PC sau Server. Un router care rulează programul de server SNMP este numit agent , în timp ce un sistem (host) care rulează programul client SNMP este numit manager .
  2. SNMP AGENT
Agentul SNMP este un modul software de management ce rulează pe un dispozitiv administrat . Managerul accesează valorile stocate în baza de date, în timp ce agentul menține informațiile din acesta . De exemplu, pentu a verifica dacă un router este congestionat(are un trafic excesiv ) sau nu, maganerul poate examina variabilele relevante pe care routerul le stochează, cum ar fi numărul de pachete primite și transmise.
Un manager SNMP poate trimite cereri către un agent fie pentru a prelua informații din MIB-ul agentului (cerere SNMP Get), fie pentru a modifica informații din MIB (cerere SNMP Set). De asemenea, un agent SNMP poate trimite mesaje nesolicitate către managerul SNMP, numite SNMP traps.
  3. MIB (Management Information Base )
MIB conține informații despre resursele care necesită administrate . Aceste informații sunt organizate ierarhic și constau din instanțele de obiecte, care sunt, în esență, variabile. MIB-ul, sau colecția de date de sub management-ul managerului, este unică pentru fiecare agent . MIB este împărțită în opt categorii : System, Interface, Address Translation, IP, UDP,ICMP , TCP .

  MIB-ul este scris în notația ASN.1 ( Abstract Syntax Notation 1).
  ASN.1 este o notație standard întreținută de ISO (Organizația Internațională pentru Standardizare) și utilizată în domenii variate, de la World Wide Web până la sisteme de control al aviației. Toată comunicația SNMP depinde de faptul că toate dispozitivele trebuie să înțeleagă mesajele SNMP, ceea ce ridică câteva probleme tehnice.
  Prima problemă apare deoarece diferitele limbaje de programare au seturi ușor diferite de tipuri de date (numere întregi, șiruri de caractere, octeți, caractere etc.).De exemplu, un manager SNMP care trimite un mesaj cu tipuri de date specifice Java poate să nu fie înțeles de un agent SNMP scris în C.
  Soluția: SNMP folosește ASN.1 (Abstract Syntax Notation One) pentru a defini tipurile de date utilizate în mesajele SNMP. Deoarece ASN.1 este independent de orice limbaj de programare, agenții și managerii SNMP pot fi scriși în orice limbaj.
  Totuși, chiar și folosind tipuri de date ASN.1 valide, apare o altă problemă: cum sunt codificate datele pentru transmisie? Șirurile trebuie terminate cu caracter nul, ca în C, sau nu? Valorile Boolean sunt pe 8 biți (C++) sau pe 16 biți (Visual Basic 6)?
  Rezolvarea: ASN.1 include Basic Encoding Rules (BER), care standardizează modul de codare a tuturor tipurilor de date înainte de a fi trimise pe rețea. Astfel, toate câmpurile unui mesaj SNMP trebuie să fie tipuri ASN.1 valide și codificate conform BER.

Pentru a construi un mesaj SNMP, programatorul trebuie să înțeleagă tipurile de date ASN.1, care se împart în două categorii:
1. Tipuri primitive:
  o Integer (număr întreg)
  o Octet String (șir de octeți/caractere)
  o Null
  o Boolean
  o Object Identifier (OID) – central pentru SNMP, deoarece OID identifică parametrul adresat în agent.
2. Tipuri complexe: ASN.1 permite gruparea tipurilor primitive în tipuri complexe, pentru organizarea datelor. Exemple:
  o Sequence: o listă de câmpuri, fiecare cu tip diferit.
  o PDU (Protocol Data Unit): tipuri complexe specifice SNMP, care conțin corpul mesajului SNMP. Exemple: GetRequest și SetRequest, pentru citirea și scrierea parametrilor.


Un mesaj SNMP este, în final, o structură formată complet din câmpuri ASN.1.
  Scopul principal al unui mesaj SNMP este de a controla (set) sau de a monitoriza (get) parametrii unui agent SNMP. În SNMP, un parametru reprezintă o instanță a unui obiect definit într-un mod general în cadrul MIB-ului (Management Information Base). Un obiect SNMP poate avea una sau mai multe instanțe, în funcție de structura și tipul resursei monitorizate. Managerul SNMP poate obține sau modifica valoarea fiecărei instanțe gestionate de agent.
  În cadrul unui agent SNMP, obiectele și parametrii monitorizați sunt organizați sub forma unui arbore ierarhic. Pentru identificarea exactă a fiecărui element din acest arbore, SNMP folosește Object Identifier-uri (OID-uri).
Object Identifier (OID)
  Un Object Identifier (OID) este o secvență numerică ce indică în mod unic poziția unui obiect sau a unei instanțe din arborele MIB. Structura sa este ierarhică, iar fiecare nivel al secvenței reprezintă o ramură în arbore.
  Un OID este exprimat sub forma unei liste de numere separate prin puncte, de exemplu: 1.3.6.1.2.1.1.5.0 Această reprezentare numerică permite identificarea precisă a unui obiect, indiferent de platformă sau producător, deoarece OID-urile sunt definite și standardizate la nivel internațional .


  Structura ierarhică a OID-urilor
Arborele OID este organizat pe nivele ierarhice, pornind de la rădăcina globală. În mod uzual, ramura utilizată de SNMP pentru obiectele de management este:1.3.6.1 care corespunde lanțului: iso → org → dod → internet
Sub această ramură se găsesc:
   .2.1 – OID-uri standard (MIB-II);
   .4.1 – OID-uri pentru companii și implementări specifice ;
Prin această ierarhie, este asigurată:
   unicitatea globală a fiecărui parametru monitorizat
   compatibilitatea între sisteme diferite
   extensibilitatea pentru implementări personalizate

  
  Rolul OID-urilor în SNMP
În orice operație SNMP (GetRequest, GetNextRequest, SetRequest sau Trap), OID-ul identifică obiectul vizat de manager. În loc să transmită un nume textual, managerul folosește OID-ul numeric, garantând interpretarea corectă de către agent. De exemplu, pentru a solicita o anumită informație sistemică de la agent, managerul transmite un OID specific, iar agentul returnează valoarea asociată obiectului respectiv. Astfel, OID-ul reprezintă elementul fundamental prin care SNMP asigură o adresare standardizată și precisă a obiectelor monitorizate sau controlate într-un sistem gestionat la distanță.

      Mod de funcționare al SNMP
   Agenții software SNMP de pe dispozitivele și serviciile de rețea comunică cu un NMS ( Network Management System) pentru a trasnmite informații despre starea sistemului și modificările de configurare ). NMS-ul oferă o interfață unică prin care administratorii pot trimite comenzi și primi alerte automate .
    SNMP se bazează pe conceptul de MIB ( Management Information Base ) pentru a determina modul în care sunt transmise și schimbate informațiile despre metricele dispozitivelor . MIB-ul reprezintă o descriere formală a componentelor unui dispozitiv de rețea și a informațiilor sale de stare . MIB-urile pot fi create pentru orice dispozitiv din rețeaua Internet of Things ( IoT), inclusiv pentru camere video IP, vehicule, echipamente industrial sau medicale .
      SNMP utilizează o combinație de comunicații de tip pull și push între dispozitivele de rețea și NMS . Agentul SNMP, care se află împreună cu MIB-ul pe un dispozitiv de rețea, colectează în mod continuu informații despre stare . Totuși, el transmite informații către NMS doar la cerere sau atunci când un anumit parametru al rețelei depășește un prag predefinit, cunoscut sun numele de trap. Mesajele trap sunt, de obicei, trimise către serverul de administrare atunci cand apare un eveniment semnificativ, cum ar fi o eroare critică .
    SNMP include și un tip de mesaj numit inform , care permite unui instrument de monitorizare a rețelei să confirme primirea unui mesaj de la un dispozitiv.     Mesajele inform îi permit agentului să reseteze o alertă declanșată .
    Instrumentele de administrare a rețelei pot folosi un mesaj de tip set pentru a modifica un dispozitiv de rețea prin intermediul agentului SNMP. Aceste mesaje predefinite permit, de asemenea, administratorului să schimbe configurațiile dispozitivelor ca răspuns la evenimente noi din rețea.
    În majoritatea cazurilor, SNMP funcționează într-un model sincron: managerul SNMP inițiază comunicarea, iar agentul răspunde. De obicei, SNMP folosește User Datagram Protocol (UDP) ca protocol de transport. Porturile UDP bine cunoscute pentru traficul SNMP sunt 161 (SNMP) și 162 (SNMPTRAP). Aceste două porturi sunt valori implicite standard, identice în toate versiunile SNMP.
    SNMP este denumit „simplu” datorită naturii sale necomplicate. El poate executa comenzi de citire/scriere, cum ar fi resetarea unei parole sau modificarea unei setări de configurare, și poate raporta cantitatea de lățime de bandă, putere de procesare și memorie utilizată.
    Fiind unul dintre cele mai utilizate protocoale, SNMP este compatibil cu o gamă largă de echipamente hardware — de la echipamente tradiționale de rețea (routere, switch-uri, puncte de acces wireless) până la dispozitive finale, cum ar fi imprimante, scanere și dispozitive IoT.


      Versiunile SNMP
  1. SNMPv1 (cea pe care o vom dezvolta în cadrul proiectului propus)
  ->Această versiunile se concentrează pe ușurința utilizării și pe o configurație simplă. Totuși, în comparație cu versiunile ulterioare, a avut capacități și mecanisme de securitate limitate ;
  ->Schimbul de date între dispozitivele conectate și sistemul central de management era autentificat doar cu o parolă necriptată, cunoscută sub numele de community string, iar orice persoană cu acces la rețea o putea vedea ;
  2.SNMPv2
  ->Acesta a oferit mai multe funcționalități decât versiunea 1, însă a păstrat același mecanism slab de autenfiticare;
  ->Pe partea pozitivă, SNMPv2c poate trimite cantități mai mari de date mai rapid și a introdus un nou tip de comunicare numit inform;
  -> În timp ce mesajele trap informau sistemul de management despre o eroare sau o problemă, mesajele inform permiteau managerului SNMP să confirme primirea mesajului trimis de agent. Agentul continua să retrimită mesajul inform până când primea un răspuns de la manager;
  3.SNMPv3
  -> Oferă cel mai ridicat nivel de securitate, având mecanisme îmbunătățite care se asigură că doar utilizatorii autorizați pot vizualiza mesajele SNMP;
  ->Versiunea 3 oferă și criptare, prin care mesajele SNMP sunt „amestecate”, astfel încât utilizatorii neautorizați să nu le poată citi ;
  ->Această versiune necesită o configurare mai complexă pentru a activa măsurile suplimentare de securitate. De asemenea, are nevoie de mai multe resurse, crescând utilizarea de procesare și memorie.

          Comenzi SNMP
  SNMP poate efectua o varietate de funcții, folosind o combinație de comunicații de tip „push” și „pull” între dispozitivele de rețea și sistemul de administrare. Aceste funcții includ trimiterea de comenzi de citire/scriere și furnizarea de informații actualizate despre lățimea de bandă, puterea de procesare , utilizarea memoriei etc..
  GET request: Managerul SNMP generează și trimite această comandă către un agent pentru a obține valoarea unei variabile, identificată prin OID-ul său dintr-un MIB.
  GETNEXT request: Managerul SNMP trimite această comandă către agent pentru a prelua valorile următorului OID din ierarhia MIB-ului.
  INFORM request: Este o alertă asincronă, similară cu un mesaj trap, dar necesită confirmarea primirii de către SNMP.
  RESPONSE: Agentul trimite această comandă către managerul SNMP ca răspuns la un GET request, GETNEXT request sau SET request. Conține valorile variabilelor solicitate.
  SET request: Managerul SNMP trimite această comandă către agent pentru a efectua configurări sau comenzi.
  TRAP: Agentul trimite această comandă către manager ca alertă asincronă, indicând că a avut loc un eveniment semnificativ, cum ar fi o eroare sau o defecțiune.





                              PROIECTAREA APLICAȚIEI
    1. Introducere
Proiectul realizat își propune să demonstreze principiile de funcționare ale protocolului SNMPv1 (Simple Network Management Protocol) prin implementarea unei aplicații complete, formată dintr-un agent SNMP și un manager SNMP, utilizând exclusiv modulul socket pentru comunicația în rețea:
Agent SNMP – rulează pe sistemul monitorizat, colectează informații despre resurse și le expune printr-un MIB intern;
Manager SNMP – rulează pe un alt sistem din rețea și interacționează cu unul sau mai mulți agenți SNMP, afișând informațiile preluate și gestionând notificările de tip Trap.
Scopul proiectului este de a evidenția modul în care poate fi realizată monitorizarea și administrarea resurselor unui sistem de calcul utilizând mecanismele standardizate ale protocolului SNMP, implementate de la zero prin intermediul modulului socket, fără a apela la biblioteci externe dedicate SNMP.
Programarea cu sockets este esențială pentru comunicațiile de rețea, permițând schimbul de date între diferite dispositive, fiind o metodă de a conecta două noduri într-o rețea pentru a comunica între ele .

În Python, socket-urile permit comunicarea între procese (IPC) prin rețele.
Acest modul oferă un ghid complet pentru:
   Crearea de servere și clienți socket ;
   Gestionarea conexiunilor multiple ;
   Manipularea erorilor folosind modulul socket din Python.
Un socket (nod) ascultă pe un anumit port la o adresă IP, în timp ce celălalt socket inițiază conexiunea către acesta.
   Serverul creează socket-ul care ascultă (listener) ;
   Clientul se conectează la server pentru a stabili legătura ;
Programarea cu socket-uri începe prin importarea bibliotecii socket și crearea unui socket simplu.




      2. Motivația proiectului
  Monitorizarea sistemelor și gestionarea eficientă a resurselor reprezintă elemente esențiale în administrarea rețelelor . SNMP este unul dintre cele mai utilizate protocoale în acest domeniu, fiind implementat în routere, servere, switch-uri, echipamente de telecomunicații și multe alte dispozitive inteligente.
Proiectul nostru urmărește familiarizarea cu funcționarea concretă a SNMP prin dezvoltarea unei aplicații de la zero, pentru înțelegerea următoarelor elemente :
- Codificarea și transmiterea pachetelor SNMP prin rețea ;
- Structurarea MIB-urilor, OID-urilor ;
- Rolul mesajelor specifice SNMPv1 (Get, GetNext, Set, Response, Trap);
- Interacțiunea dintre un manager și mai mulți agenți .
  
      3. Obiectivele proiectului
  Proiectul nostru își propune realizarea unei aplicații demonstrative SNMP funcționale formată dintr-un agent SNMP și un manager SNMP , care evidențiază modul de monitorizare și administrare a resurselor unui sistem într-o rețea locală .
Pentru a ilustra practic funcționarea protocolului, demonstrarea proiectului va fi realizată pe două laptop-uri conectate în aceeași rețea, unul acționând ca manager, dar și ca agent, și celălalt ca agent .
      Agent SNMP ( script Python )
 Monitorizează cel puțin cinci resurse ale sistemului (ex: utilizare CPU, memorie, temperatură, spațiu pe disc etc.);
 Expune aceste resurse prin intermediul unor intrări MIB ce pot fi accesate de manager;
 Permite selectarea unităților de măsură pentru anumite resurse (ex: raportarea temperaturii în °C, °F sau K);
 Oferă posibilitatea configurării unor praguri de alertă pentru resursele monitorizate;
 La atingerea pragurilor configurate, agentul generează și transmite mesaje de tip Trap către manager.
      Manager SNMP ( script Python )
 Poate comunica simultan cu cel puțin două instanțe de agenți, fiecare rulând pe sisteme diferite, aflate în aceeași rețea locală;
 Permite interogarea manuală și setarea valorilor din MIB prin mesaje SNMP;
 Oferă funcția de actualizare automată a informațiilor la un interval de timp stabilit de utilizator;
 Afișează notificări în timp real pentru pachetele Trap primite;
 Include opțiuni pentru modificarea unităților de măsură utilizate de agenți în raportarea datelor.


Ilustrații reprezentative pentru înțelegerea SNMP:
<img width="1293" height="524" alt="image" src="https://github.com/user-attachments/assets/d736d1d3-455a-4cbd-a1a9-1b2664166ca6" />
<img width="1062" height="548" alt="image" src="https://github.com/user-attachments/assets/152370b5-e5b8-4a94-a54e-00e05ee25b44" />
<img width="1007" height="548" alt="image" src="https://github.com/user-attachments/assets/41998d18-01a1-4eda-8314-5fd6512259b7" />
<img width="1017" height="588" alt="image" src="https://github.com/user-attachments/assets/86adcbcb-fb69-4352-b12a-afd9d29749db" />


Resurse bibliografice
https://www.geeksforgeeks.org/computer-networks/simple-network-management-protocol-snmp/
https://www.ibm.com/docs/en/csfdcd/7.1.0?topic=protocol-introduction-snmp
https://realpython.com/python-sockets/
https://www.geeksforgeeks.org/python/socket-programming-python/
https://www.ranecommercial.com/legacy/note161.html
https://www.techtarget.com/searchnetworking/definition/SNMP
Pentru imagini :
https://www.youtube.com/watch?v=swwZO7wWwNY





