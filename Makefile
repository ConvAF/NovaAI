PKG=chatbot
PWD=$(shell pwd)

default:
	make install_dev

clean:
	-rm -f *.o
	make pyclean

clean_all:
	make clean
	make pyclean

pyclean:
	-rm -f *.so
	-rm -rf *.egg-info*
	-rm -rf ./tmp/
	-rm -rf ./build/

install:
	pip install ${PWD}

install_dev:
	pip install -e ${PWD}

# To be implemented
test:
	# flask test
	# pytest --cov=${PKG} ${PKG}/tests/