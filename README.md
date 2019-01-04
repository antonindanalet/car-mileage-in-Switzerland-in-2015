# Distribution of the mileage of private cars in Switzerland in 2015
This code computes the distribution of mileage of private cars in Switzerland in 2015, based on the data of the Transport and Mobility Microcensus (MTMC, www.are.admin.ch/mtmc). As an example, 70% of private cars with the lowest mileage in the last 12 months travel 41% of the total mileage of private cars. This code generates a figure presenting the results and the results as a CSV-file containing the cumulative proportion of total mileage for each group of 10% of the vehicles (in increasing order of mileage).

The figure will be published on Twitter.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for reproducing the result and understanding how it has been generated. 

### Prerequisites

To run the code itself, you need python 3, pandas, numpy, matplotlib and seaborn.

For it to produce the results, you also need the raw data of the Transport and Mobility Microcensus 2015, not included on GitHub. These data are individual data and therefore not open. You can however get them by asking the Swiss Federal Statistical Office (FSO), after signing a data protection contract. Please ask mobilita2015@bfs.admin.ch, phone number 058 463 64 68. The cost of the data is available in the document "<a href="https://www.are.admin.ch/are/de/home/medien-und-publikationen/publikationen/grundlagen/mikrozensus-mobilitat-und-verkehr-2015-mogliche-zusatzauswertung.html">Mikrozensus Mobilität und Verkehr 2015: Mögliche Zusatzauswertungen</a>"/"<a href="https://www.are.admin.ch/are/fr/home/media-et-publications/publications/bases/mikrozensus-mobilitat-und-verkehr-2015-mogliche-zusatzauswertung.html">Microrecensement mobilité et transports 2015: Analyses supplémentaires possibles</a>".

### Run the code

Please copy the file <em>fahrzeuge.csv</em> that you receive from FSO in the folder "data". Then run <em>run_car_mileage_in_Switzerland_in_2015.py</em>. 

DO NOT commit or share in any way the CSV-files <em>fahrzeuge.csv</em>! These are personal data.

## Contact

Please don't hesitate to contact me if you have questions or comments about this code: antonin.danalet@are.admin.ch
