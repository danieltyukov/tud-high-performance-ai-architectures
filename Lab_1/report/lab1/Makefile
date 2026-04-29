# Tiny convenience Makefile for local builds. Overleaf doesn't need this.
# Targets:
#   make            -> build Lab1.pdf
#   make submit     -> rename PDF to the course-required convention
#   make clean      -> remove build artifacts
#   make distclean  -> also remove built PDFs

LAB     ?= 1
TEX      = Lab$(LAB).tex
PDF      = Lab$(LAB).pdf
NAME     = Daniel_Tyukov
NUMBER   = 5714699
SUBMIT   = Lab$(LAB)_$(NAME)_$(NUMBER).pdf

.PHONY: all submit clean distclean

all: $(PDF)

$(PDF): $(TEX) preamble.tex $(wildcard figures/*) $(wildcard code/*)
	pdflatex -interaction=nonstopmode -halt-on-error $(TEX)
	pdflatex -interaction=nonstopmode -halt-on-error $(TEX)

submit: $(PDF)
	cp $(PDF) $(SUBMIT)
	@echo "Ready to upload: $(SUBMIT)"

clean:
	rm -f *.aux *.log *.out *.toc *.lof *.lot *.fls *.fdb_latexmk *.synctex.gz *.bbl *.blg

distclean: clean
	rm -f Lab*.pdf
