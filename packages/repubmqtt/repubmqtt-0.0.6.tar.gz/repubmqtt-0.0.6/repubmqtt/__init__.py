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


def log(lvl, *args, **kwargs):
	time_stamp = time.time()
	if False:
		ts=time.strftime("%Y-%m-%d %H:%M:%S: ",time.localtime(time_stamp))
	else:
		ts=""
	print("%s%s" % (ts, lvl), *args, file=sys.stderr, **kwargs)
	sys.stdout.flush()

def dbgprint(lvl, *args, **kwargs):
	if DBG >= lvl: log('dbg'+str(lvl), *args, **kwargs)


def deepdictvalue(key, ddict, val=None):
	""" extract (or set) a field value from a nested dictionary.
		Raise KeyError if then field does not exits
	"""
	keys = key.split('.')
	dbgprint(4, 'deepdictvalue(%s, %s)' % (key, ddict.keys()))
	if len(keys) == 1:
		if val != None:
			ddict[key] = val
		return ddict[key]
	try:
		return deepdictvalue('.'.join(keys[1:]), ddict[keys[0]], val)
	except KeyError as e:
		dbgprint(4, "deepdictvalue error: key '%s' dict keys: '%s'" % (keys[0], ddict.keys()))
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
	# 'filter': {'field1': [['>',99],['re','(.*)']], 'field2': 'Test(.*)' }
	for filter_name_key in filters:
		filter_key, use_key = determinekey(filter_name_key)
		filter_match = filters[filter_name_key]

		msg_val = deepdictvalue(filter_key, msg)
		if msg_val == None:
			return None;
		if type(filter_match) == type([]):
			filter_match_list = filter_match		# shorthand syntax
		else:
			filter_match_list = [['re', filter_match]]
		match_result = None
		# [['>',99],['re','(.*)']]
		dbgprint(3,"filter_match_list: %s" % str(filter_match_list))
		for match_ops in filter_match_list:
			if type(match_ops) != type([]) or len(match_ops) != 2:
				raise SyntaxError ("match ops format "+filter_name_key+" "+str(match_ops))
			dbgprint(3, "filter_match_list %s, msg_val %s" % (match_ops, msg_val))
			# 'and' result of list ['>',99],['re','(.*)']
			match_type, match_val = match_ops
			dbgprint(3, "match_ops %s %s" % (match_type, match_val))
			if match_type == 're':
				try:
					r = re.match(str(match_val), str(msg_val))
				except Exception as e:
					raise SyntaxError ("re error %s pattern '%s' value '%s'" % (e, match_val, msg_val))

				dbgprint(3, "extractfromdict: %s %s: '%s' '%s' -> %s" % \
					 (name, filter_name_key, match_ops, str(msg_val),\
					  "not" if r == None else "Match"))
				if r:
					try:
						match_result = r.group(1)
					except:
						match_result = r.group(0)
					break
			elif match_type in ['==','<','<=','>','>=', '!=']:
				if str(match_val).replace('.','',1).isdigit():
					msgv = msg_val
					matchv = match_val
				else:
					msgv = "'%s'" % msg_val
					matchv = "'%s'" % match_val
				try:
					r = eval("%s %s %s" % (msgv, match_type, matchv))
				except:
					r = False
				dbgprint(3, "eval: %s %s %s --> %s" % (msgv, match_type, matchv, r))
				if not r:
					break   # 
				match_result = r
			else:
				raise KeyError("bad match op '%s' in ruleset '%s' filter '%s'" % \
					(name, match_type, filter_name_key))
 
			if match_result:	# list of 'or' conditions
				break

		if match_result:
			result_msg[use_key] = match_result
		else:
			dbgprint(3, "extractfromdict: fin None")
			raise KeyError(filter_name_key)

	dbgprint(3, "extractfromdict: fin %s" % result_msg)
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
				data = publish.get('data', new_record)
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
				pub_data = prepdata(str(data), new_record)
				self.publish_log(publish.get('logfile',''), pub_data)
		self.seen = True


	def publish_mqtt(self, topic, json_data, retain=False):
		if self.repub.testmode:
			log('test', "publish_mqtt %s %s" % (topic, json_data))
			return
		self.repub.mqttclient.publish(topic, json_data, retain=retain)
		

	def publish_log(self, fname, data):
		if self.repub.testmode:
			log('test', "publish_log (%s) %s" % (fname, data))
			return
		if fname:
			f = open(fname,"a+")
		else:
			f = sys.stdout
		print(data,file=f)
		if fname:
			f.close()


	def publish_restful(self, url, headers, data):
		if self.repub.testmode:
			log('test', "publish_restful (%s) %s" % (url, data))
			return
	
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
				log('error', "copy_fields error '%s' dst '%s' src '%s' type '%s' in '%s'" % \
					(e, dst, src, typ, str(srcdict)))
		return dstdict


class Republish:
	def __init__(self, rules, mqttclient, xlate, dbg):
		global DBG
		self.rulesets = {}
		DBG = dbg
		self.mqttclient = mqttclient
		self.xlate = xlate
		self.testmode = False

		if len(rules) == 0:
			dbgprint(1, "no rules added")
		else:
			for r in rules:
				rs = RuleSet(r, self)
				if rs.name in self.rulesets:
					log('error', "RuleSet %s already defined" % (rs.name))
					sys.exit(1)
				self.rulesets[rs.name] = rs
				dbgprint(1,"added rulesets %s" % rs.name)


	def settestmode(self, mode):
		self.testmode = mode


	def process_message(self, jrecord):
		dbgprint(1, "input %s" % jrecord)
		if not 'ts' in jrecord:
			time_stamp = time.time()
			ts=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time_stamp))
			jrecord['ts'] = ts
	
		for rule in self.rulesets:
			ruleset = self.rulesets[rule].ruleset
			for rfilter, rselector, rpublish in ruleset['rules']:
				try:
					filterrecord = extractfromdict(jrecord, ruleset[rfilter], 'filter '+ruleset['name'])
				except KeyError as e:
					dbgprint(1, "filter ruleset '%s' '%s': blocked! field '%s' not present" \
						% (ruleset['name'], rfilter, e))
					continue
				except ValueError as e:
					dbgprint(1, "filter ruleset '%s' '%s': blocked! field '%s' no value" \
						% (ruleset['name'], rfilter, e))
					continue
				except SyntaxError as e:
					log('error', "filter ruleset '%s' '%s': blocked! syntax eror: %s" \
						% (ruleset['name'], rfilter, e))
					continue
				if filterrecord == None:
					continue
				dbgprint(1, "filter ruleset '%s' '%s': passed!" % \
						 (ruleset['name'], rfilter))
				if not rselector:
					new_record = jrecord
				else:
					try:
						new_record = extractfromdict(jrecord, ruleset[rselector], 'selector '+ruleset['name'])
					except KeyError as e:
						log('error',"selector ruleset '%s', '%s' field %s not inecord '%s'" % (rule, rselector, e, str(jrecord)))
						continue
					except ValueError as e:
						log('error',"selector ruleset '%s', '%s' field %s  value mismatch  '%s'" % (rule, rselector, e, str(jrecord)))
						continue
					except SyntaxError as e:
						log('error', "selector ruleset '%s' '%s': syntax eror: %s" \
							% (ruleset['name'], rfilter, e))
						continue
					new_record['ts'] = jrecord['ts']
				if new_record:
					dbgprint(1, "selector ruleset '%s' '%s': selected: %s" % \
						 (ruleset['name'], rfilter, str(new_record)))
					if rpublish:
						self.rulesets[rule].publish(ruleset[rpublish], new_record)
