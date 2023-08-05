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
import jenkins
import logging
import sys

LOG = logging.getLogger('__main__')


def get_jobs_status(server, jobs):
    """Returns dict of jobs and their status

    :param server: Jenkins server instance
    :param jobs: list of jobs
    """

    jobs_status = {}

    try:
        for job in jobs:
            jobs_status[job] = {}
            last_build_num = server.get_job_info(
                job)['lastCompletedBuild']['number']
            status = str(server.get_build_info(
                job, last_build_num)['result'])
            sub_jobs = server.get_build_info(
                job, last_build_num)['subBuilds']

            if status == 'SUCCESS':
                jobs_status[job]['status'] = 'success'
                jobs_status[job]['button'] = 'btn-success'
            else:
                jobs_status[job]['status'] = 'failure'
                jobs_status[job]['button'] = 'btn-danger'

            jobs_status[job]['sub_jobs'] = {}

            for sub_job_dict in sub_jobs:
                sub_job = sub_job_dict['jobName']
                jobs_status[job]['sub_jobs'][sub_job] = {}
                sub_last_build_num = server.get_job_info(
                    sub_job)['lastCompletedBuild']['number']
                sub_status = str(server.get_build_info(
                    sub_job, sub_last_build_num)['result'])

                if status == 'SUCCESS':
                    jobs_status[job]['sub_jobs'][sub_job]['status'] = 'success'
                    jobs_status[job]['sub_jobs'][sub_job]['button'] = 'btn-success'
                else:
                    jobs_status[job]['sub_jobs'][sub_job]['status'] = 'failure'
                    jobs_status[job]['sub_jobs'][sub_job]['button'] = 'btn-danger'
                    
            #jobs_status[job]['subBuilds'] = [str(sub_job['jobName']) for sub_job in sub_jobs]
            LOG.info("Got info for job: %s", job)

    except Exception as e:
        LOG.info("Could not get information for %s", job['jobName'])
        LOG.info("Error: %s", e)
        sys.exit(2)

    return jobs_status


def get_job_detailed_result(server, job):
    """Return detailed job result."""

    last_build_num = server.get_job_info(
        job)['lastCompletedBuild']['number']

    output = server.get_build_console_output(job, last_build_num)

    #failure_url = server_url + '/job/' + job + '/' + str(last_build_num) + '/api/xml?depth=2}'
    #request = Request(failure_url)
    #auth = '%s:%s' % (username, password)
    #request.add_header('Authorization', auth)
    #failure = urlopen(request).read()


class JenkinsClient(object):

    def __init__(self, url, user, password):
        self.url = url
        self.user = user
        self.password = password

        self.client = jenkins.Jenkins(self.url, self.user, self.password)

    def get_last_build_number(self, job):
        """Given a job name, returns the last build number."""
        return self.client.get_job_info(job)['lastCompletedBuild']['number']

    def get_build_result(self, job, build_number):
        """Given a job name, it returns string of the last completed

        build result.
        """
        return str(self.client.get_build_info(job, build_number)['result'])

    def get_sub_jobs(self, job):
        """Given a job name, it returns a list of sub jobs

        dictionaries.

        [{'subJob_1': {'status': 'success'},
         {'subJob_2': {'status': 'failure'}] 

        If no sub jobs exist it returns None"""
         
        sub_jobs = []
        job_info = self.client.get_job_info(job)

        if job_info['lastCompletedBuild']['subBuilds']:

            for sub_job in job_info['lastCompletedBuild']['subBuilds']:
                sub_jobs.append({sub_job['jobName']: {}})
                sub_jobs[-1][sub_job['jobName']]['status'] = sub_job['result']
                sub_jobs[-1][sub_job['jobName']]['duration'] = sub_job['duration']
                sub_jobs[-1][sub_job['jobName']]['buildNumber'] = sub_job['buildNumber']

            return sub_jobs

        else:
            return None

    def get_console_output(self, job, build_number):
        """Given a job and a build number, returns the console 
        
        output of the build.
        """
        return self.client.get_build_console_output(job, int(build_number))
