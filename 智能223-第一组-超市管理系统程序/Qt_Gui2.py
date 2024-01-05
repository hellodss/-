from datetime import datetime
from PyQt5 import QtWidgets, uic, QtCore,QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget,QTableWidgetItem
import sys
import pymysql

def db_connect(Host = 'localhost' , User = 'root', Password = '123456'):
    db = pymysql.connect(host= Host,
                     user=User,
                     password=Password,
                     database='supermarket')
    return db

def String_Datetime():
    # 获取当前日期和时间
    now = datetime.now()
    # 格式化日期为指定样式
    formatted_date = now.strftime("%Y%m%d")
    formatted_date2 = now.strftime("%Y-%m-%d")
    return formatted_date,formatted_date2

def calculate_age_and_gender(id_card_number,into_time):
    # 获取当前日期和时间
    now = datetime.now()
    # 将目标日期字符串转换为 datetime 对象
    target_date = datetime.strptime(into_time, "%Y-%m-%d")
    time_difference =now - target_date
    # 提取出时间间隔的天数部分并转换为年份
    years_until_target = int(time_difference.days / 365)
    # 将身份证号的出生日期提取出来
    birth_date = datetime.strptime(id_card_number[6:14], "%Y%m%d")
    
    # 计算年龄
    age = now.year - birth_date.year - ((now.month, now.day) < (birth_date.month, birth_date.day))
    
    # 获取性别（根据身份证号的倒数第2位）
    gender = '男' if int(id_card_number[-2]) % 2 != 0 else '女'
    
    return age, gender,years_until_target


class Login(QWidget):
    # 定义一个信号，包括一个字符串和一个整数参数
    Login_Signal = QtCore.pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        uic.loadUi('ui\\login.ui', self)
        self.pushButton.clicked.connect(self.TO_Xiaoshou)

    def TO_Xiaoshou(self):
        user = self.ip_lineEdit.text()
        password = self.password_lineEdit.text()
        # 发送信号，将获取到的文本和数字传递给槽函数
        self.Login_Signal.emit(user, password)

