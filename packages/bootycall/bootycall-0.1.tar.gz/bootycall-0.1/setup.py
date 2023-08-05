from setuptools import setup

setup( \
    name = 'bootycall', \
    packages = ['bootycall'], \
    version = '0.1', \
    description = 'A shell nREPL client for boot nREPL and other nREPls.', \
    author = 'Christopher Auer', \
    author_email = 'high.on.bonsai@googlemail.com', \
    url = 'https://github.com/christo-auer/bootycall', \
    keywords = ['nrepl', 'clojure', 'boot', 'leiningen'], \
    classifiers = [], \
    entry_points = { 'console_scripts': [ 'bcall=bootycall.bcall:main' ]} 
)
