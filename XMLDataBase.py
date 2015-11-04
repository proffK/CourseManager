
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

'''EXAMPLE:
    #parser init
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces,0)

    DataBase = TDataBase()
    parser.setContextHandler(DataBase)
    parser.parse("./Database.xml")

    #Now you can work with DataBase
'''

import xml.sax
import copy

#*************************************************************************#
#***************************Class Course**********************************#
#*************************************************************************#

class TCourse(object):
#*************************************************************************#
    def __init__(self, Name, Id, Weeks, Hours, \
                       Description, Skill_I, Skill_O ):
        self.Name = Name
        self.Id = Id
        self.Hours = Hours
        self.Weeks = Weeks
        self.Description = Description
        self.Skill_I = Skill_I
        self.Skill_O = Skill_O
#*************************************************************************#
    def __repr__(self):
        return "Course <%s> (ID = %d): \n" \
               "Required time: %d weeks (%d hours)\n" \
               "Description: %s \n" \
               "Required skills (id): %s \n" \
               "Acquired skills (id): %s \n" \
               %(self.Name, self.Id, self.Weeks, self.Hours, \
               self.Description[0:10:1], str(self.Skill_I), \
               str(self.Skill_O))
#*************************************************************************#
    def check(self):
        if len(self.Name) == 0 or self.Id < 0 or self.Hours <= 0 or \
           self.Weeks <= 0 or len(self.Description) == 0 or \
           len(self.Skill_O) == 0:
            return -1
        return 0
#*************************************************************************#

#*************************************************************************#
#******************************Class Skill********************************#
#*************************************************************************#

class TSkill(object):
#*************************************************************************#
    def __init__(self, Name, Id, Description):
        self.Name = Name
        self.Id = Id
        self.Description = Description
#*************************************************************************#
    def __repr__(self):
        return "Skill <%s> (ID = %d): \n" \
                "Description: %s \n" \
                %( self.Name, self.Id, self.Description[0:15:1] )
#*************************************************************************#
    def check(self):
        if len(self.Name) == 0 or len(self.Description) == 0 or \
           self.Id < 0:
            return -1
        return 0
#*************************************************************************#

#*************************************************************************#
#*****************************Class database******************************#
#*************************************************************************#

class TDataBase(xml.sax.ContentHandler):
#*************************************************************************#
    def __init__(self):
        self.CourseList = []
        self.SkillList = []
        self.CourseCID = -1
        self.SkillCID = -1
        #temp variables
        self.CurrentType = ""
        self.CurrentField = ""
        self.BufCourse = None
        self.BufSkill = None
        self.buf_content = ""
#*************************************************************************#
    def startElement(self, tag, attributes):
        if (tag == "course" or tag == "skill"):
            self.CurrentType = tag
            if tag == "course":
                self.BufCourse = TCourse("", 0, 0, 0, "", [], [])
            elif tag == "skill":
                self.BufSkill = TSkill("", 0, "")
        elif (tag == "name" or tag == "id" or tag == "hours" or \
              tag == "weeks" or tag == "description" or \
              tag == "skill_i" or tag == "skill_o"):
            self.CurrentField = tag
            self.buf_content = ""
        elif (tag == "database"):
            self.CourseList = []
            self.SkillList = []
            self.CourseCID = -1
            self.SkillCID = -1
            self.BufSkill = None
            self.BufCourse = None
            self.buf_content = ""
        #I shall think about issue with undefined label
#*************************************************************************#
    def endElement(self, tag):
        if tag == "course":
            self.CourseList.append(copy.deepcopy(self.BufCourse))
            if self.BufCourse.Id > self.CourseCID:
                self.CourseCID = self.BufCourse.Id
            self.CurrentType = ""
        elif tag == "skill":
            self.SkillList.append(copy.deepcopy(self.BufSkill))
            if self.BufSkill.Id > self.SkillCID:
                self.SkillCID = self.BufSkill.Id
            self.CurrentType = ""
        elif (tag == "name" or tag == "id" or tag == "hours" or \
              tag == "weeks" or tag == "description" or \
              tag == "skill_i" or tag == "skill_o"):
            self.write_field(self.buf_content)
            self.CurrentField = ""
        elif (tag == "database"):
            if (self.CourseCID != -1):
                self.CourseCID+=1
            if (self.SkillCID != -1 ):
                self.SkillCID+=1
        #I will think about issue with uncorrect course or skill
#*************************************************************************#
    def characters(self, content):
        self.buf_content+=content
#*************************************************************************#
    def write_field(self, content):
        if self.CurrentType == "course":
            if self.CurrentField == "name":
                self.BufCourse.Name = content
            elif self.CurrentField == "id":
                self.BufCourse.Id = int(content)
            elif self.CurrentField == "hours":
                self.BufCourse.Hours = int(content)
            elif self.CurrentField == "weeks":
                self.BufCourse.Weeks = int(content)
            elif self.CurrentField == "description":
                self.BufCourse.Description = content
            elif self.CurrentField == "skill_i":
                self.BufCourse.Skill_I = map(int, content.split(","))
            elif self.CurrentField == "skill_o":
                self.BufCourse.Skill_O = map(int, content.split(","))
        elif self.CurrentType == "skill":
            if self.CurrentField == "name":
                self.BufSkill.Name = content
            elif self.CurrentField == "id":
                self.BufSkill.Id = int(content)
            elif self.CurrentField == "description":
                self.BufSkill.Description = content
