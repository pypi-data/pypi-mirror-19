Update mobagel-python-sdk Through PYPI
======================================
* Update Package Version
	* In `/setup.py` modify **PACKAGE_VERSION**
```
PACKAGE_NAME = 'mobagel-python-sdk'
PACKAGE_VERSION = '$YOUR_NEW_VERSION_NUMBER'
PACKAGE_AUTHOR = 'MoBagel'
```


* Check if Distutils can recognize your `setup.py`. It'll display warnings if there's sth. wrong.
	* Open Terminal and `cd` to the package directory
![](http://i.imgur.com/7QhrQhs.png)
	* Enter `python setup.py check`
![](http://i.imgur.com/voliHab.png)
	Expected output: `running check`

* Make the package: `python setup.py sdist`
![](http://i.imgur.com/CY7StJN.png)

* Upload the package to PYPI
	* You Need an PYPI account. (Skip this step if you have one.)

	Register here:
	https://pypi.python.org/pypi?%3Aaction=register_form

	Contact to Mobagel and Join this SDK project in PYPI:
	E-mail: us@mobagel.com
	* Use this command in Terminal to upload: `
python setup.py register sdist upload`
![](http://i.imgur.com/AkEatjw.png)
![](http://i.imgur.com/cPLmvry.png)

* Check New Version on PYPI
https://pypi.python.org/pypi
![](http://i.imgur.com/MHeAomH.png)



