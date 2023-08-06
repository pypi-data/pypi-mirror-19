devpi-auth-gitlab
=================

An authentication plugin for use with gitlab-ci, utilising the build in registry token authentication scheme.

Installation requires the gitlab-registry url to be provided on the devpi-server startup once the plugin has been pip installed.
This url can be found in the Registry page of your gitlab project on a line like ``docker login gitlab.spring.localnet:5004``

``devpi-server --host 0.0.0.0 --port 3141 --gitlab-registry-url gitlab.spring.localnet:5004``

Usage from a Gitlab CI script is as simple as:

- devpi use https://devpi.spring.localnet
- devpi login "gitlab-ci-token" --password "$CI_BUILD_TOKEN"

