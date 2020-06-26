createuser --createdb --echo --pwprompt heroku_sample_user
createdb --owner=heroku_sample_user --echo heroku_sample "Heroku sample database"
