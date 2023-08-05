#!/usr/bin/python

from __future__ import print_function

import time
import sys
import json
import re
import string
import requests

DBG = 0

# Utility functions
def dbgprint(lvl, *args, **kwargs):
    ts=time.strftime("DBG %Y-%m-%d %H:%M:%S:",time.localtime())
    if DBG >= lvl: print(ts, *args, file=sys.stderr, **kwargs)


def deepdictvalue(key, ddict, val=None):
    """ extract (or set) a field value from a nested dictionary.
        Raise KeyError if then field does not exits
    """
    keys = key.split('.')
    dbgprint(2, 'deepdictvalue(%s, %s)' % (key, ddict.keys()))
    if len(keys) == 1:
        if val != None:
            ddict[key] = val
        return ddict.get(key, None)
    try:
        return deepdictvalue('.'.join(keys[1:]), ddict[keys[0]], val)
    except KeyError as e:
        dbgprint(3, "deepdictvalue error: key '%s' dict keys: '%s'" % (keys[0], ddict.keys()))
        raise


def extractfromdict(msg, filters, name):
    """ return a dict populated with values extracted from srcdict
        governed by a filterdict (key = fieldname,  value = re ) """

    def determinekey(name_key):
        """ parse filter name key: [new_name:]name[.name].. """
        fkey = name_key.split(':')
        filter_key = fkey[-1]
        if len(fkey) > 1:
            use_key = fkey[0]
        else:
            use_key = filter_key.split('.')[-1]
        return filter_key, use_key
        
    result_msg = {}
    for filter_name_key in filters:
        filter_key, use_key = determinekey(filter_name_key)
        filter_re = filters[filter_name_key]

        msg_val = deepdictvalue(filter_key, msg)
        if msg_val == None:
            return None;
        if type(filter_re) == type([]):
            filter_re_list = filter_re
        else:
            filter_re_list = [filter_re]
        re_result = None
        for re_item in filter_re_list:
            r = re.match(re_item, str(msg_val))
            dbgprint(2, "extractfromdict: %s %s: '%s' '%s' -> %s" % \
                (name, filter_name_key, re_item, str(msg_val),\
                 "not" if r == None else "Match"), end="")
            if r:
                try:
                    re_result = r.group(1)
                except:
                    re_result = r.group(0)
                break
        if re_result:
            result_msg[use_key] = re_result
        else:
            dbgprint(2, "extractfromdict: fin None")
            return None
    dbgprint(2, "extractfromdict: fin %s" % result_msg)
    return result_msg


