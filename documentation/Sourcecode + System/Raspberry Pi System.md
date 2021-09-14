# Raspberry Pi System

## Autostart des Skripts

"Desktop"-Datei (Pfad: `/home/pi/.config/autostart/paamestia-auto.desktop`):  

`[Desktop Entry]`
`Name=Paamestia-Auto`
`Comment=Autostart Script for PaAmEsTiA`
`Type=Application`
`Exec=python3 /home/pi/paamestia/code/paamestia.py`
`Terminal=true`



## Steuerung

Wird mittels Datei `code/src/.windows` angeschaltet