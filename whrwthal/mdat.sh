#!/bin/sh
#
# Script to update the meta data:
#
# 1) Version number on a per-tag basis
# 2) Codebase size by line-count

version=$(git tag | tail -1)
sed -Ei "s/v[0-9].[0-9].[0-9]/$version/" textile.py
sed -Ei "s/version = '.*'/version = '$version'/" textile.py

uilines=$(wc -l handler.py | sed "s/handler.py/GUI Lines of Code/")
sed -Ei "s/uilines = '.*'/uilines = '$uilines'/" textile.py

lines=$(wc -l *py | sed "s/total/Total Lines of Code/" | grep -P -e "\d+(?= Total.Lines)" | sed "s/^ //")
sed -Ei "s/totallines = '.*'/totallines = '$lines'/" textile.py
