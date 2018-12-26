from os import getcwd
from os.path import join
import requests
import json
from flask import Flask, request, send_from_directory, send_file
import celery

    # INSTANCES
from common import LOG_FILES
from controller import interrupt, observation_state, observe, observation_id
from interfaces.enclosure.plc import enclosure
from interfaces.mount.skyx import mount
from interfaces.ccd.sbig import DIRECTORY, ccd
from interfaces.weather import WeatherStation
# send_back_url = ''

CWD = getcwd()
flask = Flask(__name__)

@celery.task
def observe_callback(observation_result):
    requests.post(send_back_url, observation_result)

@flask.route('/interrupt')
def interruption_request():
    interrupt()
    pass

# @flask.route('/observation', methods=['POST'])
# def request_observe():
#     global send_back_url
#     observation_data = request.get_json()
#     observe.apply_async(
#         kwargs={'ra': observation_data['RA'], 'dec': observation_data['DEC'], 'time': observation_data['Exposure Time'],
#                 'temperature': 0, 'binning': observation_data['Binning'], 'interval': observation_data['Interval'],
#                 'count': observation_data['Number'], 'id': observation_data['ID']}, link=observe_callback.s())
#     send_back_url = observation_data['IP']
#     return 'request sent'

@flask.route('/manual', methods=['POST'])
def do_observation():
    data = eval(request.json)[0]
    print(data)
    print('id ' + str(data[0]))
    print('time ' + data[2])
    print('ra ' + data[3] + ' dec ' + data[4] + ' binning ' + data[5] + ' interval ' + data[6] + ' count ' + data[7] + ' count2 ' + data[8])
    observation = observe(ra=int(data[3]), dec=int(data[4]), time=int(data[2]), binning=int(data[5]),
                           temperature=0, interval=int(data[6]), count=int(data[7]),
                           id=data[0], count2=int(data[8]))
    #observe.apply_async(
     #    kwargs={'ra': data['ra'], 'dec': data['dec'], 'time': data['time'], 'binning': data['binning'],
      #           'temperature': data['temperature'], 'interval': data['interval'], 'count': data['count'],
       #          'id': data['id'], 'count2' : data['count2']})


@flask.route('/logs')
def get_logs():
    return send_file(join(CWD, LOG_FILES))


@flask.route('/images/<path:path>')
def get_image(path):
    return send_from_directory(DIRECTORY, path)


@flask.route('/position')
def get_mount_position():
    position = mount.celestical_to_horizontal(mount.get_position())
    position = {
        'ALT': position.alt.deg,
        'AZ': position.az.deg
    }
    position_json = json.dumps(position)
    return position_json


@flask.route('/enclosure')
def get_enclosure_state():
    return enclosure.get_enclosure_state()


@flask.route('/status')
def get_shekarchi_status():
    return observation_state


@flask.route('/tracking')
def get_tracking_status():
    return mount.is_tracking()


@flask.route('/id')
def get_observationid():
    return observation_id


@flask.route('/api')
def get_parsa():
    position = mount.celestical_to_horizontal(mount.get_position())
    api = {
        'ALT': position.alt.deg,
        'AZ': position.az.deg,
        'enclosure': enclosure.get_enclosure_state(),
        'status': observation_state,
        'tracking': mount.is_tracking(),
        'id': observation_id
    }
    return json.dumps(api)


@flask.route('/weather')
def get_weather_status():
    try:
        weather_station = WeatherStation()
        weather_station.check_weather()
        return weather_station.get_weather_status()
    except:
        return 'e'

@flask.route('/get_image_back', methods = ['POST'])
def get_image_back():
    image = request.files['file']
    print(image)
    #image.save('./out/images/' + request.data['id'] + request.data['ccd'] + '/' + image.filename)
    image.save('./run/user/1000/gvfs/smb-share\:server\=nas-la-ino.local\,share\=wfs_data/' + request.data['id'] + request.data['ccd'] + '/' + image.filename)
    return 'gir nayoft.'

@flask.route('/get_latest_image')
def get_latest_image():
    return 1
