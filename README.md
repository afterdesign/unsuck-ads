This project aims to benchmark how much memory is eaten by ads and trackers on popular pages.

## Prepare virtualenv with dependencies:
```bash
make init
```

## Run benchmark:
```bash
./venv/bin/python test.py "http://www.nytimes.com/2015/10/16/world/asia/obama-troop-withdrawal-afghanistan.html"
```

## Excample output:
||memory in MB|
|---|---|
|with adblockers|106.891|
|without adblockers|387.461|
