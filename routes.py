import os
import glob
from main import app
from qlocalmessage import send_message
from flask import Flask, render_template, send_from_directory, request, redirect, url_for, Response, json
from global_def import *
import traceback
from flask_wtf import Form
from wtforms import validators, RadioField, SubmitField, IntegerField
import jlog
log = jlog.logging_init("flask_plugin")
import os
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

class LED_PAR():
    COLOR_RED = "test_color:RED"
    COLOR_GREEN = "test_color:GREEN"
    COLOR_BLUE = "test_color:BLUE"
    COLOR_WHITE = "test_color:WHITE"

led_color = LED_PAR.COLOR_RED
led_num_option = 'led_num_all'
br_value = 64
led_select = 3

def route_set_led_br(br):
    global br_value
    br_value = br

def route_set_led_color(color):
    global led_color
    led_color = color


def get_led_num_default():
    print("in get_led_num_default, led_num_option:", led_num_option)
    if led_num_option is not None:

        return led_num_option
    else:
        log.error("no led num option")

    return 'led_num_all'

class TestForm(Form ):
    #style = "font-size:64px"
    style = {'class': 'ourClasses', 'style': 'font-size:32px;'}
    color_switcher = RadioField(
        'Led Color',
        [validators.Required()],
        choices=[('test_color:RED', 'RED'), ('test_color:GREEN', 'GREEN'), ('test_color:BLUE', 'BLUE'), ('test_color:WHITE', 'WHITE')],
        default=led_color,
        render_kw=style
    )
    led_num_default = get_led_num_default()
    print("in TestForm, led_num_default:", led_num_default)
    led_brightness_fields = IntegerField(label="Led Brightness:", _name="Led Brightness:", validators=[
                validators.Required(),
                validators.NumberRange(min=0, max=255)
            ], default=br_value,
            render_kw=style)

    choice_switcher = RadioField(
        'led_num',
        [validators.Required()],
        choices=[('led_num_all', 'ALL'), ('led_num_single', 'SINGLE')], default=led_num_default,
        render_kw=style
    )
    led_select_fields = IntegerField(
        label="Led Num:", validators=[
            validators.Required(),
            validators.NumberRange(min=1, max=961)
        ],
        default=led_select,
        render_kw=style
    )
    submit = SubmitField('Submit',render_kw=style)

@app.route("/")
def index():
    testform = TestForm()
    return render_template("index.html", title=title, br=64, form=testform)



@app.route("/TEST_COLOR/RED", methods=['POST', 'GET'])
def TEST_COLOR_RED():
    send_message(color_switch="test_color:RED")
    #return redirect(url_for('index'))
    testform = TestForm()
    testform.validate_on_submit()
    return render_template("index.html", title=title, form=testform)

@app.route("/TEST_COLOR/GREEN", methods=['POST', 'GET'])
def TEST_COLOR_GREEN():
    send_message(color_switch="test_color:GREEN")
    return redirect(url_for('index'))

@app.route("/TEST_COLOR/BLUE", methods=['POST', 'GET'])
def TEST_COLOR_BLUE():
    send_message(color_switch="test_color:BLUE")
    return redirect(url_for('index'))

@app.route("/TEST_COLOR/WHITE", methods=['POST', 'GET'])
def TEST_COLOR_WHITE():
    send_message(color_switch="test_color:WHITE")
    return redirect(url_for('index'))

@app.route("/BR_ADJUST", methods=['POST', 'GET'])
def BR_ADJUST():
    global br_value
    br_value = request.form["br_slider"]
    send_message(set_br="br_value:" + br_value)
    testform = TestForm()
    return render_template("index.html", title=title, br=br_value, form=testform)

@app.route("/LED_NUM", methods=['POST', 'GET'])
def LED_NUM():
    global led_color
    global led_num_option
    global led_select
    global br_value
    log.debug("led_color : %s", led_color)
    list_led_color = request.form.getlist('color_switcher')
    led_color = list_led_color[0]
    send_message(color_switch=led_color)

    list_led_num_option = request.form.getlist('choice_switcher')
    led_num_option = list_led_num_option[0]

    list_br_value = request.form.getlist('led_brightness_fields')
    br_value = list_br_value[0]

    list_led_select = request.form.getlist('led_select_fields')
    led_select = list_led_select[0]

    send_message(set_br="br_value:" + br_value)
    if 'all' in led_num_option[0]:
        send_message(led_num="led_num:" + led_num_option)
    else:
        send_message(led_num="led_num:" + led_num_option + ",led_select:"+ led_select)


    testform = TestForm()
    return render_template("index.html",title=title, form=testform)

def gen(video):
    """视频流生成函数"""
    while True:
        frame = video.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """视频流路由(route).放到 img 标签的 src 属性."""
    #return Response(gen(Video_C("./logos.mp4")),
    #                mimetype='multipart/x-mixed-replace; boundary=frame')
    return


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
def route_test():
    print("route test!")

