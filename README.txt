# CMS MiniAOD subscription tools

# Setup
```
source /cvmfs/cms.cern.ch/cmsset_default.sh
source /cvmfs/cms.cern.ch/rucio/setup-py3.sh
voms-proxy-init -voms cms -rfc -valid 192:00
```

# Scripts
get-old-rules.py - extracts the rules from the legacy single catch-all
                   subscription, and separates them into old and new lists for
                   manual removal

