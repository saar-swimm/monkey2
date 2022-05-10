---
title: "Server configuration"
date: 2021-11-26T12:00:19+02:00
draft: true
pre: '<i class="fas fa-cogs"></i> '
weight: 1
---

## Configuring the Island

The Island Server(C&C) is configured by creating a `server_config.json` file.

### Creating a configuration file

Here's an example `server_config.json` with all options specified:
```json
{
  "log_level": "DEBUG",
  "ssl_certificate": {
    "ssl_certificate_file": "<PATH_TO_CRT_FILE>",
    "ssl_certificate_key_file": "<PATH_TO_KEY_FILE>"
  },
  "mongodb": {
    "start_mongodb": true
  },
  "data_dir": "/monkey_island_data"
}
```

Only relevant options can be specified, for example:
```json
{
  "ssl_certificate": {
    "ssl_certificate_file": "<PATH_TO_CRT_FILE>",
    "ssl_certificate_key_file": "<PATH_TO_KEY_FILE>"
  }
}
```

### Configuration options

See setup instructions for your operating system to understand how to apply these.

 - `log_level` - can be set to `"DEBUG"`(verbose), `"INFO"`(less verbose) or `"ERROR"`(silent, except errors).
 - `ssl_certificate` - contains paths for files, required to run the Island server with custom certificate.
 - `data_dir` - path to a writeable directory where the Island will store the database and other files.
 - `mongodb` - options for MongoDB. Should not be changed unless you want to run your own instance of MongoDB.
