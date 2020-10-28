# content of export_failures.py

import pytest
import os.path


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    mode = "a" if os.path.exists("failures") else "w"
    with open("failures", mode) as f:
        f.write(rep.longreprtext + "\n")