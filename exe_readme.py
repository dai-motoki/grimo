from grimo.core import Grimo

grimo = Grimo()
packages = grimo.search_packages(keyword='numpy', language='python', category='data-science', tag=['machine-learning'])
for package in packages:
    print(package)
