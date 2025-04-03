# Resources: Schema files

some schema for offline use as download via [script](../../../tools/schema-downloader.py).
original sources: <https://github.com/CycloneDX/specification/tree/master/schema>

Currently using version
[8a27bfd1be5be0dcb2c208a34d2f4fa0b6d75bd7](https://github.com/CycloneDX/specification/commit/8a27bfd1be5be0dcb2c208a34d2f4fa0b6d75bd7)

| file | note |
|------|------|
| [`bom-1.0.SNAPSHOT.xsd`](bom-1.0.SNAPSHOT.xsd) | applied changes: 1 |
| [`bom-1.1.SNAPSHOT.xsd`](bom-1.1.SNAPSHOT.xsd) | applied changes: 1 |
| [`bom-1.2.SNAPSHOT.xsd`](bom-1.2.SNAPSHOT.xsd) | applied changes: 1 |
| [`bom-1.3.SNAPSHOT.xsd`](bom-1.3.SNAPSHOT.xsd) | applied changes: 1 |
| [`bom-1.4.SNAPSHOT.xsd`](bom-1.4.SNAPSHOT.xsd) | applied changes: 1 |
| [`bom-1.5.SNAPSHOT.xsd`](bom-1.5.SNAPSHOT.xsd) | applied changes: 1 |
| [`bom-1.6.SNAPSHOT.xsd`](bom-1.6.SNAPSHOT.xsd) | applied changes: 1 |
| [`bom-1.2.SNAPSHOT.schema.json`](bom-1.2.SNAPSHOT.schema.json) | applied changes: 2,3,4,5 |
| [`bom-1.3.SNAPSHOT.schema.json`](bom-1.3.SNAPSHOT.schema.json) | applied changes: 2,3,4,5 |
| [`bom-1.4.SNAPSHOT.schema.json`](bom-1.4.SNAPSHOT.schema.json) | applied changes: 2,3,4,5 |
| [`bom-1.5.SNAPSHOT.schema.json`](bom-1.5.SNAPSHOT.schema.json) | applied changes: 2,3,4,5 |
| [`bom-1.6.SNAPSHOT.schema.json`](bom-1.6.SNAPSHOT.schema.json) | applied changes: 2,3,4,5 |
| [`bom-1.2-strict.SNAPSHOT.schema.json`](bom-1.2-strict.SNAPSHOT.schema.json) | applied changes: 2,3,4,5 |
| [`bom-1.3-strict.SNAPSHOT.schema.json`](bom-1.3-strict.SNAPSHOT.schema.json) | applied changes: 2,3,4,5 |
| [`spdx.SNAPSHOT.xsd`](spdx.SNAPSHOT.xsd) | |
| [`spdx.SNAPSHOT.schema.json`](spdx.SNAPSHOT.schema.json) | |
| [`jsf-0.82.SNAPSHOT.schema.json`](jsf-0.82.SNAPSHOT.schema.json) | |

changes:
1. `https?://cyclonedx.org/schema/spdx` was replaced with `spdx.SNAPSHOT.xsd`
2. `spdx.schema.json` was replaced with `spdx.SNAPSHOT.schema.json`
3. `jsf-0.82.schema.json` was replaced with `jsf-0.82.SNAPSHOT.schema.json`
4. `properties.$schema.enum` was removed
5. `required.version` removed, as it is actually optional with default value
