#!/usr/bin/env python3

import json
import os
import pickle
import pprint
import re
import sys
from rucio.client import Client
c = Client()
c.ping()

#ret = c.list_replication_rules({'rse_expression': 'ddm_quota>0&rse_type=DISK&country=US'})
#print("%s rules total" % len([x for x in ret]))


sub_acct = "transfer_ops"
sub_name = "USMiniAOD"
rules = []

debug = False
if debug:
    rules = pickle.load(open("dump.pickle", "rb"))
else:
    for rule in c.list_subscription_rules(sub_acct, sub_name):
        del rule['created_at']
        del rule['updated_at']
        rules.append(rule)
        if len(rules) % 1000 == 0:
            sys.stdout.write('.')
            sys.stdout.flush()
    pickle.dump(rules, open("dump.pickle", "wb"))

print("")
globs_to_keep = [
        "Run2016*21Feb2020*UL2016*",
        "Run2017*09Aug2019*UL2017*",
        "Run2018*12Nov2019*UL2018*",
        "RunIISummer20UL16MiniAODAPV(?:v2)?-106X*",
        "RunIISummer20UL16MiniAOD(?:v2)?-106X*",
        "RunIISummer20UL17MiniAOD(?:v2)?-106X*",
        "RunIISummer20UL18MiniAOD(?:v2)?-106X*",
        "Run2016*-17Jul2018*-v*",
        "Run2017*-31Mar2018*-v*",
        "Run2018*-17Sep2018*-v*",
        "Run2018D-PromptReco*-v*",
        "Run2018*-22Jan2019*-v*",
        "RunIISummer16MiniAODv3*",
        "RunIIFall17MiniAODv2*",
        "RunIIAutumn18MiniAOD*"]

regexes_to_keep = []
for g in globs_to_keep:
    regexes_to_keep.append(g.replace('*', r'[\w_-]*'))

regex = r"^/[\w_-]*/(?:" + "|".join(regexes_to_keep) + ")/MINIAOD"
regex = re.compile(regex)

current = []
old = []
for rule in rules:
    try:
        if regex.match(rule['name']):
            current.append(rule)
        else:
            old.append(rule)
    except KeyError as e:
        print("Failed to match rule: %s" % rule)
        raise e

with open('rules-to-delete.txt', 'w') as rfd, open('ids-to-delete.txt', 'w') as idfd:
    for x in old:
        rfd.write(x['name'] + " " + x['id'] + "\n")
        idfd.write(x['id'] + "\n")

with open('rules-to-keep.txt', 'w') as rfd, open('ids-to-keep.txt', 'w') as idfd:
    for x in current:
        rfd.write(x['name'] + " " + x['id'] + "\n")
        idfd.write(x['id'] + "\n")


print("%s current rules, %s old rules to be removed" % (len(current), len(old)))
