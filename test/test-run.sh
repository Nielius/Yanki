#!/bin/bash

cd "$(dirname "$0")" # makes sure this script is running in the right directory

main="../bin/main.py"

case "$1" in
    "pdf")
        python3 ${main} -i ../questionsets/etale-fundamental-groups-md.yaml -o test-output/testrun-output.tex -t ../templates/latex-template.tex
        pdflatex -interaction=batchmode testrun-output.tex
        okular test-output/testrun-output.pdf
        ;;
    "html")
        python3 ${main} -i ../questionsets/etale-fundamental-groups-md.yaml -o test-output/testrun-output.html -t ../templates/answer-template.html
        firefox test-output/testrun-output.html
        ;;
    "html-new")
        python3 ${main} -i ../questionsets/etale-fundamental-groups-md.yaml -o test-output/testrun-new-output.html -t ../templates/answer-clickable.html
        firefox test-output/testrun-new-output.html
        ;;
    "html-new-noconvert")
        python3 ${main} -i ../questionsets/etale-fundamental-groups-html.yaml -o test-output/testrun-new-output.html -t ../templates/answer-clickable.html --noconvert
        firefox test-output/testrun-new-output.html
        ;;
    "anki")
        python3 ${main} -i ../questionsets/etale-fundamental-groups-md.yaml --anki
        ;;
    *)
        echo "Specifiy 'html' or 'pdf'."
        ;;
esac
