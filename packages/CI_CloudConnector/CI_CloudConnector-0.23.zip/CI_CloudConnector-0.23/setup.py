import os
from distutils.core import setup
# ============================    
def getVersion():
    ans = ''
    try:
        with open(os.path.join("CI_CloudConnector", 'VERSION')) as version_file:
            ans = version_file.read().strip()
    except Exception as inst:
        print "Error getting version" + str(inst)
        
    return ans

setup(name='CI_CloudConnector',
      version= getVersion(),
      py_modules=['CI_CloudConnector' , 'CI_LC_BL'],
	  packages=['CI_CloudConnector',],
	  package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['ci_cloudConnectorService', 'runCloudConnector.sh', 'SetupCloudConnector.sh', 'VERSION']
	  },
	  include_package_data = True,
	  description="IOT application that collect data from PLC (ModBus or AnB Ethernet/IP) and send to cloud using https",
	  author="Ido Peles",
	  author_email="idop@contel.co.il",
      install_requires=['pymodbus' , 'cpppo'],
	  url = "http://www.contel.co.il/en/",
	  long_description=open('README.txt').read(),
      )


	  
