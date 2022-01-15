from django import template

register = template.Library()

@register.simple_tag
def get_counter_padding(total_elements=10):
    """Adds padding for counter number displays"""
    digits_count = len(str(total_elements))
    if total_elements <= 10:
        padding_digit_count = digits_count
    else:
        padding_digit_count = digits_count - 1
    padding_string = ""
    for digit in range(padding_digit_count):
        padding_string = padding_string + "0"
    return padding_string