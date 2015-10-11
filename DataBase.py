
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

'''*************************************************************************'''
'''***************************Class Course**********************************'''
'''*************************************************************************'''

class TCourse(object):
    def __init__(self, Name, Id, Weeks, Hours, \
                       Description, Skill_I, Skill_O ):
        self.Name = Name
        self.Id = Id
        self.Hours = Hours
        self.Weeks = Weeks
        self.Description = Description
        self.Skill_I = Skill_I
        self.Skill_O = Skill_O
    def __repr__(self):
        return "Course <%s> (ID = %d): \n" \
               "Required time: %d weeks (%d hours)\n" \
               "Description: %s \n" \
               "Required skills (id): %s \n" \
               "Acquired skills (id): %s \n" \
               %(self.Name, self.Id, self.Weeks, self.Hours, \
               self.Description[0:10:1], str(self.Skill_I), \
               str(self.Skill_O))

'''*************************************************************************'''
'''******************************Class Skill********************************'''
'''*************************************************************************'''

class TSkill(object):
    def __init__(self, Name, Id, Description):
        self.Name = Name
        self.Id = Id
        self.Description = Description
    def __repr__(self):
        return "Skill <%s> (ID = %d): \n" \
                "Description: %s \n" \
                %( self.Name, self.Id, self.Description[0:10:1] )

'''*************************************************************************'''
'''*************************************************************************'''
'''*************************************************************************'''

class TDataBase(object):
    '''+++++++++++++++++++++++++++++++++++++++++++++++++++++++'''
    def __init__(self, FilePointer ):
        self.FilePointer = FilePointer
        self.CourseList = []
        self.SkillList = []
        self.CourseCID = -1
        self.SkillCID = -1
    '''+++++++++++++++++++++++++++++++++++++++++++++++++++++++'''
    def pull(self):
        pass
    '''+++++++++++++++++++++++++++++++++++++++++++++++++++++++'''
    def dump(self):
        pass
    '''+++++++++++++++++++++++++++++++++++++++++++++++++++++++'''
    def dump_console(self):
        print "\n******************Courses**********************\n"
        for current in self.CourseList:
            print current
        print "\n***********************************************\n"
        print "\n*******************Skills**********************\n"
        for current in self.SkillList:
            print current
        print "\n***********************************************\n"
        return 0
    '''+++++++++++++++++++++++++++++++++++++++++++++++++++++++'''
    def add_course( self, Name, Weeks, Hours, \
                    Description, Skill_I, Skill_O ):
        if ( self.CourseCID < 0 ):
            return -1
        BufferCourse = TCourse( Name, self.CourseCID, Weeks, Hours, \
                               Description, Skill_I, Skill_O )
        self.CourseList.append(BufferCourse)
        self.CourseCID+=1
        return self.CourseCID-1
    '''+++++++++++++++++++++++++++++++++++++++++++++++++++++++'''
    def add_skill(self, Name, Description ):
        if ( self.SkillCID < 0 ):
            return -1
        BufferSkill = TSkill( Name, self.SkillCID, Description ); 
        self.SkillList.appen ( BufferSkill )
        self.SkillCID +=1
        return self.SkillCID-1
    '''+++++++++++++++++++++++++++++++++++++++++++++++++++++++'''
    def remove_course(self, Id):
        for current in self.CourseList:
            if ( current.Id == Id ):
                self.CourseList.remove(current)
                return 0
        return -1
    '''+++++++++++++++++++++++++++++++++++++++++++++++++++++++'''
    def remove_skill(self, Id):
        for current in self.SkillList:
           if ( current.Id == Id ):
               self.SkillList.remove(current)
               return 0
        return -1
    '''+++++++++++++++++++++++++++++++++++++++++++++++++++++++'''
    def get_course(self, Id):
        for current in self.CourseList:
            if ( current.Id == Id ):
                return current
        return -1
    '''+++++++++++++++++++++++++++++++++++++++++++++++++++++++'''
    def get_skill(self, Id):
        for current in self.SkillList:
            if ( current.Id == Id ):
                return current
        return -1
    '''+++++++++++++++++++++++++++++++++++++++++++++++++++++++'''

'''*************************************************************************'''
'''*************************************************************************'''
'''*************************************************************************'''
   
