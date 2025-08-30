from qgis.core import *
from qgis.utils import iface
import processing

# Lade die Eingabedaten (Shape-Dateien)
gemeinde_layer = iface.addVectorLayer('/path/to/gemeinde.shp', 'Gemeinde', 'ogr')
gemarkung_layer = iface.addVectorLayer('/path/to/gemarkung.shp', 'Gemarkung', 'ogr')
nutzung_layer = iface.addVectorLayer('/path/to/nutzung.shp', 'Nutzung', 'ogr')

if not gemeinde_layer.isValid() or not gemarkung_layer.isValid() or not nutzung_layer.isValid():
    print("Eingabedaten sind ungültig")
else:
    # Schritt 1: Verschnitt der Schichten
    # Schnitt der Gemeinde mit der Gemarkung
    geschnitten_gemarkung_layer = processing.run('native:intersection', {
        'INPUT': gemeinde_layer,
        'OVERLAY': gemarkung_layer,
        'OUTPUT': 'memory:geschnitten_gemarkung'
    })['OUTPUT']

    # Schritt 2: Filtere Flurstücke nach benötigten Nutzarten
    needed_nutzung_values = ['Bahnverkehr', 'Begleitfläche Bahnverkehr', 'Fließgewässer', 
                             'Stehendes Gewässer', 'nicht ständig Wasser führend', 
                             'Straßenverkehr', 'Verkehrsbegleitfläche Straße', 'Weg']

    # Filtere nach der Attributspalte 'nutzung'
    expression = "nutzung IN ('" + "','".join(needed_nutzung_values) + "')"
    gefilterte_nutzung_layer = processing.run('native:extractbyexpression', {
        'INPUT': nutzung_layer,
        'EXPRESSION': expression,
        'OUTPUT': 'memory:gefilterte_nutzung'
    })['OUTPUT']

    # Schritt 3: Verschnitt der gefilterten Nutzung mit der geschnittenen Gemarkung
    geschnitten_nutzung_layer = processing.run('native:intersection', {
        'INPUT': geschnitten_gemarkung_layer,
        'OVERLAY': gefilterte_nutzung_layer,
        'OUTPUT': 'memory:geschnitten_nutzung'
    })['OUTPUT']

    # Schritt 4: Mittellinie für alle gewählten Polygone berechnen
    mittellinie_layer = processing.run('native:polygonstolines', {
        'INPUT': geschnitten_nutzung_layer,
        'OUTPUT': 'memory:mittellinien'
    })['OUTPUT']

    # Schritt 5: Linien in Segmente teilen
    segmentierte_linien_layer = processing.run('native:splitlines', {
        'INPUT': mittellinie_layer,
        'OUTPUT': 'memory:segmentierte_linien'
    })['OUTPUT']

    # Schritt 6: Alle Segmente um X verlängern
    verlängerte_segmente_layer = processing.run('native:extendlines', {
        'INPUT': segmentierte_linien_layer,
        'DISTANCE': 100,  # Beispielwert für die Verlängerung
        'OUTPUT': 'memory:verlaengerte_segmente'
    })['OUTPUT']

    # Schritt 7: Generalisieren (optional, abhängig von den Anforderungen)
    generalisierte_layer = processing.run('native:simplifygeometries', {
        'INPUT': verlängerte_segmente_layer,
        'TOLERANCE': 0.001,  # Beispielwert für die Generalisierung
        'OUTPUT': 'memory:generalisierte_layer'
    })['OUTPUT']

    # Schritt 8: Flächen aus Linien erstellen
    flaechen_layer = processing.run('native:linespolygon', {
        'INPUT': generalisierte_layer,
        'OUTPUT': 'memory:flaechen_layer'
    })['OUTPUT']

    # Schritt 9: Alle Flächen miteinander verschneiden
    verschneidete_flaechen_layer = processing.run('native:intersection', {
        'INPUT': flaechen_layer,
        'OVERLAY': gemarkung_layer,
        'OUTPUT': 'memory:verschneidete_flaechen'
    })['OUTPUT']

    # Schritt 10: Duplikate filtern (falls notwendig)
    duplikate_filt_layer = processing.run('native:dissolve', {
        'INPUT': verschneidete_flaechen_layer,
        'OUTPUT': 'memory:duplikate_filt_layer'
    })['OUTPUT']

    # Endergebnis: Baublöcke generieren
    iface.addVectorLayer(duplikate_filt_layer, 'Baublöcke', 'ogr')
