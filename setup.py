from distutils.core import setup
import py2exe,sys

sys.argv.append('py2exe')

options = {"py2exe":{
	"compressed":1,
	"optimize":2,
	"bundle_files":1,
	"excludes":["readline","Queue","_abcoll","backports","netbios","win32wnet"],
}}
	# "includes":["selenium"],

setup(
	data_files=[("",[('C:\Python34\Lib\site-packages\selenium\webdriver\\remote\getAttribute.js'),('C:\Python34\Lib\site-packages\selenium\webdriver\\remote\isDisplayed.js')])],
	console=[{"script": "test_erp.py"}],
    options=options,
    zipfile=None
)