class RuleSet:
    def __init__(self, ruleset, repub):
        self.restful_cache = {}
        self.name = ruleset['name']
        self.ruleset = ruleset
        self.repub = repub
        self.seen = False
        self.mqttclient=self.repub.mqttclient


    def publish(self, pub, new_record):
        def prepdata(data, new_record):
            try:
                ret_data = data % new_record
            except KeyError as e:
                ret_data = new_record
                log('error', "rule '%s' publish '%s' field '%s' not in record '%s'" % (self.name, publish, e, new_record))
            return ret_data
                
        if type(pub) == type([]):
            publish_dict = pub
        else:
            publish_dict = [pub]
        dbgprint(1, "publish: %s" % publish_dict)
        for publish in publish_dict:
            if publish.get('once', False) and self.seen:
                continue
            retain = publish.get('retain',False)
            if 'copy_fields' in publish:
                data = self.copydict(publish['data'], publish['copy_fields'], new_record)
                dbgprint(1,"publish: %s %s -> %s" % (publish['protocol'], data, new_record))
            else:
                data = publish['data']
                dbgprint(1,"publish: %s %s" % (publish['protocol'], new_record))

            if publish['protocol'] == 'restful':
                url = publish['url'] % new_record
                json_data = prepdata(json.dumps(data), new_record)
                res = self.publish_restful(url, publish['headers'], json_data)
            elif publish['protocol'] == 'mqtt':
                topic = publish['topic'] % new_record
                json_data = prepdata(json.dumps(data), new_record)
                self.publish_mqtt(topic, json_data, retain=retain)
            elif publish['protocol'] == 'log':
                pub_data = prepdata(data, new_record)
                self.publish_log(publish.get('logfile',''), pub_data)
        self.seen = True


    def publish_mqtt(self, topic, json_data, retain=False):
        self.repub.mqttclient.publish(topic, json_data, retain=retain)
        

    def publish_log(self, fname, data):
        if fname:
            f = open(fname,"a+")
        else:
            f = sys.stdout
        print(data,file=f)
        if fname:
            f.close()


    def publish_restful(self, url, headers, data):
    
        now = time.time()
        if not url in self.restful_cache or (self.restful_cache[url]['ts'] + 60) < now:
            rsession = {}
            self.restful_cache[url] = rsession
            rsession['sess'] = requests.Session()
            rsession['ts'] = now
        else:
            rsession = self.restful_cache[url]
        sess = rsession['sess']
    
        dbgprint(1, "restful: url='%s' data='%s'" % (url, data))
        response = sess.post(url, data=data, headers=headers)
        dbgprint(1, "restful: response='%s'" % (response))


    def copydict(self, template, fields, srcdict):
        dstdict = template.copy()
        for dst, src, typ in fields:
            try:
                if typ == 'int':
                    deepdictvalue(dst, dstdict, int(float(deepdictvalue(src, srcdict))))
                    dbgprint(3,"copydict: int %s" % dstdict)
                elif typ == 'float':
                    deepdictvalue(dst, dstdict, float(deepdictvalue(src, srcdict)))
                    dbgprint(3,"copydict: float %s" % dstdict)
                elif typ == '':
                    deepdictvalue(dst, dstdict, deepdictvalue(src, srcdict))
                    dbgprint(1,"copydict: float %s" % dstdict)
                elif typ in self.repub.xlate:
                    v=self.repub.xlate[typ][deepdictvalue(src, srcdict)]
                    dbgprint(3,"copydict: xlate %s %s %s" % (v, deepdictvalue(src, srcdict), self.repub.xlate[typ]))
                    deepdictvalue(dst, dstdict, v)
                    dbgprint(3,"copydict: xlate %s" % dstdict)
            except Exception as e:
                log('error', "copy_fields error '%s' dst '%s' src '%s' type '%s'" % \
                    (e, dst, src, typ))
        return dstdict


class Republish:
    def __init__(self, rules, mqttclient, xlate, dbg):
        self.rulesets = {}
        self.DBG = dbg
        self.mqttclient = mqttclient
        self.xlate = xlate

        if len(rules) == 0:
            dbgprint(1, "no rules added")
        else:
            for r in rules:
                rs = RuleSet(r, self)
                if rs.name in self.rulesets:
                    print("RuleSet error: %s already defined" % (rs.name))
                    sys.exit(1)
                self.rulesets[rs.name] = rs
            dbgprint(1,"added rulesets %s" % rs.name)


    def process_message(self, jrecord):
        if not 'ts' in jrecord:
            time_stamp = time.time()
            ts=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time_stamp))
            jrecord['ts'] = ts
    
        for rule in self.rulesets:
            ruleset = self.rulesets[rule].ruleset
            for rfilter, rselector, rpublish in ruleset['rules']:
                try:
                    filterrecord = extractfromdict(jrecord, ruleset[rfilter], ruleset['name'])
                except KeyError as e:
                    dbgprint(2, "process_message: ruleset '%s' missing field '%s' in filter '%s'" % (ruleset['name'], e, rfilter))
                    continue
                if filterrecord == None:
                    continue
                dbgprint(2, "process_message: ruleset '%s' filter '%s' match %s" % \
                         (ruleset['name'], rfilter, jrecord))
                if not rselector:
                    new_record = jrecord
                else:
                    new_record = extractfromdict(jrecord, ruleset[rselector], ruleset['name'])
                    if new_record == None:
                        log('error',"rule '%s', selector '%s' no match on record '%s'" % (rule, rselector, str(jrecord)))
                        continue
                    new_record['ts'] = jrecord['ts']
                if new_record and rpublish:
                    self.rulesets[rule].publish(ruleset[rpublish], new_record)
        

def log(lvl, msg):
    time_stamp = time.time()
    ts=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time_stamp))
    print("%s: %s %s" % (ts, lvl, msg), file=sys.stderr)

