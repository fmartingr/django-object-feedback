django-object-feedback
======================

A simple django app to allow feedback on model instances.

NOTE: ** Still work in progress **

## Requirements

django >= 1.5

## Installation

Install the package:

```
pip install django-object-feedback
```

Add it to `INSTALLED_APPS`
```
INSTALLED_APPS = (
	# ...
    'object_feedback',
    # ...
)
```

Configure your `urls.py`

```
urlpatterns = patterns(
    '',
    # ...
    url(r'^feedback/',
        include('object_feedback.urls', namespace="object_feedback")),
    # ...
)
```

## Usage

### Add the `ObjectFeedbackMixin` to the models you need to receive feedback from

```
from django.db import models
from object_feedback.mixins import ObjectFeedbackMixin


class Series(ObjectFeedbackMixin, models.Model):
	# model fields and stuff...
    feedback_fields = ('name', 'summary', )
	# model methods and overrides and stuff...
```

### Using django-object-feedback default views

Calling for `model.get_feedback_url()` will return the base URL for the feedback form that can be embeded into a site via `iframe` for an user to send modifications for a certain model within the page.

## Customize

### Templates

TODO

### Adding your own view to receive feedback

TODO

## API

### `ObjectFeedbackMixin`

##### Methods
`get_feedback_url()`
`add_feedback(author, comment, fields)`
##### Attributes
`pending_review`

## License

See LICENSE file