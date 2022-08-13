# udacity-fsnd-casting-agency

## Deploying to Heroku Cloud
### Create an App
```buildoutcfg
heroku create [my-app-name] --buildpack heroku/python
# For example, 
# heroku create myapp-663697908 --buildpack heroku/python
# https://myapp-663697908.herokuapp.com/ | https://git.heroku.com/myapp-663697908.git
```

### Push changes into heroku
```buildoutcfg
# Every time you make any edits to any file in the web_app folder
# Check which files are ready to be committed
git add -A
git status
git commit -m "your message"
```
```buildoutcfg
# Assuming you have already committed all your local edits.
git push heroku master
```