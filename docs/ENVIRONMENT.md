# System- und Pfadübersicht – DAX Overnight EA

Zweck
- Zentrale Referenz für Maschinen, Pfade und Netzlaufwerke, um ein konsistentes Arbeiten über Geräte hinweg zu gewährleisten.

Maschinen
- WIN11NEU (Windows 11)
  - MetaTrader 5 Root: C:\portabel\MetaTrader5
  - Zugriff auf Ryzen-Server: S:\ → /home/rodemkay/
  - Projektverzeichnis via Mount: S:\mt5\daxovernight
- RYZENSERVER (Ubuntu Linux, 24x7)
  - Projektverzeichnis: /home/rodemkay/mt5/daxovernight
- ACERLAPTOP (Windows, Cursor + Kilo Code)
  - Zugriff auf WIN11NEU MT5: X:\portabel\MetaTrader5
  - Zugriff auf Ryzen-Server: R:\ → /home/rodemkay/
  - Projektverzeichnis via Mount: R:\mt5\daxovernight

Laufwerks-/Mount-Mappings
- WIN11NEU:
  - S:\ ↔ /home/rodemkay/ (Ziel: RYZENSERVER)
- ACERLAPTOP:
  - X:\ ↔ C:\portabel\MetaTrader5 (Ziel: WIN11NEU)
  - R:\ ↔ /home/rodemkay/ (Ziel: RYZENSERVER)

Hinweise
- Aktiver Arbeitsplatz: WIN11NEU (sofern nicht anders angegeben).
- Bei Unklarheiten bitte nachfragen (Quelle: Nutzerhinweis).
- MT5-Quelltexte sind UTF-16 LE; bei Bearbeitung auf Kodierung achten.

Verweise
- Kilo Code Guide: [KILO_CODE_GUIDE.md](../KILO_CODE_GUIDE.md)
- Projekt-Gedächtnis: [.kilocode/memory.json](../.kilocode/memory.json)
- Projektindex: [docs/PROJECT_INDEX.md](PROJECT_INDEX.md)
## Netzwerk / Tailscale

- Globale Tailscale-Hosts und Arbeitsbereiche: [docs/tailscale-hosts.json](docs/tailscale-hosts.json)
- Aktuelles VS Code Workspace-File: X:\Users\rodemkay\Desktop\daxovernight_workspace.code-workspace
- Hosts:
  - ACER Laptop: 100.64.128.121
  - WIN11NEU: 100.122.144.89
  - Ryzenserver: 100.89.207.122
