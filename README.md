# coronavirus
Visualize the coronavirus tweets and statistics of the world wide  

To see a demo of this visualization website, click on: https://gellban.github.io/coronavirus/

# import conda evironments
cd py/src  
conda env create -f ir.yml  
conda env create -f mlstmfcn.yml  

In case you encounter any issue of conda installation, you can use an alternative option via pip to install the Python libraries (‘worldcloud’ ,‘gensim’,‘keras’, and ‘tensorflow’. If you still need more libraries, please check ir.yml and mlstmfcn.yml to view the required version of a library.  

Using Conda or pip should allow you to run our SVM, Naïve Bayes, and DL models and get results. To run the programs for pip (not conda), you do not need the conda activate commands below.

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