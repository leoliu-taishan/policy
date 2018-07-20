# -*- coding: UTF-8 -*-
#!/usr/bin/python3

import sys
import os
import MySQLdb
import MySQLdb.cursors
import logging
from logging import handlers

# define EPSILON 1e-6
class Logger(object):
    level_relations = {
        'debug':logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR,
        'crit':logging.CRITICAL
    }#日志级别关系映射

    def __init__(self, filename, level='info', when='D', backCount=1,
                 fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)  # 设置日志格式
        self.logger.setLevel(self.level_relations.get(level))  # 设置日志级别
        sh = logging.StreamHandler()  # 往屏幕上输出
        sh.setFormatter(format_str)  # 设置屏幕上显示的格式
        th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backCount,
                                               encoding='utf-8')  # 往文件里写入#指定间隔时间自动生成文件的处理器
        # 实例化TimedRotatingFileHandler
        # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.setFormatter(format_str)  # 设置文件里写入的格式
        self.logger.addHandler(sh)  # 把对象加到logger里
        self.logger.addHandler(th)

#************************************
# **********Gloabl parameters********
#************************************
g_host_name= [] # list
g_host_rank= []
g_guest_name =[]
g_guest_rank =[]
g_liansai = []
g_rang_num = []
g_match_id_list =[]

def peilv_change(x,y,z,x1,y1,z1,match_id, company):
    temp_log = ""
    if x > 1.01:

        if abs(x-x1) <= 1e-5 and abs(y-y1) <= 1e-5 and (z-z1) <= 1e-5:
            temp_log = "match_id = " + match_id + ":" + company + "赔率没有变化"+ str(x) + "|" + str(y) + "|" + str(z)
        return temp_log

def peilv_huyao(x,y,z, match_id, company):
    # ********************************
    # 2.50        3.xx          2.50*
    # 2.50        3.xx          2.55*
    # 2.60        3.xx          2.60*
    # 2.60        3.xx          2.65*
    # ********************************
    temp_log = ""
    if x > 1.01:
        if abs(x-z) <= 1e-5:
            temp_log = "match_id = " + match_id + ":" + company + "满足互咬赔率--" + str(x) + "|" + str(y) + "|" + str(z)

        elif abs(abs(x-z)-0.05) <= 1e-5:
            temp_log = "match_id = " + match_id + ":" + company + "满足互咬赔率--" + str(x) + "|" + str(y) + "|" + str(z)
        else:
            temp_log = ""

    return temp_log

def is_special_peilv(x,y,z,match_id,company):
    # ********************************
    # 2.20        3.xx          2.80*
    # 2.30        3.xx          2.70*
    # 2.40        3.xx          2.60*
    # 2.25        3.xx          2.88*
    # ********************************
    temp_log = ""
    if abs(x-2.20) <= 1e-5 and abs(z-2.80) <= 1e-5:
        temp_log = "match_id = " + match_id + ":" + company + "满足赔率--" + str(x) + "|" + str(y) + "|" + str(z)

    if abs(x-2.30) <= 1e-5 and abs(z-2.70) <= 1e-5:
        temp_log = "match_id = " + match_id + ":" + company + "满足赔率--" + str(x) + "|" + str(y) + "|" + str(z)

    if abs(x-2.40) <= 1e-5 and abs(z-2.60) <= 1e-5:
        temp_log = "match_id = " + match_id + ":" + company + "满足赔率--" + str(x) + "|" + str(y) + "|" + str(z)

    if abs(x - 2.25) <= 1e-5 and abs(z - 2.88) <= 1e-5:
        temp_log = "match_id = " + match_id + ":" + company + "满足赔率--" + str(x) + "|" + str(y) + "|" + str(z)

    if abs(x - 2.35) <= 1e-5 and abs(z - 2.75) <= 1e-5:
        temp_log = "match_id = " + match_id + ":" + company + "满足赔率--" + str(x) + "|" + str(y) + "|" + str(z)

    if abs(x - 2.45) <= 1e-5 and abs(z - 2.65) <= 1e-5:
        temp_log = "match_id = " + match_id + ":" + company + "满足赔率--" + str(x) + "|" + str(y) + "|" + str(z)

    if abs(x-2.10) <= 1e-5 and abs(z-2.90) <= 1e-5:
        temp_log = "match_id = " + match_id + ":" + company + "满足赔率--" + str(x) + "|" + str(y) + "|" + str(z)

    # And vice visa
    if abs(x - 2.80) <= 1e-5 and abs(z - 2.20) <= 1e-5:
        temp_log = "match_id = " + match_id + ":" + company + "满足赔率--" + str(x) + "|" + str(y) + "|" + str(z)

    if abs(x - 2.70) <= 1e-5 and abs(z - 2.30) <= 1e-5:
        temp_log = "match_id = " + match_id + ":" + company + "满足赔率--" + str(x) + "|" + str(y) + "|" + str(z)

    if abs(x - 2.60) <= 1e-5 and abs(z - 2.40) <= 1e-5:
        temp_log = "match_id = " + match_id + ":" + company + "满足赔率--" + str(x) + "|" + str(y) + "|" + str(z)

    if abs(x - 2.88) <= 1e-5 and abs(z - 2.25) <= 1e-5:
        temp_log = "match_id = " + match_id + ":" + company + "满足赔率--" + str(x) + "|" + str(y) + "|" + str(z)

    if abs(x - 2.85) <= 1e-5 and abs(z - 2.25) <= 1e-5:
        temp_log = "match_id = " + match_id + ":" + company + "满足赔率--" + str(x) + "|" + str(y) + "|" + str(z)

    if abs(x - 2.65) <= 1e-5 and abs(z - 2.45) <= 1e-5:
        temp_log = "match_id = " + match_id + ":" + company + "满足赔率--" + str(x) + "|" + str(y) + "|" + str(z)

    if abs(x - 2.75) <= 1e-5 and abs(z - 2.35) <= 1e-5:
        temp_log = "match_id = " + match_id + ":" + company + "满足赔率--" + str(x) + "|" + str(y) + "|" + str(z)

    if abs(x - 2.10) <= 1e-5 and abs(z - 2.90) <= 1e-5:
        temp_log = "match_id = " + match_id + ":" + company + "满足赔率--" + str(x) + "|" + str(y) + "|" + str(z)

    if abs(x-4.33) <= 1e-5 or abs(z - 4.33) <= 1e-5:
        temp_log = "match_id = " + match_id + ":" + company + "满足赔率--" + str(x) + "|" + str(y) + "|" + str(z)

    # LB_Win_I = '1.75' and LB_Ping_I = '3.50' and LB_Lose_I = '4.00';
    #if company == "立博i" or company == "立博c":
    #    temp_log = "match_id = " + match_id + ":" + company + "满足赔率--" + str(x) + "|" + str(y) + "|" + str(z) +"分胜负无平局"


    return temp_log

def pankou_mapping(pankou):
    if pankou == "平手":
        pk_f = "0.00"
    elif pankou == "平手/半球":
        pk_f = "0.25"
    elif pankou == "半球":
        pk_f = "0.5"
    elif pankou == "半球/一球":
        pk_f = "0.75"
    elif pankou == "一球":
        pk_f = "1.00"
    elif pankou == "一球/球半":
        pk_f = "1.25"
    elif pankou == "球半":
        pk_f = "1.50"
    elif pankou == "球半/两球":
        pk_f = "1.75"
    elif pankou == "两球":
        pk_f = "2.00"
    elif pankou == "两球/两球半":
        pk_f = "2.25"
    elif pankou == "两球半":
        pk_f = "2.50"
    elif pankou == "两球半/三球":
        pk_f = "2.75"
    elif pankou == "三球":
        pk_f = "3.00"
    elif pankou == "受平手/半球":
        pk_f = "-0.25"
    elif pankou == "受半球":
        pk_f = "-0.5"
    elif pankou == "受半球/一球":
        pk_f = "-0.75"
    elif pankou == "受一球":
        pk_f = "-1.00"
    elif pankou == "受一球/球半":
        pk_f = "-1.25"
    elif pankou == "受球半":
        pk_f = "-1.50"
    elif pankou == "受球半/两球":
        pk_f = "-1.75"
    elif pankou == "受两球":
        pk_f = "-2.00"
    elif pankou == "受两球/两球半":
        pk_f = "-2.25"
    elif pankou == "受两球半":
        pk_f = "-2.50"
    elif pankou == "受两球半/三球":
        pk_f = "-2.75"
    elif pankou == "受三球":
        pk_f = "-3.00"
    else:
        pk_f = "4.00"

    return float(pk_f)

def pankou_great_change(x,y, match_id,company,log_info):
    # 所有大于三球的盘口都不分析
    temp_log = ""
    if (abs(x) >3.00) or (abs(y) > 3.00):
        temp_log = "所有大于三球的盘口都不分析"
    else:
        if x > y:
            if abs(x - y) >= 0.5:
                temp_log = log_info + company + "主队盘口连将两级或以上" + "-From:" + str(x) + "--->To:" + str(y) + " 或者说客队连升两盘盘口"
        else:
            if abs(x - y) >= 0.5:
                temp_log = log_info + company + "主队盘口连升两级或以上" + "-From:" + str(x) + "--->To:" + str(y) + " 或者说客队连将两盘盘口"
    return temp_log

def pankou_no_change(pk_i,pk_c,pk_i_s,pk_c_s,match_id,i_value,c_value,company,host_or_not):
    return False
    if abs(i_value - 9.0) <= 1e-5 or abs(c_value - 9.0) <= 1e-5:
        pass # kong yu ju
    else:
        if abs(pk_i-pk_c) <= 1e-5: # 盘口未变
            return True
        else:
            return False
            # # 判断盘口是否合适
            # if host_or_not == True:
            #
            #    if i_value >= c_value:
            #       temp_log = "match_id = " + match_id + ":" + company + "主队盘口(" + pk_i_s + ")未变,但从From:" + str(i_value) +"--->降到To:" + str(c_value)
            #       log.logger.info(temp_log)
            #    else:
            #         temp_log = "match_id = " + match_id + ":" + company + "主队盘口(" + pk_c_s + ")未变,但从From:" + str(i_value) +"--->升到To:" + str(c_value)
            #         log.logger.info(temp_log)
            # else:
            #     if i_value >= c_value:
            #         temp_log = "match_id = " + match_id + ":" + company + "客队盘口(" + pk_i_s + ")未变,但从From:" + str(
            #             i_value) + "--->降到To:" + str(c_value)
            #         log.logger.info(temp_log)
            #     else:
            #         temp_log = "match_id = " + match_id + ":" + company + "客队盘口(" + pk_c_s + ")未变,但从From:" + str(
            #             i_value) + "--->升到To:" + str(c_value)
            #         log.logger.info(temp_log)

