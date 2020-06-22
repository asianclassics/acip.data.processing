import json


def replace_in_dict(template, canvas_items, this_key=None):
    result = {}
    for key, value in template.items():
        if isinstance(value, dict):
            result[key] = replace_in_dict(value, canvas_items)
        elif isinstance(value, list):
            new_list = []
            for item in value:
                d = replace_in_dict(item, canvas_items)
                new_list.append(d)
            result[key] = new_list
        elif isinstance(value, int):
            if key in ['width', 'height'] and key in canvas_items:
                result[key] = canvas_items[key]
            else:
                print('found an int value not in width or height')
        else:
            result[key] = value % canvas_items
    return result


test_dict = {
    "@type": "sc:Canvas",
    "@id": "%(host)s/%(name)s/canvas/1",
    "label": "1",
    "width": 1,
    "height": 1,
    "images": [
      {
        "@type": "oa:Annotation",
        "motivation": "sc:painting",
        "on": "http://iiif.asianclassics.org/%(name)s/canvas/1",
        "resource": {
          "@type": "dctypes:Image",
          "@id": "http://157.245.187.36:8182/iiif/2/%(image)s/full/500,/0/default.%(ext)s",

          "service": {
            "@context": "http://iiif.io/api/image/2/context.json",
            "@id": "http://157.245.187.36:8182/iiif/2/001__dul_ba_ka001.%(ext)s",
            "profile": "http://iiif.io/api/image/2/level2.json"
          }
        }
      }
    ]
  }

variables = {
    "replace_this": "http://iiif.asianclassics.org",
    "also_replace_this": "this is another value",
    "and_this": "also this",
    "this_is_not_replaced": "im not here",
    "host": "http://localhost",
    "name": "Biggie",
    "image": "some_name_of_image",
    "ext": "jpg",
    "width": 2319,
    "height": 389
}

# print(replace_in_dict(test_dict, variables))
print(json.dumps(replace_in_dict(test_dict, variables), indent=4))  # sort_keys=True
