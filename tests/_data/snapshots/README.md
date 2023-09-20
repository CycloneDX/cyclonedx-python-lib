# SNAPSHOTS

## RE-CREATION

Some assets here can be (re-)created automatically, by setting the env var `CDX_TEST_RECREATE_SNAPSHOTS=1`.  
Every value different from `1` is treated as "do not touch the snapshots".
 
As a shortcut just run:

```shell
CDX_TEST_RECREATE_SNAPSHOTS=1 poetry run tox -e py
```

The files will be written as is, which might not be human-readable. feel free to reformat the files manually.
