#!/bin/bash

# Kompiliere the_don.mq5 v1.13 mit Server-Lizenz-Fix

echo "Kompiliere the_don.mq5 v1.13..."

# Wechsle ins MT5 Verzeichnis
cd /home/rodemkay/CaufWin11/portabel/MetaTrader5

# Kompiliere mit Wine
wine64 MetaEditor64.exe /compile:MQL5/Experts/Don/the_don.mq5 /log 2>&1

# Warte kurz
sleep 3

# Prüfe ob .ex5 erstellt wurde
if [ -f "MQL5/Experts/Don/the_don.ex5" ]; then
    echo "✓ Kompilierung erfolgreich!"
    echo "  Version 1.13 mit Server-Lizenz-Anzeige"
    echo "  _ansTime Variable wird jetzt vom Server gelesen"
else
    echo "✗ Kompilierung fehlgeschlagen"
    echo "Prüfe die Log-Datei für Details"
fi