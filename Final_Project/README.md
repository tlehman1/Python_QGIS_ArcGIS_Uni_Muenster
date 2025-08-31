# Building Block Creator Plugin

## Überblick

Das Building Block Creator Plugin ist ein QGIS-Erweiterung, die ALKIS- und ATKIS-Daten kombiniert, um semi-automatisch Baufelder zu erstellen. Das Plugin analysiert Nutzungsflächendaten und erstellt daraus zusammenhängende Baufelder durch einen komplexen geometrischen Verarbeitungsprozess.

## Funktionen

- **Automatisierte Baublockgenerierung**: Erstellt Baufelder aus Infrastrukturdaten
- **Filterung nach Nutzungsarten**: Berücksichtigt spezifische Nutzungstypen (Straßenverkehr, Bahnverkehr, Fließgewässer, Wege)
- **Geometrische Verarbeitung**: 15-stufiger Verarbeitungsprozess mit Delaunay-Triangulation
- **PDF-Export**: Exportiert das Ergebnis als PDF mit Titel und Statistiken
- **Fortschrittsanzeige**: Zeigt den Verarbeitungsfortschritt in Echtzeit an

## Installation

1. Kopieren Sie das Plugin-Verzeichnis in Ihren QGIS-Plugin-Ordner
2. Starten Sie QGIS neu
3. Aktivieren Sie das Plugin unter **Plugins → Plugins verwalten und installieren**

## Verwendung

### Eingangsdaten

Das Plugin benötigt drei Eingabeschichten:

1. **Municipal Boundary Layer (Gemeindegrenzen)**: Polygonschicht mit Gemeindegrenzen
2. **District Boundary Layer (Gemarkungsgrenzen)**: Polygonschicht mit Gemarkungsgrenzen  
3. **Land Use Layer (nutzungFlurstueck)**: Polygonschicht mit Nutzungsflächendaten

### Workflow

1. **Plugin öffnen**: Klicken Sie auf das Building Block Creator Icon oder wählen Sie es aus dem Menü
2. **Layer auswählen**: Wählen Sie die erforderlichen Eingabeschichten aus den Dropdown-Menüs
3. **Output-Name festlegen**: Geben Sie einen Namen für die Ergebnis-Schicht ein
4. **PDF-Export (optional)**: Aktivieren Sie die Checkbox "Export result to PDF" wenn gewünscht
5. **Verarbeitung starten**: Klicken Sie auf "OK" um den Prozess zu starten

### Verarbeitungsschritte

Das Plugin führt einen 15-stufigen Verarbeitungsprozess durch:

1. **Initialisierung**: Erstellt gefilterte Schicht für Infrastrukturdaten
2. **Analyse**: Durchsucht nutzungFlurstueck-Features nach relevanten Nutzungsarten
3. **Geometrie-Verkleinerung**: Verkleinert ursprüngliche Geometrie um 2 Meter
4. **Stützpunkte-Extraktion**: Extrahiert Vertices aus gepufferten Geometrien
5. **Pufferung**: Puffert Vertices mit 5 Metern
6. **Union**: Vereinigt alle Puffer
7. **Zentroide**: Erstellt Zentroide aus Union-Puffern
8. **Delaunay-Triangulation**: Erstellt Dreiecke aus Zentroiden
9. **Linienkonvertierung**: Wandelt Dreieckspolygone in Linien um
10. **Linien-Explosion**: Zerlegt Linien in einzelne Segmente
11. **Geometrie-Pufferung**: Puffert ursprüngliche Geometrie mit 10 Metern
12. **Auflösung**: Löst 10m-Puffer auf
13. **Linienfilterung**: Filtert Linien innerhalb der Puffergeometrie
14. **Polygon-Eliminierung**: Entfernt kleine Polygone (< 1000 m²)
15. **Finalisierung**: Fügt Ergebnis zur Karte hinzu

### Gefilterte Nutzungsarten

Das Plugin filtert nach folgenden Nutzungsarten aus dem `nutzart`-Feld:

- **Bahnverkehr**: Bahnlinien und Bahninfrastruktur
- **Fließgewässer**: Flüsse, Bäche und andere Wasserläufe
- **Straßenverkehr**: Straßen und Verkehrswege
- **Weg**: Fußwege und kleinere Pfade

## Ausgabe

