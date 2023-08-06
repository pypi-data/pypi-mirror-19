all: install test

install:
	sage -pip install --upgrade --no-index -v .

test:
	sage -tp --force-lib pysemigroup/*py 

coverage:
	sage -coverage pysemigroup/*

dist: 
	sage -python setup.py sdist

register: dist
	VERSION=`cat VERSION`; sage -sh -c "twine register dist/pysemigroup-$$VERSION.tar.gz"

upload: dist
	VERSION=`cat VERSION`; sage -sh -c "twine upload dist/pysemigroup-$$VERSION.tar.gz"

