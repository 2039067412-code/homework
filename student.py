# student.py 学生实体类
class Student:
    def __init__(self, sid, name, gender, clazz, college):
        # 学号
        self.sid = sid
        # 姓名
        self.name = name
        # 性别
        self.gender = gender
        # 班级
        self.clazz = clazz
        # 学院
        self.college = college

    # 格式化输出学生信息
    def get_info(self):
        info = (f"姓名:{self.name}\n性别:{self.gender} 班级:{self.clazz} 学号:{self.sid}\n学院:{self.college}")
        return info
        
