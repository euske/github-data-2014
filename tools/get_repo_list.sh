#!/bin/sh

curl -H "Authorization: token `cat ~/.github_token`" \
    'https://api.github.com/search/repositories?q=language:c+stars:>100&per_page=100' > repos-c.json
curl -H "Authorization: token `cat ~/.github_token`" \
    'https://api.github.com/search/repositories?q=language:java+stars:>100&per_page=100' > repos-java.json
curl -H "Authorization: token `cat ~/.github_token`" \
    'https://api.github.com/search/repositories?q=language:python+stars:>100&per_page=100' > repos-python.json

python json2list.py repos-c.json > repos-c
python json2list.py repos-java.json > repos-java
python json2list.py repos-python.json > repos-python
