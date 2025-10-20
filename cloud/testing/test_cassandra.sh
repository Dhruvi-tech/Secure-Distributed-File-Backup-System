#!/bin/bash
echo 'Checking Cassandra nodes status...'
nodetool status

echo 'Running basic read/write test...'
cqlsh -e \"
INSERT INTO sdfbs.file_chunks (file_id, chunk_id, data) VALUES (uuid(), 1, 0x48656c6c6f);
SELECT * FROM sdfbs.file_chunks;
\"
