import logging
import collections
from queue import Queue, Empty
from threading import Thread, Event
from google.cloud import logging as glogging

class GCloudBatchedLogHandler(logging.Handler):
    """
        A batched log handler that sends the log output to Google Cloud Logging service using
        the Google cloud client library. When creating this handler, authentication for GCloud should
        be handled using one of the non-explicit credentials sending methods described in 
        http://gcloud-python.readthedocs.io/en/latest/gcloud-auth.html.

        The handler stores upto batch_length (200 by default) log records or send_interval_in_ms (15 s by default) 
        worth of log records before sending all those log records in a batch.
    """

    def __init__(self, log_name=None, send_interval_in_ms=15000, batch_length=200, *args, **kwargs):
        """
            Create a new GCloudBatchedLogHandler instance. 

            :param log_name: Name of the log. Used as the log name in the gcloud client
            :type log_name: String

            :param send_interval_in_ms: 
                Time (in milliseconds) to wait before sending the logs. The logs
                are sent either when this timeout is reached or when the **batch_length**
                logs are added. **15000** by default.
            :type send_interval_in_ms: Integer

            :param batch_length:
                Number of log items before sending the logs. **200** by default.
            :type batch_length: Integer
        """
        super(GCloudBatchedLogHandler, self).__init__(*args, **kwargs)
        
        self.send_interval_in_ms = send_interval_in_ms
        self.batch_length = batch_length
        self.log_name = log_name
        self.gcloud_logclient = glogging.Client()
        self.logger = logging.getLogger("GCloudBatchedLogHandler")
        
        # dictionaries to store the queues used as buffers and events used as signals for each log_name
        self.queues = {}
        self.events = {}

    def _send_batch(self, log_name, queue, send_interval_in_ms, gcloud_logger, event):
        """
            Method used by the threads. Keeps looping until the process is killed.
            In each loop, it sends all existing log records and waits for the timeout
            to expire or waits till a signal is sent to start processing (the signal is
            set when the count exceeds the batch_length member)
        """
        while True:
            log_records = []
            while True:
                try:
                    log_record = queue.get(block=False)
                    log_records.append(log_record)
                except Empty:
                    break
            
            if len(log_records) > 0:
                self.logger.debug("Collected {} log records".format(len(log_records)))
                batch = gcloud_logger.batch()

                for log_record in log_records:
                    info = { "message" : self.format(log_record), "python_logger": log_record.name }
                    batch.log_struct(info, severity=log_record.levelname)
                
                batch.commit()
                self.logger.debug("committed {} log records".format(len(log_records)))
            
            event.wait(send_interval_in_ms/1000)
            self.logger.debug("Event set or timeout expired")

    def emit(self, log_record):
        log_name = self.log_name or log_record.name or ''

        # Create the Queue and Event objects for the log_name if they
        # don't exist already and start a new thread
        if not log_name in self.queues:
            self.queues[log_name] = Queue(0)
            self.events[log_name] = Event()
            t = Thread(target=self._send_batch, args=(log_name, self.queues[log_name], self.send_interval_in_ms, self.gcloud_logclient.logger(log_name), self.events[log_name]))
            t.daemon = True
            t.start()
        
        # Add the log_record to the queue
        target_queue = self.queues[log_name]
        target_queue.put(log_record)

        # If the queue size exceeds the batch_length, signal the waiting
        # thread to start sending the log records
        if target_queue.qsize() >= self.batch_length:
            self.logger.debug("Setting the event for {} at queue size {}".format(log_name, target_queue.qsize()))
            self.events[log_name].set()