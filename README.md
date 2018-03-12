# versionist
When target strings are specified, this module detects virsion information from the list.
Then it gives latest version number, version name, next version number, and etc.

## Install

* Locate versionist any directory
* Set PYTHONPATH to the directory

## Requirement

* Python 2

## Example
* Get latest version name from the list ["dog_v001", "dog_v002", "dog_v003"]
```python
from versionist import Versionist

pat = "^dog\_<version>$"
targets = ["dog_v001", "dog_v002", "dog_v003"]
vernist = Versionist(targets, pat)
print vernist.get_latest_version_name()
# >> v003
```
---

## Class