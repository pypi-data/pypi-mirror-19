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
from sqlalchemy import DateTime
from sqlalchemy import func

from jino.main import db


jobs = db.Table('jobs',
                db.Column('parent_job', db.String(64),
                          db.ForeignKey('job.name')),
                db.Column('sub_job', db.String(64),
                          db.ForeignKey('job.name')),
                )


class Job(db.Model):
    """Represents Jenkins job."""

    __tablename__ = 'job'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    status = db.Column(db.String(64))
    button_status = db.Column(db.String(64))
    title = db.Column(db.String(64))
    display = db.Column(db.Boolean, default=False)
    build_number = db.Column(db.Integer)
    build_duration = db.Column(db.String(64))
    sub_jobs = db.relationship('Job',
                               secondary=jobs,
                               primaryjoin=(jobs.c.parent_job == name),
                               secondaryjoin=(jobs.c.sub_job == name),
                               backref=db.backref('jobs', lazy='dynamic'),
                               lazy='dynamic')
    created_at = db.Column('create_date', DateTime, default=func.now())

    def is_sub_job(self, job):
        return self.sub_jobs.filter(
            jobs.c.sub_job == job.name).count() > 0

    def add_sub_job(self, job):
        if not self.is_sub_job(job):
            self.sub_jobs.append(job)
            return self

    def __repr__(self):
        return "<Job %r" % (self.name)
