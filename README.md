
## 📝 Before usage

How does it work? 

First of all, you need to login to your account and join server that you want to scrape.
It can't be done automaticly because discord bans your account :(.

Than, add all of servers id in the config, or leave it empty to scrape all servers you are in.

The second problem is - discord asks captcha for each dm request, the only service i found is https://24captcha.online/,
the price here is 0.5$ for 1000 captchas, so it's not that expensive.

Go to this site, register, top up your balance and get your api key, than put it in the config.

When you start the bot it will listen to messages and send dm's to all active users who are writing in the chat.

## ⚙️ Usage

1. **Install Python 3.10+**  
   Download and install Python 3.10 or higher from [python.org](https://www.python.org/downloads/).

2. **Install Required Packages**
   Install dependencies by running the following command:
   ```bash
    pip install -r requirements.txt
    ```

2. **Set up config**  
   Put your discord token in the data/config.py file, also set up other variables there.
3. **Run the Program**  
   Execute the main.py file to launch the application.

---

## ❗ Disclaimer

Using this script could get your account quickly banned, so use with caution and never on your main account.

---
