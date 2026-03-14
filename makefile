default:
	git submodule update --init
	$(MAKE) -C crazyflie-clients-python

