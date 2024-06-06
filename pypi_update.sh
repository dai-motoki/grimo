pip install wheel
python setup.py sdist bdist_wheel
twine upload dist/grimo-1.2.5*
git add . && git commit -m "Release v1.2.5" && git push && git tag v1.2.5 && git push --tags
