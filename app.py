from flask import Flask, render_template, request
import subprocess
import glob
import plotly.graph_objects as go
import numpy as np
import os
from intelhex import IntelHex
ih = IntelHex()

app = Flask(__name__)
chunk_size =200
num_columns = 16
folder_path = 'bin_files'
back_data = {}

def get_binData(filename):
    decimal_list = []
    with open(os.path.join(folder_path, filename), "rb") as file:
        while True:
            chunk = file.read(1)
            if not chunk:
                break
            decimal_value = int.from_bytes(chunk, byteorder="big")
            decimal_list.append(decimal_value)
    num_elements = len(decimal_list)
    num_rows = -(-num_elements // num_columns)  # Equivalent to ceil(num_elements / num_columns)
    arr = np.array(decimal_list + [0] * (num_rows * num_columns - num_elements)).reshape(num_rows, num_columns)
    return arr, num_rows

def color_coding(value):
    if value < 30:
        fillcolor = "green"
    elif value >= 30 and value <= 100:
        fillcolor = "orange"
    else:
        fillcolor = "red"
    return fillcolor

def get_hoverText(m_array,m_address,num_rows,num_columns):
    h_text = ["{}".format(hex(val)) for row in m_array for val in row]
    m_address = ["{}".format(hex(row)) for row in m_address]
    arr = [m_address[i:i+num_columns] for i in range(0, len(m_address), num_columns)]
    arr = np.flip(arr, axis=0)
    result = arr.flatten()
    hover_text = ["Address: {} <br> Value: {}".format(addr, val) for addr, val in zip(result, h_text)]
    num_values = num_rows * num_columns
    truncated_data = hover_text[:num_values+1]
    htext = np.array(truncated_data).reshape(num_rows, num_columns)
    return htext

def get_axis_values(page_count,start_value,chunk_size,num_columns,num_values):
    for i in range(page_count):
        x_ticktext = [f'{hex(i)}' for i in range(start_value,start_value+num_columns)]
        y_ticktext = [hex(start_value + i * num_columns) for i in range(num_values)]
        y_ticktext=list(reversed(y_ticktext))
        last_value= ((start_value+num_columns)*chunk_size)-(start_value*chunk_size)+(start_value-1)
        oldstart_value = start_value
        start_value=last_value+1
    return x_ticktext ,y_ticktext , last_value,start_value,oldstart_value

def set_height(data_lenght):
    if data_lenght < 20:
        layout_height = 600
    elif data_lenght >= 20 and data_lenght <= 40:
        layout_height = 1500
    elif data_lenght >= 40 and data_lenght <= 60:
        layout_height = 1800
    elif data_lenght >= 60 and data_lenght <= 80:
        layout_height = 2000
    elif data_lenght >= 80 and data_lenght <= 100:
        layout_height = 3000
    elif data_lenght >= 100 and data_lenght <= 120:
        layout_height = 4000
    elif data_lenght >= 120 and data_lenght <= 140:
        layout_height = 5000
    elif data_lenght >= 140 and data_lenght <= 160:
        layout_height = 6000
    elif data_lenght >= 160 and data_lenght <= 180:
        layout_height = 7000
    elif data_lenght >= 180 and data_lenght <= 200:
        layout_height = 8000
    else:
        layout_height=9000
    return layout_height


def run_c_file(start_address,end_address,interval,iterations):
    # subprocess.check_output(['gcc', '-o', 'memdump', 'memdump.c'])  # Compile the C file
    # Execute the memdump.exe command with arguments
    # Get a list of all files in the folder
    file_list = os.listdir(folder_path)
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        os.remove(file_path)
    command = ['./memdump', '-s', str(start_address), '-e', str(end_address), '-i', str(interval), '-n', str(iterations)]
    result = subprocess.check_output(command)
    return result

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/generate_files')
def generate_files():
    return render_template("generate_files.html")

@app.route('/view_heatmap')
def view_heatmap():
    bin_files = glob.glob(folder_path+"/*.bin")
    bin_files=[os.path.basename(path) for path in bin_files]
    if len(bin_files):
        return render_template('heatmap.html',bin_files=bin_files,prev_page=0,next_button_tag = False)
    else:
        return render_template('index.html')

def heatmap(array1,array2,num_rows,page,filename1,next_file,start_address,end_address):
    next_button_tag = False
    start_idx = (page - 1) * chunk_size
    end_idx = min(start_idx + chunk_size, num_rows)
    page_data_1 = array1[start_idx:end_idx][::-1]
    page_data_2 = array2[start_idx:end_idx][::-1]
    x_ticktext ,y_ticktext , last_value,start_value,oldstart_value= get_axis_values(page,start_address,chunk_size,num_columns,len(page_data_1))
    if len(page_data_1):
        try:
            checkData =array1[end_idx+1:end_idx+2]
            if len(checkData):
                next_button_tag = True
            else:
                next_button_tag = False
        except Exception as e:
            print(e)
            next_button_tag = False
    # Add annotations for the second heatmap
    annotations1 = []
    annotations2 = []
    shapes = []
    for i in range(len(page_data_2)):
        for j in range(len(page_data_2[i])):
            annotations1.append(
                dict(
                    x=j,
                    y=i,
                    text=str(hex(int(round(page_data_1[i, j], 2)))),
                    showarrow=False,
                    font=dict(color='white' if page_data_1[i, j] < 50 else 'black')
                )
            )
            if page_data_1[i][j] != page_data_2[i][j]:
                fillcolor =  color_coding(page_data_2[i][j])
                color = 'black'
                shape = dict(
                    x0=j - 0.5,
                    y0=i - 0.5,
                    x1=j + 0.5,
                    y1=i + 0.5,
                    fillcolor=fillcolor,
                    opacity=1,
                    line=dict(
                        width=0.2,
                        color="white"
                    )
                )
                shapes.append(shape)
            else:
                color='white' if page_data_2[i, j] < 50 else 'black'
            annotations2.append(
                dict(
                    x=j,
                    y=i,
                    text=str(hex(int(round(page_data_2[i, j], 2)))),
                    showarrow=False,
                    font=dict(color=color)
                )
            )
    layout1 = go.Layout(
            title={    'text':'filename1',
                        'x': 0.5,
                        'y': 0.7,
                        'xanchor': 'center',
                        'yanchor': 'top'
                    },
        xaxis=dict(side='top',tickmode='array', tickvals=list(range(num_columns)),ticktext=x_ticktext),
        yaxis=dict(title='memory address',tickmode='array', tickvals=list(range(len(page_data_1))),ticktext=y_ticktext),
        annotations=annotations1,
        height=set_height(len(page_data_1))
    )
    layout2 = go.Layout(
        title={    'text':'next_file',
                    'x': 0.5,
                    'y': 0.7,
                    'xanchor': 'center',
                    'yanchor': 'top'
                    },
        xaxis=dict(side='top',tickmode='array', tickvals=list(range(num_columns)),ticktext=x_ticktext),
        yaxis=dict(title='memory address',tickmode='array', tickvals=list(range(len(page_data_2))),ticktext=y_ticktext),
        annotations=annotations2,
        height=set_height(len(page_data_2)),shapes=shapes
    )

    address= np.arange(oldstart_value,oldstart_value+len(annotations1))
    htext1 = get_hoverText(page_data_1,address,len(page_data_1),num_columns)
    htext2 = get_hoverText(page_data_2,address,len(page_data_2),num_columns)

    # Create the first heatmap plotly figure
    heatmap1 = go.Heatmap(z=page_data_1,xgap=1, ygap=1,colorscale='gray',text=htext1,hoverinfo='text')
    heatmap2 = go.Heatmap(z=page_data_2,xgap=1, ygap=1,colorscale='gray',text=htext2,hoverinfo='text')

    fig1 = go.Figure(data=[heatmap1], layout=layout1)
    fig1.update_traces(showscale=False)
    fig2 = go.Figure(data=[heatmap2], layout=layout2)
    # Convert the figures to JSON for passing to the template
    plot_json1 = fig1.to_json()
    plot_json2 = fig2.to_json()
    bin_files = glob.glob(folder_path+"/*.bin")
    bin_files=[os.path.basename(path) for path in bin_files]
    #backup data
    if next_file in back_data.keys():
            back_data['dump_1'] = \
                {
                'page':page
            }
    else:
        back_data['dump_1'] = \
            {

                'page':page,
            }
    # Render the template with the plot JSONs, page number, and previous/next page URLs
    return plot_json1, plot_json2,next_button_tag,bin_files

@app.route('/display_heatmap', methods=['GET', 'POST'])
def display_heatmap():
    global start_address,end_address,num_rows,page,filename1,filename2,m_start_address,m_end_address,fileOne_key,arr_dic
    page = int(request.args.get('page', 1))
    status=request.args.get('click')
    if request.method == 'POST':
        arr_dic = {}
        filename1 = request.form.get('base_file')
        filename2 = request.form.getlist('second_file')
        plot_list =[]
        array1,num_rows = get_binData(filename1)
        fileOne_key = filename1.replace(".bin",'')
        arr_dic[fileOne_key]=array1
        for file in filename2:
            dumpfile = file
            next_file_key = dumpfile.replace(".bin",'')
            start_address=int(str(m_start_address), 16)
            end_address=int(str(m_end_address), 16)
            array2,num_rows = get_binData(dumpfile)
            arr_dic[next_file_key]=array2
            plot_json1, plot_json2,next_button_tag,bin_files=heatmap(arr_dic[fileOne_key],arr_dic[next_file_key],num_rows,page,fileOne_key,next_file_key,start_address,end_address)
            plot_list.append(plot_json1)
            plot_list.append(plot_json2)
        return render_template('heatmap.html', plot_json=plot_list, page=page, prev_page=page - 1, next_page=page + 1,next_button_tag=next_button_tag,bin_files=bin_files)

    elif status == "next":
        updated_plot=[]
        recall_file= request.args.get('filename')
        recall_file_key = recall_file.replace(".bin",'').strip()
        page=back_data[recall_file_key]['page']+1
        plot_json1, plot_json2,next_button_tag,bin_files=heatmap(arr_dic[fileOne_key],arr_dic[recall_file_key],num_rows,page,fileOne_key,recall_file_key,start_address,end_address)
        updated_plot.append(plot_json1)
        updated_plot.append(plot_json2)
        return render_template('heatmap.html', plot_json=updated_plot, page=page, prev_page=page - 1, next_page=page + 1,next_button_tag=next_button_tag,bin_files=bin_files)

    elif status == "prev":
        updated_plot=[]
        recall_file= request.args.get('filename')
        recall_file_key = recall_file.replace(".bin",'')
        page=back_data[recall_file_key]['page']-1
        plot_json1, plot_json2,next_button_tag,bin_files=heatmap(arr_dic[fileOne_key],arr_dic[recall_file_key],num_rows,page,fileOne_key,recall_file_key,start_address,end_address)
        updated_plot.append(plot_json1)
        updated_plot.append(plot_json2)
        return render_template('heatmap.html', plot_json=updated_plot, page=page, prev_page=page - 1, next_page=page + 1,next_button_tag=next_button_tag,bin_files=bin_files)
    return render_template('index.html')

@app.route('/runfile', methods=['GET', 'POST'])
def runfile():
    global start_address,end_address,m_start_address,m_end_address
    if request.method == 'POST':
        start_address = int(request.form['start_address'])
        end_address = int(request.form['end_address'])
        interval = int(request.form['interval'])
        iterations = int(request.form['iterations'])
        m_start_address=start_address
        m_end_address=end_address
        run_resp= run_c_file(start_address,end_address,interval,iterations)
        bin_files = glob.glob(folder_path+"/*.bin")
        bin_files=[os.path.basename(path) for path in bin_files]
        return render_template('heatmap.html',bin_files=bin_files,prev_page=0,next_button_tag = False)
    return render_template('index.html')

if __name__ == '__main__':
    app.run()


