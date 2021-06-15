# page-loader
![Python CI](https://github.com/sharknoise/page-loader/workflows/Python%20CI/badge.svg?branch=main)
[![Maintainability](https://api.codeclimate.com/v1/badges/b6fc7f8c1836d253884f/maintainability)](https://codeclimate.com/github/sharknoise/page-loader/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/b6fc7f8c1836d253884f/test_coverage)](https://codeclimate.com/github/sharknoise/page-loader/test_coverage)
##
page-loader is a CLI utility that downloads a web page of your choice.
##
Installation - copy the following into the terminal:  
```
python3 -m pip install --user -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple sharknoise-page-loader
```
Usage: `page-loader [-h] [-o OUTPUT] [-l LOG_LEVEL] target_url`  
  
Positional arguments:  
  `target_url` - URL of the page  
  
Optional arguments:  
  `-h`, `--help` - show this help message and exit  
  `-o OUTPUT`, `--output OUTPUT` - set the save directory  
  `-l LOG_LEVEL, --log LOG_LEVEL` - set logging level: 'none', 'info', 'warning', 'debug'
  
  [Watch a demo video](https://asciinema.org/a/i3xzM9JdTmX8LArwX3K8xA6UY)