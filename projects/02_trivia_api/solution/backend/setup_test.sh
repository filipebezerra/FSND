dropdb -e trivia_test
createdb --owner=trivia_user --echo trivia_test \
"Trivia database for test purpose"
psql trivia_test < trivia.psql