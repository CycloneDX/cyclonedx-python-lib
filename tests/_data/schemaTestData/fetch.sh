#!/usr/bin/env bash
set -eux

SOURCE_PACKAGE='https://github.com/CycloneDX/specification/archive/refs/heads/master.zip'
SOURCE_DIR='specification-master/tools/src/test/resources'

THIS_DIR="$(dirname "$0")"
TEMP_DIR="$(mktemp -d)"
LOCAL_PACKAGE="$TEMP_DIR/source_package.zip"

wget -O "$LOCAL_PACKAGE" "$SOURCE_PACKAGE"
for SCHEMA_VERSION in '1.6' '1.5' '1.4' '1.3' '1.2' '1.1' '1.0'
do
  unzip -d "$TEMP_DIR" "$LOCAL_PACKAGE" "$SOURCE_DIR/$SCHEMA_VERSION/*"
  rm -rf "${THIS_DIR:?}/$SCHEMA_VERSION"
  mkdir -p "$THIS_DIR/$SCHEMA_VERSION"
  cp -rf "$TEMP_DIR/$SOURCE_DIR/$SCHEMA_VERSION/"*.xml "$THIS_DIR/$SCHEMA_VERSION/"
  cp -rf "$TEMP_DIR/$SOURCE_DIR/$SCHEMA_VERSION/"*.json "$THIS_DIR/$SCHEMA_VERSION/" || true
done

rm -rf "${TEMP_DIR:?}"
