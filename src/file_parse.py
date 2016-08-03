# -*- coding utf-8 -*-
import json
import os
import profile
from jinja2 import Template
from datetime import datetime


class FileParse(object):

    def __init__(self):
        self.member_id = ''
        self.result_list = []

    def filter_file(self, file_name):
        print file_name
        with open(file_name, 'r') as f:
            error_dict = {}
            self.member_id = ''
            for line_number, line_content in enumerate(f):
                member_info_dict = {}
                try:
                    if "member_id" in line_content:
                        temp_member_id = json.loads(line_content[line_content.index('=')+1:])
                        self.member_id = str(temp_member_id[0]['data']['member_id']).split('=')[0]

                    if 'paidResponse' in line_content and self.member_id and self.member_id in line_content:
                        member_info_dict['file_name'] = file_name
                        member_info_dict['line_number'] = line_number + 1
                        member_info_dict['member_id'] = self.member_id
                        current_line_time = datetime.strptime(line_content[:8], '%H:%M:%S')

                        if "code check error" in line_content:
                            if self.member_id in error_dict:
                                error_dict[self.member_id].append([len(self.result_list), current_line_time])
                            else:
                                error_dict[self.member_id] = [[len(self.result_list), current_line_time]]

                            member_info_dict['status'] = 'red'
                            self.result_list.append(member_info_dict)
                        else:
                            if self.member_id in error_dict:
                                for item in error_dict[self.member_id]:
                                    if ((current_line_time - item[1]).seconds / 60) < 5:
                                        self.result_list[item[0]]["status"] = 'yellow'
                                error_dict.pop(self.member_id, None)
                                member_info_dict['status'] = 'green'
                                self.result_list.append(member_info_dict)
                except:
                    print file_name, line_number, line_content
                    continue
                    raise

    def filter_files(self, path):
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                self.filter_file(os.path.join(root, name))

    def save_result_to_file(self, file_name):
        with open(file_name, 'w') as f:
            f.writelines([str(item) + '\n' for item in self.result_list])

    def save_result_to_html(self, file_name):
        template = Template("""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <style>
                table {
                    width:100%;
                }
                table, th, td {
                    border: 1px solid black;
                    border-collapse: collapse;
                    padding: 5px;
                    text-align: left;
                }
                table#t01 th {
                    background-color: black;
                    color: white;
                }
                .pic-container {
                    width: 80%;
                    height: 600px;
                    overflow-y: scroll;
                    overflow-x: scroll;
                }
                </style>
                <meta charset="UTF-8">
                <title>Title</title>
            </head>
            <body>
                <div class="pic-container">
                <table class="divScroll">
                    <tr>
                        <th>member_id</th>
                        <th>status</th>
                        <th>file name</th>
                        <th>line number</th>
                    </tr>
                    {% for item in code_check_error %}
                        {% if item.status == "red" %}
                            <tr bgcolor="#FF0000">
                        {% elif item.status == "yellow" %}
                            <tr bgcolor="#FFFF00">
                        {% else %}
                            <tr bgcolor="#008000">
                        {% endif %}
                            <td>{{ item.member_id }}</td>
                            <td>{{ item.status }}</td>
                            <td>{{ item.file_name }}</td>
                            <td>{{ item.line_number }}</td>
                        </tr>
                    {% endfor %}
                </table>
                </div>
            </body>
            </html>
            """)
        res = template.render(code_check_error=self.result_list)
        with open(file_name, 'w') as f:
            f.write(res)

    def summary(self, path):
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                self.filter_file(os.path.join(root, name))
        pass

    def save_result_to_json_file(self, file_name):
        with open(file_name, 'w') as f:
            f.writelines(json.dumps({"data": self.result_list}))

if __name__ == "__main__":
    print datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")
    obj = FileParse()
    # print profile.run('obj.filter_files("/Users/twer/Documents/starbucks/svc/")')
    obj.filter_files("/Users/twer/Documents/starbucks/svc/10.192.115.130")
    # obj.save_result_to_file("/Users/twer/work/pjhu/file_copy/rst.log")
    # obj.save_result_to_html("/Users/twer/work/pjhu/file_copy/rst.html")
    obj.save_result_to_json_file("/Users/twer/work/pjhu/file_copy/rst.json")
    print datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")
