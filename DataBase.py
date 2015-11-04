
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

class TDataBase(object):
#*************************************************************************#
    def __init__(self, FilePointer ):
        self.FilePointer = FilePointer
        if FilePointer == -1:
            return -1
        self.CourseList = []
        self.SkillList = []
        self.CourseCID = -1
        self.SkillCID = -1
#*************************************************************************#
    def pull(self):
        curline = self.FilePointer.readline()
        while curline != "":
            curline=curline.rstrip('\n')
            #print curline
            if curline == "course_start":
                BufferCourse = TCourse("", 0, 0, 0, "", [], [])
                courseline = self.FilePointer.readline()
                while len(courseline) != 0:
                    courseline=courseline.rstrip('\n')
                    if len(courseline.replace(" ","")) == 0:
                        continue
                    if courseline.lower() == "name:":
                        BufferCourse.Name = self.read_block("name")
                        #print BufferCourse.Name
                    elif courseline.lower() == "id:":
                        BufferCourse.Id = self.read_block("id")
                        if BufferCourse.Id > self.CourseCID:
                            self.CourseCID = BufferCourse.Id
                        #print BufferCourse.Id
                    elif courseline.lower() == "hours:":
                        BufferCourse.Hours = self.read_block("hours")
                        #print BufferCourse.Hours
                    elif courseline.lower() == "weeks:":
                        BufferCourse.Weeks = self.read_block("weeks")
                        #print BufferCourse.Weeks
                    elif courseline.lower() == "description:":
                        BufferCourse.Description = self.read_block("description")
                        #print BufferCourse.Description
                    elif courseline.lower() == "skill_i:":
                        BufferCourse.Skill_I = self.read_block("skill_i")
                        #print BufferCourse.Skill_I
                    elif courseline.lower() == "skill_o:":
                        BufferCourse.Skill_O = self.read_block("skill_o")
                        #print BufferCourse.Skill_O
                    elif courseline.lower() == "course_end":
                        if BufferCourse.check() == -1:
                            print "Database corrupted, check data.\n"
                            return -1
                    elif courseline.lower()[0] != ' ' or \
                         courseline.lower()[0] != '\t' :          
                        print "Not found 'course_end' in database.\n"
                        return -1
                    courseline = self.FilePointer.readline()
                self.CourseList.append(BufferCourse)
                if BufferCourse.check() == -1:
                    print "Database corrupted, check format.\n"
                    return -1

            elif curline == "skill_start":
                #print "hirngenre"
                BufferSkill = TSkill("", 0, "")
                skillline = self.FilePointer.readline()
                while len(skillline) != 0:
                    skillline=skillline.rstrip('\n')
                    if len(skillline.replace(" ","")) == 0:
                        continue
                    if skillline.lower() == "name:":
                        BufferSkill.Name = self.read_block("name")
                        #print BufferSkill.Name
                    elif skillline.lower() == "id:":
                        BufferSkill.Id = self.read_block("id")
                        if BufferSkill.Id > self.SkillCID:
                            self.SkillCID = BufferSkill.Id
                        #print BufferSkill.Id
                    elif skillline.lower() == "description:":
                        BufferSkill.Description = self.read_block("description")
                        #print BufferSkill.Description
                    elif skillline.lower() == "skill_end":
                        if BufferSkill.check() == -1:
                            print "Database corrupted, check data.\n"
                            return -1
                    elif skillline.lower()[0] != ' ' or \
                         skillline.lower()[0] != '\t' :
                        print "Not found 'skill_end' in database.\n"
                        return -1
                    skillline = self.FilePointer.readline()
                self.SkillList.append(BufferSkill)
                if BufferSkill.check() == -1:
                    print "Database corrupted, check format.\n"
                    return -1
            else: 
                print "Database corrupted, check format.\n"
                return -1
            curline = self.FilePointer.readline()
        if ( self.CourseCID != -1 ):
            self.CourseCID += 1
        if ( self.SkillCID != -1 ):
            self.SkillCID += 1
        return 0
