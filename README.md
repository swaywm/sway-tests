# sway-tests

Unofficial test suite for sway.

## About

The test suite starts a new sway instance in headless mode for each test. Add your tests to the `test` directory. Use the `sway` pytest fixture to get the test environment including a connection to the ipc.

## Running

The recommended way to run the sway test suite is to clone the repository and run the tests in a virtualenv for python3.

```
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

Now run the test suite like this:

```
env/bin/pytest --sway=/path/to/sway
```

The tests should work fine with i3 too:

```
env/bin/pytest --sway=$(which i3)
```

## Example Test

```python
def test_ipc_version(sway):
    version = sway.ipc.get_version()
    assert version.variant
    assert version.human_readable
    assert version.major >= 0
    assert version.minor >= 0
    assert version.patch >= 0
```

## License

Copyright 2018 Sway Contributors

MIT (see LICENSE)
