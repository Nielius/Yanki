cd "$(dirname "${BASH_SOURCE[0]}")"
. variables.sh


for file in *yanki.md; do
    yanki e -f html \
          -t "answer-clickable.html" \
          "${file}" "${file}.html"
done

