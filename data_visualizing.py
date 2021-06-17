from collections import Counter

import numpy as np
import pandas as pd
from pyecharts.charts import *
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ChartType

save_path = r'./templates'

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


# 数据导入，处理
def data_initial(path):
    count = 0
    global region, school, grade
    # 将数据进行分类
    # data_reader = pd.read_csv(path, iterator=True, chunksize=1000)
    data_reader = pd.read_csv(path, iterator=True)

    # for chunk in data_reader:
    #     df = chunk
    #     df = df.to_numpy()
    #     df = df.tolist()
    #
    #     for row in df:
    #         if data_filter(row):
    #             count += 1
    #             # 地区初始化
    #             region[row[-2] - 1].append(row[8:])
    #             # 学校类型初始化
    #             school[int(row[-1] - 1)].append(row[8:])
    #             # # 年级初始化
    #             grade[row[8] - 1].append(row[8:])
    # print(count)

    for i in range(8):
        df = data_reader.get_chunk(10000)
        df = df.to_numpy()
        df = df.tolist()

        for row in df:
            if data_filter(row):
                count += 1
                # 地区初始化
                region[row[-2] - 1].append(row[8:])
                # 学校类型初始化
                school[int(row[-1] - 1)].append(row[8:])
                # # 年级初始化
                grade[row[8] - 1].append(row[8:])
    print(count)
    for i in range(4):
        region[i] = np.array(region[i]).astype(np.int)
        school[i] = np.array(school[i]).astype(np.int)
    for i in range(12):
        grade[i] = np.array(grade[i]).astype(np.int)


