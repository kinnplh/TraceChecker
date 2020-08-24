from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify
import os
import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/upload_error_report', methods=['POST'])
def upload_error_report():
    user_name = request.json.get('user_name')
    package_name = request.json.get('package_name')
    basic_name = request.json.get('basic_name')
    report_text = request.json.get('report_text').strip()
    with open('static/error.txt', encoding='utf-8', mode='a') as error_file:
        error_file.write("%s#%s#%s#%s\n" % (user_name, package_name, basic_name, report_text))
    return jsonify(state='success')


@app.route('/upload_nlc', methods=['POST'])
def upload_nlc():
    user_name = request.json.get('user_name')
    package_name = request.json.get('package_name')
    last_name = request.json.get('last_name')
    nlc = request.json.get('nlc')
    with open('static/nlc.txt', encoding='utf-8', mode='a') as nlc_file:
        nlc_file.write("%s#%s#%s#%s\n" % (user_name, package_name, last_name, nlc))
    return jsonify(state='success')


@app.route('/check_task_result')
def check_task_result():
    user_name = request.args.get('u', "user1596339240259")  # user name
    package_name = request.args.get('p', "com.tencent.mm")  # package name
    index = int(request.args.get('i', '0'))
    task_path = os.path.join('static', user_name, 'taskResult', package_name)
    if not os.path.exists(task_path):
        return "%s 没有找到" % task_path
    files = list(filter(lambda name:
                        name.startswith("n_%d_" % index) and name.endswith('.json'),
                        os.listdir(task_path)))
    files.sort(key=lambda x: int(list(str(os.path.splitext(x)[0]).split('_'))[3]))
    if len(files) == 0:
        return "不存在的index"
    info_list = []

    for file_name in files:
        basic_name = str(os.path.splitext(file_name)[0])
        split_result = list(basic_name.split('_'))
        timestamp = int(split_result[3])
        is_prefix = split_result[4].startswith('a')
        is_circle = split_result[4].startswith('c')
        is_para = split_result[4].endswith('*')
        is_delete = split_result[4].startswith('x')
        json_path = os.path.join(task_path, basic_name + '.json')
        with open(json_path) as json_file:
            action_info = json.load(json_file)
            text = action_info['param']
            action_type = action_info['typeString']
            node_id = action_info['targetNodeId']
            node_type = node_id[node_id.rfind(';') + 1:] if node_id.rfind(';') >= 0 else node_id
        path_for_last = os.path.join(task_path, 'n_%s_%d_%s_l.png' % (split_result[1], int(split_result[2]) + 1, split_result[3]))
        is_last = os.path.exists(path_for_last)

        result = {'timestamp': timestamp, 'basic_name': basic_name, 'is_prefix': is_prefix, 'is_circle': is_circle,
                  'is_para': is_para, 'action_text': text, 'action_type': action_type, 'node_type': node_type,
                  'is_delete': is_delete, 'is_last': is_last,
                  'last_name': 'n_%s_%s_%s_l' % (split_result[1], int(split_result[2]) + 1, split_result[3])}
        info_list.append(result)
    return render_template("check_trace.html", infos=info_list, user_name=user_name, package_name=package_name,
                           task_index=index)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
