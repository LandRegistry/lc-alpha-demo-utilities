import subprocess
import re
from elasticsearch import Elasticsearch
import os

elastic = Elasticsearch()

os.chdir('/vagrant/apps/acceptance-tests')
text = str(subprocess.check_output(['grep', '-nir', "^\\(When\\|Then\\|Given\\|And\\|Or\\)", '--include', '*.rb', '.']))
lines = text.split("\\n")


try:
    elastic.indices.delete(index='tests')
except:
    pass


for line in lines:
    match = re.search('^(.*\.rb):(\d+):.*\(\/(.*)\/\)', line)
    if match is not None:
        file = match.group(1)
        line = match.group(2)

        feature = match.group(3)
        feature = re.sub(r"\\.", "", feature)
        feature = re.sub("^(Given|When|Then|And|Or)\s+", "", feature)
        feature = re.sub("\^|\$", "", feature)
        data = {
            "filename": file,
            "line": line,
            "text": feature
        }
        print(data)
        res = elastic.index(index='tests', doc_type='step', body=data)
        print(res)

elastic.indices.refresh(index="tests")
