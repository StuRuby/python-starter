import numpy as np
from flask import Flask
from flask import jsonify
from flask import request  # request可以获取请求参数
from flask import render_template  # 使用模板返回页面
import random

import dataGet

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'hello world!'


@app.route('/tem')
def my_tem():
    return render_template("index.html")


@app.route('/login')
def my_login():
    name = request.values.get('name')
    passwd = request.values.get('passwd')
    return f'name={name}, passwd={passwd}'


@app.route('/abc')
def my_abc():
    id = request.values.get('id')
    return f'''
    <form action='/login'>
        账号：<input name='name' value='{id}'><br>
        密码：<input name='passwd'>
        <input type='submit'>
    </form>
    '''


@app.route('/equipmentList', methods=["GET"])
def get_equipment_list():
    d = {"code": 0, "status": 200, "result": [], "timestamp": 12345678}
    info = dataGet.open_cfg_dat_as_obj("equipmentList.json")

    d["result"] = info["result"]
    d["timestamp"] = int(dataGet.get_time())

    return jsonify(d)


@app.route('/equipmentSetting', methods=["POST", "DELETE"])
def equipment_setting():
    req = request.values.get("reqSave")
    dataGet.debug_print(req)

    res = {"code": 0, "status": 200, "result": req,
           "timestamp": int(dataGet.get_time())}
    return jsonify(res)


@app.route('/acquisitionSetting', methods=["POST"])
def acquisition_setting():
    rr = request.values.get("Rr")
    sr = request.values.get("SR")
    snr = request.values.get("SNR")
    dataGet.debug_print(rr)
    dataGet.debug_print(sr)
    dataGet.debug_print(snr)

    res = {"code": 0, "status": 200, "result": [
        {"Rr": rr, "SR": sr, "SNR": snr}], "timestamp": int(dataGet.get_time())}
    return jsonify(res)


@app.route('/alarmSetting', methods=["POST"])
def alarm_setting():
    down = request.values.get("down")
    up = request.values.get("up")
    db = request.values.get("db")
    dataGet.debug_print(down)
    dataGet.debug_print(up)
    dataGet.debug_print(db)

    res = {"code": 0, "status": 200, "result": [{"down": down, "up": up, "db": db}],
           "timestamp": int(dataGet.get_time())}
    return jsonify(res)


@app.route('/alarmNum', methods=["GET"])
def alarm_num():
    d = {"code": 0, "status": 200, "result": [
        {"num": 0}], "timestamp": int(dataGet.get_time())}
    num = random.randint(1, 20)
    d["result"][0]["num"] = num

    return jsonify(d)


@app.route('/getTime', methods=["GET"])
def get_time():
    d = {"code": 0, "status": 200, "result": [],
         "timestamp": int(dataGet.get_time())}
    format_time = dataGet.get_time_format()
    d["result"] = [{"time": format_time}]

    return jsonify(d)


@app.route('/alarmRecord', methods=["GET"])
def alarm_record():
    info = dataGet.open_cfg_dat_as_obj("alarmRecord.json")

    res = info
    res["timestamp"] = int(dataGet.get_time())
    return jsonify(res)


@app.route('/showWave', methods=["GET"])
def show_wave():
    # equipment = request.values.get("equipment")
    # time = request.values.get("time")
    # dataGet.debug_print(equipment)
    # dataGet.debug_print(time)

    res = {"code": 0, "status": 200, "result": [{"timeDomainDataY": [1.1, 2.2],
                                                 "timeDomainDataX": [3.3, 4.4]}], "timestamp": int(dataGet.get_time())}
    frq = random.randint(1, 10) * 0.001
    res["result"][0]["timeDomainDataX"], res["result"][0]["timeDomainDataY"] = dataGet.gen_audio_wave(
        frq)

    return jsonify(res)


@app.route('/waveData', methods=["GET"])
def wave_data():
    equipment = request.values.get("equipment")
    dataGet.debug_print(equipment)

    res = {"code": 0, "status": 200, "result": [{"timeDomainDataY": [], "timeDomainDataX": [],
                                                 "frequencyDomainDataY": [], "frequencyDomainDataX": [],
                                                 "timeFrequencyDataY": [], "timeFrequencyDataX": [],
                                                 "timeFrequencyDataZ": []}], "timestamp": int(dataGet.get_time())}
    frq = random.randint(1, 10) * 0.001
    res["result"][0]["timeDomainDataX"], res["result"][0]["timeDomainDataY"] = dataGet.gen_audio_wave(
        frq)
    res["result"][0]["frequencyDomainDataX"], res["result"][0]["frequencyDomainDataY"] = dataGet.gen_audio_wave(
        frq)
    res["result"][0]["timeFrequencyDataX"], res["result"][0]["timeFrequencyDataY"] = dataGet.gen_audio_wave(
        frq)

    a = []
    for i in list(range(0, 30)):
        a.append(float(i))
    aa = []
    for j in range(len(res["result"][0]["timeFrequencyDataX"])):
        aa.append(a)
    b = []
    for i in list(np.random.randint(254, size=30)):
        b.append(float(i))
    bb = []
    for j in range(len(res["result"][0]["timeFrequencyDataX"])):
        bb.append(b)
    res["result"][0]["timeFrequencyDataY"] = aa
    res["result"][0]["timeFrequencyDataZ"] = bb

    # print(aa)
    # print(bb)
    #
    # print(len(aa), len(aa[0]), len(bb))

    return jsonify(res)


@app.route('/pieChart', methods=["GET"])
def pie_chart():
    res = {"code": 0, "status": 200, "result": [{"normal": [57, 0.67], "warning": [15, 0.18], "alarm": [10, 0.12],
                                                 "important": [3, 0.03], "critical": [0, 0],
                                                 "duration": [3, 15, 25, 30]}], "timestamp": int(dataGet.get_time())}
    return jsonify(res)


if __name__ == '__main__':
    app.run()
    # app.run(host="0.0.0.0", port=80)  # 上传服务器时用这行
