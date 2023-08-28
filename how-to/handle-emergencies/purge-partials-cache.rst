Purging the Partials Cache
==========================

Partials generation uses an S3 bucket as a cache, to avoid computing the
binary diffs of the same file once for each locale. However, if bad
partials are generated this cache can end up with invalid entries. Here
is how to remove the entire cache:

.. code:: sh

   taskcluster signin

And follow the usual environment variable process.

Set up the AWS temporary credentials, good for about an hour:

.. code:: sh

   AUTH=$(taskcluster api auth awsS3Credentials read-write tc-gp-private-1d-us-east-1 releng/mbsdiff-cache/)
   AWS_ACCESS_KEY_ID=$(echo "${AUTH}" | jq -r '.credentials.accessKeyId')
   AWS_SECRET_ACCESS_KEY=$(echo "${AUTH}" | jq -r '.credentials.secretAccessKey')
   AWS_SESSION_TOKEN=$(echo "${AUTH}" | jq -r '.credentials.sessionToken')
   export AWS_ACCESS_KEY_ID
   export AWS_SECRET_ACCESS_KEY
   export AWS_SESSION_TOKEN
   AUTH=

``aws`` cli commands should now authenticate.

.. code:: sh

   aws s3 ls s3://tc-gp-private-1d-us-east-1/releng/mbsdiff-cache/ --recursive

Remove the files:

.. code:: sh

   aws s3 rm s3://tc-gp-private-1d-us-east-1/releng/mbsdiff-cache/ --recursive
