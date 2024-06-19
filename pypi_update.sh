# pip install wheel
python setup.py sdist bdist_wheel
twine upload dist/grimo-1.3.36*
git add . && git commit -m "Release v1.3.36" && git push && git tag v1.3.36 && git push --tags
