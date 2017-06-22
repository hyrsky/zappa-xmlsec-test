# xmlsec on AWS Lambda with Zappa

Testing xmlsec on AWS Lambda.

To try this out change the s3 bucket in [settings](./zappa_settings.json) to one that you own. Then run something like the following:

```
# For python python2
virtualenv venv --python=python2.7
source venv/bin/activate
pip install -r requirements.txt
pip uninstall -y lambda-packages
pip install git+https://github.com/hyrsky/lambda-packages.git
zappa deploy dev
```

```
# For python python3
virtualenv venv --python=python3.6
source venv/bin/activate
pip install -r requirements.txt
pip uninstall -y lambda-packages
pip install git+https://github.com/hyrsky/lambda-packages.git
zappa deploy dev
```