# 地区、学校、年级人数分布图——暂时为饼图
def show_q1_q2():
    region_count = [len(region[i]) for i in range(4)]
    region_pie = (
        Pie(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
        .add("", [list(z) for z in zip(region_name, region_count)], center=["75%", "50%"], radius=[0, 160])
        .set_global_opts(title_opts=opts.TitleOpts(title="调查问卷来源分布——不同地区"))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        # .render(save_path + r"\q1_q2\region_count.html")
    )

    cities = ['广州市', '佛山市', '肇庆市', '深圳市', '东莞市', '惠州市', '珠海市', '中山市', '江门市',
              '汕头市', '汕尾市', '潮州市', '揭阳市',
              '湛江市', '茂名市', '阳江市', '云浮市',
              '韶关市', '河源市', '清远市', '梅州市']
    res = []
    res.extend([region_count[0]] * 9)
    res.extend([region_count[1]] * 4)
    res.extend([region_count[2]] * 4)
    res.extend([region_count[3]] * 4)

    region_map = (
        Map(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
        .add("", [list(z) for z in zip(cities, res)], "广东", center=[116.262738,22.602573])
        .set_global_opts(
            title_opts=opts.TitleOpts(title="调查问卷来源分布——不同地区"), visualmap_opts=opts.VisualMapOpts(max_=31834, min_=8620)
        )
        # .render(save_path + r'\q1_q2\map_guangdong.html')
    )

    grid = (
        Grid(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
        .add(region_map, grid_opts=opts.GridOpts(pos_left="10%"))
        .add(region_pie, grid_opts=opts.GridOpts(pos_top="50%", pos_right="75%"))
        .render(save_path + r'/q1_q2/grid.html')
    )

    school_count = [len(school[i]) for i in range(4)]
    c = (
        Pie(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
        .add("", [list(z) for z in zip(school_name, school_count)])
        .set_global_opts(title_opts=opts.TitleOpts(title="调查问卷来源分布——不同学校类型"))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        .render(save_path + r"\q1_q2\school_count.html")
    )

    grade_count = [len(grade[i]) for i in range(12)]
    c = (
        Pie(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
        .add("", [list(z) for z in zip(grade_name, grade_count)])
        .set_global_opts(title_opts=opts.TitleOpts(title="调查问卷来源分布——不同年级"))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        .render(save_path + r"\q1_q2\grade_count.html")
    )


def show_q4_q9_q10_q11():
    q4_name = ['回看教程视频', '作业提交', '随堂测试', '视频会议', '作业批改反馈', '课堂发言', '班级通知', '班级圈', '优秀作业查看', '线上学科竞赛游戏', '屏幕共享', '弹幕',
               '讨论']
    q9_name = ['直播', '录播', '资源包', '电视课堂', '直播+录播', '直播+资源包', '录播+资源包', '直播+录播+资源包', '录播+资源包+线上辅导答疑']
    q10_name = ['学科课程新课', '学科课程复习', '音美体劳教育', '专题教育']
    q11_name = ['查阅线上资源自主解决', '通过学习平台的视频回放', '教室集中时间线上答疑', '利用微信、钉钉等社交平台', '同学互相交流', '暂时放下，待以后解决']

    # q4_pie
    q4_res = [0] * 13
    for i in range(4):
        for j in range(7, 20):
            q4_res[j - 7] += np.sum(region[i][:, j]).item()

    # q9_pie 24 32
    q9_res = [0] * 9
    for i in range(4):
        for j in range(24, 33):
            q9_res[j - 24] += np.sum(region[i][:, j]).item()

    # q10_pie 33 36
    q10_res = [0] * 4
    for i in range(4):
        for j in range(33, 37):
            q10_res[j - 33] += np.sum(region[i][:, j]).item()

    # q11_pie 37 42
    q11_res = [0] * 6
    for i in range(4):
        for j in range(37, 43):
            q11_res[j - 37] += np.sum(region[i][:, j]).item()

    q4_pie = (
        Pie(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
            .add("", [list(z) for z in zip(q4_name, q4_res)], center=["20%", "20%"], radius=[0, 120])
            .set_global_opts(title_opts=opts.TitleOpts(title="教育平台功能使用数"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
            .set_global_opts(legend_opts=opts.LegendOpts(type_="scroll", pos_left="40%", orient="vertical"))
            # .render(save_path + r"\q4_q9_q10_q11\q4.html")
    )

    q9_pie = (
        Pie(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
            .add("", [list(z) for z in zip(q9_name, q9_res)], center=["70%", "20%"], radius=[0, 120])
            .set_global_opts(title_opts=opts.TitleOpts(title="线上课堂组织形式"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
            .set_global_opts(legend_opts=opts.LegendOpts(type_="scroll", pos_left="90%", orient="vertical"))
            # .render(save_path + r"\q4_q9_q10_q11\q9.html")
    )

    q10_pie = (
        Pie(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
            .add("", [list(z) for z in zip(q10_name, q10_res)], center=["20%", "70%"], radius=[0, 120])
            .set_global_opts(title_opts=opts.TitleOpts(title="线上课程内容分布"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
            .set_global_opts(
            legend_opts=opts.LegendOpts(type_="scroll", pos_left="40%", pos_top="50%", orient="vertical"))
            # .render(save_path + r"\q4_q9_q10_q11\q10.html")
    )

    q11_pie = (
        Pie(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
            .add("", [list(z) for z in zip(q11_name, q11_res)], center=["70%", "70%"], radius=[0, 120])
            .set_global_opts(title_opts=opts.TitleOpts(title="解决未掌握知识的方法"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
            .set_global_opts(
            legend_opts=opts.LegendOpts(type_="scroll", pos_left="90%", pos_top="50%", orient="vertical"))
            # .render(save_path + r"\q4_q9_q10_q11\q11.html")
    )

    grid = (
        Grid(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
            .add(q4_pie, grid_opts=opts.GridOpts(pos_bottom="25%"))
            .add(q9_pie, grid_opts=opts.GridOpts(pos_bottom="25%"))
            .add(q10_pie, grid_opts=opts.GridOpts(pos_bottom="25%"))
            .add(q11_pie, grid_opts=opts.GridOpts(pos_bottom="25%"))

            .render(save_path + r"\q4_q9_q10_q11\q4_q9_q10_q11.html")
    )


# 线上学习使用的材料——饼图
def show_q3():
    q3_name = ['电视', '台式电脑或笔记本电脑', '平板', '手机', '音频(广播、录音)', '纸质学习资料']

    # 地区  1 6
    q3_res = [[] for i in range(4)]

    for i in range(4):
        for j in range(1, 7):
            q3_res[i].append(np.sum(region[i][:, j]).item())

    fn_1 = """
        function() {
            return '珠三角';
        }
        """
    fn_2 = """
        function() {
            return '粤东';
        }
        """

    fn_3 = """
        function() {
            return '粤西';
        }
        """

    fn_4 = """
        function() {
            return '粤北';
        }
        """

    def new_label_opts(fn):
        return opts.LabelOpts(formatter=JsCode(fn), position="center")

    c = (
        Pie(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
            .add(
            "",
            [list(z) for z in zip(q3_name, q3_res[0])],
            center=["20%", "30%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_1),
        )
            .add(
            "",
            [list(z) for z in zip(q3_name, q3_res[1])],
            center=["55%", "30%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_2),
        )
            .add(
            "",
            [list(z) for z in zip(q3_name, q3_res[2])],
            center=["20%", "70%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_3),
        )
            .add(
            "",
            [list(z) for z in zip(q3_name, q3_res[3])],
            center=["55%", "70%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_4),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="线上学习使用的设备/材料分布——不同地区"),
            legend_opts=opts.LegendOpts(
                type_="scroll", pos_top="20%", pos_left="80%", orient="vertical"
            ),
        )
            .render(save_path + r"\q3\region.html")
    )

    # 学校   1 6
    q3_res = [[] for i in range(4)]

    for i in range(4):
        for j in range(1, 7):
            q3_res[i].append(np.sum(school[i][:, j]).item())

    fn_1 = """
            function() {
                return '乡镇小学';
            }
            """
    fn_2 = """
            function() {
                return '乡镇中学';
            }
            """

    fn_3 = """
            function() {
                return '城区小学';
            }
            """

    fn_4 = """
            function() {
                return '城区中学';
            }
            """

    def new_label_opts(fn):
        return opts.LabelOpts(formatter=JsCode(fn), position="center")

    c = (
        Pie(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
            .add(
            "",
            [list(z) for z in zip(q3_name, q3_res[0])],
            center=["20%", "30%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_1),
        )
            .add(
            "",
            [list(z) for z in zip(q3_name, q3_res[1])],
            center=["55%", "30%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_2),
        )
            .add(
            "",
            [list(z) for z in zip(q3_name, q3_res[2])],
            center=["20%", "70%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_3),
        )
            .add(
            "",
            [list(z) for z in zip(q3_name, q3_res[3])],
            center=["55%", "70%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_4),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="线上学习使用的设备/材料分布——不同学校类型"),
            legend_opts=opts.LegendOpts(
                type_="scroll", pos_top="20%", pos_left="80%", orient="vertical"
            ),
        )
            .render(save_path + r"\q3\school.html")
    )

    # 总体
    q3_res = [0] * 6

    for j in range(1, 7):
        for i in range(4):
            q3_res[j - 1] += np.sum(region[i][:, j]).item()

    total = 0
    for i in range(6):
        total += q3_res[i]

    q3_res_pie = []
    for i in range(6):
        q3_res_pie.append(round(q3_res[i] / total, 2))

    pie_3 = (
        Pie(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
            .add("", [list(z) for z in zip(q3_name, q3_res_pie)], radius=160, center=["20%", "40%"])
            .set_global_opts(
            title_opts=opts.TitleOpts(title="线上学习使用的设备/材料分布"),
            legend_opts=opts.LegendOpts(
                type_="scroll", pos_top="10%", pos_left="40%", orient="vertical"
            ),
        )
    )

    bar_3 = (
        Bar(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
            .add_xaxis(q3_name)
            .add_yaxis("人数", q3_res)
            .set_global_opts(title_opts=opts.TitleOpts(title="线上学习使用的设备/材料分布"),
                             legend_opts=opts.LegendOpts(pos_right="25%"),
                             xaxis_opts=opts.AxisOpts(axislabel_opts={"rotate": 30})))

    grid = (
        Grid(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
            .add(bar_3, grid_opts=opts.GridOpts(pos_left="60%", pos_bottom="20%"))
            .add(pie_3, grid_opts=opts.GridOpts(pos_right="55%"))
            .render(save_path + r'\q3\total.html')
    )


# 每日学习时长， 专心程度， 有效学习时间——折线图
def show_q6_q7():
    # 年级
    res_q6 = []
    res_q7 = []
    # 有效学习时间
    res_valid = []

    grade_count = [len(grade[i]) for i in range(12)]

    for i in range(12):
        # 平均数   单位：分钟
        res_q6.append(round(np.sum(grade[i][:, 21]) / grade_count[i] * 60, 2))
        # 专心程度——满分100分， 与原数据的计算公式 y = 120 - x * 20
        res_q7.append(round(120.0 - (np.sum(grade[i][:, 22]) / grade_count[i] * 20), 2))
        # 有效学习时间——每天学习时间 * 学习专心程度（0-100） / 100
        res_valid.append(round(res_q6[i] * res_q7[i] / 100.0, 2))

    c = (
        Line(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
        .add_xaxis(grade_name)
        .add_yaxis("每天学习时长", res_q6)
        .add_yaxis("专心程度", res_q7)
        .add_yaxis("有效学习时间", res_valid)
        .set_global_opts(title_opts=opts.TitleOpts(title="学习情况分析——不同年级", subtitle="(每日学习时间/分钟)"))
        .render(save_path + r"\q6_q7\grade_study_state.html")
    )

    # 地区
    res_q6 = []
    res_q7 = []
    # 有效学习时间
    res_valid = []

    region_count = [len(region[i]) for i in range(4)]

    for i in range(4):
        # 平均数   单位：分钟
        res_q6.append(round(np.sum(region[i][:, 21]) / region_count[i] * 60, 2))
        # 专心程度——满分100分， 与原数据的计算公式 y = 120 - x * 20
        res_q7.append(round(120.0 - (np.sum(region[i][:, 22]) / region_count[i] * 20), 2))
        # 有效学习时间——每天学习时间 * 学习专心程度（0-100） / 100
        res_valid.append(round(res_q6[i] * res_q7[i] / 100.0, 2))

    c = (
        Line(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
        .add_xaxis(region_name)
        .add_yaxis("每天学习时长", res_q6)
        .add_yaxis("专心程度", res_q7)
        .add_yaxis("有效学习时间", res_valid)
        .set_global_opts(title_opts=opts.TitleOpts(title="学习情况分析——不同地区", subtitle="(每日学习时间/分钟)"))
        .render(save_path + r"\q6_q7\region_study_state.html")
    )

    # 学校类型
    res_q6 = []
    res_q7 = []
    # 有效学习时间
    res_valid = []

    school_count = [len(school[i]) for i in range(4)]

    for i in range(4):
        # 平均数   单位：分钟
        res_q6.append(round(np.sum(school[i][:, 21]) / school_count[i] * 60, 2))
        # 专心程度——满分100分， 与原数据的计算公式 y = 120 - x * 20
        res_q7.append(round(120.0 - (np.sum(school[i][:, 22]) / school_count[i] * 20), 2))
        # 有效学习时间——每天学习时间 * 学习专心程度（0-100） / 100
        res_valid.append(round(res_q6[i] * res_q7[i] / 100.0, 2))

    c = (
        Line(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
        .add_xaxis(school_name)
        .add_yaxis("每天学习时长", res_q6)
        .add_yaxis("专心程度", res_q7)
        .add_yaxis("有效学习时间", res_valid)
        .set_global_opts(title_opts=opts.TitleOpts(title="学习情况分析——不同学校类型", subtitle="(每日学习时间/分钟)"))
        .render(save_path + r"\q6_q7\school_study_state.html")
    )


# 对家人陪伴的依赖程度
def show_q8():
    # 年级
    res_q8 = []
    grade_count = [len(grade[i]) for i in range(12)]
    # 专心程度——满分99.9分， 与原数据的计算公式 y = x * 33.3
    for i in range(12):
        res_q8.append(round((np.sum(grade[i][:, 23]) / grade_count[i] * 33.3), 2))

    c = (
        Line(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
            .add_xaxis(grade_name)
            .add_yaxis("对家人陪伴的依赖程度", res_q8)
            .set_global_opts(title_opts=opts.TitleOpts(title="线上学习是否需要家人陪伴——不同年级"),
                             yaxis_opts=opts.AxisOpts(min_=30, max_=80))
            .render(save_path + r"\q8\grade_rely.html")
    )

    # 地区
    res_q8 = []
    region_count = [len(region[i]) for i in range(4)]
    # 专心程度——满分99.9分， 与原数据的计算公式 y = x * 33.3
    for i in range(4):
        res_q8.append(round((np.sum(region[i][:, 23]) / region_count[i] * 33.3), 2))

    c = (
        Line(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
            .add_xaxis(region_name)
            .add_yaxis("对家人陪伴的依赖程度", res_q8)
            .set_global_opts(title_opts=opts.TitleOpts(title="线上学习是否需要家人陪伴——不同地区"),
                             yaxis_opts=opts.AxisOpts(min_=30, max_=80))
            .render(save_path + r"\q8\region_rely.html")
    )

    # 学校
    res_q8 = []
    school_count = [len(school[i]) for i in range(4)]
    # 专心程度——满分99.9分， 与原数据的计算公式 y = x * 33.3
    for i in range(4):
        res_q8.append(round((np.sum(school[i][:, 23]) / school_count[i] * 33.3), 2))

    c = (
        Line(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
            .add_xaxis(school_name)
            .add_yaxis("对家人陪伴的依赖程度", res_q8)
            .set_global_opts(title_opts=opts.TitleOpts(title="线上学习是否需要家人陪伴——不同学校类型"),
                             yaxis_opts=opts.AxisOpts(min_=30, max_=80))
            .render(save_path + r"\q8\school_rely.html")
    )


# 参与线上学习的课堂互动的积极性 43
def show_q12():
    q12_name = ['不回答问题', '偶尔参与回答问题', '大多数情况下能回答问题', '积极发言，回答问题', '课堂没有问答环节， 没计划会回答']

    # 地区
    q12_res = [[0] * 5 for i in range(4)]

    for i in range(len(region)):
        for j in range(5):
            q12_res[i][j] += np.sum(region[i][:, 43] == (j + 1)).item()

    fn_1 = """
               function() {
                   return '珠三角';
               }
               """
    fn_2 = """
               function() {
                   return '粤东';
               }
               """

    fn_3 = """
               function() {
                   return '粤西';
               }
               """

    fn_4 = """
               function() {
                   return '粤北';
               }
               """

    def new_label_opts(fn):
        return opts.LabelOpts(formatter=JsCode(fn), position="center")

    c = (
        Pie(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
            .add(
            "",
            [list(z) for z in zip(q12_name, q12_res[0])],
            center=["20%", "30%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_1),
        )
            .add(
            "",
            [list(z) for z in zip(q12_name, q12_res[1])],
            center=["55%", "30%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_2),
        )
            .add(
            "",
            [list(z) for z in zip(q12_name, q12_res[2])],
            center=["20%", "70%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_3),
        )
            .add(
            "",
            [list(z) for z in zip(q12_name, q12_res[3])],
            center=["55%", "70%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_4),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="线上学习的课堂互动频率——不同地区"),
            legend_opts=opts.LegendOpts(
                type_="scroll", pos_top="20%", pos_left="66%", orient="vertical"
            ),
        )
            .render(save_path + r"\q12\region.html")
    )

    # 学校
    q12_res = [[0] * 5 for i in range(4)]

    for i in range(len(school)):
        for j in range(5):
            q12_res[i][j] += np.sum(school[i][:, 43] == (j + 1)).item()

    fn_1 = """
                   function() {
                       return '乡镇小学';
                   }
                   """
    fn_2 = """
                   function() {
                       return '乡镇中学';
                   }
                   """

    fn_3 = """
                   function() {
                       return '城区小学';
                   }
                   """

    fn_4 = """
                   function() {
                       return '城区中学';
                   }
                   """

    def new_label_opts(fn):
        return opts.LabelOpts(formatter=JsCode(fn), position="center")

    c = (
        Pie(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
            .add(
            "",
            [list(z) for z in zip(q12_name, q12_res[0])],
            center=["20%", "30%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_1),
        )
            .add(
            "",
            [list(z) for z in zip(q12_name, q12_res[1])],
            center=["55%", "30%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_2),
        )
            .add(
            "",
            [list(z) for z in zip(q12_name, q12_res[2])],
            center=["20%", "70%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_3),
        )
            .add(
            "",
            [list(z) for z in zip(q12_name, q12_res[3])],
            center=["55%", "70%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_4),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="线上学习的课堂互动频率——不同学校类型"),
            legend_opts=opts.LegendOpts(
                type_="scroll", pos_top="20%", pos_left="66%", orient="vertical"
            ),
        )
            .render(save_path + r"\q12\school.html")
    )

    # 总体
    q12_res = [[0] * 5 for i in range(4)]

    for i in range(len(school)):
        for j in range(5):
            q12_res[i][j] += np.sum(school[i][:, 43] == (j + 1)).item()

    q12_res_ = [0] * 5
    for j in range(5):
        for i in range(4):
            q12_res_[j] += q12_res[i][j]

    q12_res = q12_res_

    total = 0
    for i in range(len(q12_res)):
        total += q12_res[i]

    q12_res_pie = []
    for i in range(5):
        q12_res_pie.append(round(q12_res[i] / total, 2))

    pie_12 = (
        Pie(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
            .add("", [list(z) for z in zip(q12_name, q12_res_pie)], radius=160, center=["20%", "40%"])
            .set_global_opts(
            title_opts=opts.TitleOpts(title="线上学习的课堂互动频率"),
            legend_opts=opts.LegendOpts(
                type_="scroll", pos_top="10%", pos_left="40%", orient="vertical"
            ),
        )
    )

    bar_12 = (
        Bar(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
            .add_xaxis(q12_name)
            .add_yaxis("人数", q12_res)
            .set_global_opts(title_opts=opts.TitleOpts(title="线上学习的课堂互动频率"),
                             legend_opts=opts.LegendOpts(pos_right="25%"),
                             xaxis_opts=opts.AxisOpts(axislabel_opts={"rotate": 30})))

    grid = (
        Grid(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
            .add(bar_12, grid_opts=opts.GridOpts(pos_left="60%", pos_bottom="20%"))
            .add(pie_12, grid_opts=opts.GridOpts(pos_right="55%"))
            .render(save_path + r'\q12\total.html')
    )


# 线上学习行为  52 56
def show_q14():
    q14_name = ['回看课程视频', '认真学习老师提供的其他课程资料', '开展居家自觉自学、自修活动', '遇到问题时，积极向老师提问', '线上完成作业的质量，能够达到与线下一样的效果']

    # 地区
    q14_res = [[] for i in range(4)]

    for i in range(4):
        for j in range(52, 57):
            q14_res[i].append(np.sum(region[i][:, j]).item())

    fn_1 = """
           function() {
               return '珠三角';
           }
           """
    fn_2 = """
           function() {
               return '粤东';
           }
           """

    fn_3 = """
           function() {
               return '粤西';
           }
           """

    fn_4 = """
           function() {
               return '粤北';
           }
           """

    def new_label_opts(fn):
        return opts.LabelOpts(formatter=JsCode(fn), position="center")

    c = (
        Pie(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
            .add(
            "",
            [list(z) for z in zip(q14_name, q14_res[0])],
            center=["20%", "30%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_1),
        )
            .add(
            "",
            [list(z) for z in zip(q14_name, q14_res[1])],
            center=["55%", "30%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_2),
        )
            .add(
            "",
            [list(z) for z in zip(q14_name, q14_res[2])],
            center=["20%", "70%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_3),
        )
            .add(
            "",
            [list(z) for z in zip(q14_name, q14_res[3])],
            center=["55%", "70%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_4),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="学习行为情况——不同地区"),
            legend_opts=opts.LegendOpts(
                type_="scroll", pos_top="20%", pos_left="66%", orient="vertical"
            ),
        )
            .render(save_path + r"\q14\region.html")
    )

    # 学校
    q14_res = [[] for i in range(4)]

    for i in range(4):
        for j in range(52, 57):
            q14_res[i].append(np.sum(school[i][:, j]).item())

    fn_1 = """
               function() {
                   return '乡镇小学';
               }
               """
    fn_2 = """
               function() {
                   return '乡镇中学';
               }
               """

    fn_3 = """
               function() {
                   return '城区小学';
               }
               """

    fn_4 = """
               function() {
                   return '城区中学';
               }
               """

    def new_label_opts(fn):
        return opts.LabelOpts(formatter=JsCode(fn), position="center")

    c = (
        Pie(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
            .add(
            "",
            [list(z) for z in zip(q14_name, q14_res[0])],
            center=["20%", "30%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_1),
        )
            .add(
            "",
            [list(z) for z in zip(q14_name, q14_res[1])],
            center=["55%", "30%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_2),
        )
            .add(
            "",
            [list(z) for z in zip(q14_name, q14_res[2])],
            center=["20%", "70%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_3),
        )
            .add(
            "",
            [list(z) for z in zip(q14_name, q14_res[3])],
            center=["55%", "70%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_4),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="学习行为情况——不同学校类型"),
            legend_opts=opts.LegendOpts(
                type_="scroll", pos_top="20%", pos_left="66%", orient="vertical"
            ),
        )
            .render(save_path + r"\q14\school.html")
    )

    # 总体
    q14_res = [0] * 5

    for j in range(52, 57):
        for i in range(4):
            q14_res[j - 52] += np.sum(region[i][:, j]).item()

    total = 0
    for i in range(5):
        total += q14_res[i]

    q14_res_pie = []
    for i in range(5):
        q14_res_pie.append(round(q14_res[i] / total, 2))

    pie_14 = (
        Pie(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
            .add("", [list(z) for z in zip(q14_name, q14_res_pie)], radius=160, center=["20%", "40%"])
            .set_global_opts(
            title_opts=opts.TitleOpts(title="学习行为情况"),
            legend_opts=opts.LegendOpts(
                type_="scroll", pos_top="2%", pos_left="35%", orient="vertical"
            ),
        )
    )

    bar_14 = (
        Bar(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
            .add_xaxis(q14_name)
            .add_yaxis("人数", q14_res)
            .set_global_opts(title_opts=opts.TitleOpts(title="学习行为情况"),
                             legend_opts=opts.LegendOpts(pos_right="25%"),
                             xaxis_opts=opts.AxisOpts(axislabel_opts={"rotate": 30})))

    grid = (
        Grid(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
            .add(bar_14, grid_opts=opts.GridOpts(pos_left="60%", pos_bottom="20%"))
            .add(pie_14, grid_opts=opts.GridOpts(pos_right="55%"))
            .render(save_path + r'\q14\total.html')
    )


# 对线上学习各方面的满意度 63 69
def show_q16():
    # 年级
    res_q16_grade = [[] for i in range(7)]
    grade_count = [len(grade[i]) for i in range(12)]

    for i in range(63, 70):
        for j in range(12):
            # 满意度计算公式 :  （75 - 平均满意度 * 25） / 0.75
            res_q16_grade[i - 63].append(round((75 - (np.sum(grade[j][:, i]).item() / grade_count[j] * 25)) / 0.75, 2))

    c = (
        Line(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
        .add_xaxis(grade_name)
        .add_yaxis("线上课堂直播方式满意度", res_q16_grade[0])
        .add_yaxis("线上课堂录播方式满意度", res_q16_grade[1])
        .add_yaxis("教师线上教学的态度满意度", res_q16_grade[2])
        .add_yaxis("教师线上教学水平、效果满意度", res_q16_grade[3])
        .add_yaxis("线上学习资源内容满意度", res_q16_grade[4])
        .add_yaxis("使用的线上学习平台满意度", res_q16_grade[5])
        .add_yaxis("线上学习总体满意度", res_q16_grade[6])
        .set_global_opts(title_opts=opts.TitleOpts(title="线上学习各方面的满意度——不同年级"),
                         yaxis_opts=opts.AxisOpts(min_=20, max_=45),
                         legend_opts=opts.LegendOpts(orient="vertical", pos_right="10%"))
        .render(save_path + r"\q16\grade.html")
    )

    # 地区
    res_q16_region = [[] for i in range(7)]
    region_count = [len(region[i]) for i in range(4)]

    for i in range(63, 70):
        for j in range(4):
            # 满意度计算公式 :  （75 - 平均满意度 * 25） / 0.75
            res_q16_region[i - 63].append(
                round((75 - (np.sum(region[j][:, i]).item() / region_count[j] * 25)) / 0.75, 2))

    c = (
        Line(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
            .add_xaxis(region_name)
            .add_yaxis("线上课堂直播方式满意度", res_q16_region[0])
            .add_yaxis("线上课堂录播方式满意度", res_q16_region[1])
            .add_yaxis("教师线上教学的态度满意度", res_q16_region[2])
            .add_yaxis("教师线上教学水平、效果满意度", res_q16_region[3])
            .add_yaxis("线上学习资源内容满意度", res_q16_region[4])
            .add_yaxis("使用的线上学习平台满意度", res_q16_region[5])
            .add_yaxis("线上学习总体满意度", res_q16_region[6])
            .set_global_opts(title_opts=opts.TitleOpts(title="线上学习各方面的满意度——不同地区"),
                             yaxis_opts=opts.AxisOpts(min_=20, max_=45),
                             legend_opts=opts.LegendOpts(orient="vertical", pos_right="10%"))
            .render(save_path + r"\q16\region.html")
    )

    # 学校
    res_q16_school = [[] for i in range(7)]
    school_count = [len(school[i]) for i in range(4)]

    for i in range(63, 70):
        for j in range(4):
            # 满意度计算公式 :  （75 - 平均满意度 * 25） / 0.75
            res_q16_school[i - 63].append(
                round((75 - (np.sum(school[j][:, i]).item() / school_count[j] * 25)) / 0.75, 2))

    c = (
        Line(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
            .add_xaxis(school_name)
            .add_yaxis("线上课堂直播方式满意度", res_q16_school[0])
            .add_yaxis("线上课堂录播方式满意度", res_q16_school[1])
            .add_yaxis("教师线上教学的态度满意度", res_q16_school[2])
            .add_yaxis("教师线上教学水平、效果满意度", res_q16_school[3])
            .add_yaxis("线上学习资源内容满意度", res_q16_school[4])
            .add_yaxis("使用的线上学习平台满意度", res_q16_school[5])
            .add_yaxis("线上学习总体满意度", res_q16_school[6])
            .set_global_opts(title_opts=opts.TitleOpts(title="线上学习各方面的满意度——不同学校类型"),
                             yaxis_opts=opts.AxisOpts(min_=20, max_=45),
                             legend_opts=opts.LegendOpts(orient="vertical", pos_right="10%"))
            .render(save_path + r"\q16\school.html")
    )


# 线上课程时间——柱状图 20
def show_q5():
    q5_name = ['20分钟及以内', '20-30分钟', '30-45分钟', '45分钟以上']
    res_q5 = [0] * 4

    for i in range(len(region)):
        res_q5[0] += np.sum(region[i][:, 20] == 1).item()
        res_q5[1] += np.sum(region[i][:, 20] == 2).item()
        res_q5[2] += np.sum(region[i][:, 20] == 3).item()
        res_q5[3] += np.sum(region[i][:, 20] == 4).item()

    c = (
        Bar(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
            .add_xaxis(q5_name)
            .add_yaxis("人数", res_q5)
            .set_global_opts(title_opts=opts.TitleOpts(title="课程时长情况"))
            .render(save_path + r"\q5\course_time.html")
    )


# 线上学习遇到的困难——柱状图 44 51
def show_q13():
    q13_name = ['网络资源有限，容易拥堵卡顿', '线上学习平台体验不好或功能受限', '与教师沟通不顺畅，问题无法及时解答', '课后作业设置不合理', '课程资源质量欠佳',
                '长时间观看屏幕，眼睛疲劳', '要求安装的软件平台过多，容易混淆', '环境干扰因素多，难以集中学习']
    q13_res = [0] * 8

    for i in range(len(region)):
        for j in range(44, 52):
            q13_res[j - 44] += np.sum(region[i][:, j]).item()

    c = (
        Bar(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
            .add_xaxis(q13_name)
            .add_yaxis("遇到的主要问题数", q13_res)
            .set_global_opts(title_opts=opts.TitleOpts(title="线上学习遇到的问题情况"),
                             xaxis_opts=opts.AxisOpts(axislabel_opts={"rotate":15}))
            # .render(save_path + r"\q13\problem_count.html")
    )
    grid = (
        Grid(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
            .add(c, grid_opts=opts.GridOpts(pos_bottom='15%', is_contain_label=True))
            .render(save_path + r"\q13\problem_count.html")
    )


# 线上教育培养了哪些能力——饼图 57 62
def show_q15():
    q15_name = ['自主学习能力', '自控能力', '数字化资源的利用能力', '表达沟通', '生活实践', '其他']

    # 地区
    q15_res = [[] for i in range(4)]

    for i in range(4):
        for j in range(57, 62):
            q15_res[i].append(np.sum(region[i][:, j]).item())

    fn_1 = """
               function() {
                   return '珠三角';
               }
               """
    fn_2 = """
               function() {
                   return '粤东';
               }
               """

    fn_3 = """
               function() {
                   return '粤西';
               }
               """

    fn_4 = """
               function() {
                   return '粤北';
               }
               """

    def new_label_opts(fn):
        return opts.LabelOpts(formatter=JsCode(fn), position="center")

    c = (
        Pie(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
            .add(
            "",
            [list(z) for z in zip(q15_name, q15_res[0])],
            center=["20%", "30%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_1),
        )
            .add(
            "",
            [list(z) for z in zip(q15_name, q15_res[1])],
            center=["55%", "30%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_2),
        )
            .add(
            "",
            [list(z) for z in zip(q15_name, q15_res[2])],
            center=["20%", "70%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_3),
        )
            .add(
            "",
            [list(z) for z in zip(q15_name, q15_res[3])],
            center=["55%", "70%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_4),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="线上教育培养的能力——不同地区"),
            legend_opts=opts.LegendOpts(
                type_="scroll", pos_top="20%", pos_left="66%", orient="vertical"
            ),
        )
            .render(save_path + r"\q15\region.html")
    )

    # 学校
    q15_res = [[] for i in range(4)]

    for i in range(4):
        for j in range(57, 62):
            q15_res[i].append(np.sum(school[i][:, j]).item())

    fn_1 = """
                   function() {
                       return '乡镇小学';
                   }
                   """
    fn_2 = """
                   function() {
                       return '乡镇中学';
                   }
                   """

    fn_3 = """
                   function() {
                       return '城区小学';
                   }
                   """

    fn_4 = """
                   function() {
                       return '城区中学';
                   }
                   """

    def new_label_opts(fn):
        return opts.LabelOpts(formatter=JsCode(fn), position="center")

    c = (
        Pie(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
            .add(
            "",
            [list(z) for z in zip(q15_name, q15_res[0])],
            center=["20%", "30%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_1),
        )
            .add(
            "",
            [list(z) for z in zip(q15_name, q15_res[1])],
            center=["55%", "30%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_2),
        )
            .add(
            "",
            [list(z) for z in zip(q15_name, q15_res[2])],
            center=["20%", "70%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_3),
        )
            .add(
            "",
            [list(z) for z in zip(q15_name, q15_res[3])],
            center=["55%", "70%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_4),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="线上教育培养的能力——不同学校类型"),
            legend_opts=opts.LegendOpts(
                type_="scroll", pos_top="20%", pos_left="66%", orient="vertical"
            ),
        )
            .render(save_path + r"\q15\school.html")
    )

    # 总体
    q15_res = [0] * 6

    for j in range(57, 62):
        for i in range(4):
            q15_res[j - 57] += np.sum(region[i][:, j]).item()


    total = 0
    for i in range(6):
        total += q15_res[i]

    q15_res_pie = []
    for i in range(6):
        q15_res_pie.append(round(q15_res[i] / total, 2))

    pie_15 = (
        Pie(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
            .add("", [list(z) for z in zip(q15_name, q15_res_pie)], radius=160, center=["20%", "40%"])
            .set_global_opts(
            title_opts=opts.TitleOpts(title="线上教育培养的能力"),
            legend_opts=opts.LegendOpts(
                type_="scroll", pos_top="10%", pos_left="40%", orient="vertical"
            ),
        )
    )

    bar_15 = (
        Bar(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
            .add_xaxis(q15_name)
            .add_yaxis("人数", q15_res)
            .set_global_opts(title_opts=opts.TitleOpts(title="线上教育培养的能力"),
                             legend_opts=opts.LegendOpts(pos_right="25%"),
                             xaxis_opts=opts.AxisOpts(axislabel_opts={"rotate": 30})))

    grid = (
        Grid(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
            .add(bar_15, grid_opts=opts.GridOpts(pos_left="60%", pos_bottom="20%"))
            .add(pie_15, grid_opts=opts.GridOpts(pos_right="55%"))
            .render(save_path + r'\q15\total.html')
    )


# 线上学习的优势——饼图，柱状图 70 76
def show_17():
    q17_name = ['能够听到更多名师优质课', '可以更加方便地回看、复习、帮助理解', '学习效果更好', '减轻了学习负担', '学习自觉性自主性增强', '可以随时随地学习', '其他']

    # 地区
    q17_res = [[] for i in range(4)]

    for i in range(4):
        for j in range(70, 77):
            q17_res[i].append(np.sum(region[i][:, j]).item())

    fn_1 = """
                   function() {
                       return '珠三角';
                   }
                   """
    fn_2 = """
                   function() {
                       return '粤东';
                   }
                   """

    fn_3 = """
                   function() {
                       return '粤西';
                   }
                   """

    fn_4 = """
                   function() {
                       return '粤北';
                   }
                   """

    def new_label_opts(fn):
        return opts.LabelOpts(formatter=JsCode(fn), position="center")

    c = (
        Pie(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
            .add(
            "",
            [list(z) for z in zip(q17_name, q17_res[0])],
            center=["20%", "30%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_1),
        )
            .add(
            "",
            [list(z) for z in zip(q17_name, q17_res[1])],
            center=["55%", "30%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_2),
        )
            .add(
            "",
            [list(z) for z in zip(q17_name, q17_res[2])],
            center=["20%", "70%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_3),
        )
            .add(
            "",
            [list(z) for z in zip(q17_name, q17_res[3])],
            center=["55%", "70%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_4),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="线上学习的优势——不同地区"),
            legend_opts=opts.LegendOpts(
                type_="scroll", pos_top="20%", pos_left="66%", orient="vertical"
            ),
        )
            .render(save_path + r"\q17\region.html")
    )

    # 学校
    q17_res = [[] for i in range(4)]

    for i in range(4):
        for j in range(70, 77):
            q17_res[i].append(np.sum(school[i][:, j]).item())

    fn_1 = """
                   function() {
                       return '乡镇小学';
                   }
                   """
    fn_2 = """
                   function() {
                       return '乡镇中学';
                   }
                   """

    fn_3 = """
                   function() {
                       return '城区小学';
                   }
                   """

    fn_4 = """
                   function() {
                       return '城区中学';
                   }
                   """

    def new_label_opts(fn):
        return opts.LabelOpts(formatter=JsCode(fn), position="center")

    c = (
        Pie(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
            .add(
            "",
            [list(z) for z in zip(q17_name, q17_res[0])],
            center=["20%", "30%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_1),
        )
            .add(
            "",
            [list(z) for z in zip(q17_name, q17_res[1])],
            center=["55%", "30%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_2),
        )
            .add(
            "",
            [list(z) for z in zip(q17_name, q17_res[2])],
            center=["20%", "70%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_3),
        )
            .add(
            "",
            [list(z) for z in zip(q17_name, q17_res[3])],
            center=["55%", "70%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_4),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="线上学习的优势——不同学校类型"),
            legend_opts=opts.LegendOpts(
                type_="scroll", pos_top="20%", pos_left="66%", orient="vertical"
            ),
        )
            .render(save_path + r"\q17\school.html")
    )

    # 总体
    q17_res = [0] * 7

    for j in range(70, 77):
        for i in range(4):
            q17_res[j - 70] += np.sum(region[i][:, j]).item()

    total = 0
    for i in range(7):
        total += q17_res[i]

    q17_res_pie = []
    for i in range(7):
        q17_res_pie.append(round(q17_res[i] / total, 2))

    pie_17 = (
        Pie(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
            .add("", [list(z) for z in zip(q17_name, q17_res_pie)], radius=160, center=["20%", "40%"])
            .set_global_opts(
            title_opts=opts.TitleOpts(title="线上学习的优势"),
            legend_opts=opts.LegendOpts(
                type_="scroll", pos_top="10%", pos_left="40%", orient="vertical"
            ),
        )
    )

    bar_17 = (
        Bar(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
            .add_xaxis(q17_name)
            .add_yaxis("人数", q17_res)
            .set_global_opts(title_opts=opts.TitleOpts(title="线上学习的优势"),
                             legend_opts=opts.LegendOpts(pos_right="25%"),
                             xaxis_opts = opts.AxisOpts(axislabel_opts={"rotate": 30})))

    grid = (
        Grid(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
            .add(bar_17, grid_opts=opts.GridOpts(pos_left="60%", pos_bottom="20%"))
            .add(pie_17, grid_opts=opts.GridOpts(pos_right="55%"))
            .render(save_path + r'\q17\total.html')
    )


# 线上学习的不足 77 81
def show_18():
    q18_name = ['不如课堂教学效果好', '视频课程资源质量参差不齐', '学习负担加重', '缺乏师生互动', '其他']

    # 地区
    q18_res = [[] for i in range(4)]

    for i in range(4):
        for j in range(77, 82):
            q18_res[i].append(np.sum(region[i][:, j]).item())

    fn_1 = """
                       function() {
                           return '珠三角';
                       }
                       """
    fn_2 = """
                       function() {
                           return '粤东';
                       }
                       """

    fn_3 = """
                       function() {
                           return '粤西';
                       }
                       """

    fn_4 = """
                       function() {
                           return '粤北';
                       }
                       """

    def new_label_opts(fn):
        return opts.LabelOpts(formatter=JsCode(fn), position="center")

    c = (
        Pie(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
            .add(
            "",
            [list(z) for z in zip(q18_name, q18_res[0])],
            center=["20%", "30%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_1),
        )
            .add(
            "",
            [list(z) for z in zip(q18_name, q18_res[1])],
            center=["55%", "30%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_2),
        )
            .add(
            "",
            [list(z) for z in zip(q18_name, q18_res[2])],
            center=["20%", "70%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_3),
        )
            .add(
            "",
            [list(z) for z in zip(q18_name, q18_res[3])],
            center=["55%", "70%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_4),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="线上学习的不足——不同地区"),
            legend_opts=opts.LegendOpts(
                type_="scroll", pos_top="20%", pos_left="66%", orient="vertical"
            ),
        )
            .render(save_path + r"\q18\region.html")
    )

    # 学校
    q18_res = [[] for i in range(4)]

    for i in range(4):
        for j in range(77, 82):
            q18_res[i].append(np.sum(school[i][:, j]).item())

    fn_1 = """
                       function() {
                           return '乡镇小学';
                       }
                       """
    fn_2 = """
                       function() {
                           return '乡镇中学';
                       }
                       """

    fn_3 = """
                       function() {
                           return '城区小学';
                       }
                       """

    fn_4 = """
                       function() {
                           return '城区中学';
                       }
                       """

    def new_label_opts(fn):
        return opts.LabelOpts(formatter=JsCode(fn), position="center")

    c = (
        Pie(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
            .add(
            "",
            [list(z) for z in zip(q18_name, q18_res[0])],
            center=["20%", "30%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_1),
        )
            .add(
            "",
            [list(z) for z in zip(q18_name, q18_res[1])],
            center=["55%", "30%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_2),
        )
            .add(
            "",
            [list(z) for z in zip(q18_name, q18_res[2])],
            center=["20%", "70%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_3),
        )
            .add(
            "",
            [list(z) for z in zip(q18_name, q18_res[3])],
            center=["55%", "70%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_4),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="线上学习的不足——不同学校类型"),
            legend_opts=opts.LegendOpts(
                type_="scroll", pos_top="20%", pos_left="66%", orient="vertical"
            ),
        )
            .render(save_path + r"\q18\school.html")
    )

    # 总体
    q18_res = [0] * 5

    for j in range(77, 82):
        for i in range(4):
            q18_res[j - 77] += np.sum(region[i][:, j]).item()

    total = 0
    for i in range(5):
        total += q18_res[i]

    q18_res_pie = []
    for i in range(5):
        q18_res_pie.append(round(q18_res[i] / total, 2))

    pie_18 = (
        Pie(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
            .add("", [list(z) for z in zip(q18_name, q18_res_pie)], radius=160, center=["20%", "40%"])
            .set_global_opts(
            title_opts=opts.TitleOpts(title="线上学习的不足"),
            legend_opts=opts.LegendOpts(
                type_="scroll", pos_top="10%", pos_left="40%", orient="vertical"
            ),
        )
    )

    bar_18 = (
        Bar(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
            .add_xaxis(q18_name)
            .add_yaxis("人数", q18_res)
            .set_global_opts(title_opts=opts.TitleOpts(title="线上学习的不足"),
                             legend_opts=opts.LegendOpts(pos_right="25%"),
                             xaxis_opts=opts.AxisOpts(axislabel_opts={"rotate":30}))
    )

    grid = (
        Grid(
            init_opts = opts.InitOpts(width="1200px", height="685px")
        )
            .add(bar_18, grid_opts=opts.GridOpts(pos_left="60%", pos_bottom="20%"))
            .add(pie_18, grid_opts=opts.GridOpts(pos_right="55%"))
            .render(save_path + r'\q18\total.html')
    )


# 期待的线上活动或体验促进线上学习 82 88
def show_19():
    q19_name = ['老师实时视音频方式的互动、答疑', '线上小组讨论和合作', '增加专题教育的内容和课时', '线上随堂测试或考试', '智能推荐学习资源', '学习状态智能检测并反馈、提醒', '其他']

    # 地区
    q19_res = [[] for i in range(4)]

    for i in range(4):
        for j in range(82, 89):
            q19_res[i].append(np.sum(region[i][:, j]).item())

    fn_1 = """
                           function() {
                               return '珠三角';
                           }
                           """
    fn_2 = """
                           function() {
                               return '粤东';
                           }
                           """

    fn_3 = """
                           function() {
                               return '粤西';
                           }
                           """

    fn_4 = """
                           function() {
                               return '粤北';
                           }
                           """

    def new_label_opts(fn):
        return opts.LabelOpts(formatter=JsCode(fn), position="center")

    c = (
        Pie(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
            .add(
            "",
            [list(z) for z in zip(q19_name, q19_res[0])],
            center=["20%", "30%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_1),
        )
            .add(
            "",
            [list(z) for z in zip(q19_name, q19_res[1])],
            center=["55%", "30%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_2),
        )
            .add(
            "",
            [list(z) for z in zip(q19_name, q19_res[2])],
            center=["20%", "70%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_3),
        )
            .add(
            "",
            [list(z) for z in zip(q19_name, q19_res[3])],
            center=["55%", "70%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_4),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="对线上学习的期待——不同地区"),
            legend_opts=opts.LegendOpts(
                type_="scroll", pos_top="20%", pos_left="66%", orient="vertical"
            ),
        )
            .render(save_path + r"\q19\region.html")
    )

    # 学校
    q19_res = [[] for i in range(4)]

    for i in range(4):
        for j in range(82, 89):
            q19_res[i].append(np.sum(school[i][:, j]).item())

    fn_1 = """
                           function() {
                               return '乡镇小学';
                           }
                           """
    fn_2 = """
                           function() {
                               return '乡镇中学';
                           }
                           """

    fn_3 = """
                           function() {
                               return '城区小学';
                           }
                           """

    fn_4 = """
                           function() {
                               return '城区中学';
                           }
                           """

    def new_label_opts(fn):
        return opts.LabelOpts(formatter=JsCode(fn), position="center")

    c = (
        Pie(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
            .add(
            "",
            [list(z) for z in zip(q19_name, q19_res[0])],
            center=["20%", "30%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_1),
        )
            .add(
            "",
            [list(z) for z in zip(q19_name, q19_res[1])],
            center=["55%", "30%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_2),
        )
            .add(
            "",
            [list(z) for z in zip(q19_name, q19_res[2])],
            center=["20%", "70%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_3),
        )
            .add(
            "",
            [list(z) for z in zip(q19_name, q19_res[3])],
            center=["55%", "70%"],
            radius=[80, 120],
            label_opts=new_label_opts(fn_4),
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="对线上学习的期待——不同学校类型"),
            legend_opts=opts.LegendOpts(
                type_="scroll", pos_top="20%", pos_left="66%", orient="vertical"
            ),
        )
            .render(save_path + r"\q19\school.html")
    )

    # 总体
    q19_res = [0] * 7

    for j in range(82, 89):
        for i in range(4):
            q19_res[j - 82] += np.sum(region[i][:, j]).item()

    total = 0
    for i in range(7):
        total += q19_res[i]

    q19_res_pie = []
    for i in range(7):
        q19_res_pie.append(round(q19_res[i] / total, 2))

    pie_19 = (
        Pie(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
            .add("", [list(z) for z in zip(q19_name, q19_res_pie)], radius=160, center=["20%", "40%"])
            .set_global_opts(
            title_opts=opts.TitleOpts(title="对线上学习的期待"),
            legend_opts=opts.LegendOpts(
                type_="scroll", pos_top="0%", pos_left="40%", orient="vertical"
            ),
        )
    )

    bar_19 = (
        Bar(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
            .add_xaxis(q19_name)
            .add_yaxis("人数", q19_res)
            .set_global_opts(title_opts=opts.TitleOpts(title="对线上学习的期待"),
                             legend_opts=opts.LegendOpts(pos_right="25%"),
                             xaxis_opts=opts.AxisOpts(axislabel_opts={"rotate":30})))

    grid = (
        Grid(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
            .add(bar_19, grid_opts=opts.GridOpts(pos_left="60%", pos_bottom="20%"))
            .add(pie_19, grid_opts=opts.GridOpts(pos_right="55%"))
            .render(save_path + r'\q19\total.html')
    )


# 疫情结束后喜欢哪种学习模式——柱状图， 饼图 89
def show_20():
    q20_name = ['以前的实体课堂模式', '实体课堂学习模式，线上学习资源作为学习资源的补充', '线上线下混合式学习模式', '完全线上的学习模式']
    # 地区
    q20_res = [[0] * 4 for i in range(4)]

    for i in range(len(region)):
        for j in range(4):
            q20_res[i][j] += np.sum(region[i][:, 89] == (j + 1)).item()

    c = (
        Bar(
            # init_opts=opts.InitOpts(width="1200px", height="685px")
        )
        .add_xaxis(q20_name)
        .add_yaxis("珠三角", q20_res[0])
        .add_yaxis("粤东", q20_res[1])
        .add_yaxis("粤西", q20_res[2])
        .add_yaxis("粤北", q20_res[3])
        .set_global_opts(title_opts=opts.TitleOpts(title="疫情结束后喜欢哪种学习模式——不同地区"), xaxis_opts=opts.AxisOpts(axislabel_opts={"rotate":15}))
        # .render(save_path + r'\q20\region.html')
    )
    grid = (
        Grid(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
        .add(c, grid_opts=opts.GridOpts(pos_bottom='15%',is_contain_label=True))
        .render(save_path + r'\q20\region.html')
    )

    # 学校
    q20_res = [[0] * 4 for i in range(4)]

    for i in range(len(school)):
        for j in range(4):
            q20_res[i][j] += np.sum(school[i][:, 89] == (j + 1)).item()

    c = (
        Bar()
        .add_xaxis(q20_name)
        .add_yaxis("乡镇小学", q20_res[0])
        .add_yaxis("乡镇中学", q20_res[1])
        .add_yaxis("城区小学", q20_res[2])
        .add_yaxis("城区中学", q20_res[3])
        .set_global_opts(title_opts=opts.TitleOpts(title="疫情结束后喜欢哪种学习模式——不同学校类型"), xaxis_opts=opts.AxisOpts(axislabel_opts={"rotate":15}))
        # .render(save_path + r'\q20\school.html')
    )
    grid = (
        Grid(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
            .add(c, grid_opts=opts.GridOpts(pos_bottom='15%', is_contain_label=True))
            .render(save_path + r'\q20\school.html')
    )

    q20_res_total = [0] * 4
    for i in range(len(q20_res[0])):
        for j in range(len(q20_res)):
            q20_res_total[i] += q20_res[j][i]

    c = (
        Pie()
        .add("", [list(z) for z in zip(q20_name, q20_res_total)])
        .set_global_opts(
            title_opts=opts.TitleOpts(title="疫情结束后喜欢哪种学习模式"),
            legend_opts=opts.LegendOpts(
                type_="scroll", pos_top="20%", pos_left="75%", orient="vertical"
            ),
        )
        # .render(save_path + r'\q20\total.html')
    )
    grid = (
        Grid(
            init_opts=opts.InitOpts(width="1200px", height="685px")
        )
            .add(c, grid_opts=opts.GridOpts(pos_bottom='15%', is_contain_label=True))
            .render(save_path + r'\q20\total.html')
    )


# 地图显示测试
def show_geo_test():
    region_count = [len(region[i]) for i in range(4)]

    cities = ['广州市', '佛山市', '肇庆市', '深圳市', '东莞市', '惠州市', '珠海市', '中山市', '江门市',
              '汕头市', '汕尾市', '潮州市', '揭阳市',
              '湛江市', '茂名市', '阳江市', '云浮市',
              '韶关市', '河源市', '清远市', '梅州市']
    res = []
    res.extend([region_count[0]] * 9)
    res.extend([region_count[1]] * 4)
    res.extend([region_count[2]] * 4)
    res.extend([region_count[3]] * 4)

    c = (
        Map()
        .add("人数分布", [list(z) for z in zip(cities, res)], "广东")
        .set_global_opts(
            title_opts=opts.TitleOpts(title="调查问卷来源分布"), visualmap_opts=opts.VisualMapOpts(max_=31834, min_=8620)
        )
        .render(save_path + r'\q1_q2\map_guangdong.html')
    )


if __name__ == "__main__":
    # path = r'D:/互联网新技术.CSV'
    path = r'D:/80万样本数据.CSV'
    data_initial(path)

    show_q1_q2()
    show_q6_q7()
    show_q8()
    show_q4_q9_q10_q11()
    show_q3()
    show_q16()
    show_q14()
    show_q5()
    show_q12()
    show_q13()
    show_q15()
    show_17()
    show_18()
    show_19()
    show_20()
    # show_geo_test()

    # init_opts=opts.InitOpts(width="1200px", height="685px")
