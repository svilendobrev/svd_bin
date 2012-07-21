#!/usr/bin/env python
import json, sys
a = json.load( sys.stdin )
json.dump( a, sys.stdout, indent=4)