class Xiaoshou(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui\\xiaoshou.ui', self)
        self.db = db_connect()
        self.cur = self.db.cursor()
        self.Gnum = []
        self.Gaount = []
        self.JieSuan  = False
        self.jiru.clicked.connect(self.fun_jiru)
        self.shanchu.clicked.connect(self.deleteLastAppendedLine)
        self.jiesuan.clicked.connect(self.fun_jiesuan)
    def fun_jiru(self):
        # 获取输入的商品编号和数量
        input_Gnum = self.lineEdit.text()
        input_Gamount = int(self.lineEdit_2.text())  # 假设数量是整数

        # 查询商品表获取商品信息
        query = f"SELECT Gname, Gprice FROM Goods WHERE Gnum = '{input_Gnum}';"
        self.cur.execute(query)
        result = self.cur.fetchone()

        if result:
            Gname, Gprice = result
            total_amount = Gprice * input_Gamount


            # 显示在textBrowser上
            self.textBrowser.append(f"商品名称: {Gname} 单价: {Gprice} 数量: {input_Gamount} 总金额: {total_amount}\n")

            # 存储商品信息
            self.Gnum.append(input_Gnum)
            self.Gaount.append(input_Gamount)
        else:
            self.textBrowser.append(f"未找到商品编号为 {input_Gnum} 的商品信息\n")

    def deleteLastAppendedLine(self):
        # 获取当前所有文本
        all_text = self.textBrowser.toPlainText().split('\n')
        # 如果有至少两行文本，删除最后一行
        if len(all_text) >= 2:
            all_text.pop()  # 删除最后一行

            # 清空 textBrowser
            self.textBrowser.clear()

            # 重新添加除了最后一行之外的内容
            self.textBrowser.append('\n'.join(all_text[:-1]))
            self.Gnum.pop()
            self.Gaount.pop()
    def fun_jiesuan(self):
        #增加销售表格记录
        for i in range (len(self.Gnum)):
            date1,date2 =  String_Datetime()
            query1 = f"SELECT COUNT(*) FROM Trade" 
            self.cur.execute(query1)
            count = self.cur.fetchone()

            Tnum = "BDT" + date1 + str(count[0])
            query = f"INSERT INTO Trade VALUES ('{Tnum}', '{date2}', '202001', '{self.Gnum[i]}', {self.Gaount[i]}, (SELECT Gbid * {self.Gaount[i]} FROM Goods WHERE Gnum = '{self.Gnum[i]}'),'00001');"
            print(query)
            self.cur.execute(query)
            self.db.commit()
            print(i)

class Entry(QWidget):
    RuKuMessage = QtCore.pyqtSignal(str, str,str,str)
    def __init__(self):
        super().__init__()
        uic.loadUi('ui\\Entry.ui', self)
        self.jiru.clicked.connect(self.RuKu)
    def RuKu(self):
        text = self.lineEdit_2.text()
        text2 = self.lineEdit_3.text()
        text3 = self.lineEdit_4.text()
        text4 = self.lineEdit_5.text()
        self.RuKuMessage.emit(text, text2,text3,text4)
        print("发送成功")
class Exit(QWidget):
    OutKuMessage = QtCore.pyqtSignal(str,str,str)
    def __init__(self):
        super().__init__()
        uic.loadUi('ui\\Exit.ui', self)
        self.chuku.clicked.connect(self.OutKu)

    def OutKu(self):
        text = self.lineEdit.text()  #商品编号
        text2 = self.lineEdit_2.text() #出库量
        text3 = self.lineEdit_3.text() #出库员
        self.OutKuMessage.emit(text, text2,text3)
        print("发送成功！")

class Chaxun_changku(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui\\chaxun_changku.ui', self)
        self.chaxun.clicked.connect(self.Search_for)
    def Search_for(self):
        Date = self.lineEdit.text()
        KuNum = self.lineEdit_2.text()
        shangpin_num = self.lineEdit_3.text()
        # 构建 SQL 查询语句
        query = f"SELECT * FROM Entry WHERE 1=1"

        if Date:
            query += f" AND Edate LIKE '%{Date}%'"
        if KuNum:
            query += f" AND Enum LIKE '%{KuNum}%'"
        if shangpin_num:
            query += f" AND Gnum LIKE '%{shangpin_num}%'"

        # 执行查询
        conn = pymysql.connect(host='localhost', user='root', password='123456', database='supermarket')

        print('***',query)
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()

        # 获取列名
        column_names = [desc[0] for desc in cursor.description]
        # 设置表格的行数和列数
        self.Row = len(result)
        self.tableWidget.setRowCount(self.Row)
        self.tableWidget.setColumnCount(len(column_names))

        # 设置表格的列名
        self.tableWidget.setHorizontalHeaderLabels(column_names)
        # 将数据插入表格
        for row_index, row_data in enumerate(result):
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.tableWidget.setItem(row_index, col_index, item)
        # 调整表格列宽
        self.tableWidget.resizeColumnsToContents()
        # 关闭数据库连接
        cursor.close()
        conn.close()

        # 构建 SQL 查询语句
        query = f"SELECT * FROM Exits WHERE 1=1"

        if Date:
            query += f" AND Xdate LIKE '%{Date}%'"
        if KuNum:
            query += f" AND Xnum LIKE '%{KuNum}%'"
        if shangpin_num:
            query += f" AND Gnum LIKE '%{shangpin_num}%'"

        # 执行查询
        conn = pymysql.connect(host='localhost', user='root', password='123456', database='supermarket')

        print('***',query)
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()

        # 获取列名
        column_names = [desc[0] for desc in cursor.description]
        # 设置表格的行数和列数
        self.Row = len(result)
        self.tableWidget_2.setRowCount(self.Row)
        self.tableWidget_2.setColumnCount(len(column_names))

        # 设置表格的列名
        self.tableWidget_2.setHorizontalHeaderLabels(column_names)
        # 将数据插入表格
        for row_index, row_data in enumerate(result):
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.tableWidget_2.setItem(row_index, col_index, item)
        # 调整表格列宽
        self.tableWidget_2.resizeColumnsToContents()
        # 关闭数据库连接
        cursor.close()
        conn.close()

class Shangpin(QWidget):
    def __init__(self):
        super().__init__()
        self.entry = Entry()
        self.exit = Exit()
        self.chaxun = Chaxun_changku()
        uic.loadUi('ui\\cangku.ui', self)
        self.db = db_connect()
        self.cur = self.db.cursor()
        self.Row = None

        #连接入库窗口获取信息
        self.entry.RuKuMessage.connect(self.RuKu)
        self.exit.OutKuMessage.connect(self.OutKu)
        self.shangpin_show_table_data()
        self.shangpin_show_table_data2()
        self.pushButton.clicked.connect(self.Show_Entry)
        self.pushButton_2.clicked.connect(self.Show_Exit)
        self.pushButton_3.clicked.connect(self.shangpin_chaxun_show)

    def shangpin_chaxun_show(self):
        self.chaxun.show()

    def shangpin_show_table_data(self):
        # 修改以下参数为你的表格信息
        # 执行查询语句
        query = f"SELECT * FROM Entry WHERE DATE(Edate) = CURDATE();"
        self.cur.execute(query)
        # 获取查询结果
        result = self.cur.fetchall()
        # 获取列名
        column_names = [desc[0] for desc in self.cur.description]
        # 设置表格的行数和列数
        self.Row = len(result)
        self.tableWidget.setRowCount(self.Row)
        self.tableWidget.setColumnCount(len(column_names))

        # 设置表格的列名
        self.tableWidget.setHorizontalHeaderLabels(column_names)
        # 将数据插入表格
        for row_index, row_data in enumerate(result):
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.tableWidget.setItem(row_index, col_index, item)
        # 调整表格列宽
        self.tableWidget.resizeColumnsToContents()

    def shangpin_show_table_data2(self):
        # 修改以下参数为你的表格信息
        # 执行查询语句
        query = f"SELECT * FROM Exits WHERE DATE(Xdate) = CURDATE();"
        self.cur.execute(query)
        # 获取查询结果
        result = self.cur.fetchall()
        # 获取列名
        column_names = [desc[0] for desc in self.cur.description]
        # 设置表格的行数和列数
        self.Row = len(result)
        self.tableWidget_2.setRowCount(self.Row)
        self.tableWidget_2.setColumnCount(len(column_names))

        # 设置表格的列名
        self.tableWidget_2.setHorizontalHeaderLabels(column_names)
        # 将数据插入表格
        for row_index, row_data in enumerate(result):
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.tableWidget_2.setItem(row_index, col_index, item)
        # 调整表格列宽
        self.tableWidget_2.resizeColumnsToContents()


#商品入库按钮
    def Show_Entry(self):
        print("111")
        self.entry.show()

    def Show_Exit(self):
        self.exit.show()

    def RuKu(self,a,b,c,d):
        try:
            date1,date2 =  String_Datetime()
            Enum = "BDI" +  date1 + str(self.Row+1)
            print(Enum)
            #入库单编号 商品编号 入库量 总金额 供货商编号 入库日期 入库员编号
            query = f"INSERT INTO Entry VALUES ('{Enum}', {a}, {b}, (SELECT Gbid * {b} FROM Goods WHERE Gnum = {a}), {c}, '{date2}', (SELECT Snum FROM Staff WHERE Sname = '{d}');"
            query2 = f"update Goods set Gstock = Gstock + Eamount where Gnum = '{a}'; " 
            self.cur.execute(query)
            self.cur.execute(query2)
            self.db.commit()
            self.shangpin_show_table_data()
        except:
            print("入库失败")

    def OutKu(self, a,b,c):
        try:
            date1,date2 = String_Datetime()
            Xnum = "BDO" + date1 + str(self.Row+1)
            print(Xnum)
            print(a,b,c)
            query = f"INSERT INTO Exits VALUES ('{Xnum}', {b}, {c}, (SELECT Gbid * {c} FROM Goods WHERE Gnum = {b}),'{date2}', (SELECT Snum FROM Staff WHERE Sname = '{a}'));"
            query2 = f"update Goods set Gstock = Gstock - Xamount where Gnum = '{a}'; " 
            self.cur.execute(query)
            self.db.commit()
            self.shangpin_show_table_data2()
        except Exception as e:
            print(e)

class Chaxun_Goods(QWidget):
    SearchFor_goods_message = QtCore.pyqtSignal(str, str,str,str,str)
    def __init__(self):
        super().__init__()
        uic.loadUi('ui\\chaxun_caigou.ui', self)
        self.pushButton.clicked.connect(self.send_chaxun_message)

    def send_chaxun_message(self):
        text = self.lineEdit.text()  #商品类别
        text2 = self.lineEdit_4.text() #商品名称
        text3 = self.lineEdit_3.text() #商品编号
        text4 = self.lineEdit_2.text() #商品进价
        text5 = self.lineEdit_5.text() #商品售价
        self.SearchFor_goods_message.emit(text, text2,text3,text4,text5)
        print("发送：",text, text2,text3,text4,text5)


class Tianjia_Goods(QWidget):
    Add_goods_message = QtCore.pyqtSignal(str, str,str,str,str)
    def __init__(self):
        super().__init__()
        uic.loadUi('ui\\tianjia_caigou.ui', self)
        self.pushButton.clicked.connect(self.send_tianjia_message)

    def send_tianjia_message(self):
        text = self.lineEdit.text()  #商品类别
        text2 = self.lineEdit_4.text() #商品名称
        text4 = self.lineEdit_2.text() #商品进价
        text5 = self.lineEdit_5.text() #商品售价
        text3 = self.lineEdit_6.text() #供货商
        self.Add_goods_message.emit(text, text2,text4,text5,text3)
        print("发送：",text, text2,text4,text5,text3)

class ShanChu_Goods(QWidget):
    Delet_goods_message = QtCore.pyqtSignal(str, str,str)
    def __init__(self):
        super().__init__()
        uic.loadUi('ui\\shanchu_caigou.ui', self)
        self.pushButton.clicked.connect(self.send_shanchu_message)
    def send_shanchu_message(self):
        text = self.lineEdit.text()  #商品类别
        text2 = self.lineEdit_2.text() #编号
        text3 = self.lineEdit_3.text() #名称
        self.Delet_goods_message.emit(text, text2,text3)
        print("发送：",text, text2,text3)

class Xiugai_Goods(QWidget):
    Change_goods_message = QtCore.pyqtSignal(str, str,str)
    def __init__(self):
        super().__init__()
        uic.loadUi('ui\\xiugai_caigou.ui', self)
        self.pushButton.clicked.connect(self.send_tianjia_message)

    def send_tianjia_message(self):
        text = self.lineEdit.text()  #商品编号
        text2 = self.lineEdit_2.text() #修改项
        text3 = self.lineEdit_3.text() #修改内容
        self.Change_goods_message.emit(text, text2,text3)
        print("发送：",text, text2,text3)

class Gong_People_Zen(QWidget):
    Add_People_message = QtCore.pyqtSignal(str, str,str)
    def __init__(self):
        super().__init__()
        uic.loadUi('ui\\gong_people_zen.ui', self)
        self.pushButton.clicked.connect(self.send_tianjia_message)

    def send_tianjia_message(self):
        text = self.lineEdit_2.text()  #名称
        text2 = self.lineEdit_3.text() #地址
        text3 = self.lineEdit_4.text() #电话
        self.Add_People_message.emit(text, text2,text3)
        print("发送：",text, text2,text3)

class Gong_People_Shan(QWidget):
    Dle_People_message = QtCore.pyqtSignal(str, str,str)
    def __init__(self):
        super().__init__()
        uic.loadUi('ui\\gong_people_shan.ui', self)
        self.pushButton.clicked.connect(self.send_tianjia_message)

    def send_tianjia_message(self):
        text = self.lineEdit.text()  #编号
        text2 = self.lineEdit_2.text() #名称
        text3 = self.lineEdit_3.text() #地址
        self.Dle_People_message.emit(text, text2,text3)
        print("发送：",text, text2,text3)

class Gong_People_Gai(QWidget):
    Change_People_message = QtCore.pyqtSignal(str, str,str)
    def __init__(self):
        super().__init__()
        uic.loadUi('ui\\gong_people_gai.ui', self)
        self.pushButton.clicked.connect(self.send_tianjia_message)

    def send_tianjia_message(self):
        text = self.lineEdit.text()  #编号
        text2 = self.lineEdit_2.text() #名称
        text3 = self.lineEdit_3.text() #地址
        self.Change_People_message.emit(text, text2,text3)
        print("发送：",text, text2,text3)

class Gong_People_Cha(QWidget):
    Search_People_message = QtCore.pyqtSignal(str, str,str,str)
    def __init__(self):
        super().__init__()
        uic.loadUi('ui\\gong_people_cha.ui', self)
        self.pushButton.clicked.connect(self.send_tianjia_message)

    def send_tianjia_message(self):
        text = self.lineEdit_2.text()  #名称
        text2 = self.lineEdit_3.text() #地址
        text3 = self.lineEdit_4.text() #电话
        text4 = self.lineEdit_5.text() #编号
        self.Search_People_message.emit(text, text2,text3,text4)
        print("发送：",text, text2,text3,text4)

class GongYing_People(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui\\caigou_gong_people.ui', self)
        self.db = db_connect()
        self.cur = self.db.cursor()
        self.gong_people_zen = Gong_People_Zen()
        self.gong_people_zen.Add_People_message.connect(self.get_zen_message)
        self.gong_people_shan = Gong_People_Shan()
        self.gong_people_shan.Dle_People_message.connect(self.get_shan_message)
        self.gong_people_gai = Gong_People_Gai()
        self.gong_people_gai.Change_People_message.connect(self.get_gai_message)
        self.gong_people_cha = Gong_People_Cha()
        self.gong_people_cha.Search_People_message.connect(self.get_cha_message)
        self.show_gong_people("SELECT * FROM Vendor")
        self.pushButton.clicked.connect(self.zen_show)
        self.pushButton_2.clicked.connect(self.shan_show)
        self.pushButton_3.clicked.connect(self.gai_show)
        self.pushButton_4.clicked.connect(self.cha_show)

    def zen_show(self):
        self.gong_people_zen.show()
    def shan_show(self):
        self.gong_people_shan.show()
    def gai_show(self):
        self.gong_people_gai.show()
    def cha_show(self):
        self.gong_people_cha.show()

    def get_shan_message(self,a,b,c):
         # 构建 SQL 查询语句
        query1 = f"SELECT * FROM Vendor WHERE 1=1"

        if a:
            query1 += f" AND Vnum LIKE '%{a}%'"
        if b:
            query1 += f" AND Vpalce LIKE '%{c}%'"
        if c:
            query1 += f" AND Vname LIKE '%{b}%'"

        self.show_gong_people(query1)
        query2 = f"DELETE FROM Entry WHERE Vnum = '{a}'"
        query = f"DELETE FROM Vendor WHERE Vnum = '{a}'"

        if a:
            query += f" AND Vname LIKE '%{b}%'"
        if b:
            query += f" AND Vpalce LIKE '%{c}%'"
        self.cur.execute(query2)
        self.db.commit()
        self.cur.execute(query)
        self.db.commit()
    def get_gai_message(self,a,b,c):
        query = f"UPDATE Vendor SET {b} = '{c}' WHERE Vnum = '{a}';"
        print(query)
        try:
            # 执行 SQL 语句
            self.cur.execute(query)
            # 提交事务
            self.db.commit()
            print("数据修改成功！")
            self.show_gong_people( f"SELECT * FROM Vendor WHERE Vnum = '{a}' ")
        except Exception as e:
            # 如果发生错误，回滚事务并打印错误信息
            self.db.rollback()
            print(f"数据修改失败：{e}")

    def get_cha_message(self,a,b,c,e):
        try:
            # 构建 SQL 查询语句
            query = f"SELECT * FROM Vendor WHERE 1=1"

            if a:
                query += f" AND Vname LIKE '%{a}%'"
            if b:
                query += f" AND Vplace LIKE '%{b}%'"
            if c:
                query += f" AND Vphone LIKE '%{c}%'"
            if e:
                query += f" AND Vnum LIKE '%{e}%'"
            self.show_gong_people(query)
        except Exception as e:
            print(e)
            
    def get_zen_message(self,a,b,c):
        # 构建 SQL 查询语句
        try:
            query1 = "SELECT COUNT(*) FROM Vendor" 
            self.cur.execute(query1)
            count = self.cur.fetchone()
            print(count)
            Vnum = "1000" + str(count[0])
            query = f"INSERT INTO Vendor VALUES ('{Vnum}', '{a}', '{b}',{c});"
            print(query)
            self.cur.execute(query)
            self.db.commit()
            self.show_gong_people(f"SELECT * FROM Vendor WHERE Vnum='{Vnum}';")
        except Exception as e:
            print(e)

    def show_gong_people(self, query):
        try:
            # 修改以下参数为你的表格信息
            # 执行查询语句
            self.cur.execute(query)
            # 获取查询结果
            result = self.cur.fetchall()
            # 获取列名
            column_names = [desc[0] for desc in self.cur.description]
            # 设置表格的行数和列数
            self.Row = len(result)
            self.tableWidget.setRowCount(self.Row)
            self.tableWidget.setColumnCount(len(column_names))

            # 设置表格的列名
            self.tableWidget.setHorizontalHeaderLabels(column_names)
            # 将数据插入表格
            for row_index, row_data in enumerate(result):
                for col_index, cell_data in enumerate(row_data):
                    item = QTableWidgetItem(str(cell_data))
                    self.tableWidget.setItem(row_index, col_index, item)
            # 调整表格列宽
            self.tableWidget.resizeColumnsToContents()
        except Exception as e:
            print(e)
    def send_tianjia_message(self):
        text = self.lineEdit.text()  #商品编号
        text2 = self.lineEdit_2.text() #修改项
        text3 = self.lineEdit_3.text() #修改内容
        self.Change_goods_message.emit(text, text2,text3)
        print("发送：",text, text2,text3)


class Caigou(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui\\caigou.ui', self)
        self.chaxun = Chaxun_Goods()
        self.tianjia = Tianjia_Goods()
        self.shanchu = ShanChu_Goods()
        self.xiugai = Xiugai_Goods()
        self.gong_people = GongYing_People()
        self.db = db_connect()
        self.cur = self.db.cursor()
        self.show_goods( "SELECT * FROM Goods")
        self.chaxun.SearchFor_goods_message.connect(self.get_chaxun_message)
        self.tianjia.Add_goods_message.connect(self.get_tianjia_message)
        self.shanchu.Delet_goods_message.connect(self.get_shanchu_message)
        self.xiugai.Change_goods_message.connect(self.get_xiugai_message)

        self.pushButton_2.clicked.connect(self.caigou_chaxun_show)
        self.pushButton_4.clicked.connect(self.caigou_tianjia_show)
        self.pushButton_3.clicked.connect(self.caigou_shanchu_show)
        self.pushButton_5.clicked.connect(self.caigou_xiugai_show)
        self.pushButton.clicked.connect(self.gong_people_show)
    
    def gong_people_show(self):
        self.gong_people.show()

    def get_xiugai_message(self,a,b,c):

        query = f"UPDATE Goods SET {b} = {c} WHERE Gnum = '{a}';"
        try:
            # 执行 SQL 语句
            self.cur.execute(query)
            # 提交事务
            self.db.commit()
            print("数据修改成功！")
            self.show_goods( f"SELECT * FROM Goods WHERE Gnum = {a} ")
        except Exception as e:
            # 如果发生错误，回滚事务并打印错误信息
            self.db.rollback()
            print(f"数据修改失败：{e}")

    def caigou_xiugai_show(self):
        self.xiugai.show()
    def caigou_chaxun_show(self):
        self.chaxun.show()
    def get_tianjia_message(self,a,b,c,d,e):
        try:
            # 构建 SQL 查询语句
            query1 = f"SELECT COUNT(*) FROM Goods" 
            self.cur.execute(query1)
            count = self.cur.fetchone()
            print(count)
            Gnum = "2000" + str(count[0]+1)
            query = f"INSERT INTO Goods VALUES ('{Gnum}', '{b}', '{a}',{d}, {c}, 0,50,500,{e});"
            print(query)
            self.cur.execute(query)
            self.db.commit()
            self.show_goods(f"SELECT * FROM Goods WHERE Gnum='{Gnum}';")
        except Exception as e  :
            print(e)

    def caigou_tianjia_show(self):
        self.tianjia.show()
    def get_chaxun_message(self,a,b,c,d,e):
        # 构建 SQL 查询语句
        query = f"SELECT * FROM Goods WHERE 1=1"

        if a:
            query += f" AND Gtype LIKE '%{a}%'"
        if b:
            query += f" AND Gname LIKE '%{b}%'"
        if c:
            query += f" AND Gnum LIKE '%{c}%'"

        if d:
            query += f" AND Gbid LIKE '%{c}%'"

        if e:
            query += f" AND Gprice LIKE '%{e}%'"
        self.show_goods(query)


    def caigou_shanchu_show(self):
        self.shanchu.show()

    def get_shanchu_message(self,a,b,c):
        # 构建 SQL 查询语句
        query1 = f"SELECT * FROM Goods WHERE 1=1"

        if a:
            query1 += f" AND Gtype LIKE '%{a}%'"
        if b:
            query1 += f" AND Gname LIKE '%{c}%'"
        if c:
            query1 += f" AND Gnum LIKE '%{b}%'"

        self.show_goods(query1)


        query2 = f"DELETE FROM Entry WHERE Gnum = '{b}'"
        query3 = f"DELETE FROM Exits WHERE Gnum = '{b}'"
        query4 = f"DELETE FROM Trade WHERE Gnum = '{b}'"
        query5 = f"DELETE FROM Infor WHERE Gnum = '{b}'"




        query = f"DELETE FROM Goods WHERE Gnum = '{b}'"

        if a:
            query += f" AND Gtype LIKE '%{a}%'"
        if b:
            query += f" AND Gname LIKE '%{c}%'"
        self.cur.execute(query2)
        self.cur.execute(query3)
        self.cur.execute(query4)
        self.cur.execute(query5)

        self.db.commit()
        self.cur.execute(query)
        self.db.commit()
    def show_goods(self,query):
        # 执行查询语句
        self.cur.execute(query)
        # 获取查询结果
        result = self.cur.fetchall()
        # 获取列名
        column_names = [desc[0] for desc in self.cur.description]
        # 设置表格的行数和列数
        self.Row = len(result)
        self.tableWidget.setRowCount(self.Row)
        self.tableWidget.setColumnCount(len(column_names))

        # 设置表格的列名
        self.tableWidget.setHorizontalHeaderLabels(column_names)
        # 将数据插入表格
        for row_index, row_data in enumerate(result):
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.tableWidget.setItem(row_index, col_index, item)
        # 调整表格列宽
        self.tableWidget.resizeColumnsToContents()

class Staff_Zen(QWidget):
    Add_Staff_message = QtCore.pyqtSignal(str, str,str,str,str,str)
    def __init__(self):
        super().__init__()
        uic.loadUi('ui\\renshi_staff_zen.ui', self)
        self.pushButton.clicked.connect(self.send_tianjia_message)

    def send_tianjia_message(self):
        text = self.lineEdit_2.text()  #名称
        text2 = self.lineEdit_3.text() #身份证
        text3 = self.lineEdit_4.text() #部门
        text4 = self.lineEdit_5.text() #电话
        text5 = self.lineEdit_6.text() #工资
        text6 = self.lineEdit_7.text() #时间

        self.Add_Staff_message.emit(text, text2,text3,text4,text5,text6)
        print("发送：",text, text2,text4,text5,text6)

class Staff_Shan(QWidget):
    Del_Staff_message = QtCore.pyqtSignal(str, str,str,str)
    def __init__(self):
        super().__init__()
        uic.loadUi('ui\\renshi_staff_shan.ui', self)
        self.pushButton.clicked.connect(self.send_shan_message)

    def send_shan_message(self):
        text = self.lineEdit_2.text()  #名称
        text2 = self.lineEdit_3.text() #编号
        text3 = self.lineEdit_4.text() #部门
        text5 = self.lineEdit_6.text() #工资

        self.Del_Staff_message.emit(text, text2,text3,text5)
        print("发送：",text, text2,text3,text5,)

class Staff_Gai(QWidget):
    Change_Staff_message = QtCore.pyqtSignal(str, str,str)
    def __init__(self):
        super().__init__()
        uic.loadUi('ui\\Staff_gai.ui', self)
        self.pushButton.clicked.connect(self.send_gai_message)

    def send_gai_message(self):
        text = self.lineEdit.text()  #编号
        text2 = self.lineEdit_2.text() 
        text3 = self.lineEdit_3.text() 
        self.Change_Staff_message.emit(text, text2,text3)
        print("发送：",text, text2,text3)


class Renshi(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui\\renshi.ui', self)
        self.db = db_connect()
        self.cur = self.db.cursor()
        self.staff_zen = Staff_Zen()
        self.staff_zen.Add_Staff_message.connect(self.get_staff_zen_message)

        self.staff_shan = Staff_Shan()
        self.staff_shan.Del_Staff_message.connect(self.get_staff_shan_message)

        self.staff_gai = Staff_Gai()
        self.staff_gai.Change_Staff_message.connect(self.get_staff_gai_message)

        self.show_staffs("SELECT * FROM Staff")
        self.pushButton.clicked.connect(self.Search_Staff)
        self.pushButton_2.clicked.connect(self.staff_zen_show)
        self.pushButton_3.clicked.connect(self.staff_shan_show)
        self.pushButton_4.clicked.connect(self.staff_gai_show)

    def staff_zen_show(self):
        self.staff_zen.show()
    def staff_shan_show(self):
        self.staff_shan.show()
    def staff_gai_show(self):
        self.staff_gai.show()

    def Search_Staff(self):
         # 构建 SQL 查询语句
        a = self.lineEdit.text()
        b = self.lineEdit_2.text()
        c =  self.lineEdit_3.text()
        d = self.lineEdit_4.text()
        e = self.lineEdit_5.text()

        query = f"SELECT * FROM Staff WHERE 1=1"

        if a:
            query += f" AND Spart LIKE '%{a}%'"
        if b:
            query += f" AND Snum LIKE '%{b}%'"
        if c:
            query += f" AND Sname LIKE '%{c}%'"
        if d:
            query += f" AND Ssalary LIKE '%{d}%'"
        if e:
            query += f" AND Ssex LIKE '%{e}%'"
        self.show_staffs(query)
    def get_staff_zen_message(self,a,b,c,d,e,f):
         # 构建 SQL 查询语句
        query1 = "SELECT COUNT(*) Staff " 
        self.cur.execute(query1)
        count = self.cur.fetchone()
        print(count)
        Snum = f + str(count[0])
        age, gender,time_difference = calculate_age_and_gender(b,f)

        query = f"INSERT INTO Staff VALUES ('{Snum}', '{a}', '{gender}',{age}, '{time_difference}','{d}','{b}','{c}','{e}');"
        print(query)
        self.cur.execute(query)
        self.db.commit()
        self.show_staffs(f"SELECT * FROM Staff WHERE Snum='{Snum}';")

    def get_staff_shan_message(self,a,b,c,d):
        # 构建 SQL 查询语句
        query1 = f"SELECT * FROM Staff WHERE 1=1"

        if a:
            query1 += f" AND Sname LIKE '%{a}%'"
        if b:
            query1 += f" AND Snum LIKE '%{b}%'"
        if c:
            query1 += f" AND Spart LIKE '%{c}%'"

        self.show_staffs(query1)

        query2 = f"DELETE FROM Entry WHERE Snum = '{b}'"
        query3 = f"DELETE FROM Exits WHERE Snum = '{b}'"
        query4 = f"DELETE FROM Trade WHERE Snum = '{b}'"

        query = f"DELETE FROM Staff WHERE Snum = '{b}'"

        if a:
            query += f" AND Sname LIKE '%{a}%'"
        if c:
            query += f" AND Spart LIKE '%{c}%'"

        if d:
            query += f" AND Ssalary LIKE '%{d}%'"

        self.cur.execute(query2)
        self.cur.execute(query3)
        self.cur.execute(query4)

        self.db.commit()
        self.cur.execute(query)
        self.db.commit()

    def get_staff_gai_message(self,a,b,c):
        query = f"UPDATE Staff SET {b} = {c} WHERE Snum = '{a}';"
        try:
            # 执行 SQL 语句
            self.cur.execute(query)
            # 提交事务
            self.db.commit()
            print("数据修改成功！")
            self.show_staffs( f"SELECT * FROM Staff WHERE Snum = {a} ")
        except Exception as e:
            # 如果发生错误，回滚事务并打印错误信息
            self.db.rollback()
            print(f"数据修改失败：{e}")
    def show_staffs(self,query):
        # 修改以下参数为你的表格信息
        # 执行查询语句
        self.cur.execute(query)
        # 获取查询结果
        result = self.cur.fetchall()
        # 获取列名
        column_names = [desc[0] for desc in self.cur.description]
        # 设置表格的行数和列数
        self.Row = len(result)
        self.tableWidget.setRowCount(self.Row)
        self.tableWidget.setColumnCount(len(column_names))

        # 设置表格的列名
        self.tableWidget.setHorizontalHeaderLabels(column_names)
        # 将数据插入表格
        for row_index, row_data in enumerate(result):
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.tableWidget.setItem(row_index, col_index, item)
        # 调整表格列宽
        self.tableWidget.resizeColumnsToContents()


class Controller:
    def __init__(self):
        self.login = Login()
        self.xiaoshou = Xiaoshou()
        self.shangpin = Shangpin()
        self.renshi = Renshi()
        self.caigou = Caigou()
        self.login.show()

        # 连接 Login 对象的 Login_Signal 信号到槽函数 SwitchToXiaoshou
        self.login.Login_Signal.connect(self.SwitchToXiaoshou)



    def SwitchToXiaoshou(self, user, password):
        print("接收到消息:", user, password)
        if user == '销售' and password == '888888':
            self.login.close()
            self.xiaoshou.show()
        elif user == '仓库' and password == '888888':
            self.login.close()
            self.shangpin.show()
        elif user == '人事' and password == '888888':
            self.login.close()
            self.renshi.show()
        elif user == '采购' and password == '888888':
            self.login.close()
            self.caigou.show()
        else:
            QtWidgets.QMessageBox.warning(self.login, '警告', '用户名或密码错误')

if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    myapp = Controller()
    sys.exit(app.exec_())