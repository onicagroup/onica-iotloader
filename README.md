A tool to load bulk simulation data into AWS IoT Analytics for experimenting with the capabilities of AWS IoT Analytics. This tool is intended to load simulation data that can then be utilized to explore the capabilities of Datasets, integration with Amazon QuickSight, etc.

Installation:
=======
**Manual install**
- Make sure you have a working Python environment
- `pip install onica-iotloader` to get the latest version installed

**Automated install**
A cloudformation template `iotloader.yml` is provided to automate the deployment of an instance that is preconfigured to run onica-iotloader.  An existing ec2 keypair, and a source IP from which you will access the instance are required.  It will include a fresh copy of `template.py` from the repository in the home directory of ec2-user.  To access the instance:

```
ssh -i your.pem ec2-user@your_ec2_hostname.compute-1.amazonaws.com
```

Template
=======
A user-provided template is invoked to create each sample message. Arbitrary Python code can be used to generate each message via this template, enabling a rich set of simulated values. The template file must set a local variable named `message` to the value of a single simulated message, each time it is invoked. See `template.py` in this repository as an example of a static, but very large (~ 127kb) message template.

Usage
=======
`onica-iotloader [--concurrency=<n>] <channel> <template> <count>`

A concurrency value of 1000 seems to be ideal to maximize the ingest rate of AWS IoT Analytics from a single source (achieving approximately 3200 msgs/sec, or 400 mb/sec on an m5.24xlarge). The `<channel>` must be an existing AWS IoT Analytics channel, `<template>` is the template Pyton script described above, and `<count>` is the number of messages (within a margin of error) to transmit. For reference, a count of 900000 results in just over 100GB of ingest using the default `template.py` included herein.

To load about 100GB in 4 minutes, run the following command using the template.py included in this repository (tested on m5.24xlarge):

`onica-iotloader --concurrency=1000 <channel> template.py 900000`

Replace `<channel>` with the name of an AWS IoT Analytics Channel configured in your account.

AWS Credentials & Region
========
The default boto3 AWS credential & region resolution (env vars, EC2 metadata, config file, etc) is utilized.

Feedback
=======
Contact us at opensource at onica.com, or via Github issues, with feedback!
