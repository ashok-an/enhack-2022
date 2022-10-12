#!/bin/bash -x

seed_bugs.py -c 20

http localhost:12345/
http localhost:12345/bugs
http localhost:12345/bugs/all

http localhost:23456/
http localhost:23456/notes
http localhost:23456/notes/all
for i in $(seq 10000 10025); do
  http "localhost:23456/notes/CSC${i}"
done
