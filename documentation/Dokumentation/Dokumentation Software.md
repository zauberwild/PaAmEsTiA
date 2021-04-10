# Dokumentation Software

## 1. Allgemein

Der Quellcode ist für dieses Projekt relativ lang und umfasst über 1000 Zeilen, von daher können wir es hier nicht komplett einfügen. Allerdings werden wir hier auf die einzelnen Teile, aus denen das Programm besteht kurz erklären.

Das Programm ist sowohl öffentlich in einem [GitHub-Repository](https://www.github.com/zauberwild/paamestia) verfügbar und befindet sich noch auf dem beigelegten Datenträger (im Ordner "code" als Originalform und im Ordner "PDF" auch als PDF-Datei exportiert.

## 2. Betriebssystem / Programmiersprache

Wir haben als Betriebssystem Raspbian OS verwendet, da es speziell für den Raspberry Pi entwickelt wurde und leicht einzusetzen ist. Außerdem bietet es einige praktische Werkzeuge an, wie zum Beispiel das Netzwerkprotokoll [???] SSH, worüber das Terminal des Raspberry Pis von einem anderen Computer gesteuert werden kann.

Um die Benutzerfreundlichkeit zu erhöhen, sollte das Programm automatisch starten, sobald der Raspberry Pi hochfährt. Zu diesem Zweck befindet sich in Linux ein Ordner, in dem alle Datei-Verknüpfungen nach dem Hochfahren automatisch ausgeführt werden. Daher wurde dort einfach eine Verknüpfung zum Hauptskript unserer Software angelegt.

Es ist außerdem immer noch möglich, auf das Betriebssystem hinter dem Programm zuzugreifen. Dafür werden lediglich ein Maus und Tastatur benötigt. Um das Programm zu beenden, muss einfach nur die `ESC`-Taste gedrückt werden. Würde man `VERLASSEN` im Hauptmenü auswählen, wird das gesamte System heruntergefahren.

Als Programmiersprache bot sich Python an, da diese ebenfalls einfach zu verwenden ist, und nötiges Grundwissen schon vorhanden war. Eine der Nachteile dieser Programmiersprache ist allerdings, dass es sich hierbei um eine interpretierte Sprache handelt, welche im Gegensatz zu kompilierten Sprachen generell etwas langsamer sind und mehr Ressourcen beanspruchen. Dies führte zu mehreren Problemen während der Entwicklung, weil der Raspberry Pi wegen seiner kompakten Größe nur begrenzt Ressourcen hat.

## 3. Python-Skripte

### I. Allgemein

Das Programm wurde aufgrund der immensen Größe in mehrere Dateien aufgeteilt, welche jeweils eine eigene Aufgabe haben. Außerdem verfügt Python über eine riesige Anzahl von Modulen, welche zahlreiche Aufgaben übernehmen oder vereinfachen. Im Folgenden werden wir auf jede einzelne Quellcode-Datei und zusätzliche Dateien eingehen.

#### A. paamestia.py

Diese Datei bildet das Kernstück der Datei und verwaltet den grundlegenden Programmablauf. so werden dort die Position in den Menüs abgerufen, und die entsprechende Funktion aufgerufen, die die einzelnen Menüs verwaltet.

#### B. globals.py

In dieser Datei werden alle Objekte und Variablen, die global, das heißt in allen Dateien verfügbar sein müssen, aufgelistet. Dazu gehören unter anderem der Dateipfad zum Quellcode (`gen_path`), um problemlos auf Bild-, Video- und Textdateien zugreifen zu können.

Außerdem wird dort berechnet, wieviel Flüssigkeit die Pumpe durchsetzt, um später auch die Menge ausgeben zu können.

#### media_lib.py

Dieses Modul bietet alle benötigten Werkzeuge für graphische Benutzerumgebung auf dem Monitor. Dies beinhaltet eine Klasse für die Video-Wiedergabe, eine für die Schaltflächen, und weitere. Hier haben wir die Module `pygame` und `opencv` verwendet. Das Pygame-Modul ist eigentlich für Spiele gedacht, ist aber relativ simpel und erlaubt es, schnell und einfach ein Fenster zu erstellen und darauf Bilder und Texte anzuzeigen. Daher haben wir es auch bei einen Großteil der der GUI verwendet. Bei Animationen, bzw. Video gestaltete sich allerdings ein kleines Problem: Zuerst unterstützt das Pygame-Modul keine Wiedergabe von Video, also haben wir uns entschieden, einzelne Bilder zu nehmen, um diese dann wie ein Daumenkino abzuspielen. Allerdings wurde dann die Anzahl der Bilder so groß, dass der Arbeitsspeicher komplett ausgefüllt werden würde, und das Programm abstürzt. Schließlich fand sich mit dem OpenCV-Modul doch noch eine Lösung, um Videos abzuspielen. Hier mussten wir zwar die Auflösung relativ weit runtersetzen, um eine ausreichende Framerate zu erreichen, aber immerhin läuft das Programm.

#### io_lib.py

Hier wird der Input und Output des Raspberry Pis kontrolliert, sprich hier werden die Taster ausgelesen und die Ventile und Pumpe angesteuert. Dafür verwendeten wir das offizielle `gpiozero`-Modul vom Raspberry Pi und wieder das Pygame-Modul für die Steuerung über eine Tastatur.

Das Auslesen gestaltete sich etwas schwieriger, weil wir immer nur ein Signal haben wollen, wenn die Taste runtergedrückt wird. Wenn die Taste gehalten wird, sollte kein Signal mehr vorhanden sein. Dazu wird der aktuelle Wert mit dem vorherigen verglichen, und wenn das vorherige Signal noch bei bei 0 war und der aktuelle bei 1 ist, wird ein Signal ausgegeben. Dafür haben wir die Funktion `update_input()` erstellt, um immer den aktuellen Stand zu haben. Die zweite Funktion, `read_input()`, gibt den aktuellen Stand eines bestimmten Taster aus.