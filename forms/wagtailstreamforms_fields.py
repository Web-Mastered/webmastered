import re
from django import forms
from django.forms import widgets
from wagtailstreamforms.fields import BaseField, register
from wagtail.core import blocks

class CustomSinglelineField(forms.CharField):
    def __init__(self,*args,**kwargs):
        self.width = kwargs.pop('width')
        self.placeholder = kwargs.pop('placeholder')
        self.widget = forms.widgets.TextInput(attrs={'col_width': self.width, 'placeholder': self.placeholder})
        super().__init__(*args,**kwargs)

class CustomMultilineField(forms.CharField):
    def __init__(self,*args,**kwargs):
        self.width = kwargs.pop('width')
        self.rows = kwargs.pop('rows')
        self.placeholder = kwargs.pop('placeholder')
        self.widget = forms.widgets.Textarea(attrs={'col_width': self.width, 'rows': self.rows, 'placeholder': self.placeholder})
        super().__init__(*args,**kwargs)

class CustomDateField(forms.DateField):
    def __init__(self,*args,**kwargs):
        self.width = kwargs.pop('width')
        self.widget = forms.widgets.DateInput(attrs={'col_width': self.width})
        super().__init__(*args,**kwargs)

class CustomDatetimeField(forms.DateField):
    def __init__(self,*args,**kwargs):
        self.width = kwargs.pop('width')
        self.widget = forms.widgets.DateTimeInput(attrs={'col_width': self.width})
        super().__init__(*args,**kwargs)

class CustomEmailField(forms.EmailField):
    def __init__(self,*args,**kwargs):
        self.width = kwargs.pop('width')
        self.placeholder = kwargs.pop('placeholder')
        self.widget = forms.widgets.EmailInput(attrs={'col_width': self.width, 'placeholder': self.placeholder})
        super().__init__(*args,**kwargs)

class CustomURLField(forms.URLField):
    def __init__(self,*args,**kwargs):
        self.width = kwargs.pop('width')
        self.placeholder = kwargs.pop('placeholder')
        self.widget = forms.widgets.URLInput(attrs={'col_width': self.width, 'placeholder': self.placeholder})
        super().__init__(*args,**kwargs)

class CustomNumberField(forms.DecimalField):
    def __init__(self,*args,**kwargs):
        self.width = kwargs.pop('width')
        self.placeholder = kwargs.pop('placeholder')
        self.widget = forms.widgets.URLInput(attrs={'col_width': self.width, 'placeholder': self.placeholder})
        super().__init__(*args,**kwargs)

class CustomDropdownField(forms.ChoiceField):
    def __init__(self,*args,**kwargs):
        self.width = kwargs.pop('width')
        self.widget = forms.widgets.Select(attrs={'col_width': self.width})
        super().__init__(*args,**kwargs)

class CustomRadioField(forms.ChoiceField):
    def __init__(self,*args,**kwargs):
        self.width = kwargs.pop('width')
        self.widget = forms.widgets.RadioSelect(attrs={'col_width': self.width})
        super().__init__(*args,**kwargs)

class CustomCheckboxesField(forms.MultipleChoiceField):
    def __init__(self,*args,**kwargs):
        self.width = kwargs.pop('width')
        self.widget = forms.widgets.SelectMultiple(attrs={'col_width': self.width})
        super().__init__(*args,**kwargs)

class CustomCheckboxField(forms.BooleanField):
    def __init__(self,*args,**kwargs):
        self.width = kwargs.pop('width')
        self.widget = forms.widgets.CheckboxInput(attrs={'col_width': self.width})
        super().__init__(*args,**kwargs)

class CustomSinglefileField(forms.FileField):
    def __init__(self,*args,**kwargs):
        self.width = kwargs.pop('width')
        self.widget = forms.widgets.ClearableFileInput(attrs={'col_width': self.width})
        super().__init__(*args,**kwargs)

class CustomMultifileField(forms.FileField):
    def __init__(self,*args,**kwargs):
        self.width = kwargs.pop('width')
        self.widget = forms.widgets.ClearableFileInput(attrs={'col_width': self.width,"multiple": True})
        super().__init__(*args,**kwargs)


@register('singleline')
class Column_SingleLineTextField(BaseField):
    field_class = CustomSinglelineField

    def get_options(self, block_value):
        options = super().get_options(block_value)
        options.update({'placeholder': block_value.get('placeholder')})
        options.update({'width': block_value.get('width')})
        return options

    def get_form_block(self):
        return blocks.StructBlock([
            ('label', blocks.CharBlock()),
            ('help_text', blocks.CharBlock(required=False)),
            ('required', blocks.BooleanBlock(required=False)),
            ('default_value', blocks.CharBlock(required=False)),
            ('placeholder', blocks.CharBlock(required=False)),
            ('width', blocks.IntegerBlock(help_text="Width of field, 1 to 12, 12 is full width.", max_value=12, min_value=1, default=12, required=True)),
        ], icon=self.icon, label=self.label)

