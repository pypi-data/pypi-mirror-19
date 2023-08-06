Allows to create multi-value attributes. Certainly not production-ready, but it
actually works quite fine.

The main purpose of this development is to create a good base for product 
catalog filters. Probably catalog filters will be a different addon, with 
`shuup-attrim` as a dependency.



# Example

Let's assume you have a `game` `ProductType`, and a product of this 
type - `the_witcher_product`, that you want to have a list of available 
subtitles translations, so on the product page it would look like:

```
Localization: english, polish, german
```

First you need to create a localization `Class`:

```python
from attrim.interface import attrim

localization_cls = attrim.cls.create(
    code='localization',
    name=dict(en='Localization', fi='Lokalisointi'),
    type=attrim.AttrimType.TRANS_STR,
    product_type=game,
    options=[
        {'order': 1, 'values': dict(en='english', fi='englanti')},
        {'order': 2, 'values': dict(en='polish',  fi='puola')},
        {'order': 3, 'values': dict(en='german',  fi='saksa')},
        {'order': 4, 'values': dict(en='italian', fi='italialainen')},
        {'order': 5, 'values': dict(en='french',  fi='ranskalainen')},
    ],
)
```

Next you need to create an `Attribute` for `the_witcher_product`, that will 
have `english`, `polish`, and `german` options from the parent Class 
`localization_cls`:

```python
attribute = the_witcher_product.attrims.create(
    cls=localization_cls,
    options=['english', 'polish', 'french'],
)
```

Alternatively you can use the option values from `fi` language, attrim will
catch it anyway:

```python
attribute = the_witcher_product.attrims.create(
    cls=localization_cls,
    options=['englanti', 'puola', 'ranskalainen'],
)
```

Now you only need to add to your jinja template output for the product
attributes:

```html
<ul>
{% for attribute in the_witcher_product.attrims.all() %}
    <li>
        {{ attribute.name }}: 
        {% for option in attribute.options %}
            {{ option }}
            {% if not loop.last %}, {% endif %}
        {% endfor %}
    </li>
{% endfor %}
</ul>
```

More comprehensive example you can find in [example test][test_url].



# GUI

Result of the example you can achieve with shuup admin GUI. It works fine, but
I'm afraid that is all what I can say about it. In the next few month I want 
to make it significant more friendly, but for now...

<a href="https://gitlab.com/nilit/shuup-attrim/raw/master/docs/edit_view.png">
    <img src="https://gitlab.com/nilit/shuup-attrim/raw/master/docs/edit_view.png" height="423px">
</a>
<a href="https://gitlab.com/nilit/shuup-attrim/raw/master/docs/product_view.png">
    <img src="https://gitlab.com/nilit/shuup-attrim/raw/master/docs/product_view.png" height="423px">
</a>



# Installation from the admin panel

You can download zip archive of the latest release from [gitlab][tags] and then
install it like a regular shuup addon from the admin panel.



# Documentation

I'm afraid this README - it is all that I can offer at the moment. I think
it is not enough, so I probably will write more docs in the next few month.



[test_url]: https://gitlab.com/nilit/shuup-attrim/blob/master/attrim/tests/test_example.py
[tags]: https://gitlab.com/nilit/shuup-attrim/tags