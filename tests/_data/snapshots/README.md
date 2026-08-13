# Test fixtures

## Model fixtures

Serialization and deserialization tests share BOM factories from
[`tests/_data/models.py`](../models.py). To cover a model change:

1. Add a descriptively named factory that starts with `get_bom_` and returns a
   `Bom`. The function is discovered automatically; its name also becomes the
   snapshot filename prefix.
2. Populate every field relevant to the change so the JSON and XML output
   tests exercise the complete model. Name a fixture ending in `_invalid` only
   when serialization is expected to fail.
3. Register a factory in `all_get_bom_funct_with_incomplete_deps` when its
   dependency graph is intentionally incomplete. Otherwise, include the
   complete dependency graph in the returned BOM.
4. Re-create the snapshots, review the changed files, then run the tests again
   without snapshot re-creation enabled.

The output tests serialize each discovered model for the applicable schema
versions, validate the generated JSON and XML, and compare it with the stored
snapshots. The deserialization tests also use these fixtures for round-trip
coverage.

## Re-creation

Some assets here can be (re-)created automatically, by setting the env var `CDX_TEST_RECREATE_SNAPSHOTS=1`.  
It might also help to set `PYTHONHASHSEED=0`!  
As a shortcut just run:

```shell
CDX_TEST_RECREATE_SNAPSHOTS=1 poetry run tox -e py
```

Only commit snapshots that belong to the model change. Snapshot tests compare
the serialized text with the stored fixture using exact string equality, so do
not reformat snapshots manually.