def pankou_1_change(x,y,match_id, company):
    return_value = []
    if abs(x-y) <= 1e-5 or abs(abs(x-y) - 0.25) > 0:
        pass
    if abs(abs(x-y)-0.25) <= 1e-5:
        if x > 0:
            if x > y:
                return_value.append(match_id)
                return_value.append(company)
                return_value.append("host")
                return_value.append("-1")
                return_value.append(x)
                return_value.append(y)
                #temp_log = match_id + "--" + company + "主队盘口将1级" + "-From:" + str(x) + "--->To:" + str(y)
            else:
                #temp_log = match_id + "--" + company + "主队盘口升1级" + "-From:" + str(x) + "--->To:" + str(y)
                return_value.append(match_id)
                return_value.append(company)
                return_value.append("host")
                return_value.append("-1")
                return_value.append(x)
                return_value.append(y)
        elif abs(x-0.00) <= 1e-5:
            if x > y:
                #temp_log = match_id + "--" + company + "客队盘口升1级" + "-From:" + str(x) + "--->To:" + str(y)
                return_value.append(match_id)
                return_value.append(company)
                return_value.append("guest")
                return_value.append("+1")
                return_value.append(x)
                return_value.append(y)
            else:
                #temp_log = match_id + "--" + company + "主队盘口将1级" + "-From:" + str(x) + "--->To:" + str(y)
                return_value.append(match_id)
                return_value.append(company)
                return_value.append("host")
                return_value.append("-1")
                return_value.append(x)
                return_value.append(y)
        else:
            if x > y:
                #temp_log = match_id + "--" + company + "客队盘口升1级" + "-From:" + str(x) + "--->To:" + str(y)
                return_value.append(match_id)
                return_value.append(company)
                return_value.append("guest")
                return_value.append("+1")
                return_value.append(x)
                return_value.append(y)
            else:
                #temp_log = match_id + "--" + company + "客队盘口将1级" + "-From:" + str(x) + "--->To:" + str(y)
                return_value.append(match_id)
                return_value.append(company)
                return_value.append("guest")
                return_value.append("-1")
                return_value.append(x)
                return_value.append(y)

    #temp_log1 = ""
    # if len(return_value) != 0:
    #     if return_value[2] == "host":
    #         if return_value[3] == "-1":
    #         # 如果降盘理论上竞彩应该升水， 但是如果竞彩还降水， 主队打出的概率极大。
    #             temp_log1 = "match_id:" + match_id + company + "如果主队降盘理论上竞彩应该升水， 但是如果主队竞彩还降水， 主队打出的概率极大"
    #         #log.logger.info(temp_log1)
    #
    #         if return_value[3] == "+1":
    #         # 如果升盘理论上竞彩应该降水， 但是如果竞彩还升水， 主队打出的概率极小.
    #             temp_log1 = "match_id:" + match_id + company + "如果主队升盘理论上竞彩应该降水， 但是如果主队竞彩还升水， 主队打出的概率极小"
    #         #log.logger.info(temp_log1)
    #     else:
    #         if return_value[3] == "-1":
    #            temp_log1 = "match_id:" + match_id + company + "如果客队降盘理论上竞彩应该升水, 但是如果客队竞彩还降水， 客队打出的概率极大"
    #
    #         if return_value[3] == "+1":
    #             temp_log1 = "match_id:" + match_id + company + "如果客队升盘理论上竞彩应该降水, 但是如果客队竞彩还升水， 客队打出的概率极小"

    return return_value

def chaoji_gaoshui_pankou(i_value, c_value,company,host_or_not,pk_i,pk_c,match_id,log_info):
    #    Now this rule is only applicable for "aomen"
    if abs(i_value - 9.0) <= 1e-5 or abs(c_value - 9.0) <= 1e-5:
        pass # Null yu ju
    else:
        if host_or_not == True :
            if i_value > 1.10:
                if pk_i == pk_c:
                    temp_log = log_info + ":" + company + "主队初盘超级高水:" + str(
                        i_value) + "(" + pk_i + "),并且盘口没有变化--主队没可能打出来,无论强弱!!!!"
                else:
                    temp_log = log_info + ":" + company + "主队初盘超级高水:" + str(i_value)+"(" + pk_i + "),但是主队降盘(" + pk_c + ")后低水(" + str(c_value) +")， 请仔细查看!"

                log.logger.warn(temp_log)
            if c_value > 1.10:
                temp_log = log_info + ":" + company + "主队终盘超级高水:" + str(c_value)+"(" + pk_c + ")--主队没可能打出来,无论强弱!!!!"
                log.logger.warn(temp_log)
        else:
            if i_value > 1.10:
                if pk_i == pk_c:
                    temp_log = log_info + ":" + company + "客队初盘超级高水:" + str(
                        i_value) + "(" + pk_i + "),并且盘口没有变化--客队没可能打出来,无论强弱!!!!"
                else:
                    temp_log = log_info + ":" + company + "客队初盘超级高水:" + str(
                        i_value) + "(" + pk_i + "),但是主队降盘(" + pk_c + ")后低水(" + str(c_value) +")， 请仔细查看!"
                log.logger.warn(temp_log)
            if c_value > 1.10:
                temp_log = log_info + ":" + company + "客队终盘超级高水:" + str(c_value)+"(" + pk_c + ")--客队没可能打出来,无论强弱!!!!"
                log.logger.warn(temp_log)

def if_pk_is_open_by_company (x):
    if abs(x-9.00) <=1e-5:
        return False
    else:
        return True

def if_gaoshui(x,y):
    if if_pk_is_open_by_company(x) == True:
        if x >= 1.00:
            return True
        else:
            return False

