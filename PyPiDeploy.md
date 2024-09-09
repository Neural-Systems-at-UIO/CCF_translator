to deploy the package to PyPi


```bash
pip install twine setuptools wheel
python setup.py sdist bdist_wheel
twine upload dist/*
```