from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in whatsapp_chatbot/__init__.py
from whatsapp_chatbot import __version__ as version

setup(
	name="whatsapp_chatbot",
	version=version,
	description="WhatsApp API client that connects through the WhatsApp Web browser app",
	author="Accurate Systems",
	author_email="info@accuratesystems.com.sa",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
