PYTEST_FLAGS = -vv
PYDEPS_COMMON = \
	'coveralls >= 4.1.0' \
	'freezegun >= 1.5.5' \
	'pytest >= 7.4.4, < 8' \
	'bddrest >= 6.3.3, < 7' \
	'bddcli >= 2.10.1, < 3' \
	'pytest-fixkit >= 1.0.3' \
	'pytest-mock'



# Assert the python-makelib version
PYTHON_MAKELIB_VERSION_REQUIRED = 4


# Ensure the python-makelib is installed
PYTHON_MAKELIB_PATH = /usr/local/lib/python-makelib
ifeq ("", "$(wildcard $(PYTHON_MAKELIB_PATH))")
  MAKELIB_URL = https://github.com/pylover/python-makelib
  $(error python-makelib is not installed. see "$(MAKELIB_URL)")
endif


# Include a proper bundle rules file.
include $(PYTHON_MAKELIB_PATH)/venv-lint-test-doc-pypi.mk