def pankou_analyze(match_x,host_name,guest_name,host_rank,guest_rank,liansai,rang_num):
    #log = Logger('all.log', level='info')
    db = MySQLdb.connect("localhost", "root", "123456", "jingcai_db", charset='utf8')
    cursor = db.cursor()
    # cursor.execute("select version()")
    # **********************************************
    # The following rules are specific for pan kou *
    # ***********************************************
    sql_pankou = "select * from t_pankou where match_id = '" + match_x + "'"
    print(sql_pankou)
    cursor.execute(sql_pankou)
    row = cursor.fetchone()
    match_id = row[0]
    b365_h_i = row[1]
    b365_pk_i = pankou_mapping(row[2])
    b365_pk_i_s = row[2]
    b365_g_i = row[3]
    b365_h_c = row[4]
    b365_pk_c = pankou_mapping(row[5])
    b365_pk_c_s = row[5]
    b365_g_c = row[6]
    # ------AO MEN------
    am_h_i = row[7]
    am_pk_i = pankou_mapping(row[8])
    am_pk_i_s = row[8]
    am_g_i = row[9]
    am_h_c = row[10]
    am_pk_c = pankou_mapping(row[11])
    am_pk_c_s = row[11]
    am_g_c = row[12]
    # -----B10-----------
    b10_h_i = row[13]
    b10_pk_i = pankou_mapping(row[14])
    b10_pk_i_s = row[14]
    b10_g_i = row[15]
    b10_h_c = row[16]
    b10_pk_c = pankou_mapping(row[17])
    b10_pk_c_s = row[17]
    b10_g_c = row[18]
    # -----Webbet-----------
    wb_h_i = row[19]
    wb_pk_i = pankou_mapping(row[20])
    wb_pk_i_s = row[20]
    wb_g_i = row[21]
    wb_h_c = row[22]
    wb_pk_c = pankou_mapping(row[23])
    wb_pk_c_s = row[23]
    wb_g_c = row[24]
    temp_log = "match_id = " + match_id + ": "
    # At first, 首先判断是否是变动两盘或者两盘以上的盘口
    step1_log = temp_log + " ===>step 2.1): " + "是否是变动两盘或者两盘以上的盘口?"
    log.logger.info(step1_log)
    log_great_pk = temp_log + " ===>step 1): "
    if pankou_great_change(b365_pk_i,b365_pk_c,match_id,"Beta 365",log_great_pk).strip():
        log.logger.warn(pankou_great_change(b365_pk_i,b365_pk_c,match_id,"Beta 365",log_great_pk))
    if pankou_great_change(am_pk_i,am_pk_c,match_id,"澳门",log_great_pk).strip():
        log.logger.warn(pankou_great_change(am_pk_i,am_pk_c,match_id,"澳门",log_great_pk))
    if pankou_great_change(b10_pk_i,b10_pk_c,match_id,"Bet 10",log_great_pk).strip():
        log.logger.warn(pankou_great_change(b10_pk_i,b10_pk_c,match_id,"Bet 10",log_great_pk))
    if pankou_great_change(wb_pk_i,wb_pk_c,match_id,"Wewbet",log_great_pk).strip():
        log.logger.warn(pankou_great_change(wb_pk_i,wb_pk_c,match_id,"Wewbet",log_great_pk))
    # Second, 第二步: 判断是否盘口有超级高水(>=1.10)， 并判断超级高水是否是升盘造成
    step2_log = temp_log + " ===>step 2.2): " + "是否盘口有超级高水?(>=1.10)?"
    log.logger.info(step2_log)
    log_chaoji_shui = temp_log + " ===>step 2.2): "
    chaoji_gaoshui_pankou(am_h_i, am_h_c, "澳门", True, am_pk_i_s, am_pk_c_s, match_id,log_chaoji_shui)
    chaoji_gaoshui_pankou(am_g_i, am_g_c, "澳门", False, am_pk_i_s, am_pk_c_s, match_id,log_chaoji_shui)
    #chaoji_gaoshui_pankou(b365_h_i, b365_h_c, "Beta365", True, b365_pk_i_s, b365_pk_c_s, match_id,log_chaoji_shui)
    #chaoji_gaoshui_pankou(b365_g_i, b365_g_c, "Beta365", False, b365_pk_i_s, b365_pk_c_s, match_id,log_chaoji_shui)
    #chaoji_gaoshui_pankou(b10_h_i, b10_h_c, "Bet10", True, b10_pk_i_s, b10_pk_c_s, match_id,log_chaoji_shui)
    #chaoji_gaoshui_pankou(b10_g_i, b10_g_c, "Bet10", False, b10_pk_i_s, b10_pk_c_s, match_id,log_chaoji_shui)
    #chaoji_gaoshui_pankou(wb_h_i, wb_h_c, "Wewbet", True, wb_pk_i_s, wb_pk_c_s, match_id,log_chaoji_shui)
    #chaoji_gaoshui_pankou(wb_g_i, wb_g_c, "Wewbet", False, wb_pk_i_s, wb_pk_c_s, match_id,log_chaoji_shui)

    # 第三步：判断初盘和尾盘， 各个盘口的高水(1.00<=X<=1.10)状态
    step3_log = temp_log + " ===>step 2.3): " + "判断初盘和尾盘， 各个盘口的高水(1.00<=X<=1.10)状态"
    log.logger.info(step3_log)
    # host section
    host_i_log = temp_log + " ===>step 2.3): "
    len_host_i_log = len(host_i_log)
    if if_gaoshui(b365_h_i,b365_pk_i_s) == True:
        host_i_log = host_i_log + "Beta365(" + b365_pk_i_s + str(b365_h_i) + ")|"
    if if_gaoshui(am_h_i,am_pk_i_s) == True:
        host_i_log = host_i_log + "澳门(" + am_pk_i_s + str(am_h_i) + ")|"
    if if_gaoshui(b10_h_i,b10_pk_i_s) == True:
        host_i_log = host_i_log + "Bet10(" +  b10_pk_i_s +str(b10_h_i) + ")|"
    if if_gaoshui(wb_h_i, wb_pk_i_s) == True:
        host_i_log = host_i_log + "Wewbet(" + wb_pk_i_s + str(wb_h_i) + ")|"
    if len(host_i_log) == len_host_i_log: # That is to say, host_i_log is not changed.
        pass
    else:
        host_i_log = host_i_log + "主队初盘高水!"
        log.logger.warn(host_i_log)

    host_c_log = temp_log + " ===>step 2.3): "
    len_host_c_log =len(host_c_log)
    if if_gaoshui(b365_h_c,b365_pk_c_s) == True:
        host_c_log = host_c_log + "Beta365(" + b365_pk_c_s + str(b365_h_c) + ")|"
    if if_gaoshui(am_h_c,am_pk_c_s) == True:
        host_c_log = host_c_log + "澳门(" + am_pk_c_s + str(am_h_c) + ")|"
    if if_gaoshui(b10_h_c,b10_pk_c_s) == True:
        host_c_log = host_c_log + "Bet10(" + b10_pk_c_s + str(b10_h_c) + ")|"
    if if_gaoshui(wb_h_c,wb_pk_c_s) == True:
        host_c_log = host_c_log + "Wewbet(" + wb_pk_c_s + str(wb_h_c) + ")|"

    if len(host_c_log) == len_host_c_log:
        pass
    else:
        host_c_log = host_c_log + "主队尾盘高水!"
        log.logger.warn(host_c_log)

    # guest section
    guest_i_log = temp_log + " ===>step 2.3): "
    len_guest_i_log = len(guest_i_log)
    if if_gaoshui(b365_g_i, b365_pk_i_s) == True:
        guest_i_log = guest_i_log + "Beta365(" + b365_pk_i_s + str(b365_g_i) + ")|"
    if if_gaoshui(am_g_i, am_pk_i_s) == True:
        guest_i_log = guest_i_log + "澳门(" + am_pk_i_s + str(am_g_i) + ")|"
    if if_gaoshui(b10_g_i, b10_pk_i_s) == True:
        guest_i_log = guest_i_log + "Bet10(" + b10_pk_i_s + str(b10_g_i) + ")|"
    if if_gaoshui(wb_g_i, wb_pk_i_s) == True:
        guest_i_log = guest_i_log + "Wewbet(" + wb_pk_i_s + str(wb_g_i) + ")|"

    if len(guest_i_log) == len_guest_i_log:
        pass
    else:
        guest_i_log = guest_i_log + "客队初盘高水!"
        log.logger.warn(guest_i_log)

    guest_c_log = temp_log + " ===>step 2.3): "
    len_guest_c_log = len(guest_c_log)
    if if_gaoshui(b365_g_c,b365_pk_c_s) == True:
        guest_c_log = guest_c_log + "Beta365(" + b365_pk_c_s + str(b365_g_c) + ")|"
    if if_gaoshui(am_g_c,am_pk_c_s) == True:
        guest_c_log = guest_c_log + "澳门(" + am_pk_c_s+  str(am_g_c) + ")|"
    if if_gaoshui(b10_g_c,b10_pk_c_s) == True:
        guest_c_log = guest_c_log + "Bet10(" + b10_pk_c_s + str(b10_g_c) + ")|"
    if if_gaoshui(wb_g_c,wb_pk_c_s) == True:
        guest_c_log = guest_c_log + "Wewbet(" + wb_pk_c_s + str(wb_g_c) + ")|"

    if len(guest_c_log) == len_guest_c_log:
        pass
    else:
        guest_c_log = guest_c_log + "客队尾盘高水!"
        log.logger.warn(guest_c_log)
    # 第四步：判断盘口没有变化的话， 各个盘口的水位变化(未完待续)
    pankou_no_change(b365_pk_i, b365_pk_c, b365_pk_i_s, b365_pk_c_s, match_id, b365_h_i, b365_h_c, "Beta365", True)
    pankou_no_change(b365_pk_i, b365_pk_c, b365_pk_i_s, b365_pk_c_s, match_id, b365_g_i, b365_g_c, "Beta365", False)
    pankou_no_change(am_pk_i, am_pk_c, am_pk_i_s, am_pk_c_s, match_id, am_h_i, am_h_c, "澳门", True)
    pankou_no_change(am_pk_i, am_pk_c, am_pk_i_s, am_pk_c_s, match_id, am_g_i, am_g_c, "澳门", False)
    pankou_no_change(b10_pk_i, b10_pk_c, b10_pk_i_s, b10_pk_c_s, match_id, b10_h_i, b10_h_c, "Bet10", True)
    pankou_no_change(b10_pk_i, b10_pk_c, b10_pk_i_s, b10_pk_c_s, match_id, b10_g_i, b10_g_c, "Bet10", False)
    pankou_no_change(wb_pk_i, wb_pk_c, wb_pk_i_s, wb_pk_c_s, match_id, wb_h_i, wb_h_c, "Wewbet", True)
    pankou_no_change(wb_pk_i, wb_pk_c, wb_pk_i_s, wb_pk_c_s, match_id, wb_g_i, wb_g_c, "Wewbet", False)
    # 第五步: 升一级盘口， 如何定论还没有想好
    # 第六步： 降一级盘口，如何定论还没有想好
    # 升降一级的盘口， 下面要看看， 是真的升降？
    # if pankou_1_change(b365_pk_i, b365_pk_c, match_id, "Beta 365").strip():
    #     log.logger.info(pankou_1_change(b365_pk_i, b365_pk_c, match_id, "Beta 365"))
    # if pankou_1_change(am_pk_i, am_pk_c, match_id, "澳门").strip():
    #     log.logger.info(pankou_1_change(am_pk_i, am_pk_c, match_id, "澳门"))
    # if pankou_1_change(b10_pk_i, b10_pk_c, match_id, "Bet 10").strip():
    #     log.logger.info(pankou_1_change(b10_pk_i, b10_pk_c, match_id, "Bet 10"))
    # if pankou_1_change(wb_pk_i, wb_pk_c, match_id, "WebNet").strip():
    #     log.logger.info(pankou_1_change(wb_pk_i, wb_pk_c, match_id, "WebNet"))

    db.close()
    # End of function #####


def recent_10_match(match10, match_id,host):
    w = 0
    p = 0
    l = 0
    temph = ""
    if len(match10) != 0:
        for i in range(0, len(match10)):
            if match10[i] == "胜":
                w = w + 1
            elif match10[i] == "平":
                p = p + 1
            else:
                l = l + 1
        if host == "Y":
            temph = "match_id--" + match_id + "主队最近" + str(len(match10)) + "场" + str(w) + "胜" + str(p) + "平" + str(l) + "负"
            print(temph)
        else:
            temph = "match_id--" + match_id + "客队最近" + str(len(match10)) + "场" + str(w) + "胜" + str(p) + "平" + str(l) + "负"
            print(temph)
    return temph


def get_real_rank(host_rank,guest_rank, liansai, match_x):
    db = MySQLdb.connect("localhost", "root", "123456", "jingcai_db", charset='utf8')
    cursor = db.cursor()
    # At first, 杯赛 还是联赛, t_match table if no guest_rank it is set to 88
    if liansai.count("杯") == 1:
        log_string = "match_id = " + match_x + ":杯赛, 联赛排名不是那么重要，看最近状态和相互战绩 "
        log.logger.info(log_string)
    else:
        if host_rank == 88 or guest_rank == 88: # this is not real rank, try the t_zhanji table.
            sql_zhanji = "select host_rank, guest_rank from t_zhanji where match_id = '" + match_x + "'"
            cursor.execute(sql_zhanji)
            row = cursor.fetchone()
            temp_host_rank = row[0]
            temp_guest_rank = row[1]

            if temp_guest_rank != 60:
                guest_rank = temp_guest_rank
            if temp_host_rank != 60:
                host_rank = temp_host_rank
            # then get the index of  match_list[i] for this match_x
            npos = g_match_id_list.index(match_x)

            if host_rank != 88: # still !=88, update it
                g_host_rank[npos] = host_rank
                print(g_host_rank[npos])
            if guest_rank != 88:
                g_guest_rank[npos] = guest_rank

    db.close()


