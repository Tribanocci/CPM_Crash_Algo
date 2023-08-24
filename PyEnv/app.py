from flask import Flask, render_template, request
import subprocess
from CPM_crash_Algo import *


app = Flask(__name__)

def custom_text_for_item(item):
    if item == 1:
        return "Project Completion Time"
    elif item == 2:
        return "Optimized minimum Cost"
    else:
        return "Unknown Custom Text"


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def submit_form():
    N = int(request.form.get('num_rows'))
    Im_Cost = int(request.form.get('Im_Cost'))
    d = request.form.getlist('cell_data_Ntime')
    d = [int(element) for element in d]

    Tm = request.form.getlist('cell_data_CTime')
    Tm = [int(element) for element in Tm]

    c = request.form.getlist('cell_data_Ccost')
    c = [int(element) for element in c]

    pr_string = request.form.getlist('cell_data_pr')
    pr=[]
    for el in pr_string:
        if len(el) == 0:
            pr.append([])
        else:
            string_list= el.split(',')
            int_list = [int(element) for element in string_list]
            pr.append(int_list)

    # Call MATLAB code using subprocess and pass data as arguments
    # matlab_output = subprocess.check_output(['matlab', '-r', 'your_matlab_script({})'.format(','.join(data))])
    print(pr)
    print(c)
    print(d)
    print(Tm)
    print(Im_Cost)
    ans=[]
    ans = CPM_crash(N, Im_Cost, Tm, c, d, pr)
    if ans[0]:
        result = ans[1:]
        print("Success")
    else:
        result = ans[1]
        print("Fail")
        print(ans[1])
    return render_template('index.html', result=result, custom_text_for_item=custom_text_for_item)

if __name__ == '__main__':
    app.run(debug=True)
