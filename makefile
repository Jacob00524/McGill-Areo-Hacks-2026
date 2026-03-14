default:
	python3 -m venv path/to/venv
	source ./env/bin/activate
	git submodule update --init
	$(MAKE) -C crazyflie-clients-python

