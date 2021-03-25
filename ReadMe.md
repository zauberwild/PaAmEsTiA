Paamestia
=========
_Teammitglieder: Schiemann, Dominik, André, Arvid (@zauberwild)_

Info
----

In diesem Repository sind alle Dateien, Quellcodes, etc.
für das Praxisprojekt für Fach Praxis im BGT an der BBS.

---

Software (./code)
-----------------
### .py-Dateien
Quellcode

### src
Alle zum Programm zugehörigen Dateien

##### einzelne Dateien

| Datei    | Erklärung                                                    |
| -------- | ------------------------------------------------------------ |
| .windows | wird genutzt, um das Betriebssystem zu erkennen. Dies ist notwendig, weil ein paar Sachen auf dem Raspberry Pi (bzw. Linux) anders funktionieren als auf Windows |
| drinks   | Auflistung aller verwendbaren Getränke                       |

##### fonts

ttf-Dateien für Schriftarten, z. B. für Text auf Schaltflächen


#####  recipes
Hier werden alle Rezepte abgespeichert.  
Der Rezept-Name wird vom Dateinamen vorgegeben und in der ersten Zeile stehen zusätzliche Details zum Rezept. Der Rest der Datei bildet das Rezept nach folgender Formatierung:  
`<Getränk1>,<Menge in ml>`  
`<Getränk2>,<Menge in ml>`  
`<Getränk3>,<Menge in ml>`  
`...`  

##### media
Beinhaltet die Video-Ordner und sonstige Mediendateien

##### props, test und test_klein
Beinhaltet Platzhalter-Dateien

---

Hardware
--------
- Logik: Raspberry Pi 3B
- Input: simple Taster
- Ansteuerung: Relais Board
- Magnetventile und Schlauchpumpe
- außerdem ein Monitor