@register('multiline')
class MultiLineTextField(BaseField):
    field_class = CustomMultilineField

    def get_options(self, block_value):
        options = super().get_options(block_value)
        options.update({'width': block_value.get('width')})
        options.update({'rows': block_value.get('rows')})
        options.update({'placeholder': block_value.get('placeholder')})
        return options

    def get_form_block(self):
        return blocks.StructBlock([
            ('label', blocks.CharBlock()),
            ('help_text', blocks.CharBlock(required=False)),
            ('required', blocks.BooleanBlock(required=False)),
            ('default_value', blocks.CharBlock(required=False)),
            ('placeholder', blocks.CharBlock(required=False)),
            ('width', blocks.IntegerBlock(help_text="Width of field, 1 to 12, 12 is full width.", max_value=12, min_value=1, default=12, required=True)),
            ('rows', blocks.IntegerBlock(help_text="Height of field", max_value=100, min_value=1, default=10, required=True)),
        ], icon=self.icon, label=self.label)

@register('date')
class DateField(BaseField):
    field_class = CustomDateField

    def get_options(self, block_value):
        options = super().get_options(block_value)
        options.update({'width': block_value.get('width')})
        return options

    def get_form_block(self):
        return blocks.StructBlock([
            ('label', blocks.CharBlock()),
            ('help_text', blocks.CharBlock(required=False)),
            ('required', blocks.BooleanBlock(required=False)),
            ('default_value', blocks.CharBlock(required=False)),
            ('width', blocks.IntegerBlock(help_text="Width of field, 1 to 12, 12 is full width.", max_value=12, min_value=1, default=12, required=True)),
        ], icon=self.icon, label=self.label)

@register('datetime')
class DateTimeField(BaseField):
    field_class = CustomDatetimeField

    def get_options(self, block_value):
        options = super().get_options(block_value)
        options.update({'width': block_value.get('width')})
        return options

    def get_form_block(self):
        return blocks.StructBlock([
            ('label', blocks.CharBlock()),
            ('help_text', blocks.CharBlock(required=False)),
            ('required', blocks.BooleanBlock(required=False)),
            ('default_value', blocks.CharBlock(required=False)),
            ('width', blocks.IntegerBlock(help_text="Width of field, 1 to 12, 12 is full width.", max_value=12, min_value=1, default=12, required=True)),
        ], icon=self.icon, label=self.label)

@register('email')
class EmailField(BaseField):
    field_class = CustomEmailField

    def get_options(self, block_value):
        options = super().get_options(block_value)
        options.update({'width': block_value.get('width')})
        options.update({'placeholder': block_value.get('placeholder')})
        return options

    def get_form_block(self):
        return blocks.StructBlock([
            ('label', blocks.CharBlock()),
            ('help_text', blocks.CharBlock(required=False)),
            ('required', blocks.BooleanBlock(required=False)),
            ('default_value', blocks.CharBlock(required=False)),
            ('placeholder', blocks.CharBlock(required=False)),
            ('width', blocks.IntegerBlock(help_text="Width of field, 1 to 12, 12 is full width.", max_value=12, min_value=1, default=12, required=True)),
        ], icon=self.icon, label=self.label)

@register('url')
class URLField(BaseField):
    field_class = CustomURLField

    def get_options(self, block_value):
        options = super().get_options(block_value)
        options.update({'width': block_value.get('width')})
        options.update({'placeholder': block_value.get('placeholder')})
        return options

    def get_form_block(self):
        return blocks.StructBlock([
            ('label', blocks.CharBlock()),
            ('help_text', blocks.CharBlock(required=False)),
            ('required', blocks.BooleanBlock(required=False)),
            ('default_value', blocks.CharBlock(required=False)),
            ('placeholder', blocks.CharBlock(required=False)),
            ('width', blocks.IntegerBlock(help_text="Width of field, 1 to 12, 12 is full width.", max_value=12, min_value=1, default=12, required=True)),
        ], icon=self.icon, label=self.label)

