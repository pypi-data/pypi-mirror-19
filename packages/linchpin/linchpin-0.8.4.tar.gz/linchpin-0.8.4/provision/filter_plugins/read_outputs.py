#!/usr/bin/env python
import yaml
import json


def read_output(output):
    return output

class FilterModule(object):
    ''' A filter to fix output format '''
    def filters(self):
        return {
            'read_outputs': read_output
        }
