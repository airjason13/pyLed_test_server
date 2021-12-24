import os
import glob
from main import app
from qlocalmessage import send_message
from flask import Flask, render_template, send_from_directory, request, redirect, url_for, Response, json
from global_def import *
import traceback
from flask_wtf import Form
from wtforms import validators, RadioField, SubmitField, IntegerField
import log_utils

log = log_utils.logging_init(__file__)
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
led_mode_option = 'led_normal_mode'
br_value = 64
led_select = 3
led_total_width = 80
led_total_height = 12
led_area_startx = 0
led_area_starty = 0
led_area_width = 80
led_area_height = 12

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

def get_led_mode_default():
    print("in get_led_mode_default, led_mode_option:", led_mode_option)
    if led_mode_option is not None:
        return led_mode_option
    else:
        log.error("no led num option")
    return 'normal_mode'

def get_led_total_width_default():
    print("in get_led_num_default, led_total_width:", led_total_width)
    if led_total_width is not None:
        return led_total_width
    else:
        log.error("no led num option")
    return 80

def get_led_total_height_default():
    print("in led_total_height, led_num_option:", led_total_height)
    if led_total_height is not None:
        return led_total_height
    else:
        log.error("no led num option")
    return 12

def get_led_area_startx_default():
    print("in led_area_startx, led_area_startx:", led_area_startx)
    if led_area_startx is not None:
        return led_area_startx
    else:
        log.error("no led num option")
    return 0

def get_led_area_starty_default():
    print("in led_area_starty, led_area_starty:", led_area_starty)
    if led_area_starty is not None:
        return led_area_starty
    else:
        log.error("no led num option")
    return 0

def get_led_area_width_default():
    print("in led_area_width, led_area_width:", led_area_width)
    if led_area_width is not None:
        return led_area_width
    else:
        log.error("no led num option")
    return 80

def get_led_area_height_default():
    print("in led_area_height, led_area_height:", led_area_height)
    if led_area_height is not None:
        return led_area_height
    else:
        log.error("no led num option")
    return 12

class TestForm(Form ):
    #style = "font-size:64px"
    style = {'class': 'ourClasses', 'style': 'font-size:32px;'}
    integerfiles_style = {'class': 'ourClasses', 'style': 'font-size:32px;width:6ch'}
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
            render_kw=integerfiles_style
    )

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
        render_kw=integerfiles_style
    )
    led_mode_default = get_led_mode_default()
    log.debug("led_mode_default:%s", led_mode_default)
    led_mode_switcher = RadioField(
        'Area_Mode',
        [validators.Required()],
        choices=[('led_normal_mode', 'Normal'), ('led_area_mode', 'Area')], default=get_led_mode_default(),
        render_kw=style
    )

    led_total_width_fields = IntegerField(
        label="LED Total Width:", validators=[
            validators.Required(),
            validators.NumberRange(min=0, max=960),
        ],
        default=get_led_total_width_default(),
        render_kw=integerfiles_style
    )
    led_total_height_fields = IntegerField(
        label="LED Total Height:", validators=[
            validators.Required(),
            validators.NumberRange(min=0, max=960),
        ],
        default=get_led_total_height_default(),
        render_kw=integerfiles_style
    )
    led_area_startx_fields = IntegerField(
        label="LED_Area_StartX:", validators=[
            validators.Required(),
            validators.NumberRange(min=0, max=960),
        ],
        default=get_led_area_startx_default(),
        render_kw=integerfiles_style
    )
    led_area_starty_fields = IntegerField(
        label="LED_Area_StartY:", validators=[
            validators.Required(),
            validators.NumberRange(min=0, max=960),
        ],
        default=get_led_area_starty_default(),
        render_kw=integerfiles_style
    )
    led_area_width_fields = IntegerField(
        label="LEDAreaWidth :", validators=[
            validators.Required(),
            validators.NumberRange(min=0, max=960),
        ],
        default=get_led_area_width_default(),
        render_kw=integerfiles_style
    )
    led_area_height_fields = IntegerField(
        label="LEDAreaHeight :", validators=[
            validators.Required(),
            validators.NumberRange(min=0, max=960),
        ],
        default=get_led_total_height_default(),
        #render_kw=style
        render_kw=integerfiles_style
    )
    submit = SubmitField('Submit', render_kw=style)


@app.route("/")
def index():
    testform = TestForm()
    testform.validate()
    return render_template("index.html", title=title, br=64, form=testform)



@app.route("/TEST_COLOR/RED", methods=['POST', 'GET'])
def TEST_COLOR_RED():
    send_message(color_switch="test_color:RED")
    #return redirect(url_for('index'))
    testform = TestForm()
    testform.validate_on_submit()
    return render_template("index.html", title=title, form=testform, validate=True)

@app.route("/TEST_COLOR/GREEN", methods=['POST', 'GET'])
def TEST_COLOR_GREEN():
    send_message(color_switch="test_color:GREEN")
    testform = TestForm()
    testform.validate_on_submit()
    return render_template("index.html", title=title, form=testform, validate=True)
    #return redirect(url_for('index'))

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
    global led_mode_option
    global led_area_startx
    global led_area_starty
    global led_area_width
    global led_area_height

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
        send_message(led_num="led_num:" + led_num_option + ",led_select:" + led_select)



    list_led_mode_option = request.form.getlist('led_mode_switcher')
    led_mode_option = list_led_mode_option[0]
    send_message(set_led_mode="led_mode_option:" + led_mode_option)

    if 'area' in led_mode_option:
        list_led_total_width = request.form.getlist('led_total_width_fields')
        led_total_width = list_led_total_width[0]
        log.debug("led_total_width:%s", led_total_width)
        send_message(set_led_tatol_width="led_total_width:" + led_total_width)

        list_led_total_height = request.form.getlist('led_total_height_fields')
        led_total_height = list_led_total_height[0]
        log.debug("led_total_height:%s", led_total_height)
        send_message(set_led_tatol_height="led_total_height:" + led_total_height)

        list_led_area_startx = request.form.getlist('led_area_startx_fields')
        led_area_startx = list_led_area_startx[0]
        log.debug("led_area_startx:%s", led_area_startx)
        send_message(set_led_area_startx="led_area_startx:" + led_area_startx)

        list_led_area_starty = request.form.getlist('led_area_starty_fields')
        led_area_starty = list_led_area_starty[0]
        log.debug("led_area_starty:%s", led_area_starty)
        send_message(set_led_area_starty="led_area_starty:" + led_area_starty)

        list_led_area_width = request.form.getlist('led_area_width_fields')
        led_area_width = list_led_area_width[0]
        log.debug("led_area_width:%s", led_area_width)
        send_message(set_led_area_width="led_area_width:" + led_area_width)

        list_led_area_height = request.form.getlist('led_area_height_fields')
        led_area_height = list_led_area_height[0]
        log.debug("led_area_height:%s", led_area_height)
        send_message(set_led_area_height="led_area_height:" + led_area_height)

        send_message(set_led_area_params_confirm="confirm:true")


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

