- Project Title
Assessment of Remotely-sensed Biophysical Observations and Retrieval (ARBOR)

- Description
Contained in this repository is the source code described in; ARBOR: A new framework for assessing the accuracy of individual tree crown delineation from remotely-sensed data. Published in Remote Sensing of Environment under: https://doi.org/10.1016/j.rse.2019.111256

In order to assess the accuracy of individual tree crown (ITC) delineation techniques the same tree needs to be identified in two different datasets, for example, ground reference (GR) data and crowns delineated from LiDAR. Many studies use arbitrary metrics or simple linear-distance thresholds to match trees in different datasets without quantifying the level of agreement. We have developed a new framework for objectively quantifying the agreement between GR and remotely-sensed tree datasets, using common biophysical properties of ITC delineated trees (location, height and crown area).The code for the ARBOR framework is applied to GR and 2 versions of remotely-sensed tree data from a woodland study site (with intended errors) to demonstrate how ARBOR can identify the optimum ITC delineation technique through quantifying an average match-pairing similarity index (AMPS), and a dataset size similarity index (DSS) between two types of remotely sensed data. 

- Getting Started
	git clone https://github.com/DrJMurray/ARBOR.git
	cd ARBOR
	python2.7 PYTHONFILE

- Prerequisites
Data: 
Delineation data in .CSV format, containing column data read in as; 'ID' 'X' 'Y' 'Height' 'Area'. 
#Note: See included csv's for example format. X and Y should be UTM coordinates, and all should be within the same UTM zone.

Python modules:
	-numpy
	-scipy.spatial
	-scipy.stats
	-scipy.optimize

#Note: On most systems you can install these by running pip install MODULE_NAME or pip2 install MODULE_NAME.

- Example
	Clone git and ensure completion of Prerequisites, load in "ARBOR_Framework.py"
	
	Navigate to:
	#now run with some examples
	trees1 = load_trees_from_CSV('ARBOR_TestData.csv') #Note: These filenames should be run for testing or changed for your own data files as required
	trees2 = load_trees_from_CSV('ARBOR_TestData1.csv')
	trees3 = load_trees_from_CSV('ARBOR_TestData2.csv')

	Run ARBOR_Framework.py

	Expected output: AMPS score (e.g. 82.32654548) & DSS score (e.g. 0.9293231)
	AMPS - Average Match Pairing Similarity index. The quantification of how well the delineations are matched.
	DSS - Dataset Size Similarity index. The quantification of how well the size of the datasets relate, following the matching of the delineations. 

- Authors (* = Corresponding Authors)
Jon Murray* - (DrJMurray) - Lancaster Environment Centre, School of Science and Technology, Lancaster University, UK.
David Gullick* - (davidsgullick) - Lancaster Environment Centre, School of Science and Technology, Lancaster University, UK.
George Alan Blackburn - Lancaster Environment Centre, School of Science and Technology, Lancaster University, UK.
James Duncan Whyatt - Lancaster Environment Centre, School of Science and Technology, Lancaster University, UK.
Christopher Edwards - InfoLab, School of Computing and Communication, Lancaster University, UK.

- License
This project is licensed under the GNU General Public License v3.0 - see the LICENSE.md file for further details. Permissions of this strong copyleft license are conditioned on making available complete source code of licensed works and modifications, which include larger works using a licensed work, under the same license. Copyright and license notices must be preserved. Contributors provide an express grant of patent rights.

- Acknowledgments
The authors would like to thank NERC ARF for their contribution to this research through the provision of facilities and resources for the capture of the remotely-sensed data of the study site. This research was supported by an EPSRC studentship for the lead author: EP/L504804/1.
