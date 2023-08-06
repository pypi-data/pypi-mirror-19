# django_i18nize
Django i18nize extends the i18nize python client. This package contains template tag for rendering translation and management command for fetching translations.

## Links
* *Website:* http://www.i18nize.com
* *Python client*: https://github.com/iktw/i18nize
* *JavaScript client*: https://github.com/iktw/i18nize-javascript


## Installation
```pip install django_i18nize```


## Example configuration (settings.py)
```python
DJANGO_I18NIZE_CONFIG = {
    "project_id": "852c3729-6098-410e-ad9e-9783958bbc2d",
    "live": False,
    'destination_dir': os.path.realpath(os.path.join(REPO_DIR, 'staticfiles', 'locale'))
}
```

### Example 1: Template tag with simple translations (Uses the django language)
```html
<p>
    {% i18n_switch "hello" %}
</p>
```

### Example 2: Template tag example with custom language:
```html
<p>
    {% i18n_switch "hello" "sv" %}
</p>
```

### Example 3: Template tag example with values

#### Passed view context:
```python
	context = {
		'values': {
			'name': 'John Doe'
		}
	}

```

#### Your translation at www.i18nize.com:
`"Hello {{name}}!"`

#### Inside your django template:
```html
<p>
    {% i18n_switch "greet_person" "en" values %}
</p>
```

### Example 4: Usage within your python code
```python
from django_i18nize.utils import get_translation as _

# Simple translation (Uses the django language)
text = _('hello')

# Translation with custom language
text = _('hello', language='sv')

# Translation with custom values, remember that your key should be injected within your translation.
# For example, your translated key at www.i18nize.com should be "Hello {{name}}!"
text = _('greeting', values={"name": "John Doe"})

```