
import setuptools

setuptools.setup(
	name="tailchart",
	description="A CLI utility for charting data on the web.",
	long_description="",
	version="0.0.1",
	url="https://github.com/usbuild/tailchart",
	author="Qichao Zhang",
	author_email="njuzhangqichao@gmail.com",
	entry_points={"console_scripts": ["tailchart=tailchart:run"]},
	packages=setuptools.find_packages(),
	license="MIT"
)
