# -*- coding: utf-8 -*-

"""
Script to generate the dynamic components of README.md

You probably don't need to run this, unless you have added a new paper and want it to show up there.
"""

import os
import re
from shutil import rmtree
from glob import iglob
import yaml


class Paper:

    def __init__(self, id, data):
        self.id = id
        self.title = None
        if 'title' in data:
            self.title = data['title']
        self.year = None
        if 'year' in data:
            self.year = str(data['year'])
        self.tags = []
        if 'tags' in data and len(data['tags']) > 0:
            self.tags = data['tags']
        self.authors = []
        if 'authors' in data and len(data['authors']) > 0:
            self.authors = data['authors']
        self.links = []
        if 'links' in data and len(data['links']) > 0:
            self.links = data['links']


# Build paper/tag lists
papers = []
tags = {}
for yaml_file in iglob('./papers/*.yaml'):
    with open(yaml_file, 'r') as f:
        try:
            paper = yaml.load(f)
            paper = Paper(os.path.basename(yaml_file[:-5]), paper)
            papers.append(paper)
            for tag in paper.tags:
                if tag not in tags:
                    tags[tag] = []
                tags[tag].append(paper)
        except yaml.YAMLError as e:
            print(e)

out_dir = './output'
if os.path.isdir(out_dir):
    rmtree(out_dir)
os.mkdir(out_dir)

# Create paper files
for paper in papers:
    paper_file = os.path.join(out_dir, '%s.md' % paper.id)
    print('Creating %s' % paper_file)
    paper_md = '\n# %s' % paper.title
    paper_md += '\n\n' + paper.year
    if len(paper.authors) > 0:
        paper_md += '\n\n' + ''.join(paper.authors)
    if len(paper.links) > 0:
        paper_md += '\n\n## Links\n\n'
        for link in paper.links:
            paper_md += '%s\n' % link
    with open(paper_file, 'w') as f:
        f.write(paper_md)

# Create tag files
for tag, papers in tags.items():
    tag_file = os.path.join(out_dir, '%s.md' % tag)
    print('Creating %s' % tag_file)
    tag_md = '# Papers for tag `%s`:' % tag
    for paper in papers:
        tag_md += '\n\n[%s](%s.md)' % (paper.title, paper.id)
    with open(tag_file, 'w') as f:
        f.write(tag_md)

# Add tag links to readme
print('Adding tag list to README.md')
tag_links = []
for tag in tags.keys():
    tag_links.append('[%s](%s/%s.md)' % (tag, out_dir[2:], tag))
# Place it in the README
tag_links = '<!--PAPERS-OUTPUT-->\n' + ', '.join(tag_links) + '\n<!--/PAPERS-OUTPUT-->'
with open('README.md', 'r') as f:
    readme = f.read()
readme = re.sub(r"(<!--PAPERS-OUTPUT-->[^\$]+<!--/PAPERS-OUTPUT-->)",
                tag_links,
                readme,
                re.M)
with open('README.md', 'w+') as f:
    f.write(readme)


print('\nDone')
