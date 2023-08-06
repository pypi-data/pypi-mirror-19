import urllib
import os
import tarfile


def download(name=None):
	if name == None:
		name = "openedoo"
	urllib.urlretrieve ("https://github.com/openedoo/openedoo/archive/master.tar.gz", "openedoo.tar.gz")

	tar = tarfile.open("openedoo.tar.gz")
	tar.extractall()
	tar.close()

	os.rename("openedoo-master", "openedoo")
	os.remove("openedoo.tar.gz")
	return file has installed

