from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    a = ""
    b = ""
    c = ""
    error_message = ""
    success_message = ""
    datetime_value = ""  # 新增变量，用于存储用户输入的4位数字

    if request.method == "POST":
        # 获取用户输入
        input_value = request.form.get("input_digits")

        # 验证输入是否为4位数字
        if len(input_value) != 4 or not input_value.isdigit():
            error_message = "请输入4位数字！"
        else:
            datetime_value = input_value  # 保存用户输入的4位数字
            # 构造目标URL
            url = f"https://storage.googleapis.com/wpt_project_data/{input_value}.txt"

            try:
                # 获取URL内容
                response = requests.get(url)
                response.raise_for_status()  # 检查请求是否成功

                # 解析文本内容
                data = response.text.strip().split()
                a = data[1]
                b = data[3]
                c = data[5]

                success_message = "查询成功！"
            except requests.exceptions.RequestException as e:
                error_message = f"无法访问目标URL ({url})。请检查网络连接或URL是否有效。"

    # 将 datetime_value 传递到模板
    return render_template(
        "index.html",
        a=a,
        b=b,
        c=c,
        error_message=error_message,
        success_message=success_message,
        datetime=datetime_value  # 新增的模板变量
    )

if __name__ == "__main__":
    app.run(debug=True)