#/bin/bash
pdflatex supp_mat.tex
bibtex supp_mat
pdflatex supp_mat.tex; pdflatex supp_mat.tex
pdfunite supp_mat.pdf all_qNML_images4.pdf all_sup_mat.pdf
