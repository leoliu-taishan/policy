#!/usr/bin/python
# -*- coding: utf-8 -*-
import smtplib
def sendMail(body):
    smtp_server = 'smtp.163.com'
    from_mail = '15810333378@163.com'
    mail_pass = 'leoliu123'
    to_mail = ['15810333378@163.com']
    cc_mail = ['15810333378@163.com']
    from_name = 'monitor'
    subject = u'监控'.encode('gbk')   # 以gbk编码发送，一般邮件客户端都能识别
#     msg = '''\
# From: %s <%s>
# To: %s
# Subject: %s
# %s''' %(from_name, from_mail, to_mail_str, subject, body)  # 这种方式必须将邮件头信息靠左，也就是每行开头不能用空格，否则报SMTP 554
    mail = [
        "From: %s <%s>" % (from_name, from_mail),
        "To: %s" % ','.join(to_mail),   # 转成字符串，以逗号分隔元素
        "Subject: %s" % subject,
        "Cc: %s" % ','.join(cc_mail),
        "",
        body
        ]
    msg = '\n'.join(mail)  # 这种方式先将头信aaa息放到列表中，然后用join拼接，并以换行符分隔元素，结果就是和上面注释一样了
    try:
        s = smtplib.SMTP()
        s.connect(smtp_server, '25')
        s.login(from_mail, mail_pass)
        s.sendmail(from_mail, to_mail+cc_mail, msg)
        s.quit()
    except smtplib.SMTPException as e:
        print("Error: %s" %e)
if __name__ == "__main__":
    sendMail("This is a test!")

def initial_peilv_gailv(x,y,z, match_id, company):
    sql1 = ""

    # **********************************************
    # The following rules are specific for ou pei  *
    # ***********************************************
    w = 0
    p = 0
    l = 0
    temp_log = ""
    if company == "LIBO":
        sql1 = "select a.w_p_l_result from t_result a, t_oupei_result b where a.match_id = b.match_id and LB_Win_I = '"\
               + x + "' and LB_Ping_I = '" + y + "' and LB_Lose_I = '" + z + "'"
        w, p, l = search_sql_wpl(sql1)
        temp_log = peilv_gailv(w,p,l)
        temp_log = "match_id = " + match_id + ":" + company + "初始赔率:" + x + "|" + y + "|" + z + "xia" + temp_log
        log.logger.info(temp_log)


    elif company == "ODDSET":
        sql1 = "select a.w_p_l_result from t_result a, t_oupei_result b where a.match_id = b.match_id and ODD_Win_I = '" + x + "' and ODD_Ping_I = '" + y + "' and ODD_Lose_I = '" + z + "'"
        w, p, l = search_sql_wpl(sql1)
        temp_log = peilv_gailv(w, p, l)
        temp_log = "match_id = " + match_id + ":" + company + "初始赔率:" + x + "|" + y + "|" + z + "xia" + temp_log
        log.logger.info(temp_log)


    elif company == "BWIN":
        sql1 = "select a.w_p_l_result from t_result a, t_oupei_result b where a.match_id = b.match_id and BW_Win_I = '" + x + "' and BW_Ping_I = '" + y + "' and BW_Lose_I = '" + z + "'"
        w, p, l = search_sql_wpl(sql1)
        temp_log = peilv_gailv(w, p, l)
        temp_log = "match_id = " + match_id + ":" + company + "初始赔率:" + x + "|" + y + "|" + z + "xia" + temp_log
        log.logger.info(temp_log)


    elif company == "William":
        sql1 = "select a.w_p_l_result from t_result a, t_oupei_result b where a.match_id = b.match_id and WL_Win_I = '" + x + "' and WL_Ping_I = '" + y + "' and WL_Lose_I = '" + z + "'"
        w, p, l = search_sql_wpl(sql1)
        temp_log = peilv_gailv(w, p, l)
        temp_log = "match_id = " + match_id + ":" + company + "初始赔率:" + x + "|" + y + "|" + z + "xia" + temp_log
        log.logger.info(temp_log)

    elif company == "Bet365":
        sql1 = "select a.w_p_l_result from t_result a, t_oupei_result b where a.match_id = b.match_id and B365_Win_I = '" + x + "' and B365_Ping_I = '" + y + "' and B365_Lose_I = '" + z + "'"
        w, p, l = search_sql_wpl(sql1)
        temp_log = peilv_gailv(w, p, l)
        temp_log = "match_id = " + match_id + ":" + company + "初始赔率:" + x + "|" + y + "|" + z + "xia" + temp_log
        log.logger.info(temp_log)

    elif company == "Interview":
        sql1 = "select a.w_p_l_result from t_result a, t_oupei_result b where a.match_id = b.match_id and IN_Win_I = '" + x + "' and IN_Ping_I = '" + y + "' and IN_Lose_I = '" + z + "'"
        w, p, l = search_sql_wpl(sql1)
        temp_log = peilv_gailv(w, p, l)
        temp_log = "match_id = " + match_id + ":" + company + "初始赔率:" + x + "|" + y + "|" + z + "xia" + temp_log
        log.logger.info(temp_log)

    elif company == "SINA":
        sql1 = "select a.w_p_l_result from t_result a, t_oupei_result b where a.match_id = b.match_id and SN_Win_I = '" + x + "' and SN_Ping_I = '" + y + "' and SN_Lose_I = '" + z + "'"
        w, p, l = search_sql_wpl(sql1)
        temp_log = peilv_gailv(w, p, l)
        temp_log = "match_id = " + match_id + ":" + company + "初始赔率:" + x + "|" + y + "|" + z + "xia" + temp_log
        log.logger.info(temp_log)
    else:
        print("no such company")