import base64
import os
from urllib.parse import quote as urlquote
# from whatstk import df_from_txt_whatsapp
from flask import Flask, send_from_directory
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
# import templates as templateUtils
import ai as openaiUtils
import pandas as pd 

UPLOAD_DIRECTORY = "files"


if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


# Normally, Dash creates its own Flask server internally. By creating our own,
# we can create a route for downloading files directly:
server = Flask(__name__)
app = dash.Dash(server=server)


@server.route("/download/<path:path>")
def download(path):
    """Serve a file from the upload directory."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)


def txt_to_df(filename):
    # df=pd.read_csv(filename,header=None,error_bad_lines=False,encoding='utf8')
    
    messages = []
    current_message = {}

    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
          

            # Check if it is a new message
            # if line.startswith('[', 1, 11):
            #     print("starts")
            if current_message:
                    messages.append(current_message)
                    
            current_message = {}

                # Extract the timestamp and sender
            timestamp, sender_message = line[1:21], line[23:]
            sender, message = sender_message.split(':', 1)
            current_message['timestamp'] = timestamp
            current_message['sender'] = sender.strip()
            current_message['message'] = message.strip()
            

    # Append the last message
    if current_message:
        messages.append(current_message)

    df = pd.DataFrame(messages)
    return df



  







app.layout = html.Div(
    [
        html.H2("Whatsapp summary generator"),
        html.H3("Upload"),
        dcc.Upload(
            id="upload-data",
            children=html.Div(
                ["Drag and drop or click to select a file to upload."]
            ),
            style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
            multiple=True,
        ),
        html.Br(),
        html.Br(),

        html.Div([
    dcc.Textarea(
        id='prompt-input',
        value='Enter your prompt here',
        style={'width': '100%', 'height': 100},
    ),
  
]),
    
        
        html.H3("Here is the summary"),
        html.Ul(id="file-list"),
    ],
    style={"max-width": "500px"},
)


def save_file(name, content):
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(UPLOAD_DIRECTORY, name), "wb") as fp:
        fp.write(base64.decodebytes(data))


def uploaded_files():
    """List the files in the upload directory."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files





@app.callback(
    Output("file-list", "children"),
    [Input("upload-data", "filename"), Input("upload-data", "contents")],
    [Input('prompt-input', 'value')]
)
def update_output(uploaded_filenames, uploaded_file_contents,value):
    """Save uploaded files and regenerate the file list."""

    if uploaded_filenames is not None and uploaded_file_contents is not None:
        for name, data in zip(uploaded_filenames, uploaded_file_contents):
            name=name
            save_file(name, data)
    
        path = os.path.join(UPLOAD_DIRECTORY, name)
      
        df=txt_to_df(path)
        # print(df)
        # print(df['message'])
      
        params   = openaiUtils.set_open_params()
        # response = openaiUtils.gpt_turbo(templateUtils.chat_summary.format(df["message"]))
        print(value)
        response = openaiUtils.gpt_turbo(value.format(df["message"]))
        res = response.choices[0].message.content.replace("\n", "").replace("  ", "").replace("'", "")
        print(res)
        return [html.Li(res)]
                

    
if __name__ == "__main__":
    app.run_server(debug=True, port=8886)