msgen
========
Microsoft Genomics Command-line Client

Installation
------------
`msgen`_ is on PyPI and can be installed via:

Linux

::

  sudo apt-get install -y build-essential libssl-dev libffi-dev libpython-dev python-dev python-pip
  sudo pip install --upgrade --no-deps msgen
  sudo pip install msgen

Windows

::

  pip install --upgrade --no-deps msgen
  pip install msgen


msgen is compatible with Python 2.7. If you do not want to install msgen
as a system-wide binary and modify system-wide python packages, use the
``--user`` flag with ``pip``.

- Base Requirements

  - `azure-storage`_
  - `requests`_


You can install these packages using pip, easy_install or through standard
setup.py procedures. These dependencies will be automatically installed if
using a package-based install or setup.py. The required versions of these
dependent packages can be found in ``setup.py``.

.. _azure-storage: https://pypi.python.org/pypi/azure-storage
.. _requests: https://pypi.python.org/pypi/requests


Release Notes
-------------

1. Ability to specify SAS token duration for input blobs and an output container. The default token duration is 24 hours.
2. Ability to provide a short description for submitted workflows.
3. Minor fixes and improvements.

Usage
-------------

After installing msgen, a simple command to check connectivity is:

::

  msgen ^
    -api_url_base     https://malibutest0044.azure-api.net ^
    -subscription_key <MsGen_Subscription_Key>  ^
    -command          LIST

..

  Note: the ``^`` at the end of the lines above is a continuation character for this document and is not part of the command. On Linux, the continuation character is ``\``.

You can get a full list of available arguments by running ``msgen -h``, but generally you will need to provide
at least ``-api_url_base``, ``-subscription_key``, and ``-command``, where the value of ``-command`` is one of the following:

=========  =====
LIST       Returns a list of jobs you have submitted. Takes no arguments.
SUBMIT     Submits a workflow request to the service. Needs at least ``-process_name`` and storage-related arguments. ``-process_name`` identifies the specific processing workflow and version to run.  Use ``snapgatk`` to run the latest process. To lock on a specific processing package you can use the explicit name, e.g. ``snapgatk-20170124_4``.
GETSTATUS  Returns the status of the workflow specified by ``-workflow_id``.
CANCEL     Sends a request to cancel processing of the workflow specified by ``-workflow_id``.
=========  =====

So, here is what a command to submit two fastq.gz files for processing may look like:

::

  msgen ^
    -api_url_base     https://malibutest0044.azure-api.net ^
    -subscription_key <MsGen_Subscription_Key> ^
    -command          SUBMIT ^
    -process_name     snapgatk ^
    -process_args     R=grch37bwa ^
    -description      <short_description>
    -input_storage_account_type       AZURE_BLOCK_BLOB ^
    -input_storage_account_name       <your_sa_name_in> ^
    -input_storage_account_key        <your_sa_key_in> ^
    -input_storage_account_container  <your_sa_container_name> ^
    -input_blob_name_1                <your_blob_reads_1> ^
    -input_blob_name_2                <your_blob_reads_2> ^
    -output_storage_account_type      AZURE_BLOCK_BLOB ^
    -output_storage_account_name      <your_sa_name_out> ^
    -output_storage_account_key       <your_sa_key_in> ^
    -output_storage_account_container <your_results_container> ^
    -output_filename_base             <your_results_basename>
    -sas_duration                     <sas_token_duration_in_hours>

All of these arguments could be read from a configuration file which is included using the ``-f`` option:

::

  msgen -f sample.001.txt

An example sample.001.txt configuration file that matches the above submit command would look like:

::

  # Microsoft Genomics Service - Command Line Interface - Configuration File
  # Instructions
  # 1.  Entries are provided in key-value pairs, like key:value
  # 2.  Whitespace (tabs, spaces) don't matter
  # 3.  Lines starting with # are ignored
  
  api_url_base:    https://malibutest0044.azure-api.net
  subscription_key: <MsGen_Subscription_Key>
  command:          SUBMIT
  process_name:     snapgatk
  process_args:     R=grch37bwa
  description:      <short_description>
  sas_duration:     <sas_token_duration_in_hours>

  input_storage_account_type:       AZURE_BLOCK_BLOB
  input_storage_account_name:       <your_sa_name_in>
  input_storage_account_key:        <your_sa_key_in>
  input_storage_account_container:  <your_sa_container_name>
  input_blob_name_1:                <your_blob_reads_1>
  input_blob_name_2:                <your_blob_reads_2>
  
  output_storage_account_type:      AZURE_BLOCK_BLOB
  output_storage_account_name:      <your_sa_name_out>
  output_storage_account_key:       <your_sa_key_in>
  output_storage_account_container: <your_results_container>
  output_filename_base:             <your_results_basename>
  output_overwrite:                 False

When using the ``-f`` option, you may have arguments in the file, on the command line, or in both places.
Any arguments you have on the command line will override a value found in the configuration file.

::

  msgen -f sample.001.txt -output_overwrite true -sas_duration 48
