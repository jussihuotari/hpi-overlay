Personal modules to use with https://github.com/karlicoss/HPI

HPI is a namespace package. We make this new namespace package and when it's
before the original in the path, these codes will override the originals.

For short intro to namespace packages, see https://github.com/karlicoss/HPI/blob/master/doc/MODULE_DESIGN.org

Background discussion regarding HPI extension: https://github.com/karlicoss/HPI/issues/102

Example overlay package: https://github.com/karlicoss/hpi-personal-overlay

A tool for reordering paths: https://github.com/seanbreckenridge/reorder_editable

## Dev

`mypy --namespace-packages .`


