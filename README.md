# coronavirus
Visualize the coronavirus tweets and statistics of the world wide  

To see a demo of this visualization website, click on: https://gellban.github.io/coronavirus/

# import conda evironments
cd py/src  
conda env create -f ir.yml  
conda env create -f mlstmfcn.yml  


# To run the SVM:
cd py/src  
conda activate ir  
python svm.py  

# To run the Naive Bayes:
<!-- cd py/src -->  
conda activate ir  
python naive_bayes.py  

# to run deep learing:
conda deactivate  
<!-- cd py/src -->  
conda activate mlstmfcn  
python dl.py  