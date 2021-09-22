Paamestia
=========
_Teammitglieder: Max, Dominik, André, Arvid

<img src="ReadMe.assets/logo_paamestia.jpeg" alt="logo_paamestia" width="400"/>

Info
----

In diesem Repository sind alle Dateien, Quellcodes, etc. für das Praxisprojekt für Fach Praxis im BGT an der BBS.  

Bei dem Projekt handelt es sich um eine Cocktail-Mischmaschine, bei der man ein Rezept auswählt und dies automatisch gemischt wird.
Außerdem soll es möglich sein, selber frei zu mischen und Rezepte zu importieren. 

---

Software (./code)
-----------------
Geschrieben wurde der Quellcode in Python, da diese relativ einfach anzuwenden ist und für den Raspberry Pi gut geeignet ist
Der Quellcode besteht aus mehreren Dateien, denen verschiedenen Aufgaben zukommen. Die Datei media_lib.py kümmert sich um alles grafische und was die Darstellung betrifft, io_lib.py kümmert isch um den direkten Input (Taster) und Output (Ventile und Pumpe) und drinks_lib.py ist u.a. für die Verwaltung der Rezepte und Getränke zuständig. Genauere Informationen zu dem Quellcode finden sich außerdem im Ordner `/documentation/Sourcecode + System`.  

---

Hardware
--------
Das Hirn des gesamten Projekts ist ein Raspberry Pi, einem Einplatinencomputer, der neben Standard-Anschlüssen, wie USB und HDMI auch über GPIO-Pins (_**G**eneral-**P**urpose-**I**nput-**O**uput-Pins_) verfügt. Diese werden dazu verwendet um die Taster auszulesen, und die Ventile anzusteuern. Die Ansteuerung erfolgt dabei über zwei Relais-Boards, um die hohe Stromaufnahme nicht direkt über den Raspberry Pi zu leiten.  
Für das Bild wird ein alter 3/4-Monitor verwendet, auf dem die grafische Benutzeröberfläche angezeigt wird.  
Die Stromversorgung gestaltete sich etwas schwieriger, weil die Pumpe und Ventile mit 12V betrieben werden müssen, Der RasPi aber nur mit 5V. Dafür wurde erst ein 12V-Netzteil verwendet, und zusätzlich ein Step-Down-Converter, der die Spannung für den RasPi auf 5V runterregelt.  
Zur Konstruktion wurden Alu-Profile als Rahmen verwendet, für die Abdeckung Blech. Zur Montage einiger Bauteile wurden außerdem Halterungen 3D-gedruckt, verwendet wurde dafür der Anycubic Mega S mit dunkelgrauem PETG und blauem PLA.  
_Weitere Informationen, Schematiken und CAD-Dateien sind im `documentation`-Ordner zu finden_

### BOM  
In dieser Liste sind hauptsächlich nur die elektronischen und mechanischen Bauteile aufgelistet. Zusätzliche Meterialien, wie Alu-Profil-Schienen werden natürlich ebenfalls benötigt.

- Raspberry Pi 3(b) ([Amazon](https://www.amazon.de/Raspberry-Pi-Model-ARM-Cortex-A53-Bluetooth/dp/B01CD5VC92/ref=sr_1_4?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=1RXH7LEMMB7TM&dchild=1&keywords=raspberry+pi+3&qid=1617360670&sprefix=Ras%2Caps%2C281&sr=8-4))
- Magnetventile (6 Stück, Öffner)
- Schlauch
- Schlauchverbinder
- Relais-Board (insgesamt 7 Relais, [Amazon](https://www.amazon.de/AZDelivery-8-Relais-Optokoppler-Low-Level-Trigger-Arduino/dp/B07CT7SLYQ/ref=sr_1_8?__mk_de_DE=ÅMÅŽÕÑ&crid=1XKVNJ5KDLTPH&dchild=1&keywords=azdelivery+relay&qid=1607777597&sprefix=azdeliver%2Caps%2C275&sr=8-8))
- Schlauchpumpe ([Amazon](https://www.amazon.de/Schlauchpumpe-Flüssigkeitspumpe-Schlauchwasserpumpe-Silikonschlauch-Pharmazeutika/dp/B07TVDXJQN))
- Silikonstopfen ([Amazon](https://www.amazon.de/Tuuters-Silikonstopfen-Konische-Abdeckstopfen-Gummistopfen/dp/B01LWOXOLZ/ref=sr_1_5?__mk_de_DE=ÅMÅŽÕÑ&crid=11L4LGF9305AW&dchild=1&keywords=silikonstopfen&qid=1607778777&sprefix=silikonstopf%2Caps%2C253&sr=8-5&th=1))
- Taster (6 Stück)
- 12 V Netzteil ([Amazon](https://www.amazon.de/Netzteil-Transformator-Universelles-AC110-240V-Geeignet/dp/B0871TVVRR/ref=pd_sbs_201_1/261-4391009-4390455?_encoding=UTF8&pd_rd_i=B0871TVVRR&pd_rd_r=9c307cf3-26e9-4868-b3f7-a5e2930114ac&pd_rd_w=Qgvps&pd_rd_wg=NaYdi&pf_rd_p=ad79fb78-2eb6-4fd8-b228-cb6e6b4589d9&pf_rd_r=7Q7QPZ3VQS7GJDGTN35V&psc=1&refRID=7Q7QPZ3VQS7GJDGTN35V))
- Step-Down-Converter (aus eigenem Lagerbestand, zu finden aber zum Beispiel hier: [Amazon](https://www.amazon.de/Stromversorgung-Spannungsregler-Abw%C3%A4rtswandler-Hocheffizienter-Einstellbares/dp/B07F38DJLS/ref=sr_1_2_sspa?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=39Q3DDQ5EOQ02&dchild=1&keywords=step-down-converter&qid=1617360609&sprefix=step-d%2Caps%2C197&sr=8-2-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUFBR0xFNFJFMlNGT1YmZW5jcnlwdGVkSWQ9QTA5MjA3NTMxRjMzM1RZUDVDWVVQJmVuY3J5cHRlZEFkSWQ9QTA4NDY1NDEzVkY1OTc5MFVXVUFBJndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ==))

Filamente:  
- [DasFilament PETG Anthrazit](https://www.dasfilament.de/filament-spulen/petg-1-75-mm/438/petg-filament-1-75-mm-anthrazit-v2?c=21)
- [Janbex PLA Blau](https://www.amazon.de/JANBEX-Filament-Drucker-Vakuumverpackung-Schwarz/dp/B08MC7LQZR/ref=sr_1_6?dchild=1&keywords=Janbex&qid=1617379500&sr=8-6&th=1)



Credits
-------

Dieses Projekt steht unter der MIT-Lizenz (komplette Lizenz [hier](https://github.com/zauberwild/paamestia/blob/main/LICENSE))

### verwendete Module:

- [`pygame`](https://www.pygame.org/news) (und `pygame.freetype`)
- [`opencv`](https://opencv.org/) (und [`numpy`](https://numpy.org/))
- [`tkinter`](https://docs.python.org/3/library/tkinter.html)
- `os`, `time` und `pathlib`
- [`gpiozero`](https://github.com/gpiozero/gpiozero)

