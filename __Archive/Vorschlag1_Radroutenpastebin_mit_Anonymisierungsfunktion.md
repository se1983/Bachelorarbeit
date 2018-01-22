---
title: Vorschlag I -- Radrouten-Pastebin mit Anonymisierungsfunktion
author: Sebastian Schmid - s0543196
---

# Themenvorschlag

Bereits heute gibt es eine Vielzahl an Webdiensten zum Anzeigen, Verwalten und
Veröffentlichen von selbst erstellten gpx-Tracks. Diese Ansammlungen von
Geokoordinaten, aufgenommen mit einem Mobiltelefon oder ähnlichem werden dort
hochgeladen und erlauben es, die eigenen sportlichen Aktivitäten hübsch dargestellt
auf Karten, zu präsentieren.
Doch all diese Dienste haben einen Makel. Meist handelt es sich dabei um
kommerzielle Webseiten. Diese erfordern zur Benutzung eine Anmeldung oder eine
Bezahlung. Dies entspricht aber weder dem Prinzip der freien Daten, wonach
gesammelte Daten, soweit möglich, frei zur Verfügung gestellt werden sollen, noch
dem Prinzip der Datensparsamkeit, wonach nur diejenigen Daten erhoben werden dürfen,
die zur Erbringung des Dienstes erforderlich sind.  

Diese Arbeit wird diese Lücke schließen  und einen Webdienst für das
Hochladen von gpx-Dateien nach dem Prinzip von Pastebins erarbeiten. Dieser Dienst
wird eine Möglichkeit der Anzeige der Kartografischen Daten, sowie die Anzeige
von Höhe und Geschwindigkeit besitzen. Außerdem wird eine Schnittstelle geschaffen,
die Daten auch in Maschinenlesbarer Form zur Verfügung zu stellen.

Da der Upload der Daten anonym erfolgt, ist eine Löschung, sowie die
Einschränkung der Zugriffe auf die Daten nicht vorgesehen. Da durch den Start-,
sowie Endpunkt der Bewegungsprofile sicherheitstechnische Problematiken in der
Form: "Dort wohnt ein Mensch mit einem schnellen Rennrad. Dort lohnt sich der Einbruch."
entstehen, wird in dieser Arbeit ein Algorithmus zur Verschleierung dieser
Punkte entwickelt werden.
