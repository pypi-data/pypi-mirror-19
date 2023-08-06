
# Windows 10 Toast Notifications

An easy-to-use Python library for displaying Windows 10 Toast Notifications which is useful for Windows GUI development.


![o7ja4 1](https://cloud.githubusercontent.com/assets/7101452/19763806/75f71ba4-9c5d-11e6-9f16-d0d4bf43e63e.png)



## Installation

```
pip install win10toast
```

## Requirements

### Installation of pywin32
```
pywin32
setuptools
```

Easiest way to install pywin32 is using executable installer published at [https://sourceforge.net/projects/pywin32/files/pywin32/](https://sourceforge.net/projects/pywin32/files/pywin32/)

## Example

```
from win10toast import ToastNotifier
toaster = ToastNotifier()
toaster.show_toast("Hello World!!!",
              "Python is 10 seconds awsm!",
              icon_path="custom.ico",
              duration=10)
toaster.show_toast("Hello World!!!",
             "Python is awsm by default!")
```


