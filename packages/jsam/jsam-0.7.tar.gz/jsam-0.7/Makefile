all:	jsam/xparse.py
	python setup.py build

sdist:	jsam/xparse.py
	python setup.py sdist

install: jsam/xparse.py
	python setup.py install

jsam/xparse.py: jsam/xparse.g jsam/yapps2.py
	jsam/yapps2.py jsam/xparse.g

runtest:
	cd test; export PYTHONPATH=..; python filetest.py
	cd test; export PYTHONPATH=..; python collect.py

clean:
	python setup.py clean
	rm -f jsam/*.py[co] jsam/*~ jsam/#* *~ #*
	rm -rf build jsam.egg-info MANIFEST

