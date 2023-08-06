# TRASHTALK

[![Build Status](https://travis-ci.org/PTank/trashtalk.svg?branch=master)](https://travis-ci.org/PTank/trashtalk) 
[![Coverage Status](https://coveralls.io/repos/github/PTank/trashtalk/badge.svg?branch=master)](https://coveralls.io/github/PTank/trashtalk?branch=master) 

## concept

*script to simplify trash access*

## install

	pip install trashtalk
	# or
	git clone git@github.com:PTank/trashtalk.git
	cd trashtalk
	python setup.py install

### .trashtalk

You can add a .trahstalk in your home for add specific trash path or media path

	# this is a comment
	TRASH_PATH=/direct/path/to/Trash , "name of this trash"
	MEDIA_PATH=/path/to/media/
	# you can add multiple path

### example

	$ trashtalk -cl # clean trash from yout home
	$ trashtalk -f "file" -cl # clean only this file from trash
	$ trashtalk media_name -ls
	>>> file1 5M
	>>> file2 100.10M
	>>> file3 100M
	>>> total 205.10M
