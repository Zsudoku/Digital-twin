'''
Date: 2022-03-13 10:37:39
LastEditors: ZSudoku
LastEditTime: 2022-03-15 20:56:08
FilePath: \python\Digital twin\test.py
'''

from tool import MyTools

#MyTools.MakeClass("cargoNow",__file__,p=["x","y","z","s1","s2","num","model","time","flag","line","row","colum","id"])

class cargoNow():
	def __init__(self):
		self.__x = None
		self.__y = None
		self.__z = None
		self.__s1 = None
		self.__s2 = None
		self.__num = None
		self.__model = None
		self.__time = None
		self.__flag = None
		self.__line = None
		self.__row = None
		self.__colum = None
		self.__id = None
		pass

	@property
	def x(self):
		return self.__x

	@x.setter
	def x(self, value:float):
		self.__x = value

	@property
	def y(self):
		return self.__y

	@y.setter
	def y(self, value:float):
		self.__y = value

	@property
	def z(self):
		return self.__z

	@z.setter
	def z(self, value:float):
		self.__z = value

	@property
	def s1(self):
		return self.__s1

	@s1.setter
	def s1(self, value:int):
		self.__s1 = value

	@property
	def s2(self):
		return self.__s2

	@s2.setter
	def s2(self, value:int):
		self.__s2 = value

	@property
	def num(self):
		return self.__num

	@num.setter
	def num(self, value):
		self.__num = value

	@property
	def model(self):
		return self.__model

	@model.setter
	def model(self, value):
		self.__model = value

	@property
	def time(self):
		return self.__time

	@time.setter
	def time(self, value):
		self.__time = value

	@property
	def flag(self):
		return self.__flag

	@flag.setter
	def flag(self, value):
		self.__flag = value

	@property
	def line(self):
		return self.__line

	@line.setter
	def line(self, value):
		self.__line = value

	@property
	def row(self):
		return self.__row

	@row.setter
	def row(self, value):
		self.__row = value

	@property
	def colum(self):
		return self.__colum

	@colum.setter
	def colum(self, value):
		self.__colum = value

	@property
	def id(self):
		return self.__id

	@id.setter
	def id(self, value):
		self.__id = value

	def ToDict(self):
		dict1={
			'x':self.__x,
			'y':self.__y,
			'z':self.__z,
			's1':self.__s1,
			's2':self.__s2,
			'num':self.__num,
			'model':self.__model,
			'time':self.__time,
			'flag':self.__flag,
			'line':self.__line,
			'row':self.__row,
			'colum':self.__colum,
			'id':self.__id,
			}
		return dict1
	pass
