# -*- coding: utf-8 -*-
"""
Start video conversations from Twist by just typing `/appear room-name`
"""
import os

from flask import Flask
from flask import jsonify
from flask import request
import requests

app = Flask(__name__)


@app.route('/transcribe/incoming', methods=['POST'])
def incoming():
    event_type = request.form['event_type']

    if event_type == 'ping':
        return jsonify({'content': 'pong'})
    else:
        content = request.form['content']
        command = request.form['command']
        command_argument = request.form['command_argument']
        #image_url = "https://lh3.googleusercontent.com/GrgRpwI4qGXZNG3pra_JAgxB9TPGLrEoW7eng7AaatV9RVW_P8e9GeXjKQXv_2XKmSI"
        #image_url = request.form['image']


        print ("content: " + content)
        print ("command: " + command)
        print ("command_argument: " + command_argument)
        print("comment_id:" + request.form['comment_id'])

        image_url = 'modificat %s' % command_argument

        #if (len(request.form['attachments'])>0):
        #image_url = image_url + "hi ha algo"
        appear_url =  'https://appear.in/%s' % command_argument

        response = requests.get("https://api.twistapp.com/api/v2/comments/getone?id=" + request.form['comment_id'], headers="Authorization: Bearer oauth2:4754b6fb12f8557221b9975701ca2f7b0432a23d").content

        image_url = response.json()

        content = content.replace(u'%s %s' % (command, command_argument),
                                  u'%s' % (image_url))

        return jsonify({
            'content': content,
        })

@app.route('/config/')
def conf():
    """
    URL d'inici = https://twist-transcribe.herokuapp.com/?install_id=30078&user_id=57010&post_data_url=https%3A%2F%2Ftwistapp.com%2Fapi%2Fv2%2Fintegration_incoming%2Fpost_data%3Finstall_id%3D30078%26install_token%3D30078_40c17672a965cca1dae424de0baac187&user_name=Pau+C.

    """

    install = request.args.get('install_id')
    user_id = request.args.get('user_id')
    user_name = request.args.get('user_name')
    return "<h1>Welcome to this integration</h1>" + "<p>"+ install +"</p>"

@app.route('/', methods=['GET'])
def index():
    return "<h1>Welcome to this integration</h1>"


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)