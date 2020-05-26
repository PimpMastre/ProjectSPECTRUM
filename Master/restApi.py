from flask import Flask, jsonify, request, abort
import atexit

from Model.serializableSettings import SerializableSettings
from SettingsManagers.settingsFileManager import SettingsFileManager
from Communication.udpTransmitter import UdpTransmitter

app = Flask(__name__)
master_settings_manager = SettingsFileManager('Data', 'master.config')
master_settings = SerializableSettings(master_settings_manager.get_all_settings())
master_transmitter = UdpTransmitter('192.168.0.70', 6943)

slave_settings_manager = SettingsFileManager('Data', 'slave.config')
slave_settings = SerializableSettings(slave_settings_manager.get_all_settings())
slave_transmitter = UdpTransmitter('192.168.0.69', 6943)


'''
    Master Endpoints
'''


@app.route('/master/getAll', methods=['GET'])
def get_master_settings():
    return jsonify(master_settings.serialize())


@app.route('/master/update/<string:setting_name>', methods=['POST'])
def update_master_setting(setting_name):
    if setting_name not in master_settings.get_setting_names():
        abort(400)
    if not request.json:
        abort(400)

    master_settings.settings[setting_name] = str(request.json['newValue'])
    master_transmitter.send_pair((setting_name, master_settings.settings[setting_name]))


'''
    Slave Endpoints
'''


@app.route('/slave/getAll', methods=['GET'])
def get_slave_settings():
    return jsonify(slave_settings.serialize())


@app.route('/slave/update/<string:setting_name>', methods=['POST'])
def update_slave_setting(setting_name):
    if setting_name not in slave_settings.get_setting_names():
        abort(400)
    if not request.json:
        abort(400)

    slave_settings.settings[setting_name] = str(request.json['newValue'])
    slave_transmitter.send_pair((setting_name, slave_settings.settings[setting_name]))

    return ''


@app.route('/slave/update/colors/<int:index>', methods=['POST'])
def update_slave_color(index):
    previous_colors = slave_settings.settings['colors']
    color_list = previous_colors.split(',')

    if len(color_list) // 3 <= index:
        abort(400)
    if not request.json:
        abort(400)

    new_color_data = request.json['newValue']
    for i in range(len(new_color_data)):
        color_list[index * 3 + i] = str(new_color_data[i])

    slave_settings.settings['colors'] = ','.join(color_list)
    slave_transmitter.send_pair(('colors', slave_settings.settings['colors']))

    return ''


@app.route('/saveAllSettings')
def save_all():
    save_all_settings()


def save_all_settings():
    master_settings_manager.save_all(master_settings.settings)
    slave_settings_manager.save_all(slave_settings.settings)


if __name__ == '__main__':
    atexit.register(save_all_settings)
    app.run(host="192.168.0.70")