def host_guest_more_hot(match_x, host_name,guest_name,host_rank,guest_rank,liansai,rang_num):
    get_real_rank(host_rank, guest_rank, liansai, match_x)
    db = MySQLdb.connect("localhost", "root", "123456", "jingcai_db",charset='utf8')
    cursor = db.cursor()

    # ***********************************************
    # At first, need to check who is "hot" *********
    # ***********************************************
    sql_zhanji = "select * from t_zhanji where match_id = '" + match_x + "'"
    cursor.execute(sql_zhanji)
    row = cursor.fetchone()
    # Set the data
    match_id = row[0]
    host_rank = row[1]
    guest_rank = row[2]
    host_zhuchang_win = row[3]
    host_zhuchang_ping = row[4]
    host_zhuchang_lose = row[5]
    guest_kechang_win = row[6]
    guest_kechang_ping = row[7]
    guest_kechang_lose = row[8]
    host_win_count = row[9]
    host_ping_count = row[10]
    host_lose_count = row[11]
    latest_match1_host = row[12]
    latest_match1_host_score = row[13]
    latest_match1_guest_score = row[14]
    latest_match2_host = row[15]
    latest_match2_host_score = row[16]
    latest_match2_guest_score = row[17]
    latest_match3_host = row[18]
    latest_match3_host_score = row[19]
    latest_match3_guest_score = row[20]
    host_recent10_matchs = row[21]
    guest_recent10_matchs = row[22]

    #if host_rank != 60 and guest_rank != 60:
        # wu dang, xuyao yige dafenxitong , danshi zhege tainanle. buxiang zheme gao
    # Step 1: set : global "rank" and "host_name" and guest_name

    recent_10_match(host_recent10_matchs,  match_id, "Y")
    recent_10_match(guest_recent10_matchs, match_id, "N")
    # 主队主场状态
    temph = "match_id = " + match_id + ":主队:"+ host_name + "(联赛排名" + str(host_rank) + ")-主场状态" + str(host_zhuchang_win) + "胜" + str(host_zhuchang_ping) + "平" + str(host_zhuchang_lose) + "负"
    log.logger.info(temph)
    # 客队客场状态
    tempg = "match_id = " + match_id + ":客队:" + guest_name + "(联赛排名" + str(guest_rank) + ")-客场状态" + str(guest_kechang_win) + "胜" + str(guest_kechang_ping) + "平" + str(guest_kechang_lose) + "负"
    log.logger.info(tempg)
    # 主队|客队 交手情况 "match_id:" + match_id +
    temp_jiaoshou = "match_id = "  + match_id + "--" + host_name + "|" + guest_name + "交手,主队" + str(host_win_count) + "胜" + str(host_ping_count) + "平" + str(host_lose_count) + "负"
    log.logger.info(temp_jiaoshou)

    total_jiaoshou = host_win_count + host_ping_count + host_lose_count
    if total_jiaoshou == 0:
        no_jiaoshou = "match_id = "  + match_id + "两队无交手记录!"
        log.logger.info (no_jiaoshou)
    else:
        if total_jiaoshou == 1:
            if host_name == latest_match1_host:
                match1 = "match_id = " + match_id + ":最近三场比赛(1):" + host_name + "(as主)进球:" + str(
                    latest_match1_host_score) + "|" + guest_name + "(as客)进球:" + str(latest_match1_guest_score)
            else:
                match1 = "match_id = " + match_id + ":最近三场比赛(1):" + guest_name + "(as主)进球:" + str(
                    latest_match1_host_score) + "|" + host_name + "(as客)进球:" + str(latest_match1_guest_score)
            log.logger.info(match1)

        elif total_jiaoshou == 2:
            if host_name == latest_match1_host:
                match1 = "match_id = " + match_id + ":最近三场比赛(1):" + host_name + "(as主)进球:" + str(
                    latest_match1_host_score) + "|" + guest_name + "(as客)进球:" + str(latest_match1_guest_score)
            else:
                match1 = "match_id = " + match_id + ":最近三场比赛(1):" + guest_name + "(as主)进球:" + str(
                    latest_match1_host_score) + "|" + host_name + "(as客)进球:" + str(latest_match1_guest_score)

            if host_name == latest_match2_host:
                match2 = "match_id = " + match_id + ":最近三场比赛(2):" + host_name + "(as主)进球:" + str(
                    latest_match2_host_score) + "|" + guest_name + "(as客)进球:" + str(latest_match2_guest_score)
            else:
                match2 = "match_id = " + match_id + ":最近三场比赛(2):" + guest_name + "(as主)进球:" + str(
                    latest_match2_host_score) + "|" + host_name + "(as客)进球:" + str(latest_match2_guest_score)
            log.logger.info(match1)
            log.logger.info(match2)
        else:
            if host_name == latest_match1_host:
                match1 = "match_id = " + match_id + ":最近三场比赛(1):" + host_name + str(
                    latest_match1_host_score) + ":" + str(latest_match1_guest_score) + guest_name
            else:
                match1 = "match_id = " + match_id + ":最近三场比赛(1):" + guest_name + str(
                    latest_match1_host_score) + ":" + str(latest_match1_guest_score) + host_name

            if host_name == latest_match2_host:
                match2 = "match_id = " + match_id + ":最近三场比赛(2):" + host_name + str(
                    latest_match2_host_score) + ":" + str(latest_match2_guest_score) + guest_name
            else:
                match2 = "match_id = " + match_id + ":最近三场比赛(2):" + guest_name + str(
                    latest_match2_host_score) + ":" + str(latest_match2_guest_score) + host_name

            if host_name == latest_match3_host:
                match3 = "match_id = " + match_id + ":最近三场比赛(3):" + host_name + str(
                    latest_match3_host_score) + ":"  + str(latest_match3_guest_score) + guest_name
            else:
                match3 = "match_id = " + match_id + ":最近三场比赛(3):" + guest_name +  str(
                    latest_match3_host_score) + ":"  + str(latest_match3_guest_score) + host_name

            log.logger.info(match1)
            log.logger.info(match2)
            log.logger.info(match3)
            pass



    # if host_name == latest_match3_host:
    #     match3 = "match_id = " + match_id + ":最近三场比赛(2):" + host_name + "(as主)进球:" + str(
    #         latest_match3_host_score) + "|" + guest_name + "(as客)进球:" + str(latest_match3_guest_score)
    # else:
    #     match3 = "match_id = " + match_id + ":最近三场比赛(3):" + guest_name + "(as主)进球:" + str(latest_match3_host_score) + "|" + "(as客)进球:" + str(latest_match3_guest_score)
    # #log.logger.info(match3)

    db.close()

#def team_rank_level(match_id):
    # 日职乙 22
# Analysis jingcai peilv
def analyze_jicai_peilv(match_x,host_name,guest_name,host_rank,guest_rank,liansai,rang_num):
    db = MySQLdb.connect("localhost", "root", "123456", "jingcai_db",charset='utf8')
    cursor = db.cursor()
    sql_jingcai = "select * from t_match where match_id = '" + match_x + "'"
    cursor.execute(sql_jingcai)
    row = cursor.fetchone()
    match_id = row[0]
    liansai = row[2]
    host_name = row[3]
    host_guest_rank = int(row[4])
    guest_name = row[5]
    guest_league_rank = int(row[6])
    host_win_pei_lv = float(row[7])
    ping_pei_lv = float(row[8])
    guest_win_pei_lv = float(row[9])
    rang_num = row[10]
    rang_host_win_pei_lv = float(row[11])
    rang_ping_pei_lv = float(row[12])
    rang_guest_win_pei_lv = float(row[13])
    # Set global infomation:

    # judge the dui yao pei lv
    if peilv_huyao(host_win_pei_lv,ping_pei_lv,guest_win_pei_lv,match_id,"竞彩i").strip():
        log.logger.info(peilv_huyao(host_win_pei_lv, ping_pei_lv, guest_win_pei_lv, match_id, "竞彩i"))
        # judge who is the weaker team.
    if peilv_huyao(rang_host_win_pei_lv,ping_pei_lv,rang_guest_win_pei_lv,match_id,"竞彩r").strip():
        log.logger.info(peilv_huyao(rang_host_win_pei_lv, rang_ping_pei_lv, rang_guest_win_pei_lv, match_id, "竞彩r"))
    if peilv_huyao(host_win_pei_lv, 3.00, rang_guest_win_pei_lv, match_id, "竞彩主队让1球"):
        log.logger.info(peilv_huyao(host_win_pei_lv, 3.00, rang_guest_win_pei_lv, match_id, "竞彩主队让1球"))
    if peilv_huyao(guest_win_pei_lv, 3.00, rang_host_win_pei_lv, match_id, "竞彩客队让1球"):
        log.logger.info(peilv_huyao(guest_win_pei_lv, 3.00, rang_host_win_pei_lv, match_id, "竞彩客队让1球"))
    # 评估打出的概率

    db.close()

#
def search_sql_wpl(sql):
    wnum = 0
    pnum = 0
    lnum = 0
    db1 = MySQLdb.connect("localhost", "root", "123456", "jingcai_db", charset='utf8')
    cursor1 = db1.cursor()
    cursor1.execute(sql)
    data = cursor1.fetchall()
    if len(data) != 0:
        for row in data:
            if row[0] == 'W':
                wnum = wnum + 1
            elif row[0] == 'P':
                pnum = pnum + 1
            else:
                lnum = lnum + 1

    db1.close()
    return wnum, pnum, lnum

def peilv_gailv(x,y,z):
    total_num = x + y + z
    win_gailv =""
    ping_gailv = ""
    lose_gailv = ""
    return_string = ""
    if total_num == 0:
        return_string = ":没有这样的赔率组合"
    else:
        if x == 0:
            win_gailv = "0%"
        else:
            temp_win_gailv = x/(total_num)
            # Conver it into the percentage
            win_gailv = "%.2f%%" % (temp_win_gailv * 100)
        if y == 0:
            ping_gailv = "0%"
        else:
            temp_ping_gailv = y/(total_num)
            ping_gailv = "%.2f%%" % (temp_ping_gailv * 100)
        if z == 0:
            lose_gailv = "0%"
        else:
            temp_lose_gailv = z/(total_num)
            lose_gailv = "%.2f%%" % (temp_lose_gailv * 100)
        return_string = "主队赢得概率:"+ win_gailv + "(" + str(x) + "次)-平的概率：" + ping_gailv + "(" + str(y) + "次)-输的概率：" + lose_gailv + "(" + str(z) + "次)!"
    return return_string

