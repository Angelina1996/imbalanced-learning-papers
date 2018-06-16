# -*- coding: utf-8 -*-

"""
Script to generate the dynamic components of README.md

You probably don't need to run this, unless you have added a new paper and want it to show up there.
"""

import re
from glob import iglob
import yaml


# Build paper/tag lists
papers = []
tags = []
for yaml_file in iglob('./papers/*.yaml'):
    print(yaml_file)
    with open(yaml_file, 'r') as f:
        try:
            paper = yaml.load(f)
            papers.append(paper)
            for tag in paper['tags']:
                if tag not in tags:
                    tags.append(tag)
        except yaml.YAMLError as e:
            print(e)

# Generate output
output = 'Tags (use CTRL-F to find in page): '
for tag in tags:
    output += '`%s` ' % tag
for paper in papers:
    output += '\n\n\n### %s' % paper['title']
    # Tags
    if 'tags' in paper and len(paper['tags']) > 0:
        output += '\n\nTag(s): '
        for tag in paper['tags']:
            output += '`%s` ' % tag
    # Links
    if 'links' in paper and len(paper['links']) > 0:
        output += '\n\nLink(s): '
        for i, link in enumerate(paper['links']):
            output += '[%s](%s)' % (i + 1, link)
    # summary = ''
    # if 'summary' in paper:
    #     summary = 'summary'


# Place it in the README
output = '<!--PAPERS-OUTPUT-->\n' + output + '\n<!--/PAPERS-OUTPUT-->'
with open('README.md', 'r') as f:
    readme = f.read()
readme = re.sub(r"(<!--PAPERS-OUTPUT-->[^\$]+<!--/PAPERS-OUTPUT-->)",
                output,
                readme,
                re.M)
with open('README.md', 'w+') as f:
    f.write(readme)

print('Done')
