#!/usr/bin/python3
import json
import time
import sqlite3
import numpy as np


def debug_print(msg):
    debug_flg = 1
    if debug_flg:
        print(msg)
    else:
        pass


def get_time():
    """
    时间戳
    :return:
    """
    tt = time.time()
    debug_print(tt)
    return tt


def get_time_format():
    """
    时间格式："2020年08月26日 20:18:16"
    :return:
    """
    now = int(time.time())

    time_array = time.localtime(now)
    other_style_time = time.strftime("%Y年%m月%d日 %H:%M:%S", time_array)

    return other_style_time


def convert_format_time_to_stamp(format_time):
    tt = time.strptime(format_time, "%Y年%m月%d日 %H:%M:%S")
    time_stamp = int(time.mktime(tt))

    return time_stamp


def crt_table_dbs(db_name, sql):
    """
    连接数据库，若不存在则创建，创建表
    :param db_name: 'test.db'
    :param sql: CREATE TABLE COMPANY
                (ID INT PRIMARY KEY     NOT NULL,
                NAME           TEXT    NOT NULL);
    :return: void
    """
    debug_print("crt_table_dbs")
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute(sql)
    debug_print("Table created successfully")
    conn.commit()
    conn.close()


def insert_to_dbs(db_name, sql):
    """
    连接数据库，插入数据
    :param db_name:
    :param sql: "INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (1, 'Paul', 32, 'California', 20000.00 )"
    :return:
    """
    debug_print("insert_to_dbs")
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute(sql)
    conn.commit()
    debug_print("Records created successfully")
    conn.close()


def select_to_dbs(db_name, sql):
    """
    连接数据库，查询数据
    :param db_name:
    :param sql: "SELECT id, name, address, salary  from COMPANY"
    :return:
    """
    debug_print("select_to_dbs")
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    cursor = c.execute(sql)
    data = []
    for row in cursor:
        data.append(row)

    debug_print("Operation done successfully")
    conn.close()

    return data


def update_to_dbs(db_name, sql):
    """

    :param db_name:
    :param sql: "UPDATE COMPANY set SALARY = 25000.00 where ID=1"
    :return:
    """
    debug_print("update_to_dbs")
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute(sql)
    conn.commit()
    debug_print("update done successfully")

    conn.close()


def delete_to_dbs(db_name, sql):
    """

    :param db_name:
    :param sql: "DELETE from COMPANY where ID=2;"
    :return:
    """
    debug_print("delete_to_dbs")
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute(sql)
    conn.commit()

    debug_print("delete done successfully")
    conn.close()


def open_cfg_dat_as_obj(json_file):
    info = {}
    with open("./jsonFiles/" + json_file, 'r', encoding='utf-8') as f:
        info = json.load(f)

    debug_print(info)
    return info


'''
def get_or_set_alarm_num(opt, *arg):
    
    cfg_info = open_cfg_dat_as_obj()
    if 'GET' == opt:
        return cfg_info['num']
    else :
        cfg_info['num'] = arg
'''


def gen_audio_wave(frq):
    fs = 44100

    f = frq  # int(raw_input("Enter fundamental frequency: "))
    t = 0.01  # float(raw_input("Enter duration of signal (in seconds): "))

    samples = np.arange(t * fs)
    # print("111: ", samples)
    ll = []
    for i in samples:
        ll.append(i)
    # print("ll:", ll)

    signal = np.sin(2 * np.pi * f * samples)
    signal *= 32767
    signal = np.int16(signal)

    samples_list = []
    signal_list = []
    for m in samples:
        if m == 0:
            m = 1
        samples_list.append(float(m))

    for m in signal:
        if m == 0:
            m = 1
        signal_list.append(float(m))

    # print("len of samples:", len(samples))
    # print(samples)
    # print(samples[0])
    # print(samples[1])
    # print(type(samples))
    # print("len of signal:", len(signal))
    # print(signal)
    # print(type(signal))

    # debug_print(samples_list)
    # debug_print(len(samples_list))
    # debug_print(type(samples_list))
    # debug_print(signal_list)
    # debug_print(len(signal_list))
    # debug_print(type(signal_list))

    return samples_list, signal_list


if __name__ == '__main__':
    gen_audio_wave(0.1)
