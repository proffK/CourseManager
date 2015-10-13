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

from networkx import * 
from DataBase import *

class CoursesGraph(object):

    DB = 0 
    Graph = 0
    FakeBeginNode = 0
    FakeEndNodes = []

###############################################################################
 
    def __init__ (self, MainDB):
        
        self.Graph = nx.DiGraph()
        self.DB = MainDB
        self.Graph.add_nodes_from(MainDB.get_courses_id_list())
        self.Graph.add_weighted_edges_from(self.gen_base_edges())

###############################################################################

    def __repr__ (self):

        return self.Graph

###############################################################################
    
    def get_optimal_path(self, InSkills, OutSkills):
        
        self.Graph.add_node(self.FakeBeginNode)
        FakeBeginEdges = self.gen_out_node_edges(self.FakeBeginNode, InSkills)
        self.Graph.add_weighted_edges_from(FakeBeginEdges)

        self.FakeEndNodes = range(self.DB.CourseCID,\
                             self.DB.CourseCID + len(OutSkills))
        
        self.Graph.add_nodes_from(self.FakeEndNodes)

        PathesList = []

        for EndNode in self.FakeEndNodes:
            
            FakeEndEdges = self.gen_inp_node_edges(EndNode, [OutSkills[self.DB.CourseCID - EndNode]])
            self.Graph.add_weighted_edges_from(FakeEndEdges)

            NewPath = shortest_path(self.Graph, self.FakeBeginNode, EndNode)
            print NewPath
            PathesList.append(NewPath)
            

        return self.merge_pathes(PathesList)

###############################################################################
    
    def get_all_pathes(self, InSkills, OutSkills):
        pass

###############################################################################

    def gen_base_edges(self):

        NewEdgesList = []

        for Course in self.DB.get_courses_id_list():

            InpEdgesList = self.gen_inp_node_edges(Course,\
                                              self.DB.get_inp_skills_with_id(Course))
            #print InpEdgesList
            NewEdgesList.extend(InpEdgesList)

            OutEdgesList = self.gen_out_node_edges(Course,\
                                              self.DB.get_out_skills_with_id(Course))

            NewEdgesList.extend(OutEdgesList)

        return NewEdgesList
        
###############################################################################
   
    def gen_inp_node_edges(self, Node, SkillsList):
        
        NewEdgesList = []

        for Skill in SkillsList:

            CourseList = self.DB.find_courses_with_out_skill(Skill)

            for Course in CourseList:
                NewEdgesList.append((Course, Node, self.DB.get_time(Course)))
            
        
        return NewEdgesList

###############################################################################

    def gen_out_node_edges(self, Node, SkillsList):
        
        NewEdgesList = []

        for Skill in SkillsList:

            CourseList = self.DB.find_courses_with_inp_skill(Skill)
            #print CourseList

            for Course in CourseList:
                NewEdgesList.append((Node, Course, self.DB.get_time(Course)))
            
        return NewEdgesList

###############################################################################
    
    def merge_pathes(self, PathesList):

        OutPath = []
        #print PathesList

        for path in PathesList:

            if path == []:
                continue

            path.pop(0)
            path.pop(len(path) - 1)
            i = 0

            while i < len(path):

                if path[i] not in OutPath:

                    if i == 0:
                        OutPath.insert(0, path[i])
                    elif i == len(OutPath) - 1:
                        OutPath.append(path[i])
                    else: 
                        OutPath.insert(OutPath.index(path[i-1]) + 1, path[i])

                i += 1


        return OutPath

###############################################################################