#*************************************************************************#
    def dump(self, FileName):
        FilePointer = open(FileName, "r+")
        FilePointer.seek(0,0)
        FilePointer.truncate()
        FilePointer.seek(0,0)
        FilePointer.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
        FilePointer.write("<database title=\"DataBase.xml\">\n\n")
        for curcourse in self.CourseList:
            FilePointer.write ("<course>\n")
            FilePointer.write ("   <name>"+curcourse.Name+"</name>\n")
            FilePointer.write ("   <id>"+str(curcourse.Id)+"</id>\n")
            FilePointer.write ("   <hours>"+str(curcourse.Hours)+"</hours>\n")
            FilePointer.write ("   <weeks>"+str(curcourse.Weeks)+"</weeks>\n")
            FilePointer.write ("   <description>"+curcourse.Description+"</description>\n")
            FilePointer.write ("   <skill_i>"+str(curcourse.Skill_I).replace(", ",",").\
                               replace("[", "").replace("]","")+"</skill_i>\n")
            FilePointer.write ("   <skill_o>"+str(curcourse.Skill_O).replace(", ",",").\
                               replace("[", "").replace("]","")+"</skill_o>\n")
            FilePointer.write ("</course>\n\n")
        for curskill in self.SkillList:
            FilePointer.write ("<skill>\n")
            FilePointer.write ("   <name>"+curskill.Name+"</name>\n")
            FilePointer.write ("   <id>"+str(curskill.Id)+"</id>\n")
            FilePointer.write ("   <description>"+curskill.Description+"</description>\n")
            FilePointer.write ("</skill>\n\n")
        FilePointer.write("</database>\n")
#*************************************************************************#
    def dump_console(self):
        print "\n******************Courses**********************\n"
        for current in self.CourseList:
            print current
        print "\n***********************************************\n"
        print "\n*******************Skills**********************\n"
        for current in self.SkillList:
            print current
        print "\n***********************************************\n"
#*************************************************************************#
    def find_courses_with_inp_skill(self, Id ):
        BufferList = []
        for current in self.CourseList:
            if current.Skill_I.count(Id) > 0:
                BufferList.append(current.Id)
        return BufferList
#*************************************************************************#
    def get_courses_id_list(self):
        BufferListId = []
        for current in self.CourseList:
           BufferListId.append(current.Id)
        return BufferListId
#*************************************************************************#
    def get_time(self, Id):
        for current in self.CourseList:
            if current.Id == Id:
                return current.Hours
        return -1
#*************************************************************************#
    def find_courses_with_out_skill(self, Id ):
        BufferList = []
        for current in self.CourseList:
            if current.Skill_O.count(Id) > 0:
                BufferList.append(current.Id)
        return BufferList
#*************************************************************************#
    def get_inp_skills_with_id(self, Id):
        for current in self.CourseList:
            if current.Id == Id:
                return current.Skill_I
#*************************************************************************#
    def get_out_skills_with_id(self, Id):
        for current in self.CourseList:
            if current.Id == Id:
                return current.Skill_O
#*************************************************************************#
    def exist_course(self, Id):
        for current in self.CourseList:
            if current.Id == Id:
                return 0
        return -1
#*************************************************************************#
    def exist_skill(self, Id):
        for current in self.SkillList:
            if current.Id == Id:
                return 0
        return -1
#*************************************************************************#
    def add_course( self, Name, Weeks, Hours, \
                    Description, Skill_I, Skill_O ):
        if ( self.CourseCID < 0 ):
            return -1
        BufferCourse = TCourse( Name, self.CourseCID, Weeks, Hours, \
                               Description, Skill_I, Skill_O )
        self.CourseList.append(BufferCourse)
        self.CourseCID+=1
        return self.CourseCID-1
#*************************************************************************#
    def add_skill(self, Name, Description ):
        if ( self.SkillCID < 0 ):
            return -1
        BufferSkill = TSkill( Name, self.SkillCID, Description ); 
        self.SkillList.append( BufferSkill )
        self.SkillCID +=1
        return self.SkillCID-1
#*************************************************************************#
    def remove_course(self, Id):
        for current in self.CourseList:
            if ( current.Id == Id ):
                self.CourseList.remove(current)
                return 0
        return -1
#*************************************************************************#
    def remove_skill(self, Id):
        if len(self.find_courses_with_inp_skill(Id)) == 0:
            return -1
        if len(self.find_courses_with_out_skill(Id)) == 0:
            return -1
        for current in self.SkillList:
           if ( current.Id == Id ):
               self.SkillList.remove(current)
               return 0
        return -1
#*************************************************************************#
    def get_course(self, Id):
        for current in self.CourseList:
            if ( current.Id == Id ):
                return current
        return -1
#*************************************************************************#
    def get_skill(self, Id):
        for current in self.SkillList:
            if ( current.Id == Id ):
                return current
        return -1
#*************************************************************************#

#*************************************************************************#
#*************************************************************************#
#*************************************************************************#
   
