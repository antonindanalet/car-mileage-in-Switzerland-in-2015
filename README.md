# Distribution of the mileage of private cars in Switzerland in 2015
This code computes the distribution of mileage of private cars in Switzerland in 2015, based on the data of the Transport and Mobility Microcensus (MTMC, www.are.admin.ch/mtmc). As an example, 70% of private cars with the lowest mileage in the last 12 months travel 42% of the total mileage of private cars. This code generates a figure (available in French, German and English) presenting the results and the results as a CSV-file containing the cumulative proportion of total mileage for each group of 10% of the vehicles (in increasing order of mileage).

The sample basis is similar to the one used in figure G 3.3.2.3 in the main report of the MTMC (p.31, <a href="https://www.are.admin.ch/dam/are/fr/dokumente/verkehr/dokumente/mikrozensus/verkehrsverhalten-der-bevolkerung-ergebnisse-des-mikrozensus-mobilitat-und-verkehr-2015.pdf.download.pdf/Mikrozensus_Verkehrsverhalten%20der%20Bev%C3%B6lkerung%202015_fr.pdf">in French</a> and <a href="https://www.are.admin.ch/dam/are/de/dokumente/verkehr/dokumente/mikrozensus/verkehrsverhalten-der-bevolkerung-ergebnisse-des-mikrozensus-mobilitat-und-verkehr-2015.pdf.download.pdf/Mikrozensus_Verkehrsverhalten%20der%20Bev%C3%B6lkerung%202015_de.pdf">in German</a>). It is slightly higher here than in the main report, because we don't decompose the mileage between "in Switzerland" and "abroad". Consequently, we don't remove observations without this information.

The figure has been published on Mastodon in <a href="https://datasci.social/@AntoninDanalet/111692099748158615">French</a>, <a href="https://datasci.social/@AntoninDanalet/111692113882442363">German</a> and <a href="https://datasci.social/@AntoninDanalet/111692123716349187">English</a> and <a href="https://www.linkedin.com/feed/update/urn:li:activity:6489459673538846720/">on Linkedin in English</a>.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for reproducing the result and understanding how it has been generated. 

### Prerequisites

To run the code itself, you need python 3, pandas, numpy, matplotlib and seaborn.

For it to produce the results, you also need the raw data of the Transport and Mobility Microcensus 2015, not included on GitHub. These data are individual data and therefore not open. You can however get them by filling in this form in <a href="https://www.are.admin.ch/are/de/home/verkehr-und-infrastruktur/grundlagen-und-daten/mzmv/datenzugang.html">German</a>, <a href="https://www.are.admin.ch/are/fr/home/mobilite/bases-et-donnees/mrmt/accesauxdonnees.html">French</a> or <a href="https://www.are.admin.ch/are/it/home/mobilita/basi-e-dati/mcmt/accessoaidati.html">Italian</a>. The cost of the data is available in the document "<a href="https://www.are.admin.ch/are/de/home/medien-und-publikationen/publikationen/grundlagen/mikrozensus-mobilitat-und-verkehr-2015-mogliche-zusatzauswertung.html">Mikrozensus Mobilität und Verkehr 2015: Mögliche Zusatzauswertungen</a>"/"<a href="https://www.are.admin.ch/are/fr/home/media-et-publications/publications/bases/mikrozensus-mobilitat-und-verkehr-2015-mogliche-zusatzauswertung.html">Microrecensement mobilité et transports 2015: Analyses supplémentaires possibles</a>".

### Run the code

Please copy the file <em>fahrzeuge.csv</em> that you receive from the Federal Statistical Office in the folder "<a href="https://github.com/antonindanalet/car-mileage-in-Switzerland-in-2015/tree/master/data/input">data/input</a>". Then run <em><a href="https://github.com/antonindanalet/car-mileage-in-Switzerland-in-2015/blob/master/src/run_car_mileage_in_Switzerland_in_2015.py">run_car_mileage_in_Switzerland_in_2015.py</a></em>. 

DO NOT commit or share in any way the CSV-file <em>fahrzeuge.csv</em>! These are personal data.
