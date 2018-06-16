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

in_dir = './input'
out_dir = './output'


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

    @property
    def author(self):
        authors = []
        for author in self.authors:
            authors.append(author.split(' ')[-1])
        if len(authors) > 1:
            return authors[0] + ' et al.'
        elif len(authors) == 1:
            return authors[0]
        else:
            return 'Unknown'


if os.path.isdir(out_dir):
    rmtree(out_dir)
os.mkdir(out_dir)

# Build paper/tag lists
papers = []
tags = {}
for yaml_file in iglob(os.path.join(in_dir, '*.yaml')):
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

# Create paper files
for paper in papers:
    paper_file = os.path.join(out_dir, '%s.md' % paper.id)
    print('Creating %s' % paper_file)
    paper_md = '# [Imbalanced Learning Papers](../README.md)\n## ↳ %s (%s, %s)' % (paper.title, paper.author, paper.year)
    if len(paper.authors) > 0:
        paper_md += '\n\n' + ', '.join(paper.authors)
    if len(paper.links) > 0:
        paper_md += '\n\n### Link(s)\n\n'
        for link in paper.links:
            paper_md += '%s\n' % link
    with open(paper_file, 'w') as f:
        f.write(paper_md)

# Create tag files
for tag, papers in tags.items():
    tag_file = os.path.join(out_dir, '%s.md' % tag)
    print('Creating %s' % tag_file)
    tag_md = '# [Imbalanced Learning Papers](../README.md)\n## ↳ Tag: `%s`' % tag
    for paper in papers:
        tag_md += '\n\n### [%s (%s, %s)](%s.md)\n\n' % (paper.title, paper.author, paper.year, paper.id)
        tag_md += ', '.join(paper.tags)
    with open(tag_file, 'w') as f:
        f.write(tag_md)

# Add tag links to readme
print('Adding tag list to README.md')
tag_links = []
for tag in sorted(list(tags.keys())):
    tag_links.append('### ↳ [%s](%s/%s.md)' % (tag, out_dir[2:], tag))
# Place it in the README
tag_links = '<!--PAPERS-OUTPUT-->\n' + '\n\n'.join(tag_links) + '\n<!--/PAPERS-OUTPUT-->'
with open('README.md', 'r') as f:
    readme = f.read()
readme = re.sub(r"(<!--PAPERS-OUTPUT-->[^\$]+<!--/PAPERS-OUTPUT-->)",
                tag_links,
                readme,
                re.M)
with open('README.md', 'w+') as f:
    f.write(readme)


print('\nDone')
