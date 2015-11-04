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
from bitarray import *
import matplotlib.pyplot as plt


MAX_INT = 65536

class CoursesGraph(object):

    DB = 0 
    Graph = 0
    FakeBeginNode = 0
    FakeEndNode = 0 
    debug_i = 0    # number of check operation
    debug_m = 0    # number of missed check operation

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

        OldGraph = self.Graph
        self.Graph.add_node(self.FakeBeginNode)
        FakeBeginEdges = self.gen_out_node_edges(self.FakeBeginNode, InSkills)
        self.Graph.add_weighted_edges_from(FakeBeginEdges)

        self.FakeEndNode =  self.DB.CourseCID
        
        self.Graph.add_nodes_from([self.FakeEndNode])

        PathesList = []

        FakeEndEdges = self.gen_inp_node_edges(self.FakeEndNode, OutSkills)
        self.Graph.add_weighted_edges_from(FakeEndEdges)

        #print InSkills, OutSkills

        answer = topological_sort(self.Graph)
        answer = answer[answer.index(0) + 1:answer.index(self.FakeEndNode)]    

        #print answer, self.check_path(answer, InSkills, OutSkills)

        barr = bitarray(2**len(answer))
        barr.setall(False)

        opt_path = self.recurse_search(answer, answer, InSkills, OutSkills, barr)

        self.Graph.remove_node(self.FakeBeginNode)
        self.Graph.remove_node(self.FakeEndNode)

        #print '^ ', self.debug_i, self.debug_m, ' ^'

        return index2path(opt_path[1], answer)

###############################################################################

    def gen_base_edges(self):

        NewEdgesList = []

        for Course in self.DB.get_courses_id_list():

            InpEdgesList = self.gen_inp_node_edges(Course,\
                                              self.DB.get_inp_skills_with_id(Course))
            #print InpEdgesList
            NewEdgesList.extend(InpEdgesList)

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
    
    def check_path(self, Path, InSkills, OutSkills):

        cur_skills = set(InSkills)
        needed_skills = set(OutSkills)

        for course in Path:

            passed = 1

            temp_lst = self.DB.get_inp_skills_with_id(course)
            #print '!', temp_lst

            for skill in temp_lst:

                if skill not in cur_skills:

                    passed = 0

            #print '!!', course, self.DB.get_out_skills_with_id(course)
            if passed == 1:

                cur_skills = cur_skills.union(set(self.DB.get_out_skills_with_id(course)))
                needed_skills = needed_skills.difference(cur_skills)

            #print '>', cur_skills
            #print '<', needed_skills

            if len(needed_skills) == 0:

                return self.get_sum_time(Path)

        return MAX_INT

################################################################################

    def recurse_search(self, CurPath, Path, InSkills, OutSkills, BitArray):

        num = gen_barr_index(CurPath, Path)
        #print '@', num
        #print '@@', CurPath

        if BitArray[num] == True:

            #print '@@@ exist'
            self.debug_m += 1
            return MAX_INT, num

        if CurPath == []:

            return MAX_INT, num
        
        self.debug_i = self.debug_i + 1
        time = self.check_path(CurPath, InSkills, OutSkills)
        #print '@@@', time, CurPath

        BitArray[num] = True

        if time == MAX_INT:

            set_barr(num, BitArray)
            #BitArray[num] = True
            #print '!!!!', index2path(num, Path)

            return MAX_INT, num

        result = [(time, num)]
        #print '!', result

        for course in CurPath:

            new_lst = []

            new_lst += CurPath

            new_lst.remove(course)
            
            #print '$#', num, new_lst, CurPath
            result.append(self.recurse_search(new_lst, Path, InSkills, OutSkills, BitArray))
            #print '$$', num, new_lst, result


        opt_path = (MAX_INT, 0)

        for x, y in result:

            if x < opt_path[0]:

                opt_path = x, y

        return opt_path

################################################################################

    def get_sum_time(self,Path):
    
        result = 0
    
        for course in Path:
    
            result += self.DB.get_time(course)
    
        return result

################################################################################

    def check_cycles(self):

        return find_cycle(self.Graph, orientation="original")

################################################################################

    def visualization(self):

        pos=nx.shell_layout(self.Graph) # positions for all nodes
        
        # nodes
        nx.draw_networkx_nodes(self.Graph,pos,node_size=700)
        
        # edges
        nx.draw_networkx_edges(self.Graph,pos,
                                    width=6,alpha=0.5,edge_color='b',style='dashed')
        
        # labels
        nx.draw_networkx_labels(self.Graph,pos,font_size=20,font_family='sans-serif')
        
        plt.axis('off')
        plt.show()

################################################################################

def gen_barr_index(CurPath, Path):

    if CurPath == []:

        return 0

    result = 0

    for course in CurPath:

        result += 2**Path.index(course)

    return result

def set_barr(num, BitArray):

    if num == 0:

        BitArray[0] = True
        return 0

    i = len(BitArray) - 1

    while i >= 0:

        if num | i == num:

            BitArray[i] = True

        i -= 1

    return 0

def index2path(num, answer):

    if num == 0:

        return []

    i = 0
    result = []

    while num > 0:

        if i >= len(answer):

            return []

        if num % 2 == 1:

           result.append(answer[i])

        num /= 2
        i += 1

    return result


