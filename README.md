<div align="center">

# SQL Injection-XSS Exploit by Python
<em><h5 align="center">(Programming Language - Python 3)</h5></em>
<em><h5 align="center">for studying</h5></em>
![image](https://github.com/refiaa/SQLi-XSS-Exploit_Python/assets/112306763/19f8de05-bdee-46aa-b7f6-730d393faf9e)

*actually work on various site*


<div align="left">

## Disclaimer

```
The rights holder shall not be liable for any damages incurred by the user or third parties arising from the use of this data, except in cases caused by the intentional or negligent acts of the rights holder.

The rights holder does not guarantee the suitability of the data for specific purposes, non-infringement of third-party rights, absence of defects, or compliance with laws, culture, commercial practices, or matters arising from the process of use.

The rights holder shall not be liable for any damages arising from the use or inability to use this data.

Even if the rights holder is liable, except in cases of intentional or gross negligence or where prohibited by law, the liability of the rights holder shall be limited to direct and ordinary damages up to the price of providing this data.
```

## Features
- `HTTP Client`: Custom HTTP client to handle SSL/TLS connections and manage cookies.
- `SQL Injection Scanner`: Detects SQL injection vulnerabilities by injecting various payloads.
- `XSS Scanner`: Identifies Cross-Site Scripting (XSS) vulnerabilities using common payloads.
- `Web Crawler`: Crawls the website to discover and map out the structure of the web application.
- `Attack Executor`: Exploits detected vulnerabilities to verify the potential for exploitation.

## Requirements
Python 3.7+
Requests library
BeautifulSoup4 library
urllib3 library

## Usage 
To run the scanner on a target website, modify the base_url variable in main.py with the target URL and execute the script.

```shell
python src/main.py
```
Modify base_url in `main.py`:
```py
def main():
    base_url = "https://targetwebsite.com"
```

Run the script:
```shell
python src/main.py

```

