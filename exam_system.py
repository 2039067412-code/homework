# exam_system.py 考场管理系统类
import random
import os
from student import Student

class ExamSys:
    def __init__(self):
        # 存储全部学生对象列表
        self.student_list = []
        # 存储打乱后的考场座位信息：[{座位号:1,学生对象},...]
        self.arrange_data = []
        # 初始化加载学生数据
        self.load_students()

    def load_students(self):
        """功能2：从txt读取学生信息，封装Student对象，文件制表符分隔、跳过表头"""
        # 固定文件绝对路径
        file_name = r"E:\中山大学\作业\python\homework2\人工智能编程语言学生名单.txt"
        try:
            with open(file_name, "r", encoding="utf-8") as f:
                lines = f.readlines()
                # 跳过第1行表头
                for index, line in enumerate(lines):
                    line = line.strip()
                    if not line:
                        continue
                    # 第一行是表头直接跳过
                    if index == 0:
                        continue
                    # 使用制表符\t切割内容
                    parts = line.split("\t")
                    if len(parts) == 6:
                        # parts[1]姓名 parts[2]性别 parts[3]班级 parts[4]学号 parts[5]学院
                        sid = parts[4]
                        name = parts[1]
                        gender = parts[2]
                        clazz = parts[3]
                        college = parts[5]
                        stu = Student(sid, name, gender, clazz, college)
                        self.student_list.append(stu)
            print(f"[系统] 已成功加载 {len(self.student_list)} 名学生信息。")
        except FileNotFoundError:
            print("【错误】学生名单文件不存在！请检查路径是否正确：", file_name)

    def find_student(self):
        """功能3：根据学号查询学生信息"""
        input_id = input("请输入要查询的学号:").strip()
        find_flag = False
        for stu in self.student_list:
            if stu.sid == input_id:
                print("查询结果:")
                print(stu.get_info())
                find_flag = True
                break
        if not find_flag:
            print("未找到该学号对应的学生，请检查输入是否正确。")

    def random_roll_call(self):
        """功能4：随机不重复点名，异常捕获：非数字、<=0、超总人数"""
        total = len(self.student_list)
        print(f"当前总学生数量：{total}名")
        while True:
            num_str = input("请输入需要点名的学生数量：").strip()
            try:
                num = int(num_str)
                if num <= 0:
                    print("[输入错误]点名人数必须大于0。")
                    continue
                if num > total:
                    print(f"[输入错误]点名人数({num})超过学生总人数({total}),请重新输入。")
                    continue
                # 随机抽取不重复学生
                pick_list = random.sample(self.student_list, num)
                print("本次随机点名结果：")
                for index, s in enumerate(pick_list, start=1):
                    print(f"{index}.{s.name} {s.sid}")
                break
            except ValueError:
                print(f"[输入错误]invalid Literal for int() with base 10:'{num_str}'")

    def generate_exam_arrangement(self):
        """功能5：随机打乱顺序，生成考场安排表.txt"""
        # 拷贝列表并打乱
        temp_stu = self.student_list.copy()
        random.shuffle(temp_stu)
        self.arrange_data.clear()
        # 写入文件
        with open("考场安排表.txt", "w", encoding="utf-8") as f:
            for seat, stu in enumerate(temp_stu, start=1):
                # 座位号,姓名,学号
                line = f"{seat},{stu.name},{stu.sid}\n"
                f.write(line)
                self.arrange_data.append({"seat": seat, "stu": stu})
        print("考场安排表.txt 生成成功！")

    def generate_admission_tickets(self):
        """功能6：创建准考证文件夹，每个学生单独txt准考证"""
        folder_name = "准考证"
        # 不存在则创建文件夹，存在不报错
        if not os.path.exists(folder_name):
            os.mkdir(folder_name)
        # 遍历座位数据生成准考证
        for item in self.arrange_data:
            seat_no = item["seat"]
            stu_obj = item["stu"]
            # 文件名：01.txt、02.txt...
            file_path = os.path.join(folder_name, f"{seat_no:02d}.txt")
            with open(file_path, "w", encoding="utf-8") as f:
                content = f"考场座位号:{seat_no}\n姓名:{stu_obj.name}\n学号:{stu_obj.sid}"
                f.write(content)
        print("全部准考证文件生成完毕，保存在【准考证】文件夹！")

    def run(self):
        """功能1：系统菜单主循环"""
        while True:
            print("===== 学生信息与考场管理系统 =====")
            print("1. 查询学生信息")
            print("2. 随机点名")
            print("3. 生成考场安排表")
            print("4. 生成准考证文件")
            print("+--------------------------------------------------------------------------")
            print("0. 退出系统")
            select = input("请输入功能编号：").strip()
            if select == "1":
                self.find_student()
            elif select == "2":
                self.random_roll_call()
            elif select == "3":
                self.generate_exam_arrangement()
            elif select == "4":
                self.generate_admission_tickets()
            elif select == "0":
                print("系统退出，感谢使用！")
                break
            else:
                print("功能编号不存在，请正确输入功能编号（0~4）：")
            print("-"*40)
            