#如果赔率不变， 次赔率下的胜平负的场次:
def wpl_pei_nochange(x,y,z, match_id, company):
    sql1 = ""
    sql2 = ""
    sql3 = ""
    # **********************************************
    # The following rules are specific for ou pei  *
    # ***********************************************
    w = 0
    p = 0
    l = 0
    temp_log = ""
    if abs(float(x)-1.01) <=1e-5:
        pass
    else:
        if company == "LIBO":
            sql1 = "select a.w_p_l_result from t_result a, t_oupei_result b where a.match_id = b.match_id and LB_Win_I = '"\
                   + x + "' and LB_Ping_I = '" + y + "' and LB_Lose_I = '" + z + "'"
            w, p, l = search_sql_wpl(sql1)
            if (w != 0) or (p != 0) or (l != 0):
                temp_log = "match_id = " + match_id + ":" + company + " Only初始赔率:" + x + "|" + y + "|" + z + " 胜:" + str(w) + "|平" + str(p) + "|负" + str(l)
                log.logger.info(temp_log)

            sql2 = "select a.w_p_l_result from t_result a, t_oupei_result b where a.match_id = b.match_id and LB_Win_C = '" \
                   + x + "' and LB_Ping_C = '" + y + "' and LB_Lose_C = '" + z + "'"
            w, p, l = search_sql_wpl(sql2)
            if (w != 0) or (p != 0) or (l != 0):
                temp_log = "match_id = " + match_id + ":" + company + " Only最终赔率:" + x + "|" + y + "|" + z + " 胜:" + str(
                    w) + "|平" + str(p) + "|负" + str(l)
                log.logger.info(temp_log)

            sql3 = "select a.w_p_l_result from t_result a, t_oupei_result b where a.match_id = b.match_id and LB_Win_I = '" \
                   + x + "' and LB_Ping_I = '" + y + "' and LB_Lose_I = '" + z + "' and LB_Win_C = '" + x + "' and LB_Ping_C = '" + y + "' and LB_Lose_C = '" + z + "'"
            w, p, l = search_sql_wpl(sql3)
            if (w != 0) or (p != 0) or (l != 0):
                temp_log = "match_id = " + match_id + ":" + company + " 初始+最终赔率:" + x + "|" + y + "|" + z + " 胜:" + str(
                    w) + "|平" + str(p) + "|负" + str(l)
                log.logger.info(temp_log)

        elif company == "ODDSET":
            sql1 = "select a.w_p_l_result from t_result a, t_oupei_result b where a.match_id = b.match_id and ODD_Win_I = '" + x + "' and ODD_Ping_I = '" + y + "' and ODD_Lose_I = '" + z + "'"
            w, p, l = search_sql_wpl(sql1)
            if (w != 0) or (p != 0) or (l != 0):
                temp_log = "match_id = " + match_id + ":" + company + " Only初始赔率:" + x + "|" + y + "|" + z + " 胜:" + str(
                    w) + "|平" + str(p) + "|负" + str(l)
                log.logger.info(temp_log)

            sql2 = "select a.w_p_l_result from t_result a, t_oupei_result b where a.match_id = b.match_id and ODD_Win_C = '" + x + "' and ODD_Ping_C = '" + y + "' and ODD_Lose_C = '" + z + "'"
            w, p, l = search_sql_wpl(sql2)
            if (w != 0) or (p != 0) or (l != 0):
                temp_log = "match_id = " + match_id + ":" + company + " Only最终赔率:" + x + "|" + y + "|" + z + " 胜:" + str(
                    w) + "|平" + str(p) + "|负" + str(l)
                log.logger.info(temp_log)

            sql3 = "select a.w_p_l_result from t_result a, t_oupei_result b where a.match_id = b.match_id and ODD_Win_I = '" + x + "' and ODD_Ping_I = '" + y + "' and ODD_Lose_I = '" + z + "' and ODD_Win_C = '" + x + "' and ODD_Ping_C = '" + y + "' and ODD_Lose_C = '" + z + "'"
            w, p, l = search_sql_wpl(sql3)
            if (w != 0) or (p != 0) or (l != 0):
                temp_log = "match_id = " + match_id + ":" + company + " 初始+最终赔率:" + x + "|" + y + "|" + z + " 胜:" + str(
                    w) + "|平" + str(p) + "|负" + str(l)
                log.logger.info(temp_log)

        elif company == "BWIN":
            sql1 = "select a.w_p_l_result from t_result a, t_oupei_result b where a.match_id = b.match_id and BW_Win_I = '" + x + "' and BW_Ping_I = '" + y + "' and BW_Lose_I = '" + z + "'"
            w, p, l = search_sql_wpl(sql1)
            if (w != 0) or (p != 0) or (l != 0):
                temp_log = "match_id = " + match_id + ":" + company + " Only初始赔率:" + x + "|" + y + "|" + z + "胜:" + str(
                    w) + "|平" + str(p) + "|负" + str(l)
                log.logger.info(temp_log)

            sql2 = "select a.w_p_l_result from t_result a, t_oupei_result b where a.match_id = b.match_id and BW_Win_C = '" + x + "' and BW_Ping_C = '" + y + "' and BW_Lose_C = '" + z + "'"
            w, p, l = search_sql_wpl(sql2)
            if (w != 0) or (p != 0) or (l != 0):
                temp_log = "match_id = " + match_id + ":" + company + " Only最终赔率:" + x + "|" + y + "|" + z + "胜:" + str(
                    w) + "|平" + str(p) + "|负" + str(l)
                log.logger.info(temp_log)

            sql3 = "select a.w_p_l_result from t_result a, t_oupei_result b where a.match_id = b.match_id and BW_Win_I = '" + x + "' and BW_Ping_I = '" + y + "' and BW_Lose_I = '" + z + "' and BW_Win_C = '" + x + "' and BW_Ping_C = '" + y + "' and BW_Lose_C = '" + z + "'"
            w, p, l = search_sql_wpl(sql3)
            if (w != 0) or (p != 0) or (l != 0):
                temp_log = "match_id = " + match_id + ":" + company + " 初始+最终赔率:" + x + "|" + y + "|" + z + "胜:" + str(
                    w) + "|平" + str(p) + "|负" + str(l)
                log.logger.info(temp_log)

        elif company == "William":
            sql1 = "select a.w_p_l_result from t_result a, t_oupei_result b where a.match_id = b.match_id and WL_Win_I = '" + x + "' and WL_Ping_I = '" + y + "' and WL_Lose_I = '" + z + "'"
            w, p, l = search_sql_wpl(sql1)
            if (w != 0) or (p != 0) or (l != 0):
                temp_log = "match_id = " + match_id + ":" + company + " Only初始赔率:" + x + "|" + y + "|" + z + "胜:" + str(
                    w) + "|平" + str(p) + "|负" + str(l)
                log.logger.info(temp_log)

            sql2 = "select a.w_p_l_result from t_result a, t_oupei_result b where a.match_id = b.match_id and WL_Win_C = '" + x + "' and WL_Ping_C = '" + y + "' and WL_Lose_C = '" + z + "'"
            w, p, l = search_sql_wpl(sql2)
            if (w != 0) or (p != 0) or (l != 0):
                temp_log = "match_id = " + match_id + ":" + company + " Only最终赔率:" + x + "|" + y + "|" + z + "胜:" + str(
                    w) + "|平" + str(p) + "|负" + str(l)
                log.logger.info(temp_log)

            sql3 = "select a.w_p_l_result from t_result a, t_oupei_result b where a.match_id = b.match_id and WL_Win_I = '" + x + "' and WL_Ping_I = '" + y + "' and WL_Lose_I = '" + z + "' and WL_Win_C = '" + x + "' and WL_Ping_C = '" + y + "' and WL_Lose_C = '" + z + "'"
            w, p, l = search_sql_wpl(sql3)
            if (w != 0) or (p != 0) or (l != 0):
                temp_log = "match_id = " + match_id + ":" + company + " 初始+最终赔率:" + x + "|" + y + "|" + z + " 胜:" + str(
                    w) + "|平" + str(p) + "|负" + str(l)
                log.logger.info(temp_log)

        elif company == "Bet365":
            sql1 = "select a.w_p_l_result from t_result a, t_oupei_result b where a.match_id = b.match_id and B365_Win_I = '" + x + "' and B365_Ping_I = '" + y + "' and B365_Lose_I = '" + z + "'"
            w, p, l = search_sql_wpl(sql1)
            if (w != 0) or (p != 0) or (l != 0):
                temp_log = "match_id = " + match_id + ":" + company + " Only初始赔率:" + x + "|" + y + "|" + z + "胜:" + str(
                    w) + "|平" + str(p) + "|负" + str(l)
                log.logger.info(temp_log)

            sql2 = "select a.w_p_l_result from t_result a, t_oupei_result b where a.match_id = b.match_id and B365_Win_C = '" + x + "' and B365_Ping_C = '" + y + "' and B365_Lose_C = '" + z + "'"
            w, p, l = search_sql_wpl(sql2)
            if (w != 0) or (p != 0) or (l != 0):
                temp_log = "match_id = " + match_id + ":" + company + " Only最终赔率:" + x + "|" + y + "|" + z + "胜:" + str(
                    w) + "|平" + str(p) + "|负" + str(l)
                log.logger.info(temp_log)

            sql3 = "select a.w_p_l_result from t_result a, t_oupei_result b where a.match_id = b.match_id and B365_Win_I = '" + x + "' and B365_Ping_I = '" + y + "' and B365_Lose_I = '" + z + "' and B365_Win_C = '" + x + "' and B365_Ping_C = '" + y + "' and B365_Lose_C = '" + z + "'"
            w, p, l = search_sql_wpl(sql3)
            if (w != 0) or (p != 0) or (l != 0):
                temp_log = "match_id = " + match_id + ":" + company + "初始+最终赔率:" + x + "|" + y + "|" + z + " 胜:" + str(
                    w) + "|平" + str(p) + "|负" + str(l)
                log.logger.info(temp_log)

        elif company == "Interview":
            sql1 = "select a.w_p_l_result from t_result a, t_oupei_result b where a.match_id = b.match_id and IN_Win_I = '" + x + "' and IN_Ping_I = '" + y + "' and IN_Lose_I = '" + z + "'"
            w, p, l = search_sql_wpl(sql1)
            if (w != 0) or (p != 0) or (l != 0):
                temp_log = "match_id = " + match_id + ":" + company + " Only初始赔率:" + x + "|" + y + "|" + z + "胜:" + str(
                    w) + "|平" + str(p) + "|负" + str(l)
                log.logger.info(temp_log)

            sql2 = "select a.w_p_l_result from t_result a, t_oupei_result b where a.match_id = b.match_id and IN_Win_C = '" + x + "' and IN_Ping_C = '" + y + "' and IN_Lose_C = '" + z + "'"
            w, p, l = search_sql_wpl(sql2)
            if (w != 0) or (p != 0) or (l != 0):
                temp_log = "match_id = " + match_id + ":" + company + " Only最终赔率:" + x + "|" + y + "|" + z + "胜:" + str(
                    w) + "|平" + str(p) + "|负" + str(l)
                log.logger.info(temp_log)

            sql3 = "select a.w_p_l_result from t_result a, t_oupei_result b where a.match_id = b.match_id and IN_Win_I = '" + x + "' and IN_Ping_I = '" + y + "' and IN_Lose_I = '" + z + "' and IN_Win_C = '" + x + "' and IN_Ping_C = '" + y + "' and IN_Lose_C = '" + z + "'"
            w, p, l = search_sql_wpl(sql3)
            if (w != 0) or (p != 0) or (l != 0):
                temp_log = "match_id = " + match_id + ":" + company + " 初始+最终赔率:" + x + "|" + y + "|" + z + " 胜:" + str(
                    w) + "|平" + str(p) + "|负" + str(l)
                log.logger.info(temp_log)

        elif company == "SINA":
            sql1 = "select a.w_p_l_result from t_result a, t_oupei_result b where a.match_id = b.match_id and SN_Win_I = '" + x + "' and SN_Ping_I = '" + y + "' and SN_Lose_I = '" + z + "'"
            w, p, l = search_sql_wpl(sql1)
            if (w != 0) or (p != 0) or (l != 0):
                temp_log = "match_id = " + match_id + ":" + company + " Only初始赔率:" + x + "|" + y + "|" + z + " 胜:" + str(
                    w) + "|平" + str(p) + "|负" + str(l)
                log.logger.info(temp_log)

            sql2 = "select a.w_p_l_result from t_result a, t_oupei_result b where a.match_id = b.match_id and SN_Win_C = '" + x + "' and SN_Ping_C = '" + y + "' and SN_Lose_C = '" + z + "'"
            w, p, l = search_sql_wpl(sql2)
            if (w != 0) or (p != 0) or (l != 0):
                temp_log = "match_id = " + match_id + ":" + company + " Only最终赔率:" + x + "|" + y + "|" + z + " 胜:" + str(
                    w) + "|平" + str(p) + "|负" + str(l)
                log.logger.info(temp_log)

            sql3 = "select a.w_p_l_result from t_result a, t_oupei_result b where a.match_id = b.match_id and SN_Win_I = '" + x + "' and SN_Ping_I = '" + y + "' and SN_Lose_I = '" + z + "' and SN_Win_C = '" + x + "' and SN_Ping_C = '" + y + "' and SN_Lose_C = '" + z + "'"
            w, p, l = search_sql_wpl(sql3)
            if (w != 0) or (p != 0) or (l != 0):
                temp_log = "match_id = " + match_id + ":" + company + " 初始+最终赔率:" + x + "|" + y + "|" + z + " 胜:" + str(
                    w) + "|平" + str(p) + "|负" + str(l)
                log.logger.info(temp_log)
        else:
            print("no such company")


