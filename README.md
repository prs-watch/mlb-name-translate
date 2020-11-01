# MLB Name Translate

Translate MLB player's English name into Japanese name.

## Installation

```bash
$ pip install mlb-name-translate
```

## Usage

```python
import mlbname

mlbname.translate("Noah Syndergaard")
# -> ノア・シンダーガード

mlbname.translate("noah syndergaard")
# This tool is case insensitive.
# -> ノア・シンダーガード

mlbname.translate("Noah Syndergaard", True)
# If pass "True", name dictionary will be updated before translation.
# -> ノア・シンダーガード

mlbname.translate("Max Verlander")
# -> マックス・バーランダー

mlbname.translate("Max AAA")
# -> マックス・AAA

mlbname.translate("AAA BBB")
# -> AAA・BBB
```

## Changelogs

- 0.0.1
    - Pre-release.