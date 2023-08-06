#!/bin/bash

set -e
echo 'Installing python dependencies'

# http://stackoverflow.com/a/27776822
case "$(uname -s)" in

   Darwin)
	 # upgrade pip
	 python -m pip install --upgrade pip

	 pip install --user numpy scipy matplotlib
	 pip install --user pyfits
	 pip install --user --no-deps astropy
     ;;

   Linux)
	 # upgrade pip
	 python -m pip install --upgrade pip
	 
	 # numpy, scipy
	 sudo apt-get install gfortran libatlas-base-dev
	 pip install --user numpy scipy

	 # matplotlib
	 sudo apt-get install libpng12-dev libfreetype6-dev libxft-dev
	 pip install --user matplotlib

	 # astropy
	 pip install --user --no-deps astropy

	 # pyfits
	 sudo apt-get install python-tk
	 pip install --user pyfits
     ;;

   CYGWIN*|MINGW32*|MSYS*)
     echo 'ERROR Windows is not supported.'
     exit 1
     ;;

   # Add here more strings to compare
   # See correspondence table at the bottom of this answer

   *)
     echo 'other OS'
     echo 'ERROR Only Linux and Mac OS X are supported.'
     exit 1
     ;;
esac

pip install --user jsonschema