def initial_peilv_gailv(x, y, z, match_id, company):
    sql1 = ""

    # **********************************************
    # The following rules are specific for ou pei  *
    # ***********************************************
    w = 0
    p = 0
    l = 0
    temp_log = ""
    if (float(x) - 1.01) <= 1e-5:
        pass
    else:
        if company == "LIBO":
            sql1 = "select a.w_p_l_result from t_result a, t_oupei_result b where a.match_id = b.match_id and LB_Win_I = '" + x + "' and LB_Ping_I = '" + y + "' and LB_Lose_I = '" + z + "'"
            w, p, l = search_sql_wpl(sql1)
            temp_log = peilv_gailv(w, p, l)
            temp_log = "match_id = " + match_id + ":" + company + "初始赔率:" + x + "|" + y + "|" + z + "下" + temp_log
            log.logger.info(temp_log)


        elif company == "ODDSET":
            sql1 = "select a.w_p_l_result from t_result a, t_oupei_result b where a.match_id = b.match_id and ODD_Win_I = '" + x + "' and ODD_Ping_I = '" + y + "' and ODD_Lose_I = '" + z + "'"
            w, p, l = search_sql_wpl(sql1)
            temp_log = peilv_gailv(w, p, l)
            temp_log = "match_id = " + match_id + ":" + company + "初始赔率:" + x + "|" + y + "|" + z + "下" + temp_log
            log.logger.info(temp_log)


        elif company == "BWIN":
            sql1 = "select a.w_p_l_result from t_result a, t_oupei_result b where a.match_id = b.match_id and BW_Win_I = '" + x + "' and BW_Ping_I = '" + y + "' and BW_Lose_I = '" + z + "'"
            w, p, l = search_sql_wpl(sql1)
            temp_log = peilv_gailv(w, p, l)
            temp_log = "match_id = " + match_id + ":" + company + "初始赔率:" + x + "|" + y + "|" + z + "下" + temp_log
            log.logger.info(temp_log)


        elif company == "William":
            sql1 = "select a.w_p_l_result from t_result a, t_oupei_result b where a.match_id = b.match_id and WL_Win_I = '" + x + "' and WL_Ping_I = '" + y + "' and WL_Lose_I = '" + z + "'"
            w, p, l = search_sql_wpl(sql1)
            temp_log = peilv_gailv(w, p, l)
            temp_log = "match_id = " + match_id + ":" + company + "初始赔率:" + x + "|" + y + "|" + z + "下" + temp_log
            log.logger.info(temp_log)

        elif company == "Bet365":
            sql1 = "select a.w_p_l_result from t_result a, t_oupei_result b where a.match_id = b.match_id and B365_Win_I = '" + x + "' and B365_Ping_I = '" + y + "' and B365_Lose_I = '" + z + "'"
            w, p, l = search_sql_wpl(sql1)
            temp_log = peilv_gailv(w, p, l)
            temp_log = "match_id = " + match_id + ":" + company + "初始赔率:" + x + "|" + y + "|" + z + "下" + temp_log
            log.logger.info(temp_log)

        elif company == "Interview":
            sql1 = "select a.w_p_l_result from t_result a, t_oupei_result b where a.match_id = b.match_id and IN_Win_I = '" + x + "' and IN_Ping_I = '" + y + "' and IN_Lose_I = '" + z + "'"
            w, p, l = search_sql_wpl(sql1)
            temp_log = peilv_gailv(w, p, l)
            temp_log = "match_id = " + match_id + ":" + company + "初始赔率:" + x + "|" + y + "|" + z + "下" + temp_log
            log.logger.info(temp_log)

        elif company == "SINA":
            sql1 = "select a.w_p_l_result from t_result a, t_oupei_result b where a.match_id = b.match_id and SN_Win_I = '" + x + "' and SN_Ping_I = '" + y + "' and SN_Lose_I = '" + z + "'"
            w, p, l = search_sql_wpl(sql1)
            temp_log = peilv_gailv(w, p, l)
            temp_log = "match_id = " + match_id + ":" + company + "初始赔率:" + x + "|" + y + "|" + z + "下" + temp_log
            log.logger.info(temp_log)
        else:
            print("no such company")

def changed_peilv_gailv(x, y, z, match_id, company):
    sql1 = ""

    # **********************************************
    # The following rules are specific for ou pei  *
    # ***********************************************
    w = 0
    p = 0
    l = 0
    temp_log = ""
    if (float(x) - 1.01) <= 1e-5:
        pass
    else:
        if company == "LIBO":
            sql1 = "select a.w_p_l_result from t_result a, t_oupei_result b where a.match_id = b.match_id and LB_Win_C = '" + x + "' and LB_Ping_C = '" + y + "' and LB_Lose_C = '" + z + "'"
            w, p, l = search_sql_wpl(sql1)
            temp_log = peilv_gailv(w, p, l)
            temp_log = "match_id = " + match_id + ":" + company + "变盘赔率:" + x + "|" + y + "|" + z + "下" + temp_log
            log.logger.info(temp_log)


        elif company == "ODDSET":
            sql1 = "select a.w_p_l_result from t_result a, t_oupei_result b where a.match_id = b.match_id and ODD_Win_C = '" + x + "' and ODD_Ping_C = '" + y + "' and ODD_Lose_C = '" + z + "'"
            w, p, l = search_sql_wpl(sql1)
            temp_log = peilv_gailv(w, p, l)
            temp_log = "match_id = " + match_id + ":" + company + "变盘赔率:" + x + "|" + y + "|" + z + "下" + temp_log
            log.logger.info(temp_log)


        elif company == "BWIN":
            sql1 = "select a.w_p_l_result from t_result a, t_oupei_result b where a.match_id = b.match_id and BW_Win_C = '" + x + "' and BW_Ping_C = '" + y + "' and BW_Lose_C = '" + z + "'"
            w, p, l = search_sql_wpl(sql1)
            temp_log = peilv_gailv(w, p, l)
            temp_log = "match_id = " + match_id + ":" + company + "变盘赔率:" + x + "|" + y + "|" + z + "下" + temp_log
            log.logger.info(temp_log)


        elif company == "William":
            sql1 = "select a.w_p_l_result from t_result a, t_oupei_result b where a.match_id = b.match_id and WL_Win_C = '" + x + "' and WL_Ping_C = '" + y + "' and WL_Lose_C = '" + z + "'"
            w, p, l = search_sql_wpl(sql1)
            temp_log = peilv_gailv(w, p, l)
            temp_log = "match_id = " + match_id + ":" + company + "变盘赔率:" + x + "|" + y + "|" + z + "下" + temp_log
            log.logger.info(temp_log)

        elif company == "Bet365":
            sql1 = "select a.w_p_l_result from t_result a, t_oupei_result b where a.match_id = b.match_id and B365_Win_C = '" + x + "' and B365_Ping_C = '" + y + "' and B365_Lose_C = '" + z + "'"
            w, p, l = search_sql_wpl(sql1)
            temp_log = peilv_gailv(w, p, l)
            temp_log = "match_id = " + match_id + ":" + company + "变盘赔率:" + x + "|" + y + "|" + z + "下" + temp_log
            log.logger.info(temp_log)

        elif company == "Interview":
            sql1 = "select a.w_p_l_result from t_result a, t_oupei_result b where a.match_id = b.match_id and IN_Win_C = '" + x + "' and IN_Ping_C = '" + y + "' and IN_Lose_C = '" + z + "'"
            w, p, l = search_sql_wpl(sql1)
            temp_log = peilv_gailv(w, p, l)
            temp_log = "match_id = " + match_id + ":" + company + "变盘赔率:" + x + "|" + y + "|" + z + "下" + temp_log
            log.logger.info(temp_log)

        elif company == "SINA":
            sql1 = "select a.w_p_l_result from t_result a, t_oupei_result b where a.match_id = b.match_id and SN_Win_C = '" + x + "' and SN_Ping_C = '" + y + "' and SN_Lose_C = '" + z + "'"
            w, p, l = search_sql_wpl(sql1)
            temp_log = peilv_gailv(w, p, l)
            temp_log = "match_id = " + match_id + ":" + company + "变盘赔率:" + x + "|" + y + "|" + z + "下" + temp_log
            log.logger.info(temp_log)
        else:
            print("no such company")