@register('number')
class NumberField(BaseField):
    field_class = forms.DecimalField

    def get_options(self, block_value):
        options = super().get_options(block_value)
        options.update({'width': block_value.get('width')})
        options.update({'placeholder': block_value.get('placeholder')})
        return options

    def get_form_block(self):
        return blocks.StructBlock([
            ('label', blocks.CharBlock()),
            ('help_text', blocks.CharBlock(required=False)),
            ('required', blocks.BooleanBlock(required=False)),
            ('default_value', blocks.CharBlock(required=False)),
            ('placeholder', blocks.CharBlock(required=False)),
            ('width', blocks.IntegerBlock(help_text="Width of field, 1 to 12, 12 is full width.", max_value=12, min_value=1, default=12, required=True)),
        ], icon=self.icon, label=self.label)

@register('dropdown')
class DropdownField(BaseField):
    field_class = CustomDropdownField

    def get_options(self, block_value):
        options = super().get_options(block_value)
        options.update({'width': block_value.get('width')})
        return options

    def get_form_block(self):
        return blocks.StructBlock(
            [
                ("label", blocks.CharBlock()),
                ("help_text", blocks.CharBlock(required=False)),
                ("required", blocks.BooleanBlock(required=False)),
                ("empty_label", blocks.CharBlock(required=False)),
                ("choices", blocks.ListBlock(blocks.CharBlock(label="Option"))),
                ('width', blocks.IntegerBlock(help_text="Width of field, 1 to 12, 12 is full width.", max_value=12, min_value=1, default=12, required=True)),
            ],
            icon=self.icon,
            label=self.label,
        )

@register('radio')
class RadioField(BaseField):
    field_class = CustomRadioField

    def get_options(self, block_value):
        options = super().get_options(block_value)
        options.update({'width': block_value.get('width')})
        return options

    def get_form_block(self):
        return blocks.StructBlock(
            [
                ("label", blocks.CharBlock()),
                ("help_text", blocks.CharBlock(required=False)),
                ("required", blocks.BooleanBlock(required=False)),
                ("choices", blocks.ListBlock(blocks.CharBlock(label="Option"))),
                ('width', blocks.IntegerBlock(help_text="Width of field, 1 to 12, 12 is full width.", max_value=12, min_value=1, default=12, required=True)),
            ],
            icon=self.icon,
            label=self.label,
        )

@register('checkboxes')
class CheckboxesField(BaseField):
    field_class = CustomCheckboxesField

    def get_options(self, block_value):
        options = super().get_options(block_value)
        options.update({'width': block_value.get('width')})
        return options

    def get_form_block(self):
        return blocks.StructBlock(
            [
                ("label", blocks.CharBlock()),
                ("help_text", blocks.CharBlock(required=False)),
                ("required", blocks.BooleanBlock(required=False)),
                ("choices", blocks.ListBlock(blocks.CharBlock(label="Option"))),
                ('width', blocks.IntegerBlock(help_text="Width of field, 1 to 12, 12 is full width.", max_value=12, min_value=1, default=12, required=True)),
            ],
            icon=self.icon,
            label=self.label,
        )

@register('checkbox')
class CheckboxField(BaseField):
    field_class = forms.BooleanField

    def get_options(self, block_value):
        options = super().get_options(block_value)
        options.update({'width': block_value.get('width')})
        return options

    def get_form_block(self):
        return blocks.StructBlock(
            [
                ("label", blocks.CharBlock()),
                ("help_text", blocks.CharBlock(required=False)),
                ("required", blocks.BooleanBlock(required=False)),
                ('width', blocks.IntegerBlock(help_text="Width of field, 1 to 12, 12 is full width.", max_value=12, min_value=1, default=12, required=True)),
            ],
            icon=self.icon,
            label=self.label,
        )

@register('singlefile')
class SingleFileField(BaseField):
    field_class = CustomSinglefileField

    def get_options(self, block_value):
        options = super().get_options(block_value)
        options.update({'width': block_value.get('width')})
        return options

    def get_form_block(self):
        return blocks.StructBlock(
            [
                ("label", blocks.CharBlock()),
                ("help_text", blocks.CharBlock(required=False)),
                ("required", blocks.BooleanBlock(required=False)),
                ('width', blocks.IntegerBlock(help_text="Width of field, 1 to 12, 12 is full width.", max_value=12, min_value=1, default=12, required=True)),
            ],
            icon=self.icon,
            label=self.label,
        )

@register('multifile')
class MultiFileField(BaseField):
    field_class = forms.FileField

    def get_form_block(self):
        return blocks.StructBlock(
            [
                ("label", blocks.CharBlock()),
                ("help_text", blocks.CharBlock(required=False)),
                ("required", blocks.BooleanBlock(required=False)),
                ('width', blocks.IntegerBlock(help_text="Width of field, 1 to 12, 12 is full width.", max_value=12, min_value=1, default=12, required=True)),
            ],
            icon=self.icon,
            label=self.label,
        )