#!/usr/bin/env python3

from dictvalidator import DictValidator

class SampleFieldValidator(object):

    def __init__(self):
        self.error = None

    def __call__(self, value, form_data):
        if value == 'test':
            self.error="Must not equal 'test'"
            return False
        elif value == 'test2':
            self.error="Must not equal 'test2'"
            return False
        return True

def sample_field_validator(value, form_data):
    return False

class SampleDictValidator(DictValidator):
    """docstring for LoginValidator."""

    schema = {
        'sample' : {
            'required' : True,
            'not_empty' : True,
            'validators': [
                SampleFieldValidator()
            ]
        },
        'sample2' : {
            'required' : True,
            'not_empty' : True,
            'validators': [
                SampleFieldValidator()
            ]
        },
        'sample3' : {
            'required' : True,
            'not_empty' : True,
            'validators': [
                sample_field_validator
            ]
        },
    }

if __name__ == '__main__':
    validator = SampleDictValidator()
    validator.load({
        'sample': 'test',
        'sample2': 'test2',
        'sample3': 'test3'
    })
    assert validator.validate() == False
    assert validator.errors['sample2'] == "Must not equal 'test2'"
    assert 'sample3' not in validator.errors
    print("ok")

