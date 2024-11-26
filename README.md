
## Overview of the request

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
 
An example YAML was provided, but it does seem to make some an assumption that the input is actually an array. This has been corrected so we can correctly parse the YAML:

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

If we are to assume this is NOT to be used as an array, the YAML must be formatted differently as the one provided in the example would not be considered valid.

**Running the health checks**

After parsing the YAML input configuration file, the program should send an HTTP request to each endpoint every 15 seconds. Each time an HTTP request is executed by the program, determine if the outcome is UP or DOWN:

 - UP — The HTTP response code is 2xx (any 200–299 response code) and the response
latency is less than 500 ms.
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

