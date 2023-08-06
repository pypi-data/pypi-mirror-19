import datetime
import json
import re
import urllib.parse

from . import widgets
from .exceptions import ValidationError


__all__ = (
    'Field',
    'Boolean',
    'String',
    'Integer',
    'Float',
    'Choice',
    'Array',
    'MultipleChoice',
    'URL',
    'RegexMatch',
    'Host',
    'Slug',
    'Map',
    'JSON',
    'Date',
    'Time',
    'DateTime',
    'Method'
)


class Field(object):

    widget = None
    errors = {
        'required': 'Value is required',
        'invalid': 'Value is invalid',
        'unique': 'Value must be unique',
        'read_only': 'Read-only field'
    }

    def __init__(self, *, name=None, required=True, default=None, label=None,
                 unique=False, help_text=None, read_only=False,
                 validators=None, errors=None, widget=None):

        """
        :param required (optional): value is required flag.
        :type required: bool.
        :param default (optional): default value.
        :type default: type.
        :param validators (optional): additional validators.
        :type validators: iterable of callable.
        :param errors (optional): override default error messages.
        :type errors: dict.
        """
        self.name = name
        self.required = required
        self._default = default
        self._label = label
        self.unique = unique
        self.help_text = help_text
        self.read_only = read_only
        self.validators = validators or []
        self.widget = widget or self.widget

        if self._default is not None:
            self.required = False

        _errors = {}

        for cls in reversed(self.__class__.__mro__):
            _errors.update(getattr(cls, 'errors', {}))

        _errors.update(errors or {})

        self.errors = _errors

    @property
    def label(self):
        if self._label is None and self.name is not None:
            self._label = ' '.join(re.split(r'[\W_]', self.name)).capitalize()

        return self._label

    @property
    def default(self):
        if callable(self._default):
            return self._default()

        return self._default

    def bind(self, **kwargs):
        self.__dict__.update(kwargs)

    async def validate(self, value=None, model=None):
        if value is None:
            value = self.default

        if value is None:
            if self.required:
                self.fail('required')
            else:
                return None

        value = await self.deserialize(value)

        for validator in self.validators:
            value = await validator(value)

        if self.unique and hasattr(self, 'model'):
            try:
                instance = await self.model.objects.get(**{self.name: value})
            except self.model.DoesNotExist:
                instance = None

            if instance and model and instance._id != model._id:
                self.fail('unique')

        return value

    def fail(self, error, **kwargs):
        raise ValidationError(
            self.errors[error].format(self, **kwargs), self.name
        )

    async def deserialize(self, value):
        return value

    def serialize(self, value):
        return value

    async def to_db_value(self, value):
        return self.serialize(value)

    async def on_save(self, value):
        return value

    async def on_create(self, value):
        return value

    async def get_options(self):
        options = {
            'name': self.name,
            'label': self.label,
            'help_text': self.help_text,
            'required': self.required,
            'read_only': self.read_only,
            'default': None,
            'widget': None
        }

        if not (self._default is None or callable(self._default)):
            options['default'] = self.serialize(self._default)

        if self.widget:
            options['widget'] = self.widget.get_options()

        return options


class Type(Field):

    type = type
    widget = widgets.Input('text')
    errors = {
        'invalid': 'Value must be a valid {0.type.__name__}'
    }

    async def deserialize(self, value):
        if not isinstance(value, self.type):
            self.fail('invalid')

        return value


class Boolean(Type):

    type = bool
    widget = widgets.Input('checkbox')
    errors = {
        'invalid': 'Value must be a valid boolean'
    }


class String(Type):

    type = str
    errors = {
        'invalid': 'Value must be a valid string',
        'min_length': 'String must be greater {0.min_length} characters',
        'max_length': 'String must be less {0.max_length} characters'
    }

    def __init__(self, *, min_length=None, max_length=None, **kwargs):
        self.min_length = min_length
        self.max_length = max_length
        super().__init__(**kwargs)

    async def deserialize(self, value):
        value = await super().deserialize(value)

        if self.min_length is not None and len(value) < self.min_length:
            self.fail('min_length')

        if self.max_length is not None and len(value) > self.max_length:
            self.fail('max_length')

        return value


class Numeric(Type):

    errors = {
        'invalid': 'Value must be a valid integer or float',
        'min_value': 'Number must be greater {0.min_value} characters',
        'max_value': 'Number must be less {0.max_value} characters'
    }

    def __init__(self, *, min_value=None, max_value=None, **kwargs):
        self.min_value = min_value
        self.max_value = max_value
        super().__init__(**kwargs)

    async def deserialize(self, value):
        try:
            value = self.type(value)
        except (TypeError, ValueError):
            self.fail('invalid')

        if self.min_value is not None and value < self.min_value:
            self.fail('min_value')

        if self.max_value is not None and value > self.max_value:
            self.fail('max_value')

        return value


class Integer(Numeric):

    type = int
    errors = {
        'invalid': 'Value must be a valid integer',
    }


class Float(Numeric):

    type = float
    errors = {
        'invalid': 'Value must be a valid float',
    }


