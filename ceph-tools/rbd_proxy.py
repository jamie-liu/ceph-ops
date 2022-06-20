#!/usr/bin/env python
#coding=utf-8
'''
Describtion: RBD proxy deamon for handling rest API request
Created on 2017-11-10
@author: liu jun
'''

import logging
import subprocess
from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)


# List all snaps of the image
@app.route('/api/public/v1/<pool>/<image>', methods=['GET'])
def list_snaps(pool,image):
    snaps = []
    command = "rbd snap list {0}/{1} |grep -v 'SNAPID NAME' |".format(pool,image) + "awk '{print $2}'"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    if process.returncode:
        logging.error(err)
        return jsonify({'error': err}), 500

    snaps = out.strip().split('\n')
    return jsonify({'snaps': snaps}), 200

# Create snap of the image
@app.route('/api/public/v1/<pool>/<image>/<snap>', methods=['POST'])
def create_snap(pool,image,snap):
    command = "rbd snap create {0}/{1}@{2}".format(pool,image,snap)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    if process.returncode:
        logging.error(err)
        return jsonify({'error': err}), 500

    return '', 200

# Delete snap of the image
@app.route('/api/public/v1/<pool>/<image>/<snap>', methods=['DELETE'])
def delete_snap(pool,image,snap):
    command = "rbd snap rm {0}/{1}@{2}".format(pool,image,snap)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    if process.returncode:
        logging.error(err)
        return jsonify({'error': err}), 500

    return '', 200

# Rollback snap of the image
@app.route('/api/public/v1/<pool>/<image>/<snap>', methods=['PUT'])
def rollback_snap(pool,image,snap):
    command = "rbd snap rollback {0}/{1}@{2}".format(pool,image,snap)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    if process.returncode:
        logging.error(err)
        return jsonify({'error': err}), 500

    return '', 200

# List all images by pool
@app.route('/api/public/v1/<pool>', methods=['GET'])
def list_pool(pool):
    images = []
    command = "rbd list -p {0}".format(pool)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    if process.returncode:
        logging.error(err)
        return jsonify({'error': err}), 500

    images = out.strip().split('\n')
    return jsonify({'images': images}), 200

# Resize iamge
@app.route('/api/public/v1/<pool>/<image>/<size>', methods=['PUT'])
def resize_image(pool,image,size):
    command = "rbd resize {0}/{1} --size {2}".format(pool,image,size)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    if process.returncode:
        logging.error(err)
        return jsonify({'error': err}), 500

    logging.info(out)
    return '', 200

if __name__ == '__main__':
    log_format = '[%(asctime)s] [%(levelname)s] [LINE %(lineno)d]%(message)s'
    logging.basicConfig(filename='/var/log/rbd-proxy.log', filemode='a', format=log_format,datefmt='%Y-%m-%d %H:%M:%S %p', level=logging.INFO)
    logging.info('RBD Proxy started...')
    app.run(host='0.0.0.0', port=8080)
    logging.info('RBD Proxy stoped...')
