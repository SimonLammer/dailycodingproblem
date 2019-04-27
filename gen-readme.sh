#!/bin/bash

file=README.md
tmp=$file.tmp

grep -A1 -n '| Number' $file\
  | tail -n 1\
  | cut -d- -f1\
  | xargs -I{} sh -c "head $file -n {}"\
  > $tmp
mv $tmp $file
for i in $(ls src | sort -nr); do
  printf "| $(echo $i | cut -d- -f1 | sed 's#^0*##') | [" >> $file
  f=$(ls src/$i/$(echo $i | cut -d- -f2).*)
  printf "$f" | sed -e 's!^.*/!! ; s!\..*$!! ; s!_! !g' >> $file
  printf "]($f) | " >> $file
  if [[ "$f" == *.py ]]; then
    # Python
    grep '# Difficulty: ' $f | sed 's!# Difficulty: !!' | tr -d '\n' >> $file
    printf " | " >> $file
    grep '# Questioner: ' $f | sed 's!# Questioner: !!' | tr -d '\n' >> $file
    printf " | " >> $file
    awk "NR>$(
      grep -n '"""' $f\
        | cut -d: -f1\
        | head -n 2\
        | sed '1!s#^#\&\&NR<#'\
        | tr -d '\n')" $f\
      | sed 's#$#<br/>#'\
      | tr -d '\n'\
      >> $file
    echo " |" >> $file
  else
    >&2 echo "File of unknown type: $f"
  fi
done