class Choice(Field):

    errors = {
        'invalid': 'Value must be in {choices}',
    }

    def __init__(self, *, choices, **kwargs):
        """Initialization instance.

        :param choices: choices.
        :type choices: iterable.
        """
        self.choices = list(choices)
        self.widget = widgets.Select(self.choices)
        super().__init__(**kwargs)

    async def deserialize(self, value):
        choices = [choice[0] for choice in self.choices]

        if value not in choices:
            self.fail('invalid', choices=choices)

        return value


class Array(Type):

    type = list
    widget = widgets.TextArea()
    errors = {
        'invalid': 'Value must be a valid array',
        'child': '{index}: {message}'
    }

    def __init__(self, *, field=None, **kwargs):
        self.field = field
        super().__init__(**kwargs)

    async def deserialize(self, value):
        value = await super().deserialize(value)

        if self.field:
            values = []

            for index, item in enumerate(value):
                try:
                    values.append(await self.field.deserialize(item))
                except ValidationError as e:
                    self.fail('child', index=index, message=e.error)

            return values

        return value

    def serialize(self, value):
        if self.field:
            values = []

            for item in value:
                values.append(self.field.serialize(item))

            return values

        return value


class MultipleChoice(Array, Choice):

    errors = {
        'choices': 'All values must be in {choices}',
    }

    def __init__(self, **kwargs):
        Choice.__init__(self, **kwargs)
        Array.__init__(self, **kwargs)

        self.widget.attributes['multiple'] = True

    async def deserialize(self, value):
        value = await Array.deserialize(self, value)

        choices = [choice[0] for choice in self.choices]

        if any(choice not in choices for choice in value):
            self.fail('choices', choices=choices)

        return value


class URL(String):

    errors = {
        'url': 'Value must be a valid URL',
    }

    async def deserialize(self, value):
        value = await super().deserialize(value)

        url = urllib.parse.urlparse(value)

        if not (url.scheme and url.netloc):
            self.fail('url')

        return value


class RegexMatch(String):

    errors = {
        'pattern': 'Value must match by {0.pattern}',
    }

    def __init__(self, *, pattern=None, **kwargs):
        self.pattern = re.compile(pattern or self.pattern)
        super().__init__(**kwargs)

    async def deserialize(self, value):
        value = await super().deserialize(value)

        if not self.pattern.match(value):
            self.fail('pattern')

        return value


class Host(RegexMatch):

    errors = {
        'pattern': 'Value must be a valid host',
    }
    pattern = (
        # domain
        r'(?:[\w](?:[\w-]{0,61}[\w])?\.)+'
        r'(?:[A-Za-z]{2,6}\.?|[\w-]{2,}\.?$)'
        # ipv4 address
        r'|^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
    )


class Slug(RegexMatch):

    errors = {
        'pattern': 'Value must be a valid slug',
    }
    pattern = r'^[a-zA-Z\d\-_]+$'


class Map(Field):

    widget = widgets.TextArea()
    errors = {
        'invalid': 'Value must be a map',
    }

    async def deserialize(self, value):
        if not isinstance(value, dict):
            self.fail('invalid')

        return value


class JSON(Field):

    widget = widgets.TextArea()
    errors = {
        'invalid': 'Value must be a valid JSON string',
    }

    async def deserialize(self, value):
        try:
            return json.loads(value)
        except (ValueError, TypeError):
            self.fail('invalid')


class DateTime(Field):

    widget = widgets.Input('datetime')
    errors = {
        'invalid': 'Datetime must be in next formats: {0.available_formats}'
    }

    default_format = '%Y-%m-%dT%H:%M:%S.%f'

    def __init__(self, *, input_formats=None, output_format=None,
                 auto_now=False, auto_now_on_create=False, **kwargs):

        super().__init__(**kwargs)
        self.input_formats = input_formats or []
        self.output_format = output_format
        self.auto_now = auto_now
        self.auto_now_on_create = auto_now_on_create

        if self.auto_now or self.auto_now_on_create:
            self.required = False

        self.widget.attributes['format'] = self.output_format

    @property
    def available_formats(self):
        return list(set(self.input_formats + [self.default_format]))

    async def on_save(self, value):
        if self.auto_now:
            return datetime.datetime.utcnow()

        return value

    async def on_create(self, value):
        if self.auto_now_on_create:
            return datetime.datetime.utcnow()

        return value

    async def deserialize(self, value):
        if isinstance(value, str):
            for input_format in self.available_formats:
                try:
                    value = datetime.datetime.strptime(value, input_format)
                    break
                except ValueError:
                    continue
            else:
                self.fail('invalid')
        elif not hasattr(value, 'strftime'):
            self.fail('invalid')

        return value

    def serialize(self, value):
        return value.isoformat()

    async def to_db_value(self, value):
        return value


class Date(DateTime):

    widget = widgets.Input('date')
    errors = {
        'invalid': 'Date must be in next formats: {0.available_formats}'
    }

    default_format = '%Y-%m-%d'

    async def deserialize(self, value):
        return (await super().deserialize(value)).date()


class Time(DateTime):

    widget = widgets.Input('time')
    errors = {
        'invalid': 'Time must be in next formats: {0.available_formats}'
    }

    default_format = '%H:%M:%S'

    async def deserialize(self, value):
        return (await super().deserialize(value)).time()


class Method(Field):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.read_only = True
        self.required = False
