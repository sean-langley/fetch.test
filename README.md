# Purpose of the exercise

**The following is a summary of the included PDF. It may include additional edits or information not contained with the original document**

Implement a program to check the health of a set of HTTP endpoints. A basic overview is given in this section. Additional details are provided in the Prompt section.

Read an input argument to a file path with a list of HTTP endpoints in YAML format. Test the health of the endpoints every 15 seconds. Keep track of the availability percentage of the HTTP domain names being monitored by the program. Log the cumulative availability percentage for each domain to the console after the completion of each 15-second test cycle.

**What this should do per the requirements**

The program must accept a single, required input argument to a configuration file path. A well-formed configuration file is a YAML list. Each entry in the YAML list follows a consistent schema, and contains enough information for the program to send a well-formed HTTP request.

You may assume that the contents of a configuration file given to your program are valid (you do not need to validate the schema of the configuration file).

An example of a valid YAML configuration file is included in the Sample input file section. While you may use this particular file for testing and validation purposes, your program must accept an arbitrary file path as its input.

Each HTTP endpoint element in the YAML list has the following schema:

 - name (string, required) — A free-text name to describe the HTTP endpoint.
 - url (string, required) — The URL of the HTTP endpoint.
 - method (string, optional) — The HTTP method of the endpoint.
 - headers (dictionary, optional) — The HTTP headers to include in the request.
 - body (string, optional) — The HTTP body to include in the request.
 
An example YAML was provided, but it does seem to make some an assumption that the input is actually an array. Additionally, the array does not seem to be properly formatted YAML. This has been corrected so we can correctly parse the file:

```
sites:
  - headers:
      - "User-Agent: fetch-synthetic-monitor"
    method: GET
    name: fetch index page
    url: https://fetch.com/

  - headers:
      - "User-Agent: fetch-synthetic-monitor"
    method: GET
    name: fetch careers page
    url: https://fetch.com/careers

  - body: '{"foo":"bar"}'
    headers:
      - "Content-Type: application/json"
      - "User-Agent: fetch-synthetic-monitor"
    method: POST
    name: fetch some fake post endpoint
    url: https://fetch.com/some/post/endpoint

  - name: fetch rewards index page
    url: https://www.fetchrewards.com/
```

If we are to assume this is NOT to be used as an array, the YAML must be formatted differently as the one provided in the example would not be considered valid.

**Running the health checks**

After parsing the YAML input configuration file, the program should send an HTTP request to each endpoint every 15 seconds. Each time an HTTP request is executed by the program, determine if the outcome is UP or DOWN:

 - UP — The HTTP response code is 2xx (any 200–299 response code) and the response latency is less than 500 ms.
 - DOWN — The endpoint is not UP.

Keep testing the endpoints every 15 seconds until the user manually exits the program, Logging the results.

Each time the program finishes testing all the endpoints in the configuration file, log the availability percentage of each URL domain over the lifetime of the program to the console.

Availability percentage is defined as:
*100 * (number of HTTP requests that had an outcome of UP / number of HTTP requests)*

The example YAML file in the Sample input file section contains two URL domains: fetch.com
and www.fetchrewards.com. Note that the number of domains present in a configuration file
can differ from the number of endpoints present in the file (two domains vs. four endpoints in
this particular file).

Here’s the complete expected output to the console of a sample execution of the program:

    fetch.com has 33% availability percentage
    www.fetchrewards.com has 100% availability percentage
    fetch.com has 67% availability percentage
    www.fetchrewards.com has 50% availability percentage

Further details can be found in the included PDF.

# Getting started

This guide makes some assumptions, mostly that the user is familar with command line environments (CLI). It also assumes that certain tools are available on their operating system of choice.

## Installing git

Please see https://github.com/git-guides/install-git for the process of installing git on your target system.

## Cloning this repository

Run the following to clone down the repository:

```
cd ~
git clone https://github.com/sean-langley/fetch.test.git
```

## Setting up pyenv

The included scripts were designed with python3 (3.12 in this case). To ensure consistiency, a virtual environment should be set up. This guide assumes comfortablity with command line tooks on Linux or MacOS. Please see this URL for information on setting up pyenv on your specific system: https://github.com/pyenv/pyenv?tab=readme-ov-file

For this exercise, you should install python 3.12:

```
pyenv install 3.12
```

Once pyenv has been set up, you need to activate the environment:

```
python3 -m venv myenv
source myenv/bin/activate
```

## Install library requirements

Once python is ready, use the requirements.txt file to install the required python libraries.

```
cd ~/fetch.test/
pip install -r requirements.txt
```
## Running the tool

Simply execute the tool with the default python version within the environment:

```
python checkuptime.py --yaml example.yaml
```

To exit the loop, use Ctrl-C.
