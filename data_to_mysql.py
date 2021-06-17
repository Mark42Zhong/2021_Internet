import pandas as pd
import pymysql

import numpy as np


# region[i]
# 0——珠三角 1——粤东  2——粤西   3——粤北
region_name = ['珠三角', '粤东', '粤西', '粤北']
region = [[] for i in range(4)]

# school[i]
# 0——乡镇小学     1——乡镇中学     2——城区小学     3——城区中学
school_name = ['乡镇小学', '乡镇中学', '城区小学', '城区中学']
school = [[] for j in range(4)]

# grades[i]   i:年级
grade_name = ['一年级', '二年级', '三年级', '四年级', '五年级', '六年级', '初一', '初二', '初三', '高一', '高二', '高三']
grade = [[] for k in range(12)]


# 数据清洗
def data_filter(data):
    if not (isinstance(data[29], float) or isinstance(data[29], int)):
        return False
    region_filter = [1, 2, 3, 4]
    school_filter = [1, 2, 3, 4]
    grade_filter = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    if (data[-2] in region_filter) and (data[-1] in school_filter) and (data[8] in grade_filter) \
            and (0 <= data[29] <= 15):
        return True
    return False


def read_data(path):
    count = 0
    global region, school, grade
    # 将数据进行分类
    # data_reader = pd.read_csv(path, iterator=True, chunksize=1000)
    data_reader = pd.read_csv(path, iterator=True)

    for i in range(8):
        df = data_reader.get_chunk(10000)
        df = df.to_numpy()
        df = df.tolist()

        conn = pymysql.connect(host='localhost', user='root', password='123456', db='2021internet', charset='utf8')
        cursor = conn.cursor()

        for row in df:
            if data_filter(row):
                input_data = row[8:]
                input_data.insert(0, row[1])

                sql = "INSERT INTO data_set VALUES" + str(tuple(input_data))

                cursor.execute(sql)  # 执行SQL语句`


                # 地区初始化
                region[row[-2] - 1].append(row[8:])
                # 学校类型初始化
                school[int(row[-1] - 1)].append(row[8:])
                # # 年级初始化
                grade[row[8] - 1].append(row[8:])

        conn.commit()  # 提交数据
        cursor.close()  # 关闭游标
        conn.close()  # 关闭数据库


    for i in range(4):
        region[i] = np.array(region[i]).astype(np.int)
        school[i] = np.array(school[i]).astype(np.int)
    for i in range(12):
        grade[i] = np.array(grade[i]).astype(np.int)


if __name__ == "__main__":
    path = r'D:/80万样本数据.CSV'
    read_data(path)
