from django.template.defaulttags import register


# Custom template tag to fetch a key
# From dictionary
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
