# logshuttle
Python 3+ log handler for sending log records to Google Cloud Stackdriver service as custom logs in batches.

A batched log handler that sends the log output to Google Cloud Logging service using
the Google cloud client library. When creating this handler, authentication for GCloud should
be handled using one of the non-explicit credentials sending methods described in 
http://gcloud-python.readthedocs.io/en/latest/gcloud-auth.html.

The handler stores upto batch_length (200 by default) log records or send_interval_in_ms (15 s by default) 
worth of log records before sending all those log records in a batch.

**Installation**

`pip install logshuttle`

**Usage**

*Sample - In Code*

```python
import logging
from logshuttle import GCloudBatchedLogHandler

logger = logging.getLogger()
logger.addHandler(GCloudBatchedLogHandler())
logger.setLevel(logging.INFO)
logger.info("Test log message to google cloud logging service")

```

*Sample - In Config*

```ini
[loggers]
keys=gunicorn.access

[handlers]
keys=gcloud

[formatters]
keys=generic

[logger_gunicorn.access]
level=INFO
handlers=gcloud
qualname=gunicorn.access

[handler_gcloud]
class=gcloud_batched_logger.GCloudBatchedLogHandler
level=INFO
formatter=generic
args=()

[formatter_generic]

```