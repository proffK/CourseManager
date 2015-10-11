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

class MainPage(QtGui.QWidget):
	def __init__(self, parent = None):
		QtGui.QWidget.__init__(self, parent)

		self.setWindowTitle(u"Менеджер курсов")

		self.grid = QtGui.QGridLayout()

		self.viewListCourses = QtGui.QPushButton(u"Список курсов")
		self.connect(self.viewListCourses, QtCore.SIGNAL('clicked()'), self.view_list_of_course)
		self.addCourseButton = QtGui.QPushButton(u"Добавить курс")
		self.connect(self.addCourseButton, QtCore.SIGNAL('clicked()'), self.view_add_course)
		vButtonBox			 = QtGui.QVBoxLayout()

		vButtonBox.addWidget(self.viewListCourses)
		vButtonBox.addWidget(self.addCourseButton)
		
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

class CourseInBase(QtGui.QWidget):
	def __init__(self, name, parent = None):
		QtGui.QWidget.__init__(self, parent)
		
		hbox = QtGui.QHBoxLayout()

		hbox.addWidget(QtGui.QLabel(name))
		hbox.addWidget(QtGui.QPushButton(u"Редактировать"))
		hbox.addWidget(QtGui.QPushButton(u"Удалить"))

		self.setLayout(hbox)

class EditCourse(QtGui.QWidget):
	def __init__(self, parent = None):
		QtGui.QWidget.__init__(self, parent)

		self.grid = QtGui.QGridLayout()

		self.grid.addWidget(QtGui.QLabel(u"Входные навыки"), 0, 0)
		self.grid.addWidget(QtGui.QLabel(u"Название курса"), 0, 1)
		self.grid.addWidget(QtGui.QLabel(u"Выходные навыки"), 0, 2)

		self.inputSkills = QtGui.QListWidget()

		self.inputSkills.addItem(QtGui.QListWidgetItem(u"Один"))
		self.inputSkills.addItem(QtGui.QListWidgetItem(u"Два"))

		self.grid.addWidget(self.inputSkills, 1, 0)

		self.outputSkills = QtGui.QListWidget()
		self.outputSkills.addItem(QtGui.QListWidgetItem(u"Один"))
		self.outputSkills.addItem(QtGui.QListWidgetItem(u"Два"))

		self.grid.addWidget(self.outputSkills, 1, 2)

		self.editInputSkills 	= QtGui.QPushButton(u"Редактировать навык")
		self.deleteInputSkills 	= QtGui.QPushButton(u"Удалить навык")
		self.connect(self.deleteInputSkills, QtCore.SIGNAL('clicked()'), self.delete_input_skill)

		self.editOutputSkills	= QtGui.QPushButton(u"Редактировать навык")
		self.deleteOutputSkills	= QtGui.QPushButton(u"Удалить навык")
		self.connect(self.deleteOutputSkills, QtCore.SIGNAL('clicked()'), self.delete_output_skill)

		self.addNewSkill		= QtGui.QPushButton(u"Добавить навык")

		self.grid.addWidget(self.editInputSkills, 2, 0)
		self.grid.addWidget(self.deleteInputSkills, 3, 0)
		self.grid.addWidget(self.editOutputSkills, 2, 2)
		self.grid.addWidget(self.deleteOutputSkills, 3, 2)
		self.grid.addWidget(self.addNewSkill, 3, 1)

		self.currentCourseTitle		= QtGui.QLabel(u"Текущее название")
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

	def delete_input_skill(self):
		listItems = self.inputSkills.selectedItems()
		for item in listItems:
			self.inputSkills.takeItem(self.inputSkills.row(item))

	def delete_output_skill(self):
		listItems = self.outputSkills.selectedItems()
		for item in listItems:
			self.outputSkills.takeItem(self.outputSkills.row(item))

class EditSkill(QtGui.QWidget):
	def __init__(self, parent = None):
		QtGui.QWidget.__init__(self, parent)

		grid = QtGui.QGridLayout()

		self.skillDefinition 	= QtGui.QLineEdit()
		self.skillDeclaration 	= QtGui.QTextEdit()
		self.editSkillButton	= QtGui.QPushButton(u"Изменить навык")

		grid.addWidget(QtGui.QLabel(u"Навык:"), 0, 0)
		grid.addWidget(QtGui.QLabel(u"Описание навыка:"), 1, 0)
		grid.addWidget(self.skillDefinition, 0, 1)
		grid.addWidget(self.skillDeclaration, 1, 1)
		grid.addWidget(self.editSkillButton, 2, 1)

		self.setLayout(grid)

class ViewCourses(QtGui.QWidget):
	def __init__(self, parent = None):
		QtGui.QWidget.__init__(self, parent)

		grid = QtGui.QGridLayout()

		self.coursesList = QtGui.QListWidget()
		self.editCourse  = QtGui.QPushButton(u"Изменить курс")
		self.addCourse	 = QtGui.QPushButton(u"Добавить курс")

		grid.addWidget(self.coursesList, 0, 0)
		grid.addWidget(self.editCourse, 1, 0)
		grid.addWidget(self.addCourse, 2, 0)

		self.setLayout(grid)

app = QtGui.QApplication(sys.argv)
qb = MainPage()
qb.show()

sys.exit(app.exec_())