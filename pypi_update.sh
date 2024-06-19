# pip install wheel
python setup.py sdist bdist_wheel
twine upload dist/gowl-0.0.1*
git add . && git commit -m "Release v0.0.1" && git push && git tag v0.0.1 && git push --tags
