#########################################################################
## Define your tables below, for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

## These tables are synched "up" from the clients to the server.

import datetime

############### Procedure Harness Table ###############

db.define_table('procedures',
                Field('procedure_id', 'bigint', required=True),  # key
                Field('last_update', 'datetime', default=datetime.datetime.utcnow(), required=True),
                Field('name', 'string') # Name of procedure
                )

############### Procedure API Tables #################


# Synched server -> client (except for some special rows).
db.define_table('settings',
                Field('procedure_id'), # Can be Null for device-wide settings.
                Field('setting_name'),
                Field('setting_value'), # Encoded in json-plus.
                Field('last_updated', 'datetime', default=datetime.datetime.utcnow(), update=datetime.datetime.utcnow())
                )

# Synched client -> server
db.define_table('logs',
                Field('time_stamp', 'datetime', default=datetime.datetime.utcnow()),
                Field('procedure_id'),
                Field('log_level', 'integer'),  # int, 0 = most important.
                Field('log_message', 'text')
                )

# Synched client -> server
db.define_table('outputs',
                Field('time_stamp', 'datetime', default=datetime.datetime.utcnow()),
                Field('procedure_id'),
                Field('name'),  # Name of variable
                Field('output_value', 'text'),  # Json, short please
                Field('tag')
                )

# Synched client -> server
# modulename + name is a key (only one row for combination).
db.define_table('module_values',
                Field('time_stamp', 'datetime', default=datetime.datetime.utcnow()),
                Field('procedure_id'),
                Field('name'),  # Name of variable
                Field('module_value', 'text'),  # Json, short please
                )

db.define_table('synchronization_events',
                Field('table_name'),
                Field('time_stamp', 'datetime', default=datetime.datetime.utcnow()),
                )

# State of the procedure when last run.
# Note: when we synch this, we always have to keep at least one entry.
db.define_table('procedure_state',
                Field('procedure_id'),
                Field('class_name'), # Name of the class that run in the procedure.
                Field('procedure_state', 'text'),
                Field('time_stamp', 'datetime', default=datetime.datetime.utcnow())
                )

# initialize settings manager
import slugiot_settings
settings = slugiot_settings.SlugIOTSettings()

# Let's initialize the setup.
import slugiot_setup
slugiot_setup = slugiot_setup.SlugIOTSetup()
slugiot_setup.db = db
slugiot_setup.server_url = server_url
slugiot_setup.settings = settings
slugiot_setup.device_id = settings.get_device_id()



