# coding: utf-8


class Field:
    def __init__(self, object, key, value):
        self.object = object
        self.key = key
        self.value = value

    @property
    def current_value(self):
        return getattr(self.object, self.key, None)

    @property
    def new_value(self):
        return self.value

    def has_changed(self):
        return self.current_value != self.value


class ForeignKey(Field):
    def from_native(self):
        return self.value.pk

    def to_native(self):
        return self.current_value.__class__.objects.get(pk=self.value)


class ManyToManyField(Field):
    def from_native(self):
        return self.value.values_list('id', flat=True)

    def to_native(self):
        return self.current_value.model.objects.filter(pk__in=self.value)


fields_map = dict(
    ForeignKey=ForeignKey,
    ManyToManyField=ManyToManyField,
    CharField=Field,
    DateField=Field,
    IntegerField=Field,
    PositiveIntegerField=Field,
    DecimalField=Field,
)