#*************************************************************************#
    def read_block(self, option):
        Buffer = ""
        PrevLine = 0
        #-----------------------------------------------------------------
        if len(option) > 0:
            current = self.FilePointer.readline()
            while current != "":
                #print "!",current
                #print str(len(current.rstrip('\n').replace(" ","")))
                if current[0] == ' ' or current[0] == '\t':
                    Count = 0
                    symbol = ' '                   
                    while symbol.isspace() == True:
                        Count+=1
                        symbol = current[Count]
                    Buffer+=current[Count::1]
                else: 
                    self.FilePointer.seek(PrevLine)
                    break
                PrevLine = self.FilePointer.tell()
                current = self.FilePointer.readline()
            Buffer = Buffer.strip('\n')
            Buffer = Buffer.replace('\n',' ')
            if option == "name" or option == "description": 
                return Buffer
            if option == "id" or option == "hours" or option == "weeks":
                return int(Buffer.replace(' ',''))
            if option == "skill_i" or option == "skill_o":
                BufferSkill = []
                if len(Buffer)==1 and int(Buffer) == 0:
                    return BufferSkill
                for cur in Buffer.split(","):
                    BufferSkill.append(int(cur))
                return BufferSkill
        #-----------------------------------------------------------------
        '''if option == "id":
            for current in self.FilePointer:
                if current[0] == ' ' or current[0] == '\t':
                    Buffer += current
                else:
                    break
            return int(Buffer)
        #-----------------------------------------------------------------
        if option == "hours":
            for current in self.FilePointer:
                if current[0] == ' ' or current[0] == '\t':
                    Buffer += current
                else:
                    break
            return int(Buffer)       
        #-----------------------------------------------------------------
        elif option == "weeks":
            for current in self.FilePointer:
                if current[0] == ' ' or current[0] == '\t':
                    Buffer += current
                else:
                    break
            return int(Buffer)
        #-----------------------------------------------------------------
        elif option == "description":
            for current in self.FilePointer:
                if current[0] == ' ' or current[0] == '\t':
                    Buffer += current
                else:
                    break
            return Buffer
        #-----------------------------------------------------------------
        if option == "skill_i":
            for current in self.FilePointer:
                if current[0] == ' ' or current[0] == '\t':
                    Buffer += current
                else:
                   break
            return Buffer.split(",")           
        #-----------------------------------------------------------------
        elif option == "skill_o":
            for current in self.FilePointer:
                if current[0] == ' ' or current[0] == '\t':
                    Buffer += current
                else:
                    break
            return Buffer.split(",")'''
        #-----------------------------------------------------------------
        return -1
#*************************************************************************#
    def dump(self):
        self.FilePointer.seek(0,0)
        self.FilePointer.truncate()
        self.FilePointer.seek(0,0)
        for curcourse in self.CourseList:
            self.FilePointer.write ("course_start\n")
            self.FilePointer.write ("name:\n")
            self.FilePointer.write ("    "+curcourse.Name+'\n')
            self.FilePointer.write ("id:\n")
            self.FilePointer.write ("    "+str(curcourse.Id)+'\n')
            self.FilePointer.write ("hours:\n")
            self.FilePointer.write ("    "+str(curcourse.Hours)+'\n')
            self.FilePointer.write ("weeks:"+'\n')
            self.FilePointer.write ("    "+str(curcourse.Weeks)+'\n')
            self.FilePointer.write ("description:"+'\n')
            self.FilePointer.write ("    "+curcourse.Description+'\n')
            self.FilePointer.write ("skill_i:"+'\n')
            self.FilePointer.write ("    "+str(curcourse.Skill_I).replace(", ",",").\
                                    replace("[", "").replace("]","")+'\n')
            self.FilePointer.write ("skill_o:"+'\n')
            self.FilePointer.write ("    "+str(curcourse.Skill_O).replace(", ",",").\
                                    replace("[", "").replace("]","")+'\n')
            self.FilePointer.write ("course_end\n\n")
        for curcourse in self.SkillList:
            self.FilePointer.write ("skill_start"+'\n')
            self.FilePointer.write ("name:"+'\n')
            self.FilePointer.write ("    "+curcourse.Name+'\n')
            self.FilePointer.write ("id:"+'\n')
            self.FilePointer.write ("    "+str(curcourse.Id)+'\n')
            self.FilePointer.write ("description:"+'\n')
            self.FilePointer.write ("    "+curcourse.Description+'\n')
            self.FilePointer.write ("skill_end\n\n")
        return 0
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
        return 0
#*************************************************************************#
    def find_courses_with_inp_skill(self, Id ):
        BufferList = []
        #print self.CourseList
        for current in self.CourseList:
            #print current.Skill_I
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
        #print Id
        for current in self.SkillList:
            if ( current.Id == Id ):
                return current
        return -1
#*************************************************************************#

#*************************************************************************#
#*************************************************************************#
#*************************************************************************#
   
