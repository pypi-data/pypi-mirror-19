RepubMQTT
=========

RepubMQTT re-publishes MQTT messages to MQTT, RESTful or logfiles, allowing
filtering and selection of fields via regular expressions.

A Python dict structure is used to describe all actions. For example, the
following definition 

~~~python
myrule = {
    'name': 'outside_temp',
    'rules': [['filter','selector', 'publish']],
    'filter': {'topic': '(loftha.*)', 'event_data.entity_id': '(sensor.dark_sky_temperature)'},

    'selector': { 'temperature:event_data.new_state.state': '(.*)'},
    'publish':  {'protocol': 'log', 'data': "%(ts)s: temperature is %(temperature)s" }
}

RULES = [myrule]
~~~

will produce the output 

```
2016-12-22 14:16:31: temperature is 2.2
```

from this (very complex) MQTT msg:

```
 2016-12-22 14:16:31: loftha -> {
    "event_data": {
        "entity_id": "sensor.dark_sky_temperature",
        "new_state": {
            "attributes": {
                "attribution": "Powered by Dark Sky",
                "friendly_name": "Outside",
                "icon": "mdi:thermometer",
                "unit_of_measurement": "\u00b0C"
            },
            "entity_id": "sensor.dark_sky_temperature",
            "last_changed": "2016-12-22T19:16:31.073761+00:00",
            "last_updated": "2016-12-22T19:16:31.073761+00:00",
            "state": "2.2"
        },
        "old_state": {
            "attributes": {
                "attribution": "Powered by Dark Sky",
                "friendly_name": "Outside",
                "icon": "mdi:thermometer",
                "unit_of_measurement": "\u00b0C"
            },
            "entity_id": "sensor.dark_sky_temperature",
            "last_changed": "2016-12-22T19:04:00.969787+00:00",
            "last_updated": "2016-12-22T19:04:00.969787+00:00",
            "state": "2.3"
        }
    },
    "event_type": "state_changed"
}
```

Configuration
-------------

Each definition dictionary has to specify the 'name' of the entry
and a 'rules' field that contains a list of 3 items, specifying the 
'filter', 'selector' and 'publish' rules:

~~~python
    'name': 'outside_temp',
    'rules': [['filter','selector', 'publish']],
~~~

The names 'filter', 'selector', and 'publish' can be freely choosen, plus you can habe multiple sets of rules, as in

~~~python
    'name': 'aew_desk',
    'rules': [['qfilter','qselector', 'qpublish'],
            ['infilter','inselector', 'inpublish']],
~~~

Each of the names specified must exists as a key in same definition dict.


'filter' and 'selector'
----------------------
The 'filter' and 'selector' rules are themseleves dicts and the share the 
same syntax:

~~~
    'filter|selector': { '[<new_field_name>]:<fieldname>': '<re>' ... }
~~~

The ```<fieldname>``` selects the field with the same name in the incomming
MQTT message the optional ```<new_field_name>``` can be used to set a new
name in the output record, the value ```<re>``` specifies a regular expression.
If the re matches the value of the field in the incomming MQTT message, the
field is selected. For 'filter' rules the message passes through the filter
iff all the fields are selected successfully.  For 'selector' rules, all
selected fields are made available for further processing.  

Two additonal "virtual" fields are available: 'ts' is a human readble time
stamp and 'topic' is the topic of the incoming MQTT message.

A 'filter' rule must be pressent. If the 'selector' name is given as '' then
the full input message is made availabe for further processing, with the
additonal fields 'ts' and 'topic'.

The 'publish' entry specifes what actions to take. 

For example, the filter:

```'filter': {'topic': 'loftha.\*', 'entity_id': 'sensor.dark_sky_temperature'}```

would match an incoming MQTT message with the topic ```loftha/#``` and a 
json payload field ```entity_id``` with the content ```sensor.dark_sky_temperature```.

'publish'
--------
The 'publish' entry is either a dict or a list of dicts. Two keys are
required, 'protocol' and 'data'.  Valid values for 'protocol' are 'log',
    'mqtt', or 'restful'.

'data' holds the template for the data to be published. It can either be a 
string with pythonesque parenthesised mapping keys ```%(name)s```, which will 
be replaced with actual data, or it can be a dict, in which case the data will
be published as json.
    'copy_fields' is available to copy selected fields to the data dict.

'protocol' mqtt
---------------

The 'topic' field will hold the MQTT topic to publish to. Also, the optional
field 'retain' can be set to ```True``` in order to cause the MQTT broker to
retain the msg. The optional field 'once' can be set to ```True``` if this
message is only ever to be pubished once during the runtime of the program.

'protocol' restful
------------------

The field 'url' specifies the URL to post the msg to, the optional 'header'
can be used to specify additonal HTTP protocol header fields, in the form of
a dictionary.


'protocol' log
--------------
The 'log' publisher can specify a 'logfile' filed to which to write the
output. Default is stdout.


'copy\_fields'
-----------
The optional
    'copy_fields' field holds a list of copy definitons, consisting of
destination field, source field and conversion:

```    'copy_fields': [['value', 'lvl', 'int']] ```

In this example, the content of the field 'lvl' (either from a 'selector'
entry or from the input message) with be copied to the output field 'value'
after conversion to integer.

copy\_fields conversions
-----------------------

When copying fields, you can specify a data conversion.  Built-in convserion
are ```int``` and ```float```. In addtion, you can specify a key to
the ```xlate``` dict. In this case, a lookup is used to select the data
value for the destination field. An example of the ```xlate``` dict
might look like this:

```python
xlate = {
  'motion': { 'off':  False,    'on': True },
  'door':   { 'off':  'Closed', 'on': 'Open' },
}
```
Here, using the conversion ```door``` would translate an input field value
of 'off' to 'Closed'.


Installation
------------

Use the standard pip install:
```python[3] setup.py install```

The setup installs a sample script 'repubmqtt', it take a config file
like repub.conf-sample as argument.
