[![Build Status](https://travis-ci.org/Glf9832/DemoLib.svg?branch=master)](https://travis-ci.org/Glf9832/DemoLib)

# DemoLib  
A python demo library at any time  

## Environmental variable
```
DEMOLIB_HOME
DEMOLIB_PYENV
```

## Run Demo

### CeleryDemo

To celerydemo dir run.
``` bash
celery -B -A celery_app worker -l info
```

### FlaskDemo

To bin dir run.
``` bash
python webApi_manage.py -h 0.0.0.0 -p 8000
```

### NamekoDemo

To bin dir run.
``` bash
python taskService_run.py
```


## Integration Testing

### Test
``` bash
pytest -vv
```

### Integration
``` bash
tox
```
