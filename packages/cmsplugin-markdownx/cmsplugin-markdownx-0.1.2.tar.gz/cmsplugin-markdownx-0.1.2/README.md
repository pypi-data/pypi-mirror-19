Shims the estimable [django-markdownx](https://github.com/adi-/django-markdownx) into the venerable [django-cms](https://github.com/divio/django-cms).
Provides a `Markdown` plugin for Django-cms which stores content in markdown but displays as HTML.
We consider it an advantage that the rendering is all done server-side, 
that ensures the editing preview looks
just like the final result in case we do preprocessing enhancements for the markdown dialect.


* [Quick Start](#quick-start)
* [Usage](#usage)
* [Customization](#customization)
* [Dependencies](#dependencies)
* [License](#license)
* [Changelog](#changelog)


# Quick Start

1. Install prerequisites, then `cmsmarkdown-markdownx` package (by hand, for now).

    ```bash
    pip install django-markdownx
    pip install django-cms

    cd <somewhere>
    git clone https://github.com/bobhy/cmsplugin-markdownx
    cd cmsplugin-markdownx
    python setup.py develop
    ```

1. Add `cmsplugin-markdownx` to your `INSTALLED_APPS`.

    ```python
    #settings.py
    INSTALLED_APPS = (
        ...
        'markdownx',
    )
    ```

1. Collect included templates and statics to your `STATIC_ROOT` folder.

    ```bash
    python manage.py collectstatic
    ```

# Usage

1. in CMS, edit a page with a placeholder.
1. Add a `Markdown` plugin
1. As you type, the preview window is updated (thank you @django-markdownx)

From the 'frontend' view, you can update the plugin content.

1. Be sure you're logged into CMS, with adequate privilees.
1. Browse to a page containing Markdown
1. Double-click on the section of the page containing the Markdown plugin.


# Customization

## Settings

Place settings in your `settings.py` to override default values:

```python
#settings.py

## for cmsplugin_markdownx (see https://github.com/adi-/django-markdownx#customization)

# Markdownify
MARKDOWNX_MARKDOWNIFY_FUNCTION = 'markdownx.utils.markdownify'

# Markdown extensions
MARKDOWNX_MARKDOWN_EXTENSIONS = [
    'markdown.extensions.extra',
    'markdown.extensions.codehilite',       ## wants Pygments
]

# specify the code highlighting stylesheet used by `markdown.extensions.codehilite`
CMSPLUGIN_MARKDOWNX_CODEHILITE_CSS = 'cmsplugin_markdownx/codehilite_colorful.css'
```

## Template Tags

If you want to design your own template to display rendered HTML from Markdown text, you need to do 2 things:

1. Include the CMSPLUGIN_MARKDOWNX_CODEHILITE_CSS stylesheet in the CSS section of the page header.
1. Run the markdown text from some instance of the Markdown plugin through the MARKDOWNX_MARKDOWNIFY_FUNCTION you configured for `django-markdownx'

In order to do any or all of the above, you must load the template tags first.

```html+django
{% load cmsplugin_markdownx %}
```

### Custom tag `{% get_settings _settingsVariable_ default=None %}`
This tag extracts the value of _settingsVariable_ from your site `settings.py`.  You can specify the default value to use if it is not defined.

This tag is not dependent on markdown processing, it can be used in other apps and projects.

### Filter `{{ ... |markdownify }}`
Converts the markdown text provided by its left-hand argument into HTML using `django-markdownx`'s `MARKDOWNX_MARKDOWNIFY_FUNCTION```

The HTML blob itself does not have a `<div`> wrapper, leaving you free to style one in the template.

### Example

```html_django
{% load static sekizai_tags cmsplugin_markdownx %}
{% get_setting "CMSPLUGIN_MARKDOWNX_CODEHILITE_CSS" as codehilite_css  %}
{% if codehilite_css %}
{% addtoblock "css" %}
<link rel="stylesheet" href="{% static codehilite_css %}"/>
{% endaddtoblock %}
{% endif %}

<div>{{ instance.markdown_text|markdownify }}</div>
```

# Dependencies

* Markdown
* Pillow
* Django
* jQuery


# License

cmsplugin-markdown is licensed under the MIT open source license. Read `LICENSE` file for details.

# Changelog

| version | date | notes |
| :---------: | :-------: | -------------------------- |
| 0.1 | Jan 29, 2017 | Initial release |



