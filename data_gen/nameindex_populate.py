import subprocess
from elasticsearch import Elasticsearch
import json
import requests

# This will load ES with a set of data suitable for demonstrating various searching approaches
# It does NOT generate representative data.

elastic = Elasticsearch()
try:
    elastic.indices.delete(index='index')
except:
    pass

# Create the filter
metaphone = {
    "settings": {
        "analysis": {
            "filter": {
                "dbl_metaphone": {
                    "type": "phonetic",
                    "encoder": "double_metaphone"
                }
            },
            "analyzer": {
                "dbl_metaphone": {
                    "tokenizer": "standard",
                    "filter": "dbl_metaphone"
                }
            }
        }
    }
}

# maps some fields...
mapping_surname = {
    "properties": {
        "surname": {
            "type": "string",
            "fields": {
                "phonetic": {
                    "type": "string",
                    "analyzer": "dbl_metaphone"
                }
            }
        },
        "forenames": {
            "type": "string",
            "fields": {
                "phonetic": {
                    "type": "string",
                    "analyzer": "dbl_metaphone"
                }
            }
        }
    }
}

resp = requests.put("http://localhost:9200/index", data=json.dumps(metaphone), headers={'Content-Type': 'application/json'})
print("Add filters: " + str(resp.status_code))
print(resp.text)

# Test the filter
resp = requests.post("http://localhost:9200/index/_analyze?analyzer=dbl_metaphone", data="Smith")
print("Execute Filter: " + str(resp.status_code))
print(resp.text)

resp = requests.put("http://localhost:9200/index/_mapping/names", data=json.dumps(mapping_surname), headers={'Content-Type': 'application/json'})
print("Add surname map: " + str(resp.status_code))
if resp.status_code != 200:
    print(resp.text)
    exit(1)

limit = 100
iteration_size = 10000

elastic_id = 1
for j in range(0, limit):
    print("Beginning a {}-iteration - {} of {}".format(iteration_size, j + 1, limit))
    names = json.loads(subprocess.check_output(['ruby', 'generate.rb', 'namelist', str(iteration_size)]).decode())
    print("   Names loaded")

    bulk = []
    for i in range(0, iteration_size):
        name = names.pop(0)

        operation = {
            "index": {
                "_index": "index",
                "_type": "names",
                "_id": str(elastic_id)
            }
        }
        elastic_id += 1

        data = {
            "title_number": "ZZ" + str(elastic_id),
            "forenames": " ".join(name["forenames"]),
            "surname": name["surname"],
            "full_name": " ".join(name["forenames"]) + " " + name["surname"],
            "office": "OFFICE HERE",
            "sub_register": "B",
            "name_type": "Private"
        }
        bulk.append(operation)
        bulk.append(data)
        #res = elastic.index(index='index', doc_type='names', body=data)
    print('   Bulk indexing')
    res = elastic.bulk(index='index', body=bulk)

    print("   Names indexed")

elastic.indices.refresh(index="index")

# Default ES storage is /var/lib/elasticsearch/elasticsearch/nodes
# 50,000 names is approx 27Mb (quick extrapolation: 30Gb for for the full index
# 1,000,000 names is 451236Kb (440Mb) - extrapolates to 22Gb for the full index