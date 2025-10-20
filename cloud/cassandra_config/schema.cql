CREATE KEYSPACE IF NOT EXISTS sdfbs WITH replication = {
  'class' : 'SimpleStrategy',
  'replication_factor' : 3
};

CREATE TABLE IF NOT EXISTS sdfbs.file_chunks (
  file_id uuid,
  chunk_id int,
  data blob,
  PRIMARY KEY (file_id, chunk_id)
);
