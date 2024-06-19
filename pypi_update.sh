# pip install wheel
python setup.py sdist bdist_wheel
twine upload dist/grimo-1.3.46*
git add . && git commit -m "Release v1.3.46" && git push && git tag v1.3.46 && git push --tags
