# -*- coding: utf-8 -*-

"""
Script to generate the HTML for the one-page.
"""

import os
import re
from shutil import rmtree
from glob import iglob
import yaml

in_dir = './papers'


class Paper:

    def __init__(self, id, data):
        self.id = id
        self.title = None
        if 'title' in data:
            self.title = data['title']
        self.year = None
        if 'year' in data:
            self.year = str(data['year'])
        self.summary = None
        if 'summary' in data:
            summary = str(data['summary'])
            summary = summary.split('\n')
            for i, line in enumerate(summary):
                summary[i] = '  ' + summary[i]
            summary = '\n'.join(summary)
            self.summary = summary
        self._tags = []
        if 'tags' in data and len(data['tags']) > 0:
            self._tags = data['tags']
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

    @property
    def tags(self):
        tags = self._tags[:]
        if self.summary is not None:
            tags.append('has-summary')
        return tags


papers = []
for yaml_file in iglob(os.path.join(in_dir, '*.yaml')):
    with open(yaml_file, 'r') as f:
        try:
            papers.append(Paper(os.path.basename(yaml_file[:-5]), yaml.load(f)))
        except yaml.YAMLError as e:
            print(e)
papers.sort(key=lambda p: p.year)

# Table rows
table = [['Paper', 'Tags']]
for paper in papers:

    title = '%s (%s, %s)' % (paper.title, paper.author, paper.year)
    summary = ''
    if paper.summary is not None:
        summary = paper.summary.replace('"', '&quot;')
        
    if len(paper.links) > 0:
        title = '<a target="_blank" href="%s"title="%s">%s</a>' % (paper.links[0], summary, title)
    else:
        title = '<span title="%s">%s</span>' % (summary, title)
	
    tags = []
    for tag in paper.tags:
        tags.append('<a class="tag">%s</a>' % (tag))
    tags = ' '.join(tags)

    table.append([title, tags, summary])

def generate_html_table(table):

    table_html = ''

    # # Table header
    # table_html = '\t<thead>\n\t\t<tr>\n'
    # for th in table[0]:
    #     table_html += '\t\t\t<th>%s</th>\n' % str(th)
    # table_html += '\t\t</tr>\n\t</thead>\n'

    # Table body
    table_html += '\t<tbody id="paper-list">\n'
    for row in table[1:]:
        table_html += '\t\t<tr>\n'
        for td in row:
            table_html += '\t\t\t<td>%s</td>\n' % str(td)
        table_html += '\t\t</tr>\n'
    table_html += '\t</tbody>\n'

    return table_html


table_html = '<!--PAPERS-TABLE-->\n' + generate_html_table(table) + '\n<!--/PAPERS-TABLE-->'
with open('index.html', 'r') as f:
    readme = f.read()
readme = re.sub(r"(<!--PAPERS-TABLE-->[^\$]+<!--/PAPERS-TABLE-->)",
                table_html,
                readme,
                re.M)
with open('index.html', 'w+') as f:
    f.write(readme)


print('\nDone')
