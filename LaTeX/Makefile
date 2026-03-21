TEX = lualatex
MAIN = schulchronik
FLAGS = -interaction=nonstopmode

.PHONY: pdf clean

pdf:
	$(TEX) $(FLAGS) $(MAIN).tex
	$(TEX) $(FLAGS) $(MAIN).tex

clean:
	rm -f $(MAIN).{aux,log,out,toc,pdf,bbl,blg,synctex.gz}
	rm -f $(MAIN).{1,1R,end,enR}
