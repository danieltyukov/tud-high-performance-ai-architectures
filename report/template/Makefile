# Lab-agnostic Makefile. Auto-detects the LabN.tex file in this directory.
#
# Targets:
#   make            -> build LabN.pdf
#   make submit     -> rename PDF to LabN_Firstname_Lastname_StudentNumber.pdf
#   make watch      -> live rebuild (requires latexmk)
#   make clean      -> remove build artifacts
#   make distclean  -> also remove built PDFs

# Override these from the command line if a different student uses the template.
NAME    ?= Daniel_Tyukov
NUMBER  ?= 5714699

# Auto-detect the lab .tex file. Expects exactly one Lab*.tex (or Lab.tex).
TEX    := $(firstword $(wildcard Lab*.tex))
ifeq ($(TEX),)
$(error No Lab*.tex found in this directory)
endif
PDF    := $(TEX:.tex=.pdf)
LAB    := $(patsubst Lab%.tex,%,$(TEX))
SUBMIT := Lab$(LAB)_$(NAME)_$(NUMBER).pdf

.PHONY: all submit watch clean distclean

all: $(PDF)

$(PDF): $(TEX) preamble.tex $(wildcard figures/*) $(wildcard code/*)
	pdflatex -interaction=nonstopmode -halt-on-error $(TEX)
	pdflatex -interaction=nonstopmode -halt-on-error $(TEX)

submit: $(PDF)
	cp $(PDF) $(SUBMIT)
	@echo "Ready to upload: $(SUBMIT)"

watch:
	latexmk -pdf -pvc -interaction=nonstopmode $(TEX)

clean:
	rm -f *.aux *.log *.out *.toc *.lof *.lot *.fls *.fdb_latexmk *.synctex.gz *.bbl *.blg *.run.xml

distclean: clean
	rm -f Lab*.pdf
