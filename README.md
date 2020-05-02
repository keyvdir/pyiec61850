# pyiec61850
Server and Client of PyIEC61850 based on mz-automation

# A.	Requirements
a.	Python 2.7 or higher

b.	CMake 3.7.2 or higher
1. wget https://cmake.org/files/v3.7/cmake-3.7.2.tar.gz
2. tar zxvf cmake-3.7.2.tar.gz
3. cd cmake-3.7.2
4. ./bootstrap && make
5. sudo make install

c.	SWIG 4.0.0 or higher
1. wget http://prdownloads.sourceforge.net/swig/swig-4.0.0.tar.gz
2. tar xzf swig-4.0.0.tar.gz
3. cd swig-4.0.0
4. ./configure
5. make
6. sudo make install

# B.	Installation
1.	cd ~
2.	sudo apt update && upgrade
3.	git clone https://github.com/keyvdir/pyiec61850.git
4.	cd pyiec61850
5.	git clone https://github.com/mz-automation/libiec61850.git
6.	wget https://tls.mbed.org/download/mbedtls-2.16.0-apache.tgz
7.	tar zxvf mbedtls-2.16.0-apache.tgz
8.	mv mbedtls-2.16.0 libiec61850/third_party/mbedtls/mbedtls-2.16
9.	cd libiec61850
10.	cmake -DBUILD_PYTHON_BINDINGS=ON -DPYTHON_EXECUTABLE=/usr/bin/python3 .
11.	make WITH_MBEDTLS=1
12.	cd ..
13.	python3 server.py and python3 client.py (different terminal window)

![Server example](server.PNG)
![Client example](client.PNG)

# C.	IEC 61850 Information Model
![IEC 61850 Information Model](data.png)

# D.	Write and Read Data
Data type for write, read, and other complete functions can be found in “libiec61850/pyiec61850/iec61850.py”. Please refer to the original website of IEC61850 for further information of the data types. https://libiec61850.com/api/modules.html
