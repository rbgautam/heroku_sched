# schedule-python-script-in-heroku
### This is a workaround method to schedule jobs using python script on heroku for free.

#### For detailed explanation checkout : https://youtu.be/SH_KOHyU6Dg

### USE Case: The job scheduled in here is to populate scrap a webpage every 5 minutes for data and send notification through Twilio Api if the data is different.

#### Refrence: https://github.com/Amal4m41/schedule-python-script-in-heroku
Thanks for the nice tutorial

Steps to push local git repo to heroku remote and start the application:

- Create a local git repo 

- Use the following commands to deploy and start application:
```
1.heroku login

2.heroku create <name_app>  #(create a new empty application on Heroku. If you run this command from your app’s root directory,
the empty Heroku Git repository is automatically set as a remote for your local repository.)

3.git remote -v   #(to view the remote heroku app)

4.git push heroku master  #(deploying the code)


#To start the worker process :
5.heroku ps:scale worker=1 --app <app_name>

#To view the logs
6.heroku logs --tail --app <app_name>

#Later when we need to kill the worker process : 
7.heroku scale worker=0 --app <app_name>


```
