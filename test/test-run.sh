#!/bin/bash

# For pdf:

case "$1" in
    "pdf")
        python3 new-md.py -i ../tests/etale-fundamental-groups-md.yaml -o testrun-output.tex -t latex-template.tex
        pdflatex -interaction=batchmode testrun-output.tex
        okular testrun-output.pdf
        ;;
    "html")
        python3 new-md.py -i ../tests/etale-fundamental-groups-md.yaml -o testrun-output.html -t answer-template.html
        firefox testrun-output.html
        ;;
    "html-new")
        python3 new-md.py -i ../tests/etale-fundamental-groups-md.yaml -o testrun-new-output.html -t answer-clickable.html
        firefox testrun-new-output.html
        ;;
    "html-new-noconvert")
        python3 new-md.py -i ../tests/etale-fundamental-groups-html.yaml -o testrun-new-output.html -t answer-clickable.html --noconvert
        firefox testrun-new-output.html
        ;;
    *)
        echo "Specifiy 'html' or 'pdf'."
        ;;
esac


