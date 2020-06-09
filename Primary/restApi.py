from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import atexit

from Model.serializableSettings import SerializableSettings
from SettingsManagers.settingsFileManager import SettingsFileManager
from Communication.udpTransmitter import UdpTransmitter

app = Flask(__name__)
cors = CORS(app)
primary_settings_manager = SettingsFileManager('Data', 'primary.config')
primary_settings = SerializableSettings(primary_settings_manager.get_all_settings())
primary_transmitter = UdpTransmitter('192.168.0.70', 6943)

secondary_settings_manager = SettingsFileManager('Data', 'secondary.config')
secondary_settings = SerializableSettings(secondary_settings_manager.get_all_settings())
secondary_transmitter = UdpTransmitter('192.168.0.69', 6943)


'''
    Primary Endpoints
'''


@app.route('/master/getAll', methods=['GET'])
def get_master_settings():
    return jsonify(primary_settings.serialize())


@app.route('/master/update/<string:setting_name>', methods=['POST'])
def update_master_setting(setting_name):
    if setting_name not in primary_settings.get_setting_names():
        abort(400)
    if not request.json:
        abort(400)

    primary_settings.settings[setting_name] = str(request.json['newValue'])
    primary_transmitter.send_pair((setting_name, primary_settings.settings[setting_name]))

    return ''


'''
    Secondary Endpoints
'''


@app.route('/slave/getAll', methods=['GET'])
def get_slave_settings():
    return jsonify(secondary_settings.serialize())


@app.route('/slave/update/<string:setting_name>', methods=['POST'])
def update_slave_setting(setting_name):
    if setting_name not in secondary_settings.get_setting_names():
        abort(400)
    if not request.json:
        abort(400)

    secondary_settings.settings[setting_name] = str(request.json['newValue'])
    secondary_transmitter.send_pair((setting_name, secondary_settings.settings[setting_name]))

    return ''


@app.route('/slave/update/colors/<int:index>', methods=['POST'])
def update_slave_color(index):
    previous_colors = secondary_settings.settings['colors']
    color_list = previous_colors.split(',')

    if len(color_list) // 3 <= index:
        abort(400)
    if not request.json:
        abort(400)

    new_color_data = request.json['newValue']
    for i in range(len(new_color_data)):
        color_list[index * 3 + i] = str(new_color_data[i])

    secondary_settings.settings['colors'] = ','.join(color_list)
    secondary_transmitter.send_pair(('colors', secondary_settings.settings['colors']))

    return ''


@app.route('/saveAllSettings')
def save_all():
    save_all_settings()


def save_all_settings():
    primary_settings_manager.save_all(primary_settings.settings)
    secondary_settings_manager.save_all(secondary_settings.settings)


if __name__ == '__main__':
    atexit.register(save_all_settings)
    app.run(host="192.168.0.70")
