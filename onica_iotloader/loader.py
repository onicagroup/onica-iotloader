"""Manages the actual loading of messages"""

from __future__ import print_function
from multiprocessing import Process, Value

import time
import json
import os
import boto3

class Loader(object):
    """Manages the actual loading of messages"""

    def __init__(self, channel, template, count, concurrency):
        self.channel = channel
        with open(template) as f:
            self.template = compile(f.read(), "<template>", "exec", 0 , True)
        self.count = count
        self.concurrency = concurrency
        self.total_messages = Value('l', 0)
        self.total_bytes = Value('l', 0)
        self.go = Value('i', 0)

    def run(self):
        print("Starting")

        threads = []

        for x in range(0, self.concurrency):
            t = Process(target=self.worker)
            threads.append(t)
            t.start()
            if x > 0 and x % 100 == 0:
                print("%s threads started" % x)

        print("All threads started")

        start_time = time.time()
        self.go.value = 1

        while True in (t.is_alive() for t in threads):
            current_total_messages = self.total_messages.value
            current_total_bytes = self.total_bytes.value

            runtime = time.time() - start_time
            message_per_sec = int(current_total_messages / runtime)
            mb_per_sec = int(current_total_bytes/1024/1024 / runtime)
            print("Running (%s min): %s msgs (%s/sec) / %s mb (%s/sec) completed" % (
                int(runtime/60),
                current_total_messages,
                message_per_sec,
                current_total_bytes/1024/1024,
                mb_per_sec
            ))
            time.sleep(1)

        # We have to join all threads or we'll never exit
        for t in threads:
            t.join()

        print("All threads finished")
        print("Final: %s msgs / %s mb completed" % (
            self.total_messages.value,
            self.total_bytes.value/1024/1024,
        ))

    def worker(self):
        # We want to be sure each worker gets a unique iotanalytics client to avoid
        # any accidental socket sharing
        self.iotanalytics = boto3.client('iotanalytics')

        while not self.go.value:
            time.sleep(1)

        while True:
            (batch_messages, batch_bytes) = self.put_batch()

            self.incrementValue(self.total_bytes, batch_bytes)

            if self.incrementValue(self.total_messages, batch_messages) >= self.count:
                break

    def put_batch(self):
        batch_bytes = 0
        messages = []
        
        data = json.dumps(self.invoke_template())
        
        for i in range(0,10):    
            batch_bytes += len(data)

            messages.append({
                'messageId': str(i), 
                'payload': data
            })

        s = time.time()
        res = self.iotanalytics.batch_put_message(
            channelName = self.channel,
            messages = messages
        )
        d = time.time() - s

        # print("Put took %s secs" % d)

        if len(res['batchPutMessageErrorEntries']):
            print("Batch errors")
            print(res)

        return (len(messages),batch_bytes)
    
    def invoke_template(self):
        gl = {}
        exec(self.template, gl)
        return gl['message']

    def incrementValue(self, val, increment):
        with val.get_lock():
            val.value += increment

            return val.value
