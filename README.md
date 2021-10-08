# CredzCheckr
Testing default web credentials

# Usage

```
usage: credzcheckr.py [-h] [-u URL] [-U URLS_FILE] [-uap UAP] [-w WORDLIST] [-b] [-i INPUTS]

 optional arguments:
    -h, --help            show this help message and exit
    -u URL                URL login to test [required]
    -U URLS_FILE, --urls_file URLS_FILE Provide file instead of url, one per line.
    -w WORDLIST           list of your passwords to test Default: credz/top_200_default_passwd.txt
    -b, --bruteforce      Bruteforce username/password
    -i INPUTS, --inputs INPUTS if that not found inputs during the scan, this option add auto in inputs.txt file. Ex: -i "user:passwd"
```

# Exemples

```
	//Basic
	python3 credzcheckr.py -u URL/login.php 

	// with particular inputs
	python3 credzcheckr.py -u URL/login.php -i user_input:password_input
```

# Credits

- ztgrace for "changeme" tool https://github.com/ztgrace/changeme


