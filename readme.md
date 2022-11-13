# Opendata Hackathon St. Gallen
[DevPost](https://opendatahack-stgallen.devpost.com/)

![Example](./docs/example_few_data.png)
_Erstellt am 12.11.2022 auf basis der Daten im Ordner `data`_

# Flat Finder
Die Stadt St. Gallen hat in ihrer Wohnraum-Strategie festgelegt, dass es wichtig ist auch in Zukunft genügend günstigen Wohnraum in der Stadt zu haben.
Es wurde festgestellt, dass günstiger Wohnraum in der Stadt vorhanden ist. Jedoch weiss man nicht genau, wo es günstigen Wohnraum hat und in welchem Zustand er ist.
Um die Frage, wo sich günstiger Wohnraum befindet zu beantworten, vergleichen wir Immobilien auf Websites wie ImmoScout24. Wir nehmen dazu Daten wie den Preis, die Fläche,
die Lage etc. und berechnen so für jede Wohnung einen Score von 1 bis 10. Je nach Wichtigkeit der Faktoren werden sie verschieden gewichtet.
Um den Zustand des Wohnraumes zu bestimmen, gehen wir ähnlich vor. Wir berechnen einen Score, welcher von Faktoren wie der Zeit der letzten Renovation, dem Baujahr etc. 
abhängt. In einem nächsten Schritt könnte man auch die Bilder der Wohnungen nutzen. Man kann mit Deep Learning ein Algorithmus trainieren, welcher auf Grund der Bilder auf 
den Zustand der Wohnung schliessen kann. Die Idee ist, mit der Zeit eine Datenbank aufzubauen, welche das Preislevel des Wohnraums, geografisch aufgelöst und den 
Zustand der Wohnungen enthält.

## Umsetzung
Als Proof of Concept haben wir mit einem Skript die nötigen Daten von comparis geholt. Dann haben wir mit einem Python Skript die Daten aus den HTML-Files ausgelesen und 
in einem CVS-File aufbereitet. Mit einem weiteren Skript rechnen wir den Score der Wohnungen anhand von den folgenden 3 Unterkategorien aus:
- **‘cheapness’** gibt an, wie günstig die Wohnung basierend auf dem aktuellen Mietpreis und der Anzahl Zimmer der Wohnung ist.
- **‘condition’** gibt an, in welchem Zustand sich die Wohnung befindet. Sie basiert auf dem Baujahr und falls gegeben, auf dem Rennovationsjahr.
- **‘location’** gibt an, wie gut die Lage der Wohnung ist und basiert auf folgenden Faktoren:
Strassendistanz zum nächsten Kindergarten, Strassendistanz zur nächsten Primarschule, Strassendistanz zur nächsten Sekundarschule, Strassendistanz zum nächsten Supermarkt, 
Strassendistanz zum Hauptbahnhof, Lärmemissionen des Strassenverkehrs

Die einzelnen Faktoren der Unterkategorien werden unterschiedlich gewichtet, welche durch das Anpassen der Parameter zu jederzeit optimiert werden können. Als Output 
erhalten wir für jeden Entscheidungsfaktor einen Score von 1 bis 10. Der ‘Hauptscore’ wird aus der ‘cheapness’, der ‘location’ und der ‘condition’ durch verschiedene 
Gewichtungen berechnet. Er beinhaltet also alle Entscheidungs-Faktoren. Die Visualisierung erfolgt mit ‘public.tableau’. Jede Wohnung wird als farbiger Kreis auf 
der Karte dargestellt. Die Farbe gibt den ‘cheapness’-Faktor wieder. Die Grösse der Kreise repräsentieren den ‘condition’-Faktor. Den ‘location’-Faktor sieht man beim Anklicken eines Punktes. Den ‘score’ sieht man unter den Kreisen als Zahl von 1 bis 10. 

## Schwierigkeiten
Leider sind wir in dieser kurzen Zeit nicht an genügend Daten gekommen. Deshalb haben wir mit wenigen Daten einen Prototyp erstellt. 

## Nächste Schritte
Man kann ein Skript implementieren, welches periodisch die aktuellen Wohnungsdaten abfragt. Dabei sollen die alten Daten behalten werden oder gegebenenfalls
aktualisiert werden. So kann mit der Zeit eine grössere Datenbank aufgebaut werden. Da die Bestimmung des Zustandes einer Wohnung noch nicht sehr aussagekräftig 
ist, sollte man sie erweitern. Dazu kann man, wie oben erwähnt die Bilder der Wohnungen mit Hilfe einer AI klassifizieren. Dies sollte eine bessere Zustandsermittlung ermöglichen.

# Mitwirkende
Dieses Projekt wurde im Rahmen des Hackathon der Opendata St. Gallen 2022 umgesetzt. Folgende Personen haben zum Erfolg beigetragen:
<table style="border-collapse: collapse; width: 100%;" border="1">
<tbody>
<tr>
<td style="width: 12.5%;"><a href="https://github.com/selblo"><img src="https://avatars.githubusercontent.com/u/98223614?v=4" height="50px" /></br>Selblo</a></td>
<td style="width: 12.5%;"><a href="https://github.com/RobinEberle"><img src="https://avatars.githubusercontent.com/u/108194564?v=4" height="50px" /></br>RobinEberle</a></td>
<td style="width: 12.5%;"><a href="https://github.com/waleedmadi"><img src="https://avatars.githubusercontent.com/u/118048083?v=4" height="50px" /></br>waleedmadi</a></td>
<td style="width: 12.5%;"><a href="https://github.com/phlehnert"><img src="https://avatars.githubusercontent.com/u/118047993?v=4" height="50px" /></br>phlehnert</a></td>
<td style="width: 12.5%;"><a href="https://github.com/SilvanAmmann"><img src="https://avatars.githubusercontent.com/u/94677070?v=4" height="50px" /></br>SilvanAmmann</a></td>
<td style="width: 12.5%;"><a href="https://github.com/selblo"><img src="https://avatars.githubusercontent.com/u/98223614?v=4" height="50px" /></br>Selblo</a></td>
<td style="width: 12.5%;"><a href="https://github.com/sanore"><img src="https://avatars.githubusercontent.com/u/4846634?v=4" height="50px" /></br>sanore</a></td>
<td style="width: 12.5%;"><img src="https://www.orthopaediezentrum-am-venet-haus.de/wp-content/uploads/2019/06/foto-unbekannt.jpg" height="50px" /></br>David</td>
</tr>
</tbody>
</table>
