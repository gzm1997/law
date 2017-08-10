# Mailbox signup authentication and login

标签（空格分隔）： signup authentication login 


----------

I rewrite my homework in Modern Web Program class, I wrote it by html5, jquery, nodejs before, now I rebuild with **python flask** and here it is its [demo][1]


----------
## run_signup.py ##
Because I make this small project a **package**, so it's necessary to use a **run.py** to run the project (*just a py file exactly outside this package no matter what you name it*)

run.py should look like below:
```
from signup import app

app = app
if __name__ == "__main__":
	app.run(host = "0.0.0.0", port = 8080)
```


----------
## Install modules ##

    pip install -r requirements.txt

----------
## Renderings ##
![Rendering][2]

## signup ##
![signup][3]

## login ##
![login][4]

## detail ##
![detail][5]


  [1]: http://139.199.182.179/signup
  [2]: https://github.com/gzm1997/signup/blob/master/screenshots/signup.gif?raw=true
  [3]: https://github.com/gzm1997/signup/blob/master/screenshots/signup.png?raw=true
  [4]: https://github.com/gzm1997/signup/blob/master/screenshots/login.png?raw=true
  [5]: https://github.com/gzm1997/signup/blob/master/screenshots/detail.png?raw=true