### Ergebnis-Layer

Das Plugin erstellt eine neue Polygonschicht mit folgenden Attributen:

- **Geometrie**: Baufeld-Polygone
- **Layer-spezifische Attribute**: Abhängig vom Verarbeitungsschritt

### PDF-Export

Wenn die PDF-Export-Option aktiviert ist, wird ein PDF erstellt mit:

- **Titel**: "Building Blocks Export"
- **Karte**: Visualisierung der Baufelder
- **Statistiken**: Layer-Name und Anzahl der Features
- **Layout**: A4-Format mit professionellem Layout

## Technische Details

### Systemanforderungen

- QGIS 3.x
- PyQt5
- QGIS Processing Framework

### Abhängigkeiten

- `qgis.core`: Kern-QGIS-Funktionalitäten
- `qgis.processing`: Verarbeitungsalgorithmen
- `PyQt5.QtWidgets`: Benutzeroberfläche
- `PyQt5.QtCore`: Qt-Kernfunktionalitäten

### Verarbeitungsalgorithmen

Das Plugin verwendet folgende QGIS-Processing-Algorithmen:

- `native:dissolve`: Geometrie-Auflösung
- `native:centroids`: Zentroide-Erstellung
- `qgis:delaunaytriangulation`: Delaunay-Triangulation
- `native:polygonstolines`: Polygon-zu-Linien-Konvertierung
- `native:explodelines`: Linien-Explosion
- `native:buffer`: Pufferung
- `native:extractbylocation`: Räumliche Filterung
- `native:polygonize`: Polygonisierung
- `native:multiparttosingleparts`: Multipart-Aufteilung
- `qgis:eliminateselectedpolygons`: Polygon-Eliminierung

## Fehlerbehebung

### Häufige Probleme

1. **"Layer nicht gefunden"**: Stellen Sie sicher, dass alle erforderlichen Layer geladen sind
2. **"Keine Features gefunden"**: Überprüfen Sie, ob die Nutzungsschicht die erwarteten Nutzungsarten enthält
3. **"PDF-Export fehlgeschlagen"**: Überprüfen Sie die Schreibberechtigung für das Zielverzeichnis

### Debug-Informationen

Das Plugin gibt Debug-Informationen in der QGIS-Konsole aus:

- Feature-Anzahlen für jeden Verarbeitungsschritt
- Geometrie-Validierungsmeldungen
- Verarbeitungszeiten

## Entwicklung

### Plugin-Struktur

```
building_block_creator/
├── __init__.py                           # Plugin-Initialisierung
├── building_block_creator.py            # Haupt-Plugin-Klasse
├── creator_dialog.py                    # Dialog-Logik
├── building_block_creator_dialog_base.py # UI-Basis-Klasse
├── building_block_creator_dialog_base.ui # UI-Definition
├── building_block_creator_dialog_creator.ui # Creator-Dialog-UI
├── resources.py                         # Ressourcen
├── resources.qrc                        # Qt-Ressourcen
└── README.md                           # Diese Datei
```

### Code-Organisation

- **UI-Layer**: Dialog-Management und Benutzerinteraktion
- **Processing-Layer**: Geometrische Verarbeitungslogik
- **Export-Layer**: PDF-Export-Funktionalität

## Autoren

- **T. Lehmann** - Universität Münster (t.lehmann@uni-muenster.de)
- **T. Brand** - Universität Münster (t.brand@uni-muenster.de)

## Lizenz

Dieses Programm ist freie Software; Sie können es unter den Bedingungen der GNU General Public License, wie von der Free Software Foundation veröffentlicht, weitergeben und/oder modifizieren; entweder gemäß Version 2 der Lizenz oder (nach Ihrer Option) jeder späteren Version.

## Version

**Version**: 1.0  
**Erstellt**: 2025-08-21  
**Letztes Update**: 2025-08-31

## Support

Bei Fragen oder Problemen wenden Sie sich an:
- t.lehmann@uni-muenster.de
- t.brand@uni-muenster.de

## Changelog

### Version 1.0 (2025-08-31)
- Initiale Version
- 15-stufiger Verarbeitungsprozess implementiert
- PDF-Export-Funktionalität hinzugefügt
- Fortschrittsanzeige implementiert
- Automatische Layer-Filterung nach Nutzungsarten