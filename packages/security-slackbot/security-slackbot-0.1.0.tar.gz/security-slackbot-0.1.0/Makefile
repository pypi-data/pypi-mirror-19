help:
	@echo "clean - remove all build/python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"

clean: clean-build clean-pyc clean-debsrc

clean-build:
	find . -name 'htmlcov' -exec rm -fr {} +
	find . -name 'dist' -exec rm -fr {} +
	find . -name 'deb_dist' -exec rm -fr {} +
	find . -name 'build' -exec rm -fr {} +
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.tar.gz' -exec rm -fr {} +
	find . -name '*.xml' -exec rm -fr {} +
	find . -name '*.log' -exec rm -fr {} +
	find . -name '.tox' -exec rm -fr {} +
	find . -name '.coverage' -exec rm -fr {} +
	find . -name '.cache' -exec rm -fr {} +
	find . -name '__pycache__' -exec rm -fr {} +
	find . -name 'junit.xml' -exec rm -fr {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

clean-debsrc:
	find . -name '*.build' -exec rm -f {} +
	find . -name '*.changes' -exec rm -f {} +
	find . -name '*.dsc' -exec rm -f {} +
	find . -name '*.tar.xz' -exec rm -f {} +
	find . -name '*.deb' -exec rm -f {} +
	find . -name '*.pybuild' -exec rm -rf {} +
	find . -name '*.substvars' -exec rm -rf {} +
	find . -wholename '*/debian/changelog' -exec rm -rf {} +
	find . -wholename '*/debian/files' -exec rm -rf {} +

