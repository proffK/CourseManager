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

import sys
from PyQt4 import QtGui, QtCore
import DataBase

DATA_BASE_NAME = open("DataBase.txt", "r+") 
GLOBAL_DATA_BASE = DataBase.TDataBase(DATA_BASE_NAME)
GLOBAL_DATA_BASE.pull()

class MainPage(QtGui.QWidget):
	def __init__(self, parent = None):
		QtGui.QWidget.__init__(self, parent)

		self.setWindowTitle(u"Менеджер курсов")

		self.grid = QtGui.QGridLayout()

		self.viewListCourses = QtGui.QPushButton(u"Список курсов")
		self.connect(self.viewListCourses, QtCore.SIGNAL('clicked()'), self.view_list_of_course)
		self.addCourseButton = QtGui.QPushButton(u"Добавить курс")
		self.connect(self.addCourseButton, QtCore.SIGNAL('clicked()'), self.view_add_course)
		self.addSkillButton	 = QtGui.QPushButton(u"Добавить навык")
		self.connect(self.addSkillButton, QtCore.SIGNAL('clicked()'), self.view_add_skill)
		vButtonBox			 = QtGui.QVBoxLayout()

		vButtonBox.addWidget(self.viewListCourses)
		vButtonBox.addWidget(self.addCourseButton)
		vButtonBox.addWidget(self.addSkillButton)
		
		self.mainWindow		 = ViewCourses()
		self.grid.addLayout(vButtonBox, 0, 0)
		self.grid.addWidget(self.mainWindow, 0, 1)

		self.setLayout(self.grid)

	def view_list_of_course(self):
		self.mainWindow.close()
		self.mainWindow = ViewCourses()
		self.grid.addWidget(self.mainWindow, 0, 1)

	def view_add_course(self):
		self.mainWindow.close()
		self.mainWindow = EditCourse()
		self.grid.addWidget(self.mainWindow, 0, 1)

	def view_add_skill(self):
		self.mainWindow.close()
		self.mainWindow = EditSkill()
		self.grid.addWidget(self.mainWindow, 0, 1)


class EditCourse(QtGui.QWidget):
	def __init__(self, CourseCId = -1, parent = None):
		QtGui.QWidget.__init__(self, parent)

		#Opening Data Base
		
		
		print GLOBAL_DATA_BASE.CourseCID
		if CourseCId == -1:
			self.courseForEdit = GLOBAL_DATA_BASE.get_course(GLOBAL_DATA_BASE.add_course("Course", 1, 1, "Hi", [], []))
		else:
			self.courseForEdit = GLOBAL_DATA_BASE.get_course(CourseCId)
		#self.courseForEdit = GLOBAL_DATA_BASE.get_course(GLOBAL_DATA_BASE.add_course("Course", "0", "0", "0", [], []))

		self.grid = QtGui.QGridLayout()

		self.grid.addWidget(QtGui.QLabel(u"Входные навыки"), 0, 0)
		self.grid.addWidget(QtGui.QLabel(u"Название курса"), 0, 1)
		self.grid.addWidget(QtGui.QLabel(u"Выходные навыки"), 0, 2)

		self.inputSkills = QtGui.QListWidget()
		for skillId in self.courseForEdit.Skill_I:
			skill = GLOBAL_DATA_BASE.get_skill(skillId)
			listItem = QtGui.QListWidgetItem();
			listItem.setData(32, skill.Id)
			listItem.setText(skill.Name)
			self.inputSkills.addItem(QtGui.QListWidgetItem(listItem))
		self.grid.addWidget(self.inputSkills, 1, 0)

		self.outputSkills = QtGui.QListWidget()
		for skillId in self.courseForEdit.Skill_O:
			skill = GLOBAL_DATA_BASE.get_skill(skillId)
			listItem = QtGui.QListWidgetItem();
			listItem.setData(32, skill.Id)
			listItem.setText(skill.Name)
			self.outputSkills.addItem(QtGui.QListWidgetItem(listItem))
		self.grid.addWidget(self.outputSkills, 1, 2)

		self.editInputSkills 	= QtGui.QPushButton(u"Редактировать навык")
		self.connect(self.editInputSkills, QtCore.SIGNAL('clicked()'), self.add_input_skill)
		self.deleteInputSkills 	= QtGui.QPushButton(u"Удалить навык")
		self.connect(self.deleteInputSkills, QtCore.SIGNAL('clicked()'), self.delete_input_skill)

		self.editOutputSkills	= QtGui.QPushButton(u"Редактировать навык")
		self.connect(self.editOutputSkills, QtCore.SIGNAL('clicked()'), self.add_output_skill)
		self.deleteOutputSkills	= QtGui.QPushButton(u"Удалить навык")
		self.connect(self.deleteOutputSkills, QtCore.SIGNAL('clicked()'), self.delete_output_skill)

		self.addNewSkill		= QtGui.QPushButton(u"Добавить навык")

		self.grid.addWidget(self.editInputSkills, 2, 0)
		self.grid.addWidget(self.deleteInputSkills, 3, 0)
		self.grid.addWidget(self.editOutputSkills, 2, 2)
		self.grid.addWidget(self.deleteOutputSkills, 3, 2)
		self.grid.addWidget(self.addNewSkill, 3, 1)

		self.currentCourseTitle		= QtGui.QLabel(self.courseForEdit.Name)
		self.editCourseTitle 		= QtGui.QLineEdit()
		self.editCourseTitleButton	= QtGui.QPushButton(u"Изменить название курса")
		self.connect(self.editCourseTitleButton, QtCore.SIGNAL('clicked()'), self.change_course_name)
		self.vBoxTitle				= QtGui.QVBoxLayout()

		self.vBoxTitle.addWidget(self.currentCourseTitle)
		self.vBoxTitle.addWidget(self.editCourseTitle)
		self.vBoxTitle.addWidget(self.editCourseTitleButton)

		self.grid.addLayout(self.vBoxTitle, 1, 1)
		self.grid.addWidget(self.editCourseTitleButton, 2, 1)

		self.setLayout(self.grid)
	
	def change_course_name(self):
		self.currentCourseTitle.setText(self.editCourseTitle.displayText())
		self.courseForEdit.Name = self.editCourseTitle.displayText()
		GLOBAL_DATA_BASE.dump()

	def delete_input_skill(self):
		listItems = self.inputSkills.selectedItems()
		for item in listItems:
			for skill in self.courseForEdit.Skill_I:
				if(skill == item.data(32)):
					self.courseForEdit.Skill_I.remove(skill)
			self.inputSkills.takeItem(self.inputSkills.row(item))
		GLOBAL_DATA_BASE.dump()


	def delete_output_skill(self):
		listItems = self.outputSkills.selectedItems()
		for item in listItems:
			for skill in self.courseForEdit.Skill_O:
				if(skill == item.data(32)):
					self.courseForEdit.Skill_O.remove(skill)
			self.outputSkills.takeItem(self.outputSkills.row(item))
		GLOBAL_DATA_BASE.dump()

	def add_input_skill(self):
		name_skills = []
		for skill in GLOBAL_DATA_BASE.SkillList:
			name_skills.append(skill.Name)

		item, ok = QtGui.QInputDialog.getItem(self, u"Выбрать навык", "w", name_skills, 0, False)
		if ok and item:
			self.courseForEdit.Skill_I.append(GLOBAL_DATA_BASE.SkillList[name_skills.index(item)].Id)
		GLOBAL_DATA_BASE.dump()
		listItem = QtGui.QListWidgetItem();
		listItem.setData(32, GLOBAL_DATA_BASE.SkillList[name_skills.index(item)].Id)
		listItem.setText(GLOBAL_DATA_BASE.SkillList[name_skills.index(item)].Name)
		self.inputSkills.addItem(QtGui.QListWidgetItem(listItem))

	def add_output_skill(self):
		name_skills = []
		for skill in GLOBAL_DATA_BASE.SkillList:
			name_skills.append(skill.Name)

		item, ok = QtGui.QInputDialog.getItem(self, u"Выбрать навык", "w", name_skills, 0, False)
		if ok and item:
			self.courseForEdit.Skill_O.append(GLOBAL_DATA_BASE.SkillList[name_skills.index(item)].Id)
		GLOBAL_DATA_BASE.dump()
		listItem = QtGui.QListWidgetItem();
		listItem.setData(32, GLOBAL_DATA_BASE.SkillList[name_skills.index(item)].Id)
		listItem.setText(GLOBAL_DATA_BASE.SkillList[name_skills.index(item)].Name)
		self.outputSkills.addItem(QtGui.QListWidgetItem(listItem))

