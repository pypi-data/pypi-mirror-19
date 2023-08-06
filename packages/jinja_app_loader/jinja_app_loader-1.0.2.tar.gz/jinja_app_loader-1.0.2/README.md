jinja_app_loader
================
Jinja 2 loader for resource-based apps.

You can setup it like:
```python
    jinja_app.loader.Loader(
        root_dir='my_templates',
        app_subdir='app_temlates',
    )
```

And it will look for template `myapp/template.html` in the next order:

- `my_templates/myapp/template.html`
- path of `myapp` module + `app_templates/template.html`

Available params:

- `root_dir` - first source of templates, you can use it to rewrite
  apps-defined templates, default: `templates`
- `app_subdir` - templates folder inside apps (python modules or packages),
  default: `templates`
- `lstrip` - remove left whitespaces for each template string, default: `False` 
