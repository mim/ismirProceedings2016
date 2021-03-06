#!/bin/bash -xue

rm -f 2016_Proceedings_ISMIR.{aux,ain,log,toc}
pdflatex 2016_Proceedings_ISMIR.tex

#ReplaceText.vbs 2016_Proceedings_ISMIR.aux "\IeC " ""
sed -e 's/\\IeC //g' 2016_Proceedings_ISMIR.aux > 2016_Proceedings_ISMIR_2.aux

authorindex -d 2016_Proceedings_ISMIR_2.aux

pdflatex 2016_Proceedings_ISMIR.tex
pdflatex 2016_Proceedings_ISMIR.tex

cp 2016_Proceedings_ISMIR.pdf ../2016_Proceedings_ISMIR_Electronic/
# cp 2016_Proceedings_ISMIR.pdf ../2016_Proceedings_ISMIR_Electronic_Tools/data/
