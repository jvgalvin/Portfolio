pandoc -s report.md -t pdf -o report.pdf --citeproc --bibliography=library.bib --csl=acm-sig-proceedings.csl --lua-filter=pagebreak.lua