class EditSkill(QtGui.QWidget):
	def __init__(self, parent = None):
		QtGui.QWidget.__init__(self, parent)

		

		grid = QtGui.QGridLayout()

		self.skillDefinition 	= QtGui.QLineEdit()
		self.skillDeclaration 	= QtGui.QTextEdit()
		self.editSkillButton	= QtGui.QPushButton(u"Добавить навык")
		self.connect(self.editSkillButton, QtCore.SIGNAL('clicked()'), self.add_skill_in_base)


		grid.addWidget(QtGui.QLabel(u"Навык:"), 0, 0)
		grid.addWidget(QtGui.QLabel(u"Описание навыка:"), 1, 0)
		grid.addWidget(self.skillDefinition, 0, 1)
		grid.addWidget(self.skillDeclaration, 1, 1)
		grid.addWidget(self.editSkillButton, 2, 1)

		self.setLayout(grid)

	def add_skill_in_base(self):
		GLOBAL_DATA_BASE.add_skill(self.skillDefinition.displayText(), self.skillDeclaration.toPlainText())
		GLOBAL_DATA_BASE.dump()

class ViewCourses(QtGui.QWidget):
	def __init__(self, parent = None):
		QtGui.QWidget.__init__(self, parent)

		self.grid = QtGui.QGridLayout()

		self.coursesList = QtGui.QListWidget()
		self.editCourse  = QtGui.QPushButton(u"Изменить курс")
		self.connect(self.editCourse, QtCore.SIGNAL('clicked()'), self.change_course)

		self.addCourse	 = QtGui.QPushButton(u"Добавить курс")

		self.view_courses()

		self.grid.addWidget(self.coursesList, 0, 0)
		self.grid.addWidget(self.editCourse, 1, 0)
		self.grid.addWidget(self.addCourse, 2, 0)

		self.setLayout(self.grid)

	def view_courses(self):
		for course in GLOBAL_DATA_BASE.CourseList:
			listItem = QtGui.QListWidgetItem();
			listItem.setData(32, course.Id)
			listItem.setText(course.Name)
			self.coursesList.addItem(QtGui.QListWidgetItem(listItem))

	def change_course(self):
		courseId = int(self.coursesList.selectedItems()[0].data(32).toString())
		print courseId
		self.grid.addWidget(EditCourse(courseId), 0, 1)
		#GLOBAL_DATA_BASE.dump()


app = QtGui.QApplication(sys.argv)
qb = MainPage()
qb.show()

sys.exit(app.exec_())