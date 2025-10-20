#!/usr/bin/env pwsh
echo 'Initializing Cassandra Keyspace and Table...'
cqlsh -f schema.cql
echo 'Cassandra setup complete.'