def Policy_Decison(match_x,host_name,guest_name,host_rank,guest_rank,liansai,rang_num):
    # Open a log
    #log = Logger('all.log', clevel=logging.INFO, flevel=logging.INFO)
    #log = Logger('all.log', level='debug')
    db = MySQLdb.connect("localhost","root","123456","jingcai_db", charset='utf8')
    cursor = db.cursor()

        # **********************************************
    # The following rules are specific for ou pei  *
    # ***********************************************
    sql = "select * from t_oupei where match_id = '" + match_x + "'"
    cursor.execute(sql)
    row = cursor.fetchone()

    match_id = row[0]
    ## Jing Cai pei lv
    jc_win_i = float(row[1])
    jc_ping_i = float(row[2])
    jc_lose_i = float(row[3])
    jc_win_c = float(row[4])
    jc_ping_c = float(row[5])
    jc_lose_c = float(row[6])

    s_jc_win_i = row[1]
    s_jc_ping_i = row[2]
    s_jc_lose_i = row[3]
    s_jc_win_c = row[4]
    s_jc_ping_c = row[5]
    s_jc_lose_c = row[6]

    # william
    wl_win_i = float(row[7])
    wl_ping_i = float(row[8])
    wl_lose_i = float(row[9])
    wl_win_c = float(row[10])
    wl_ping_c = float(row[11])
    wl_lose_c = float(row[12])

    s_wl_win_i = row[7]
    s_wl_ping_i = row[8]
    s_wl_lose_i = row[9]
    s_wl_win_c = row[10]
    s_wl_ping_c = row[11]
    s_wl_lose_c = row[12]

    # 立博
    lb_win_i = float(row[13])
    lb_ping_i = float(row[14])
    lb_lose_i = float(row[15])
    lb_win_c = float(row[16])
    lb_ping_c = float(row[17])
    lb_lose_c = float(row[18])

    s_lb_win_i = row[13]
    s_lb_ping_i = row[14]
    s_lb_lose_i = row[15]
    s_lb_win_c = row[16]
    s_lb_ping_c = row[17]
    s_lb_lose_c = row[18]

    # bwin
    bw_win_i = float(row[19])
    bw_ping_i = float(row[20])
    bw_lose_i = float(row[21])
    bw_win_c = float(row[22])
    bw_ping_c = float(row[23])
    bw_lose_c = float(row[24])

    s_bw_win_i = row[19]
    s_bw_ping_i = row[20]
    s_bw_lose_i = row[21]
    s_bw_win_c = row[22]
    s_bw_ping_c = row[23]
    s_bw_lose_c = row[24]

    # Interview
    in_win_i = float(row[25])
    in_ping_i = float(row[26])
    in_lose_i = float(row[27])
    in_win_c = float(row[28])
    in_ping_c = float(row[29])
    in_lose_c = float(row[30])

    s_in_win_i = row[25]
    s_in_ping_i = row[26]
    s_in_lose_i = row[27]
    s_in_win_c = row[28]
    s_in_ping_c = row[29]
    s_in_lose_c = row[30]

    # SINA
    sn_win_i = float(row[31])
    sn_ping_i = float(row[32])
    sn_lose_i = float(row[33])
    sn_win_c = float(row[34])
    sn_ping_c = float(row[35])
    sn_lose_c = float(row[36])

    s_sn_win_i = row[31]
    s_sn_ping_i = row[32]
    s_sn_lose_i = row[33]
    s_sn_win_c = row[34]
    s_sn_ping_c = row[35]
    s_sn_lose_c = row[36]

    # ODDSET
    odd_win_i = float(row[37])
    odd_ping_i = float(row[38])
    odd_lose_i = float(row[39])
    odd_win_c = float(row[40])
    odd_ping_c = float(row[41])
    odd_lose_c = float(row[42])

    s_odd_win_i = row[37]
    s_odd_ping_i = row[38]
    s_odd_lose_i = row[39]
    s_odd_win_c = row[40]
    s_odd_ping_c = row[41]
    s_odd_lose_c = row[42]

    # Bet 365
    b365_win_i = float(row[43])
    b365_ping_i = float(row[44])
    b365_lose_i = float(row[45])
    b365_win_c = float(row[46])
    b365_ping_c = float(row[47])
    b365_lose_c = float(row[48])

    s_b365_win_i = row[43]
    s_b365_ping_i = row[44]
    s_b365_lose_i = row[45]
    s_b365_win_c = row[46]
    s_b365_ping_c = row[47]
    s_b365_lose_c = row[48]
    # At first, go to initial peilv of four companys
    step3_sub1 = "match_id = " + match_id + " ===>step 3.1): " + "赔率分析第一步:"
    log.logger.info(step3_sub1)
    initial_peilv_gailv(s_lb_win_i, s_lb_ping_i, s_lb_lose_i, match_id, "LIBO")
    changed_peilv_gailv(s_lb_win_c, s_lb_ping_c, s_lb_lose_c, match_id, "LIBO")
    initial_peilv_gailv(s_wl_win_i, s_wl_ping_i, s_wl_lose_i, match_id, "William")
    changed_peilv_gailv(s_wl_win_c, s_wl_ping_c, s_wl_lose_c, match_id, "William")
    initial_peilv_gailv(s_odd_win_i, s_odd_ping_i, s_odd_lose_i, match_id, "ODDSET")
    changed_peilv_gailv(s_odd_win_c, s_odd_ping_c, s_odd_lose_c, match_id, "ODDSET")
    initial_peilv_gailv(s_b365_win_i, s_b365_ping_i, s_b365_lose_i, match_id, "Bet365")
    changed_peilv_gailv(s_b365_win_c, s_b365_ping_c, s_b365_lose_c, match_id, "Bet365")
    initial_peilv_gailv(s_bw_win_i, s_bw_ping_i, s_bw_lose_i, match_id, "BWIN")
    changed_peilv_gailv(s_bw_win_c, s_bw_ping_c, s_bw_lose_c, match_id, "BWIN")
    initial_peilv_gailv(s_sn_win_i, s_sn_ping_i, s_sn_lose_i, match_id, "SINA")
    changed_peilv_gailv(s_sn_win_c, s_sn_ping_c, s_sn_lose_c, match_id, "SINA")
    initial_peilv_gailv(s_in_win_i, s_in_ping_i, s_in_lose_i, match_id, "Interview")
    changed_peilv_gailv(s_in_win_c, s_in_ping_c, s_in_lose_c, match_id, "Interview")
    #

    if rang_num == "-1" or rang_num == "-2":

        if (lb_win_i > wl_win_i) and (lb_win_i > odd_win_i) and (lb_win_i > b365_win_i) and (lb_win_i > bw_win_i) and (lb_win_i > sn_win_i) and (lb_win_i > in_win_i):
            temp_log = "match_id = " + match_id + "--LIBO 初始赢得赔率高于所有其他公司!" + host_name + "(让" + rang_num + ")球"
            log.logger.warn(temp_log)
        temp_log1 = ""
        if (b365_win_i/lb_win_i) >= 1.30:
            temp_log1 = ":B365"
        if (bw_win_i/lb_win_i) >= 1.30:
            temp_log1 =temp_log1 + ":BWIN"
        if (in_win_i/lb_win_i) >= 1.30:
            temp_log1 = temp_log1 + ":Interview"
        if (sn_win_i/lb_win_i) >= 1.30:
            temp_log1 = temp_log1 + ":SINA"
        if (odd_win_i/lb_win_i) >= 1.30:
            temp_log1 = temp_log1 + ":ODDSet"
        if len(temp_log1) > 0:
            temp_log1 = "match_id = " + match_id + host_name +"（主队）--" + temp_log1 + "赢的赔率超过立博30%!!!!"
            log.logger.warn(temp_log1)

    elif rang_num == "+1" and rang_num == "+2":
        if (lb_lose_i > wl_lose_i) and (lb_lose_i > odd_lose_i) and (lb_lose_i > b365_lose_i) and (
                lb_lose_i > bw_lose_i) and (lb_lose_i > sn_lose_i) and (lb_lose_i > in_lose_i):
            temp_log = "match_id = " + match_id + "--LIBO 初始赢得赔率高于所有其他公司!" + guest_name + "(让" + rang_num + ")球"
            log.logger.warn(temp_log)
        temp_log1 = ""
        if (b365_lose_i / lb_lose_i) >= 1.30:
            temp_log1 = ":B365"
        if (bw_lose_i / lb_lose_i) >= 1.30:
            temp_log1 = temp_log1 + ":BWIN"
        if (in_lose_i / lb_lose_i) >= 1.30:
            temp_log1 = temp_log1 + ":Interview"
        if (sn_lose_i / lb_lose_i) >= 1.30:
            temp_log1 = temp_log1 + ":SINA"
        if (odd_lose_i / lb_lose_i) >= 1.30:
            temp_log1 = temp_log1 + ":ODDSet"
        if len(temp_log1) > 0:
            temp_log1 = "match_id = " + match_id + guest_name + "（客队）--" + temp_log1 + "赢的赔率超过立博30%!!!!"
            log.logger.warn(temp_log1)

    step3_sub2= "match_id = " + match_id + " ===>step 3.2): " + "赔率分析第2步:"
    log.logger.info(step3_sub2)
    if peilv_change(lb_win_i,lb_ping_i,lb_lose_i,lb_win_c,lb_ping_c,lb_lose_c, match_id, "立博"):
        log.logger.info(peilv_change(lb_win_i,lb_ping_i,lb_lose_i,lb_win_c,lb_ping_c,lb_lose_c, match_id, "立博"))
        # 如果赔率不变， 次赔率下的胜平负的场次：
        wpl_pei_nochange(s_lb_win_i,s_lb_ping_i,s_lb_lose_i, match_id, "LIBO")

    # judge if meet some specific peilv
    if is_special_peilv(lb_win_i,lb_ping_i,lb_lose_i,match_id,"立博i").strip():
       log.logger.info(is_special_peilv(lb_win_i,lb_ping_i,lb_lose_i,match_id,"立博i"))
    if is_special_peilv(lb_win_c,lb_ping_c,lb_lose_c,match_id,"立博c").strip():
       log.logger.info(is_special_peilv(lb_win_c,lb_ping_c,lb_lose_c,match_id,"立博c"))

    if peilv_huyao(lb_win_i,lb_ping_i,lb_lose_i,match_id,"立博i").strip():
        log.logger.info(peilv_huyao(lb_win_i,lb_ping_i,lb_lose_i,match_id,"立博i"))
    if peilv_huyao(lb_win_c,lb_ping_c,lb_lose_c,match_id,"立博c").strip():
        log.logger.info(peilv_huyao(lb_win_c,lb_ping_c,lb_lose_c,match_id,"立博c"))

    # William
    if peilv_change(wl_win_i, wl_ping_i, wl_lose_i, wl_win_c, wl_ping_c, wl_lose_c, match_id, "William"):
        log.logger.info(peilv_change(wl_win_i, wl_ping_i, wl_lose_i, wl_win_c, wl_ping_c, wl_lose_c,match_id, "William"))
        wpl_pei_nochange(s_wl_win_i, s_wl_ping_i, s_wl_lose_i, match_id, "William")

    # judge if meet some specific peilv
    if is_special_peilv(wl_win_i, wl_ping_i, wl_lose_i, match_id, "Williami").strip():
        log.logger.info(is_special_peilv(wl_win_i, wl_ping_i, wl_lose_i, match_id, "Williami"))
    if is_special_peilv(wl_win_c, wl_ping_c, wl_lose_c, match_id, "Williamc").strip():
        log.logger.info(is_special_peilv(wl_win_c, wl_ping_c, wl_lose_c, match_id, "Williamc"))

    if peilv_huyao(wl_win_i, wl_ping_i, wl_lose_i, match_id, "Williami").strip():
        log.logger.info(peilv_huyao(wl_win_i, wl_ping_i, wl_lose_i, match_id, "Williami"))
    if peilv_huyao(wl_win_c, wl_ping_c, wl_lose_c, match_id, "Williamc").strip():
        log.logger.info(peilv_huyao(wl_win_c, wl_ping_c, wl_lose_c, match_id, "Williamc"))

    # ODDSET
    # 初始赔率打出概率
    if peilv_change(odd_win_i, odd_ping_i, odd_lose_i, odd_win_c, odd_ping_c, odd_lose_c, match_id, "ODDSET"):
        log.logger.info(
            peilv_change(odd_win_i, odd_ping_i, odd_lose_i, odd_win_c, odd_ping_c, odd_lose_c, match_id, "ODDSET"))

        wpl_pei_nochange(s_odd_win_i, s_odd_ping_i, s_odd_lose_i, match_id, "ODDSET")

        # judge if meet some specific peilv
    if is_special_peilv(odd_win_i, odd_ping_i, odd_lose_i, match_id, "ODDSETi").strip():
        log.logger.info(is_special_peilv(odd_win_i, odd_ping_i, odd_lose_i, match_id, "ODDSETi"))
    if is_special_peilv(odd_win_c, odd_ping_c, odd_lose_c, match_id, "ODDSETc").strip():
        log.logger.info(is_special_peilv(odd_win_c, odd_ping_c, odd_lose_c, match_id, "ODDSETc"))

    if peilv_huyao(odd_win_i, odd_ping_i, odd_lose_i, match_id, "ODDSETi").strip():
        log.logger.info(peilv_huyao(odd_win_i, odd_ping_i, odd_lose_i, match_id, "ODDSETi"))
    if peilv_huyao(odd_win_c, odd_ping_c, odd_lose_c, match_id, "ODDSETc").strip():
        log.logger.info(peilv_huyao(odd_win_c, odd_ping_c, odd_lose_c, match_id, "ODDSETc"))

    # Beta 365
    if peilv_change(b365_win_i, b365_ping_i, b365_lose_i, b365_win_c, b365_ping_c, b365_lose_c,match_id, "Beta 365"):
        log.logger.info(
            peilv_change(b365_win_i, b365_ping_i, b365_lose_i, b365_win_c, b365_ping_c, b365_lose_c, match_id,  "Beta 365"))
        wpl_pei_nochange(s_b365_win_i, s_b365_ping_i, s_b365_lose_i, match_id, "Bet365")
        # judge if meet some specific peilv
    if is_special_peilv(b365_win_i, b365_ping_i, b365_lose_i, match_id, "Beta 365i").strip():
        log.logger.info(is_special_peilv(b365_win_i, b365_ping_i, b365_lose_i, match_id, "Beta 365i"))
    if is_special_peilv(b365_win_c, b365_ping_c, b365_lose_c, match_id, "Beta 365c").strip():
        log.logger.info(is_special_peilv(b365_win_c, b365_ping_c, b365_lose_c, match_id, "Beta 365c"))

    if peilv_huyao(b365_win_i, b365_ping_i, b365_lose_i, match_id, "Beta 365i").strip():
        log.logger.info(peilv_huyao(b365_win_i, b365_ping_i, b365_lose_i, match_id, "Beta 365i"))
    if peilv_huyao(b365_win_c, b365_ping_c, b365_lose_c, match_id, "Beta 365c").strip():
        log.logger.info(peilv_huyao(b365_win_c, b365_ping_c, b365_lose_c, match_id, "Beta 365c"))

    # SINA
    if peilv_change(sn_win_i, sn_ping_i, sn_lose_i, sn_win_c, sn_ping_c, sn_lose_c, match_id, "SINA"):
        log.logger.info(peilv_change(sn_win_i, sn_ping_i, sn_lose_i, sn_win_c, sn_ping_c, sn_lose_c, match_id, "SINA"))
        wpl_pei_nochange(s_sn_win_i, s_sn_ping_i, s_sn_lose_i, match_id, "SINA")
        # judge if meet some specific peilv
    if is_special_peilv(sn_win_i, sn_ping_i, sn_lose_i, match_id, "SINAi").strip():
        log.logger.info(is_special_peilv(sn_win_i, sn_ping_i, sn_lose_i, match_id, "SINAi"))
    if is_special_peilv(sn_win_c, sn_ping_c, sn_lose_c, match_id, "SINAc").strip():
        log.logger.info(is_special_peilv(sn_win_c, sn_ping_c, sn_lose_c, match_id, "SINAc"))

    if peilv_huyao(sn_win_i, sn_ping_i, sn_lose_i, match_id, "SINAi").strip():
        log.logger.info(peilv_huyao(sn_win_i, sn_ping_i, sn_lose_i, match_id, "SINAi"))
    if peilv_huyao(sn_win_c, sn_ping_c, sn_lose_c, match_id, "SINAc").strip():
        log.logger.info(peilv_huyao(sn_win_c, sn_ping_c, sn_lose_c, match_id, "SINAc"))


    # Bwin
    if peilv_change(bw_win_i, bw_ping_i, bw_lose_i, bw_win_c, bw_ping_c, bw_lose_c, match_id, "BWIN"):
        log.logger.info(peilv_change(bw_win_i, bw_ping_i, bw_lose_i, bw_win_c, bw_ping_c, bw_lose_c, match_id, "BWIN"))
        wpl_pei_nochange(s_bw_win_i, s_bw_ping_i, s_bw_lose_i, match_id, "BWIN")
        # judge if meet some specific peilv
    if is_special_peilv(bw_win_i, bw_ping_i, bw_lose_i, match_id, "BWINi").strip():
        log.logger.info(is_special_peilv(bw_win_i, bw_ping_i, bw_lose_i, match_id, "BWINi"))
    if is_special_peilv(bw_win_c, bw_ping_c, bw_lose_c, match_id, "BWINc").strip():
        log.logger.info(is_special_peilv(bw_win_c, bw_ping_c, bw_lose_c, match_id, "BWINc"))

    if peilv_huyao(bw_win_i, bw_ping_i, bw_lose_i, match_id, "BWINi").strip():
        log.logger.info(peilv_huyao(bw_win_i, bw_ping_i, bw_lose_i, match_id, "BWINi"))
    if peilv_huyao(bw_win_c, bw_ping_c, bw_lose_c, match_id, "BWINc").strip():
        log.logger.info(peilv_huyao(bw_win_c, bw_ping_c, bw_lose_c, match_id, "BWINc"))


    # 竞彩
    if peilv_change(jc_win_i, jc_ping_i, jc_lose_i, jc_win_c, jc_ping_c, jc_lose_c, match_id,"竞彩"):
        log.logger.info(peilv_change(jc_win_i, jc_ping_i, jc_lose_i, jc_win_c, jc_ping_c, jc_lose_c, match_id, "竞彩"))
    if abs(jc_win_i - 1.88) <= 1e-5 or abs(jc_win_c - 1.88) < 1e-5:
        log_188 = "match_id = " + match_id + ":" + "竞彩赔率 1.88"
        log.logger.warn(log_188)
        # judge if meet some specific peilv
    if is_special_peilv(jc_win_i, jc_ping_i, jc_lose_i, match_id, "竞彩i").strip():
        log.logger.info(is_special_peilv(jc_win_i, jc_ping_i, jc_lose_i, match_id, "竞彩i"))
    if is_special_peilv(jc_win_c, jc_ping_c, jc_lose_c, match_id, "竞彩c").strip():
        log.logger.info(is_special_peilv(jc_win_c, jc_ping_c, jc_lose_c, match_id, "竞彩c"))

    if peilv_huyao(jc_win_i, jc_ping_i, jc_lose_i, match_id, "竞彩i").strip():
        log.logger.info(peilv_huyao(jc_win_i, jc_ping_i, jc_lose_i, match_id, "竞彩i"))
    if peilv_huyao(jc_win_c, jc_ping_c, jc_lose_c, match_id, "竞彩c").strip():
        log.logger.info(peilv_huyao(jc_win_c, jc_ping_c, jc_lose_c, match_id, "竞彩c"))


    # Interview
    if peilv_change(in_win_i, in_ping_i, in_lose_i, in_win_c, in_ping_c, in_lose_c, match_id, "Interview"):
        log.logger.info(peilv_change(in_win_i, in_ping_i, in_lose_i, in_win_c, in_ping_c, in_lose_c, match_id, "Interview"))
        wpl_pei_nochange(s_in_win_i, s_in_ping_i, s_in_lose_i, match_id, "Interview")
        # judge if meet some specific peilv
    if is_special_peilv(in_win_i, in_ping_i, in_lose_i, match_id, "Interviewi").strip():
        log.logger.info(is_special_peilv(in_win_i, in_ping_i, in_lose_i, match_id, "Interviewi"))
    if is_special_peilv(in_win_c, in_ping_c, in_lose_c, match_id, "Interviewc").strip():
        log.logger.info(is_special_peilv(in_win_c, in_ping_c, in_lose_c, match_id, "Interviewc"))

    if peilv_huyao(in_win_i, in_ping_i, in_lose_i, match_id, "Interview-i").strip():
        log.logger.info(peilv_huyao(in_win_i, in_ping_i, in_lose_i, match_id, "Interview-i"))
    if peilv_huyao(in_win_c, in_ping_c, in_lose_c, match_id, "Interview-c").strip():
        log.logger.info(peilv_huyao(in_win_c, in_ping_c, in_lose_c, match_id, "Interview-c"))

    #print("Database version: %s" %data)


    db.close()

