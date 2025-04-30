# lzu_net_login

use selenium to login lzu_net automatically

## main tool version

```text
Python 3.9.2
selenium 4.27.1
```

## fill username, password and chromedriver's path in lzu_net.py before run the script

Fill the three variable below, which are in lzu_net.py.

```text
account_username
account_password
chrome_driver_path
```

## lzu_net.sh is used to run lzu_net.py

I use `crontab` to run lzu_net.sh when machine starts up.

```text
# edit crontab
crontab -e
```

```text
# write in
@reboot bash /path/to/lzu_net.sh
```

```text
# remove all tasks
crontab -r
```

You need to **edit path variable in lzu_net.sh first** before using it.

Open lzu_net.sh and just read it. It's not difficult to modify.

## lzu_net.log will be created in lzu_net_login directory

You can check lzu_net.log to see if something goes wrong.

## and maybe you want to know how i debug the code?

I write a blog to record the process. It's in Chinese. Click <a href="https://wuhulamb.me/p/using-selenium-to-login-campus-network/" target="_blank">here</a> to see it.
