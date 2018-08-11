class DictValidator(object):
    """Class for validating a dictionary object"""

    def __init__(self):
        self.schema = None if not hasattr(self, 'schema') else self.schema
        self.errors = []
        self.is_valid = None


    # Summon json data from request body
    def load(self, data=None):
        """ Dictionary object setter

            :param data: a dictionary
        """
        self.data = data


    def set_schema(self, schema):
        """ Validation schema setter

            :param schema: Validation schema
            """
        self.schema = schema


    def validate(self, data=None):
        """ Validates given object against the given schema"""
        is_valid     = True
        errors         = {}

        if data is None:
            data = self.data

        if data is None:
            raise RuntimeError('Missing data for validation.')
        if self.schema is None:
            raise RuntimeError('Missing schema for validation.')

        for key, field in self.schema.items():
            field_name    = field['name'] if field.get('name') is not None else key.capitalize()
            value         = data.get(key)

            # Validate required
            if key not in data and field.get('required', False):
                is_valid = False
                errors[key] = field_name + ' is required.'
                continue

            # Validate not empty
            if key in data and (value == '' or value is None) and field.get('not_empty', False):
                is_valid = False
                errors[key] = field_name + ' must not be empty.'
                continue

            # Field is not required and can be empty. Continue if it IS empty.
            elif (value == '' or value is None) and not field.get('not_empty', False):
                continue

            # Validate type
            if field.get('type') is not None and not isinstance(value, field['type']):
                is_valid = False
                errors[key] = field_name + ': unexpected type.'
                continue

            # Validate against regex
            # TODO: validate type 'str' first
            regex = field.get('regex')
            if hasattr(value, "decode") and regex is not None:
                if regex.match(value) is None:
                    is_valid = False
                    errors[key] = 'Entered invalid ' + field_name + '.' if field.get('error_msg') is None else field['error_msg']

            # Run custom validators
            for validator in field.get('validators', []):
                if not validator(value, self.data):

                    # Default error
                    error = 'Entered invalid ' + field_name + '.' if field.get('error_msg') is None else field['error_msg']
                    # Set error from validator's attribute if available
                    if str(type(validator)) != "<type 'function'>" \
                        and str(type(validator)) != "<class 'function'>" \
                        and validator.error is not None:
                        error = validator.error

                    is_valid = False
                    errors[key] = error

        # Search for undescribed fields - we don't trust requests with unexpected data
        for key in data.keys():
            if key not in self.schema:
                is_valid = False
                errors[key] = 'Unexpected field.'

        self.is_valid = is_valid
        self.errors = errors
        return is_valid
