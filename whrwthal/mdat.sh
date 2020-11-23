#!/bin/sh
#
# Script to update the meta data:
#
# 1) Version number on a per-tag basis
# 2) Codebase size by line-count

version=$(git tag | tail -1)
sed -Ei "s/v[0-9]+.[0-9]+.[0-9]+/$version/" textile.py
sed -Ei "s/(version = )'.*'/\1'$version'/" textile.py

uilines=$(wc -l tkhandler.py | sed "s/handler.py/GUI Lines of Code/")
sed -Ei "s/(uilines = )'.*'/\1'$uilines'/" textile.py

lines=$(wc -l *py | sed "s/total/Total Lines of Code/" | grep -P -e "\d+(?= Total.Lines)" | sed "s/^ //")
sed -Ei "s/(totallines = )'.*'/\1'$lines'/" textile.py
