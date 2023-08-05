# Copyright 2016 Arie Bregman
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
from flask import render_template
from flask import request
from flask import jsonify
from flask_wtf import Form
import logging
from wtforms import SubmitField

from jino.main import app
from jino.main import db
import jino.models as models

LOG = logging.getLogger('__main__')


class Result(Form):
        job_result = SubmitField()


@app.route('/')
def home():

    form = Result()

    jobs = models.Job.query.filter_by(display=True).order_by(models.Job.created_at)

    return render_template('home.html', jobs=jobs, form=form, config=app.config)


@app.route('/get_console_output')
def get_console_output():

    job_name = request.args.get('job_name')
    build_number = request.args.get('build_number')
    LOG.info("Getting console output for!: %s #%s", job_name, build_number)

    console_output = app.config['client'].get_console_output(job_name, build_number)

    return jsonify(output=console_output)
