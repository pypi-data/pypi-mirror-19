from setuptools import setup
from distutils.extension import Extension
#import extension
setup(
	name="rak_arth",
	version="1.5.4",
	description="it does arthimatical operations",
	long_description="it will peform add,sub,mul,",
	author="sripelli",
	author_email="sripelli.rakesh@gmail.com",
	maintainer="santoshi",
	maintainer_email="santhoshi.medasani@gmail.com",
	url="http://pypi.python.org/pypi/rak_arth/",
	download_url="http://pypi.python.org/pypi/rak_arth/Download",
	packages=["opt","opt.fun","fib"],
	py_modules=["opt/Addition","opt/subraction","opt/fun/func","fib/fibonacci"],
	ext_package='opt',
	#ext_modules=[Extension('opt.details',['opt/details.txt'])],
	classifiers=[
		  'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Environment :: Web Environment',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: Python Software Foundation License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Topic :: Communications :: Email',
          'Topic :: Office/Business',
          'Topic :: Software Development :: Bug Tracking'],
    	license="OSI Approved",
    	keywords=["rak","add","sub",'mul'],
    	#package_dir={"rak_arth.opt.fun":"home/rakesh/rak_arth/opt/"}
)
