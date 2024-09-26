## MEWSMET_code
Code for experiments presented in "Opinions are Buildings: Metaphors in Secondary Education EFL Essays" (Hülsing and Horbach, 2024).

# Data
For obtaining the data, please fill in the form "Data License Agreement" (tba) and send it to huelsing@uni-hildesheim.de. You will receive the MEWSMET corpus (MEWSMET.txt), as well as the original files from the MEWS corpus that were used for annotation and a list containing the scores that expert raters attributed to each of the essays (both contained in a directory called MEWS, compare ["English writing skills of students in upper secondary education: Results from an empirical study in Switzerland and Germany" by Keller et al., 2020](https://www.sciencedirect.com/science/article/abs/pii/S1060374319303911)). 
In order to reproduce the experiments, the file MEWSMET.txt and the MEWS-directory have to be stored in the file [data](data).

# Annotation Study

Once the data has been stored, the analysis of our annotation data can be carried out. Pearson correlation between TLMs / CMs / all metaphors and the essay scores can be obtained by running `python corpus.py`.

# Metaphor Detection Experiments with DeepMet

The code that was used for metaphor detection was taken from the [DeepMet github repository](https://github.com/YU-NLPLab/DeepMet). In order to use DeepMet for our MEWS-data, the data has to be processed to conform to the requirements of DeepMet, i.e. the local context as well as POS-tags have to be added. The directory [use_deepmet](use_deepmet) contains the code for processing MEWSMET for DeepMet. 
