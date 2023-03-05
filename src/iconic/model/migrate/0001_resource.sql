CREATE TABLE IF NOT EXISTS resource (
  resource_name      VARCHAR PRIMARY KEY,
  resource_url       VARCHAR,
  resource_password  VARCHAR
);

INSERT INTO resource (resource_name, resource_url, resource_password)
VALUES ('test_data.zip', 'https://github.com/theiconic/technical-challenges/raw/master/data/sample-data/test_data.zip', 'welcometotheiconic')
ON CONFLICT (resource_name) DO UPDATE
  SET resource_url = excluded.resource_url,
      resource_password = excluded.resource_password;
