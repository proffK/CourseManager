#!/usr/bin/python
# -*- coding: utf-8 -*- 
'''   
   Copyright 2015 OneRTeam (Edgar Kaziahmedov, Klim Kireev, Artem Yashuhin)

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''
import pygraphviz as pgv

import DataBase

'''
graph format:
	-->claster_ + courseId
		-->claster_ + courseId + in
		-->claster_ + courseId + out

node_format:
	skill.Name + str(course.Id) + 'in'
'''

def make_connections(graph, DATA_BASE, coursesId):
	edges = graph.edges()

	for connection in edges:
		outputSkills = graph.get_subgraph('cluster_' + connection[0]).get_subgraph('cluster_' + connection[0] + 'out').nodes()
		inputSkills = graph.get_subgraph('cluster_' + connection[1]).get_subgraph('cluster_' + connection[1] + 'in').nodes()

		unionSkills = []
		for skill in outputSkills:
			if skill.attr['label'] != '\\N':
				unionSkills.append(skill.attr['label'])

		for skill in inputSkills:
			if skill.attr['label'] != '\\N':
				unionSkills.append(skill.attr['label'])

		for label in unionSkills:
			if(unionSkills.count(label) > 1):
				graph.add_edge(label + connection[0] + 'out', label + connection[1] + 'in')

	graph.delete_nodes_from(coursesId)

def visual_path(graphWithoutSkills, DATA_BASE):
	graph = pgv.AGraph(graphWithoutSkills ,directed = 'true', style = 'filled')

	graph.node_attr['color']='grey'
	graph.node_attr['style']='filled'
	graph.graph_attr['label']='a graph'

	courseList = graph.nodes()

	for node in courseList:
		course = DATA_BASE.get_course(int(node))

		attributes = {}
		attributes.update(style ='filled, solid',
						color = 'lightgrey',
						label = course.Name,
						name = 'cluster_' + str(course.Id),
						shape = 'box')
		subgraph = graph.subgraph(nbunch = node, **attributes)
		
		attributes.update(name = 'cluster_' + str(course.Id) + 'in',
						label = u'Входные скиллы',
						color = 'grey')
		inSubgraph = subgraph.subgraph(nbunch = node, **attributes)

		attributes.update(name = 'cluster_' + str(course.Id) + 'out',
						label = u'Выходные скиллы',
						color = 'grey')
		outSubgraph = subgraph.subgraph(nbunch = node, **attributes)

		for skill in course.Skill_I:
			if(DATA_BASE.get_skill(skill) != -1):
				inSubgraph.add_node(DATA_BASE.get_skill(skill).Name + str(course.Id) + 'in',
								label = DATA_BASE.get_skill(skill).Name,
								color = 'yellow')

		if(len(inSubgraph.nodes()) <= 1):
			inSubgraph.add_node('No Knowlages' + str(course.Id) + 'in',
								label = 'No Knowledges',
								color = 'yellow')


		for skill in course.Skill_O:
			if(DATA_BASE.get_skill(skill) != -1):
				outSubgraph.add_node(DATA_BASE.get_skill(skill).Name + str(course.Id) + 'out',
								label = DATA_BASE.get_skill(skill).Name,
								color = 'red')

	make_connections(graph, DATA_BASE, courseList)

	graph.layout(prog='dot')

	graph.draw('picture.png')



	#graph.write()

	#courseList = graph.edges()#like [('1', '2'), ('3', '4')]