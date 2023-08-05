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
import imp
from jino.config import SQLALCHEMY_DATABASE_URI
from jino.config import SQLALCHEMY_MIGRATE_REPO
from jino.main import db
from migrate.versioning import api

# Get current repository version
version = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)

# New version migration script path
migration = SQLALCHEMY_MIGRATE_REPO + (
    '/versions/%03d_migration.py' % (version+1))

# Return new empty module object named "old_model"
tmp_module = imp.new_module('old_model')

# Dumps the current database as a Python model
old_model = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)

# Execute old_model
exec(old_model, tmp_module.__dict__)

# Changing the old Python module to the new (current) Python model
script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI,
                                          SQLALCHEMY_MIGRATE_REPO,
                                          tmp_module.meta, db.metadata)

# Write the new module
open(migration, "wt").write(script)

# Upgrade to the new version
api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)

# Get current version (after upgrade)
version = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)

print('New migration saved as ' + migration)
print('Current database version: ' + str(version))