if __name__ == '__main__':
    if os.path.exists('/root/PycharmProjects/policy/main/all.log'):
        os.remove('/root/PycharmProjects/policy/main/all.log')

    # At first, get all match ids today.
    log = Logger('all.log', level='debug')
    match_id_list = []
    match_host_name = []
    db = MySQLdb.connect("localhost", "root", "123456", "jingcai_db", charset='utf8')
    cursor = db.cursor()
    sql = "select match_id,host_name,guest_name,host_league_rank,guest_league_rank, lian_sai,rang_num from t_match where match_id like '20180719%'"
    cursor.execute(sql)
    data = cursor.fetchall()
    for rows in data:
        match_id_list.append(rows[0])
        g_match_id_list.append(rows[0])
        match_host_name.append(rows[1])
        g_host_name.append(rows[1])
        g_guest_name.append(rows[2])
        g_host_rank.append(rows[3])
        g_guest_rank.append(rows[4])
        g_liansai.append(rows[5])
        g_rang_num.append(rows[6])
    db.close()

    for i in range (0, len(match_id_list)):
        temp_log = "match_id = " + match_id_list[i] + ":*****************<<Step 1: 基本面分析>>*****************"
        log.logger.info(temp_log)
        host_guest_more_hot(match_id_list[i],match_host_name[i],g_guest_name[i],g_host_rank[i],g_guest_rank[i],g_liansai[i],g_rang_num[i])
        temp_log = "match_id = " + match_id_list[i] + ":*****************<<Step 2: 盘口分析>>*******************"
        log.logger.info(temp_log)
        pankou_analyze(match_id_list[i],match_host_name[i],g_guest_name[i],g_host_rank[i],g_guest_rank[i],g_liansai[i],g_rang_num[i])
        temp_log = "match_id = " + match_id_list[i] + ":*****************<<Step 3: 赔率分析>>*******************"
        log.logger.info(temp_log)
        analyze_jicai_peilv(match_id_list[i],match_host_name[i],g_guest_name[i],g_host_rank[i],g_guest_rank[i],g_liansai[i],g_rang_num[i])
        Policy_Decison(match_id_list[i],match_host_name[i],g_guest_name[i],g_host_rank[i],g_guest_rank[i],g_liansai[i],g_rang_num[i])

    f = open(r"/root/PycharmProjects/policy/main/all.log", "r")
    f1 = open(r"/root/PycharmProjects/policy/main/match_warn_info","w")
    line = f.readline()
    while line:
        info_match_id = "INFO: match_id = "
        warn_match_id = "WARNING: match_id = "
        if line.find(info_match_id) != -1:
            pos_info = line.index(info_match_id)
            match_id_info = line[pos_info+len(info_match_id):]
            f1.write(match_id_info)
            line = f.readline()

        elif line.find(warn_match_id) != -1:
            pos_warn = line.index(warn_match_id)
            match_id_warn = "WARNING:" + line[pos_warn+len(warn_match_id):]
            f1.write(match_id_warn)
            line = f.readline()

        else:
            line = f.readline()

    f.close()
    f1.close()


# judge no change between intial and final pei lv for one company

