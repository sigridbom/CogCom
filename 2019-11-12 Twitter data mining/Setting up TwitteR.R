#Downloading the twitter package

pacman::p_load(twitteR)


consumer_key <- " eKuLDzlwGYYRVzjLYY1WJ9Le7 "

consumer_secret <- " 0lewZD3WAM625maeVjhGS2svefTif6coCWP5btzRnAA1aqaA7A "

access_token <- " 280396064 - 4oBrOwnHkwwMIDxQVu283ge9afBmgbIwLKPjSSgc "

access_secret <- " yTMwRZkZlZkKQDxUGHGA3DqEDO0XG5xj9E91GkTD9mmzn "

setup_twitter_oauth(consumer_key, consumer_secret, access_token, access_secret)