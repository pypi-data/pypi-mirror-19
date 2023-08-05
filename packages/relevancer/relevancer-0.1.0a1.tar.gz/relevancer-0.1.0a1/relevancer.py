"""
RelevancerML is a machine learning system that facilitates finding relevant information in tweet collections.

"""

# Authors: Ali Hürriyetoglu <ali.hurriyetoglu@gmail.com>
# License: GPLv3

import configparser
import pickle
import sys
import logging
import json
import datetime
import time
import math as m
from collections import Counter
from html.parser import HTMLParser
import pandas as pd
import numpy as np
import scipy as sp
import re
from operator import itemgetter
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn import metrics
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.metrics.cluster import entropy
from sklearn import cross_validation as cv
from sklearn import grid_search as gs
from sklearn import model_selection as ms
import html



# Logging
root = logging.getLogger()
if root.handlers:
    for handler in root.handlers:
        root.removeHandler(handler) # remove previous ones. So It will work at module level.
logging.basicConfig(filename='RelevancerML.log', format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%d-%m-%Y, %H:%M', level=logging.INFO)
logging.info("\nScript started")

class MLStripper(HTMLParser):

	def __init__(self):
		self.reset()
		self.strict = False
		self.convert_charrefs = True
		self.fed = []

	def handle_data(self, d):
		self.fed.append(d)

	def get_data(self):
		return ''.join(self.fed)

class Twtokenizer():

	def __init__(self):
		self.abbreviations = ['i.v.m.', 'a.s.', 'knp.']
		print('init:', self.abbreviations)

	def tokenize(self, tw):
		# abbcheck = False
		newtw = ''
		lentw = len(tw)
		# print(tw)
		for i, c in enumerate(tw):
			if (c in "'`´’‘") and ((i+1 != lentw) and (i != 0)) and ((tw[i-1].isalpha()) or tw[i-1] in "0123456789") and (tw[i+1].isalpha()):
				newtw += ' '+c+' '
			elif (c in "'`´’()+*-") and ((lentw>i+1) and (i > 0)) and (tw[i-1] in ' 0123456789') and (tw[i+1].isalpha()):
				newtw += c+' '
			elif (c in '();>:') and ((lentw>i+1) and (i != 0)) and ((tw[i-1].isalpha()) or (tw[i-1] in '0123456789')) and ((tw[i+1] == ' ') or (i == lentw-1)):
				newtw += ' '+c
			elif (c in '.') and ((lentw>i + 1) and (i != 0)) and ((tw[i-1].isalpha()) or (tw[i-1] in '0123456789')) and ((tw[i+1] == ' ') or (i == lentw-1)) \
								and (newtw.split()[-1]+c not in self.abbreviations):
				newtw += " " + c
			elif (c in "'`´’‘()+*->") and (i == 0) and (lentw > 1) and ((tw[1].isalpha()) or tw[1] in "0123456789"):
				newtw += c+' '
			elif (c in "'`´’‘()+*->") and (i+1 == lentw) and (lentw > 1) and ((tw[i-1].isalpha()) or tw[i-1] in "0123456789"):
				newtw += ' '+c
			elif (c in ",") and ((i != 0) and (i+1 != lentw)) and tw[i-1].isdigit() and tw[i+1].isdigit():  # for 3,5 7,5
				newtw += c
			elif (c in ",&"):
				newtw += " "+c+" "
			elif (c in "â"):  # create a dictionary for character mappings. if c in dict: newtw += dict[c]
				newtw += "a"
			elif (c in "ê"):
				newtw += "e"
			elif (c in "î"):
				newtw += "i"
			elif (c in "ú"):
				newtw += "ü"
			# elif (c in ":")
			else:
				newtw += c
			# print(c in "'`´’()+*-", lentw>i+1, i>0, tw[i-1] == ' 0123456789', tw[i+1].isalpha())
			# if abbcheck:
			# 	print("abbcheck is true:",newtw.split())
			# print(i,c,(c in '.'), ((lentw>i+1) and (i!=0)), ((tw[i-1].isalpha()) or (tw[i-1] in '0123456789')), ((tw[i+1] == ' ') or (i == lentw-1)) \
			# 							and (newtw.split()[-1]+c not in self.abbreviations))
		# print('\n\n')
		return newtw

	def tokenize_df(self, tokdf, texcol="tweet", newtexcol='texttokCap', rescol="ttextlist", addLowerTok=True):
		# concert_table.drop_duplicates()
		# Note
		# tokdf[newtexcol] = tokdf[newtexcol].str.replace("""\xa0"""," ")
		# tokdf[newtexcol] = tokdf[newtexcol].str.replace("\n"," . ")
		tokdf[newtexcol] = tokdf[texcol].copy()
		# tokdf[newtexcol] = tokdf[newtexcol].replace(self.toReplaceDict, regex=True)
		tokdf[newtexcol][tokdf[newtexcol].str.endswith(".")] = tokdf[tokdf[newtexcol].str.endswith(".")][newtexcol].apply(lambda tw: tw[:-1] + ' .')
		tokdf[newtexcol][tokdf[newtexcol].str.endswith(".'")] = tokdf[tokdf[newtexcol].str.endswith(".'")][newtexcol].apply(lambda tw: tw[:-2] + " . '")
		tokdf[newtexcol][tokdf[newtexcol].str.startswith("'")] = tokdf[tokdf[newtexcol].str.startswith("'")][newtexcol].apply(lambda tw: "' " + tw[1:])
		tokdf[newtexcol] = tokdf[newtexcol].apply(self.tokenize)
		tokdf[newtexcol] = tokdf[newtexcol].str.strip()
		# tokdf[rescol] = tokdf[newtexcol].str.split()

		if addLowerTok:
			tokdf[newtexcol[:-3]] = tokdf[newtexcol].str.lower()

		return tokdf.copy()


class Relevancer():

	def __init__(self, main_col="text", active_col="text_active", lang="en"):

		self.http_re = re.compile(r'https?[^\s]*')
		self.usr_re = re.compile(r'@[^\s]*') # \b@ # formal definition.
		self.no_tok = False  # no_tok by default.

		self.lang = lang

		self.active_column = active_col
		self.main_col = main_col

		self.my_token_pattern=r"\w+(?:-\w+)+|[-+]?\d+[.,]?\d+|[#@]?\w+\b|[\U00010000-\U0010ffff\U0001F300-\U0001F64F\U0001F680-\U0001F6FF\u2600-\u26FF\u2700-\u27BF]|[.:()\[\],;?!*'-]{2,4}"

		if self.no_tok:  # create a function for that step!
			self.tok_result_col = self.main_col + "tokCap"
		else:
			self.tok_result_col = self.main_col

		self.remove_text = {}
		self.remove_text["en"] = [r"^\s*retweeted\s*", r"^\s*I liked a usrusr video urlurl\s*", r"^\s*(?:#\s+)+", r"^\s*live updates:", r"^\s*learn the story behind", \
				r"^\s*news:?", r"^\s*live:", r"^\new post:?", r"^\s*#?breaking:", r"^\s*breaking news", r"^\s*RT usrusr\s*", r"^\s*RT usrusr\s*", \
				r"^\s*MT usrusr\s*", r"^\s*I liked a usrusr video from usrusr urlurl\s*", r"^\s*I posted [0-9]+ photos on Facebook in the album\s*", \
				r"^\s*(?:#\s+)+", r"^\s*i added a video to a usrusr playlist urlurl\s*", r"^\s?[\.\"\'“]?(?:\s*usrusr)+\s*",
				r"^(?:\s*usrusr)+\s*", r"(?:\s*urlurl)+\s*$", r"(?:\s*via\s*usrusr)+\s*$", r"(?:\s*usrusr)+\s*$", r"(?:\s*urlurl)+\s*$", \
				r"(?:\s*usrusr)+\s*$", r"(?:\.\s?)+\s*$"]


		init_report = ""
		init_report += "Language of the data: "+ self.lang + "\n"
		init_report += "Main text column: " + self.main_col + "\n"
		init_report += "Transformation will be applied on the column: "+self.active_column + "\n"
		init_report += "The token pattern: "+ self.my_token_pattern + "\n"


		print(init_report)

	def connect_mongodb(self, configfile="myconfig.ini", coll_name=None):
		"""
		This method gets data from a mongodb collection that is specified in a configuration file.

		Parameters
		----------
		configfile : array-like
		coll_name : array-like
		Returns
		-------
		type_true : one of {'multilabel-indicator', 'multiclass', 'binary'}
		    The type of the true target data, as output by
		    ``utils.multiclass.type_of_target``
		y_true : array or indicator matrix
		y_pred : array or indicator matrix
		"""
		import pymongo as pm

		logging.info("Connecting to the db with parameters:\n configfile:"+str(configfile)+"\t coll_name:"+str(coll_name))

	# Config Parser;
		config = configparser.ConfigParser()
		config.read(configfile)
	# MongoLab OAuth;
		client_host = config.get('mongodb', 'client_host')
		client_port = int(config.get('mongodb', 'client_port'))
		db_name = config.get('mongodb', 'db_name')
		if coll_name is None:
			coll_name = config.get('mongodb', 'coll_name')
		if config.has_option('mongodb', 'user_name'):
			user_name = config.get('mongodb', 'user_name')
		if config.has_option('mongodb', 'passwd'):
			passwd = config.get('mongodb', 'passwd')
	# Connect to database;
		try:
			connection = pm.MongoClient(client_host, client_port)
			rlvdb = connection[db_name]  # Database
			if ('user_name' in locals()) and ('passwd' in locals()):
				rlvdb.authenticate(user_name, passwd)
			rlvcl = rlvdb[coll_name]  # Collection
			logging.info("Connected to the DB successfully.")
		except Exception:
			sys.exit("Database connection failed!")

		return rlvdb, rlvcl


	def strip_tags(self, html):

		s = MLStripper()
		s.feed(html)
		return s.get_data()

	def set_active_column(self, active_col="active_text"):
		#global active_column
		self.active_column = active_col

	def set_token_pattern(self, new_token_pattern):
		#global my_token_pattern
		self.my_token_pattern = new_token_pattern

		print("The new token pattern is:", self.my_token_pattern)
		logging.info("The new token pattern is:"+self.my_token_pattern)

	def read_json_tweets_file(self, myjsontweetfile, linecount=-1, skip_nolang=True):
		"Each tweet should be in a line. The parameter linecount restricts number of tweets in case it is not -1."

		ftwits = []
		lang_cntr = Counter()
		with open(myjsontweetfile) as jfile:
			for i, ln in enumerate(jfile):
				if i == linecount:  # restrict line numbers for test
					break
				t = json.loads(ln)

				# t["lang"] = t["user"]["lang"]

				if ("lang" in t):
					lang_cntr[t["lang"]] += 1
				else:
					lang_cntr["NoLang"] += 1

				if skip_nolang and ("lang" not in t):
					continue

				if ("lang" in t) and (t["lang"] != self.lang):

					continue
				elif ("lang" not in t) or (t["lang"] == self.lang):
					t["created_at"] = datetime.datetime.strptime(t["created_at"], "%a %b %d %H:%M:%S +0000 %Y")
					# if t["created_at"].strftime("%Y-%m-%d") in flood_AnomBreakoutDaysList:
					if "entities" in t and "media" in t["entities"]:
						for tm in t["entities"]["media"]:
							if tm["type"] == 'photo':
								t["entity_type"] = 'photo'
								break

					if "entities" in t and "hashtags" in t["entities"]:
						t["entity_hashtags"] = [ehs["text"] for ehs in t["entities"]["hashtags"]]

					if "entities" in t and "user_mentions" in t["entities"]:
						t["entity_mentions"] = [ems["screen_name"] for ems in t["entities"]["user_mentions"]]


					# if "entities" in t and "urls" in t["entities"]:
					# 	t["entity_urls"] = [ers["display_url"] for ers in t["entities"]["urls"]]

					if "entities" in t and "urls" in t["entities"]:
						t["entity_urls"] = [ers.get("display_url",None) for ers in t["entities"]["urls"]]


					try:
						if "place" in t:
							t["country"] = t["place"]["country"]
					except:
						pass
					if "retweeted_status" in t:
						t["is_retweet"] = True
					else:
						t["is_retweet"] = False


					if 'source' in t:
						t["device"] = self.strip_tags(t["source"])

					t["user_id"] = t["user"]["id_str"]

					if "followers_count" in t["user"]:
						t["user_followers"] = t["user"]["followers_count"]

					if "friends_count" in t["user"]:
						t["user_following"] = t["user"]["friends_count"]

					t["screen_name"] = t["user"]["screen_name"]

					t["user_loc"] = t["user"]["location"]
					t["user_tzone"] = t["user"]["time_zone"]


					t2 = {k:v for k,v in t.items() if k in ["entity_type","entity_hashtags","entity_mentions","entity_urls",\
															"country","created_at","text","in_reply_to_user_id","id_str","user_id",\
															"user_followers","user_following", "coordinates", "is_retweet","device","screen_name","user_loc","user_tzone"]}
					# print(i, end = ',')
					ftwits.append(t2)  # .splitlines()
			print("Number of documents per languge:", lang_cntr)
			return ftwits

	def read_json_tweets_file_ftags(self, myjsontweetfile, linecount=-1):
		"This is one list of tweets contains all tweets. It contains a single line. The parameter linecount restricts number of tweets in case it is not -1."

		ftwits = []
		with open(myjsontweetfile) as jfile:
			twts = json.load(jfile)
			logging.info("Lengtht of the tweet list is:"+str(len(twts)))
			for i, t in enumerate(twts):
				if i == linecount:  # restrict line numbers for test
					break

				if i == 0:
					print('1. item as an example:\t',t)

				t["created_at"] = t['date']
				t2 = {k:v for k,v in t.items() if k in ["text","created_at","classes","keywords"]}
				# print(i, end = ',')
				ftwits.append(t2)  # .splitlines()
			return ftwits

	def read_json_tweets_database(self, rlvcl, mongo_query, tweet_count=-1):

		ftwits = []
		lang_cntr = Counter()

		for i, t in enumerate(rlvcl.find(mongo_query)):
			# time = datetime.datetime.now()
			# logging.info("reading_database_started_at: " + str(time))
			if i == tweet_count:  # restrict line numbers for test
				break
		# t = json.loads(ln)
			lang_cntr[t["lang"]] += 1
			if t["lang"] == self.lang:
				if isinstance(t["created_at"],str):
					t["created_at"] = datetime.datetime.strptime(t["created_at"], "%a %b %d %H:%M:%S +0000 %Y")
				# if t["created_at"].strftime("%Y-%m-%d") in flood_AnomBreakoutDaysList:

				if "entities" in t and "media" in t["entities"]:
					for tm in t["entities"]["media"]:
						if tm["type"] == 'photo':
							t["entity_type"] = 'photo'
							break
				if "entities" in t and "hashtags" in t["entities"]:
					t["entity_hashtags"] = [ehs["text"] for ehs in t["entities"]["hashtags"]]

				if "entities" in t and "user_mentions" in t["entities"]:
					t["entity_mentions"] = [ems["screen_name"] for ems in t["entities"]["user_mentions"]]

				if "entities" in t and "urls" in t["entities"]:
					t["entity_urls"] = [ers["display_url"] for ers in t["entities"]["urls"]]

				try:
					if "place" in t:
						t["country"] = t["place"]["country"]
				except:
					pass
				if "retweeted_status" in t:
					t["is_retweet"] = True
				else:
					t["is_retweet"] = False

				if 'source' in t:
					t["device"] = self.strip_tags(t["source"])

				t["user_id"] = t["user"]["id_str"]

				if "followers_count" in t["user"]:
					t["user_followers"] = t["user"]["followers_count"]

				if "friends_count" in t["user"]:
					t["user_following"] = t["user"]["friends_count"]

				t["screen_name"] = t["user"]["screen_name"]

				t2 = {k:v for k,v in t.items() if k in ["entity_type","entity_hashtags","entity_mentions","entity_urls",\
														"country","created_at","text","in_reply_to_user_id","id_str","user_id",\
														"user_followers","user_following", "coordinates", "is_retweet","device","screen_name"]}
				# print(i, end=',')
				ftwits.append(t2)  # .splitlines()
			# time2 = datetime.datetime.now()
			# logging.info("reading_database_ended_at: " + str(time2))
		print("Number of documents per languge:", lang_cntr)
		return ftwits

	def read_json_tweet_fields_database(self, rlvcl, mongo_query, read_fields={'text': 1, 'id_str': 1, '_id': 0, 'user': 1}, tweet_count=-1, annotated_ids=[], annotated_users=[]):
		"""
			"annotated_users" may contain user screen names or user_ids.

		"""
		logging.info("reading_fields_started with the following parameters:\nmongoquery="+str(mongo_query)+"\trlvcl(collection)="+str(rlvcl))
		logging.info("")


		ftwits = []
		for i, t in enumerate(rlvcl.find(mongo_query, read_fields)):
			if (i != tweet_count) and (t['id_str'] not in annotated_ids) and ((("user" in t) and (t["user"]["screen_name"] not in annotated_users)) or (("user_id" in t) and (t["user_id"] not in annotated_users))):  # restrict line numbers for test
				# break

				if "created_at" in t:
					t["created_at"] = datetime.datetime.strptime(t["created_at"], "%a %b %d %H:%M:%S +0000 %Y")

				if "retweeted_status" in t:
					t["is_retweet"] = True
				else:
					t["is_retweet"] = False

				if "user" in t:
					t['screen_name'] = t["user"]['screen_name']

				t1 = {k: v for k, v in t.items() if k not in ["user"]} # exclude it after you get the required information. It contains many information in an original tweet.
				ftwits.append(t1)  # .splitlines()
			elif i == tweet_count:
				logging.info("Number of tweets read:"+str(i))
				break

		logging.info("Length of tweets that were read:"+str(len(ftwits)))
		logging.info("end of database read, example tweet:" + str(ftwits[-1]))

		return ftwits

	def get_ids_from_tw_collection(self, rlvcl):

		time1 = datetime.datetime.now()
		logging.info("get_tw_ids_started_at: " + str(time1))

		print('In get_tw_ids')
		tw_id_list = []
		for clstr in rlvcl.find({}, {"id_str": 1, "_id": 0}):
			# print("cluster from rlvcl:\n",clstr)
			tw_id_list.append(clstr["id_str"])
			# break

		return tw_id_list

	def get_cluster_sizes(self, kmeans_result, doclist):

		clust_len_cntr = Counter()
		for l in set(kmeans_result.labels_):
			clust_len_cntr[str(l)] = len(doclist[np.where(kmeans_result.labels_ == l)])

		return clust_len_cntr

	def create_dataframe(self, tweetlist):

		dataframe = pd.DataFrame(tweetlist)
		logging.info("columns:" + str(dataframe.columns))
		print(len(dataframe))

		if "created_at" in dataframe.columns:
			dataframe.set_index("created_at", inplace=True)
			dataframe.sort_index(inplace=True)
		else:
			logging.info("There is not the field created_at, continue without datetime index.")

		logging.info("Number of the tweets:" + str(len(dataframe)))
		logging.info("Available attributes of the tweets:" + str(dataframe.columns))

		return dataframe

	def transform_metatext(self, mytextDF, create_intermediate_result=False):
		"""
              User and hashtags were converted to certain values.

		"""

		if self.active_column not in mytextDF.columns:
			mytextDF[self.active_column] = mytextDF[self.main_col].copy()

		mytextDF[self.active_column] = mytextDF[self.active_column].apply(lambda t: html.unescape(t))

		if create_intermediate_result:
			mytextDF["normalized_http"] = mytextDF[self.active_column].apply(lambda tw: re.sub(self.http_re, 'urlurl', tw))
			mytextDF["normalized_usr"] = mytextDF["normalized_http"].apply(lambda tw: re.sub(self.usr_re, 'usrusr', tw))
			mytextDF[self.active_column] = mytextDF["normalized_usr"]
		else:
			mytextDF[self.active_column] = mytextDF[self.active_column].apply(lambda tw: re.sub(self.http_re, 'urlurl', tw))
			mytextDF[self.active_column] = mytextDF[self.active_column].apply(lambda tw: re.sub(self.usr_re, 'usrusr', tw))


		return mytextDF

	def clean_text(self, mytextDF):
		mytextDF[self.active_column] = mytextDF[self.active_column].str.strip(to_strip="!:\n“ \"\'")

	def remove_text_parts(self, mytextDF):

		self.clean_text(mytextDF)

		if self.lang in self.remove_text:
			for pttrn in self.remove_text[self.lang]:
				mytextDF[self.active_column] = mytextDF[self.active_column].str.replace(pttrn, "", case=False)
		else:
			print("No defined text parts to be removed for:", self.lang)
			print("Only language independent normalisation will take place.")

		self.clean_text(mytextDF)

		# following reduces consecutive duplicate words to 1 occurrence.
		mytextDF[self.active_column] = mytextDF[self.active_column].str.replace(r"\b(\w+)\b[:]?(\s+\b\1\b)+", r"\1", flags=re.I)

		# after cleaning some text have part of words followed by: …$  --> remove
		mytextDF[self.active_column] = mytextDF[self.active_column].str.replace(r"\w+…$", "", flags=re.I)

		return mytextDF


	def get_document_feature_matrix(self, mydf):
		freqcutoff = int(m.log(len(mydf)))
		word_vectorizer = TfidfVectorizer(ngram_range=(1, 2), lowercase=True, norm='l2', min_df=freqcutoff, token_pattern=my_token_pattern, sublinear_tf=True)
		doc_feat_mtrx = word_vectorizer.fit_transform(mydf[self.active_column])
		return doc_feat_mtrx

	def get_and_eliminate_near_duplicate_tweets(self, tweetsDF, distancemetric='cosine', debug=False, similarity_threshold=0.20, debug_threshold=1000, defaultfreqcut_off=2):

		start_time = datetime.datetime.now()

		# active_tweet_df = tweetsDF

		logging.info("We use 'np.random.choice' method for creating a data frame 'active_tweet_df' that contains random tweets and its parameter is 'tweetsDF'.")
		logging.info("The used distance metric is:"+distancemetric)

		if debug:
			if len(tweetsDF) > debug_threshold:
				active_tweet_df = tweetsDF[:debug_threshold]    # We choose random data for testing.
			else:
				active_tweet_df = tweetsDF
		else:
			active_tweet_df = tweetsDF


		#logging.info("mytext:" + str(active_tweet_df["text"]))
		logging.info("\n size of mytext:" + str(len(active_tweet_df[self.active_column])))

		if len(active_tweet_df) > 1000:
			freqcutoff = int(m.log(len(active_tweet_df)))
		else:
			freqcutoff = defaultfreqcut_off # default 2 is applicable for short texts tweets.

		logging.info("Tweet count is:"+str(len(active_tweet_df))+"\tfreqcutoff:"+str(freqcutoff))

		logging.info("In 'word_vectorizer' method, we use 'TfidfVectorizer' to get feature names and parameter is 'active_tweet_df[self.active_column]' .")

		if len(active_tweet_df) > 1000:
			word_vectorizer = TfidfVectorizer(ngram_range=(1, 2), lowercase=False, norm='l2', min_df=freqcutoff, token_pattern=self.my_token_pattern, sublinear_tf=True)
		else: # otherwise min_df is bigger than max_df ValueError:
			word_vectorizer = TfidfVectorizer(ngram_range=(1, 2), lowercase=False, norm='l2', token_pattern=self.my_token_pattern, sublinear_tf=True)

		X2_train = word_vectorizer.fit_transform(active_tweet_df[self.active_column])
		#X2_train = X2_train.toarray() # we do not need this, we should work with sparse matrices for the efficiency.
		logging.info("features:" + str(word_vectorizer.get_feature_names()))
		logging.info("number of features:" + str(len(word_vectorizer.get_feature_names())))
		logging.info("End of the 'word_vectorizer' method.")

		allowed_metrics = ['cosine',  'euclidean', 'cityblock', 'jaccard']
		if distancemetric not in allowed_metrics:
			raise Exception("distance metric should be one of the allowed ones. Allowed metrics are: " + str(allowed_metrics))

		# dist = distance.pdist(X2_train, distancemetric2)  # Distances are defined as a parameter in the function.
		# dist_matrix = scipy.spatial.distance.squareform(dist)   # Valid values for metric are 'Cosine', 'Cityblock', 'Euclidean' and 'Jaccard'.
		# logging.info("distances:"+str(dist_matrix))   # These metrics do not support sparse matrix inputs.

		logging.info("In scikit-learn pairwise distance, we use different parameters for different distances that are defined in 'allowed_metrics'.")
		dist_matrix = pairwise_distances(X2_train, metric=distancemetric, n_jobs=1)   # Valid values for metric are 'Cosine', 'Cityblock', 'Euclidean' and 'Manhattan'.
		logging.info("distances:" + str(dist_matrix))  # These metrics support sparse matrix inputs.

		similarity_dict = {}
		for a, b in np.column_stack(np.where(dist_matrix < similarity_threshold)):  # zip(np.where(overthreshold)[0],np.where(overthreshold)[1]):
			if a != b:
				if active_tweet_df.index[a] not in similarity_dict: # work with the actual index no in the dataframe, not with the order based one!
					similarity_dict[active_tweet_df.index[a]] = [active_tweet_df.index[a]]  # a is the first member of the group.
				similarity_dict[active_tweet_df.index[a]].append(active_tweet_df.index[b])


		if len(similarity_dict) == 0:
			print("There is not any group of near-duplicate tweets.")
			return active_tweet_df

		# unique_tweets =
		# return unique_tweets =

		# logging.info("Demote the duplicate tweets to 1 'list(set([tuple(sorted(km))'.")
		# Delete the duplicate clusters.
		cluster_tuples_list = list(set([tuple(sorted(km)) for km in similarity_dict.values()]))  # for each element have a group copy in the group, decrease 1.
		cluster_tuples_list = sorted(cluster_tuples_list, key=len, reverse=True)

		cluster_tuples2 = [cluster_tuples_list[0]]

		if debug:
			logging.info("The length based sorted cluster tuples are:"+str(cluster_tuples_list)) # being in this dictionary means a and b are similar.
			logging.info("The length of the length based sorted cluster tuples are:"+str(len((cluster_tuples_list)))) # being in this dictionary means a and b are similar.


		duplicate_tweet_indexes = list(cluster_tuples_list[0])
		for ct in cluster_tuples_list[1:]:
			if len(set(duplicate_tweet_indexes) & set(ct)) == 0:
				cluster_tuples2.append(ct)
				duplicate_tweet_indexes += list(ct)
		#print("Number of cluster2:", len(cluster_tuples2))

		duplicate_tweet_indexes = list(set(duplicate_tweet_indexes))

		one_index_per_duplicate_group = []
		for clst in cluster_tuples2:
			one_index_per_duplicate_group.append(clst[0])

		#print("list len vs. set len (one_index_per_duplicate_group):", len(one_index_per_duplicate_group), len(set(one_index_per_duplicate_group)))
		#print("list len vs. set len (duplicate_tweet_indexes):", len(duplicate_tweet_indexes), len(set(duplicate_tweet_indexes)))

		indexes_of_the_uniques = [i for i in active_tweet_df.index if i not in duplicate_tweet_indexes]
		#print("list len vs. set len (indexes_of_the_uniques):", len(indexes_of_the_uniques), len(set(indexes_of_the_uniques)))


		#print("Any null in the main dataframe:",active_tweet_df[active_tweet_df.text.isnull()])
		unique_active_tweet_df = active_tweet_df.ix[[i for i in active_tweet_df.index if i not in duplicate_tweet_indexes]+one_index_per_duplicate_group] # +
		#print("Any null in the unique dataframe:",unique_active_tweet_df[unique_active_tweet_df.text.isnull()])

		tweet_sets = []
		for i, ct in enumerate(cluster_tuples2):
			tweets = []
			for t_indx in ct:
				tweets.append(active_tweet_df[self.active_column].ix[t_indx])
			tweet_sets.append(tweets)
			logging.info("\nNear duplicate tweet groups are below: ")
			logging.info("\nsize of group " + str(i) + ':' + str(len(tweets)))

		if debug:
			logging.info("COMPLETE: Near duplicate tweet sets:" + "\n\n\n".join(["\n".join(twset) + "\n" + "\n".join(twset) for twset in tweet_sets]))
		else:
			logging.info("SUMMARY: Near duplicate tweet sets:" + "\n\n\n".join(["\n".join(twset[:1]) + "\n" + "\n".join(twset[-1:]) for twset in tweet_sets]))

		# logging.info("Near duplicate tweet sets:" + "\n\n\n".join(["\n".join(twset) for twset in tweet_sets]))
		logging.info('End of the "scikit-learn pairwise distance".')
		# logging.info('End of the 'scipy pairwise distance'.')



		logging.info("unique tweet sets:" + '\n' + str(unique_active_tweet_df[self.active_column][:3]) + str(unique_active_tweet_df[self.active_column][:3][-3:]))
		logging.info("\n size of unique tweets:" + str(len(unique_active_tweet_df)))

		logging.info(" 'datetime.datetime.now()' method is used for calculating the process time. ")
		end_time = datetime.datetime.now()
		logging.info(str('Duration: {}'.format(end_time - start_time)))  # It calculates the processing time.
		logging.info("end of the datetime.datetime.now() method.")

		number_eliminated = len(active_tweet_df) - len(unique_active_tweet_df)
		logging.info("number of eliminated text:"+str(number_eliminated))

		per = number_eliminated/len(active_tweet_df)  # It calculates the number of eliminated tweets as percentage.
		logging.info("percentage of eliminated tweet is " + str(per))

		logging.info("final DataFrame info:" + str(unique_active_tweet_df.info()))
		# logging.info("head:"+str(active_tweet_df.head()))

		return unique_active_tweet_df

	def tok_results(self, tweetsDF, elimrt=False):

		results = []
		if no_tok:  # create a function for that step!
			tok_result_lower_col = "texttok"

			twtknzr = Twtokenizer()
			tweetsDF = twtknzr.tokenize_df(tweetsDF, texcol=self.active_column, rescol=tok_result_col, addLowerTok=False)
			tweetsDF[tok_result_lower_col] = tweetsDF[tok_result_col].str.lower()
			print("\nAvailable attributes of the tokenized tweets:", tweetsDF.columns)
			print("\ntweet set summary:", tweetsDF.info())
			print(tweetsDF[tok_result_col][:5])
			print("Tweets ARE tokenized.")
		else:  # do not change the text col
			tok_result_lower_col = "texttok"

			tweetsDF[tok_result_lower_col] = tweetsDF[tok_result_col].str.lower()
			print("\nAvailable attributes of the tweets:", tweetsDF.columns)
			print("\ntweet set summary:", tweetsDF.info())
			print(tweetsDF[tok_result_col][:5])
			print("\ntweets are NOT tokenized.")
		if elimrt:

			rttext = ~tweetsDF[tok_result_lower_col].str.contains(r"\brt @")

			if "is_retweet" in tweetsDF.columns:
				rtfield = tweetsDF["is_retweet"] == False
				tweetsDF["is_notrt"] = rtfield.values & rttext.values  # The default setting is to eliminate retweets
			else:
				logging.info("The is_retweet field is not present. We check just the text field.")
				print("The is_retweet field is not present. We check just the text field.")
				tweetsDF["is_notrt"] = rttext.values

			print("To be Eliminated tweets:", tweetsDF[~tweetsDF.is_notrt])
			tweetsDF = tweetsDF[tweetsDF.is_notrt]
			print("Retweets were eliminated.")
		else:
			print("Retweets were NOT eliminated.")

		tweetsDF[self.active_column] = tweetsDF[tok_result_lower_col].copy()
		return tweetsDF

	def elim_rts(self, tweetsDF):
		"Return the dataframe after eliminating the retweets in it. It checks both the is_retweet field and /rt @/ pattern."
		rttext = tweetsDF[self.active_column].str.contains(r"\brt @", case=False)

		if "is_retweet" in tweetsDF.columns:
			tweetsDF["is_rt"] = tweetsDF["is_retweet"].values | rttext.values  # The default setting is to eliminate retweets
		else:
			logging.info("The is_retweet field is not present. We check just the text field.")
			print("The is_retweet field is not present. We check just the text field.")
			tweetsDF["is_rt"] = rttext.values

		return tweetsDF[~tweetsDF.is_rt]

	def get_uni_bigrams(self, text, token_pattern):
		logging.info("The token pattern in get_uni_bigrams: " + token_pattern)
		token_list = re.findall(token_pattern, text)
		return [" ".join((u, v)) for (u, v) in zip(token_list[:-1], token_list[1:])] + token_list

	def reverse_index_frequency(self, cluster_bigram_cntr):

		reverse_index_freq_dict = {}
		for k, freq in cluster_bigram_cntr.most_common():
			if str(freq) not in reverse_index_freq_dict:
				reverse_index_freq_dict[str(freq)] = []
			reverse_index_freq_dict[str(freq)].append(k)

		return reverse_index_freq_dict

	def get_annotated_tweets(self, collection_name):

		"""
		Dataframe of:
			text    label

			txt1     l1
			txt2     l2
		"""

		return None

	def get_vectorizer_and_mnb_classifier(self, tweets_as_text_label_df, my_token_pattern, pickle_file=None):

		print('In get_mnb_classifier ..')

		freqcutoff = int(m.log(len(tweets_as_text_label_df))/2)

		now = datetime.datetime.now()
		logging.info("feature_extraction_started_at: " + str(now))

		word_vectorizer = TfidfVectorizer(ngram_range=(1, 2), lowercase=False, norm='l2', min_df=freqcutoff, token_pattern=self.my_token_pattern, sublinear_tf=True)
		X2_train = word_vectorizer.fit_transform(tweets_as_text_label_df.text.values)

		logging.info("Number of features:"+str(len(word_vectorizer.get_feature_names())))
		logging.info("Features are:"+str(word_vectorizer.get_feature_names()))
		# logging("n_samples: %d, n_features: %d" % X2_train.shape)

		now2 = datetime.datetime.now()
		logging.info("feature_extraction_ended_at: " + str(now2))

		now3 = datetime.datetime.now()
		logging.info("Training started at: " + str(now3))

		y_train = tweets_as_text_label_df.label.values
		MNB = MultinomialNB(alpha=.1)
		MNB.fit(X2_train, y_train)

		now4 = datetime.datetime.now()
		logging.info("Training ended at: " + str(now4))

		vect_and_classifier = {'vectorizer': word_vectorizer, 'classifier': MNB}

		if (pickle_file is not None) and isinstance(pickle_file, str):
			if not pickle_file.endswith(".pickle"):
				pickle_file += '.pickle'
			with open(pickle_file, 'wb') as f:
				pickle.dump(vect_and_classifier, f, pickle.HIGHEST_PROTOCOL)
				print("Pickle file was written to", pickle_file)
		else:
			print("The pickle file is not a string. It was not written to a pickle file.")

		return vect_and_classifier

	def get_evaluated_classifier_cwb(self, tweets_as_text_label_df, ngrams, myanalyzer='word', mynorm='l2', mysublinear_tf=True):
		"""
			tweets_as_text_label_df: a dataframe that has at least 'label' and 'text' columns.

		"""
		print("Parameters (ngrams, myanalyzer):", ngrams, myanalyzer)
		#y = tweets_as_text_label_df["label"].values
		#print(tweets_as_text_label_df)

		freqcutoff = int(m.log(len(tweets_as_text_label_df))/2)
		print("freqcutoff:", freqcutoff)

		word_vectorizer = TfidfVectorizer(ngram_range=ngrams, lowercase=True, norm=mynorm, min_df=freqcutoff,
		                                  sublinear_tf=mysublinear_tf, analyzer=myanalyzer)
		fitted_data = word_vectorizer.fit_transform(tweets_as_text_label_df["text"].values)

		x = fitted_data

		X_train, X_test, y_train, y_test = cv.train_test_split(fitted_data, tweets_as_text_label_df.label.values, test_size=0.15, random_state=0)

		# Grid Search
		#kf_total = cv.KFold(len(x), n_folds=10, shuffle=True, random_state=4)
		kf_total = cv.StratifiedKFold(y_train, n_folds=10, shuffle=True, random_state=4)
		nb_gs = gs.GridSearchCV(estimator=MultinomialNB(), param_grid=dict(alpha=np.linspace(0,3,40))) # , n_jobs=6
		#[nb_gs.fit(x[train],y[train]).score(x[test],y[test]) for train, test in kf_total]
		[nb_gs.fit(X_train[train],y_train[train]).score(X_train[test],y_train[test]) for train, test in kf_total]
		print(nb_gs, "\nbest score:", nb_gs.best_score_, "\nalpha:", nb_gs.best_estimator_.alpha)


		# Run with best alpha
		MNB = MultinomialNB(alpha=nb_gs.best_estimator_.alpha)

		MNB.fit(X_train, y_train)

		predicted = MNB.predict(X_test)
		expected = y_test

		print("class order:", MNB.classes_)
		#print("number of items per class:\n", y_test.value_counts())

		conf_m = confusion_matrix(expected, predicted, labels=MNB.classes_)
		clf_report = classification_report(expected, predicted, target_names=MNB.classes_)
		vect_and_classifier = {'vectorizer': word_vectorizer, 'classifier': MNB, 'conf_mtrx':conf_m, 'report':clf_report}
		print('accuracy:', metrics.accuracy_score(expected, predicted))
		print('confusion matrix:\n', conf_m)
		print('Classification report:', clf_report)
		print()

		return vect_and_classifier, conf_m, clf_report

	def get_evaluated_classifier_cwb2(self, tweets_as_text_label_df, ngrams, myanalyzer='word', mynorm='l2', mysublinear_tf=True):
		"""
			tweets_as_text_label_df: a dataframe that has at least 'label' and 'text' columns.

		"""
		print("Parameters (ngrams, myanalyzer):", ngrams, myanalyzer)
		#y = tweets_as_text_label_df["label"].values
		#print(tweets_as_text_label_df)

		freqcutoff = int(m.log(len(tweets_as_text_label_df))/2)
		print("freqcutoff:", freqcutoff)

		word_vectorizer = TfidfVectorizer(ngram_range=ngrams, lowercase=True, norm=mynorm, min_df=freqcutoff,
		                                  sublinear_tf=mysublinear_tf, analyzer=myanalyzer)

		fitted_data = word_vectorizer.fit_transform(tweets_as_text_label_df["text"].values)

		x = fitted_data

		X_train, X_test, y_train, y_test = ms.train_test_split(fitted_data, tweets_as_text_label_df.label.values, test_size=0.15, random_state=0)

		# Grid Search
		#kf_total = ms.KFold(len(x), n_folds=10, shuffle=True, random_state=4)
		kf_total = ms.StratifiedKFold(n_splits=10, shuffle=True, random_state=4)
		kf_total.split(X_train, y_train)
		nb_gs = ms.GridSearchCV(estimator=MultinomialNB(), param_grid=dict(alpha=np.linspace(0,3,40))) # , n_jobs=6
		#[nb_gs.fit(x[train],y[train]).score(x[test],y[test]) for train, test in kf_total]
		[nb_gs.fit(X_train[train],y_train[train]).score(X_train[test],y_train[test]) for train, test in kf_total]
		print(nb_gs, "\nbest score:", nb_gs.best_score_, "\nalpha:", nb_gs.best_estimator_.alpha)


		# Run with best alpha
		MNB = MultinomialNB(alpha=nb_gs.best_estimator_.alpha)

		MNB.fit(X_train, y_train)

		predicted = MNB.predict(X_test)
		expected = y_test

		print("class order:", MNB.classes_)
		#print("number of items per class:\n", y_test.value_counts())

		conf_m = confusion_matrix(expected, predicted, labels=MNB.classes_)
		clf_report = classification_report(expected, predicted, target_names=MNB.classes_)
		vect_and_classifier = {'vectorizer': word_vectorizer, 'classifier': MNB, 'conf_mtrx':conf_m, 'report':clf_report}
		print('accuracy:', metrics.accuracy_score(expected, predicted))
		print('confusion matrix:\n', conf_m)
		print('Classification report:', clf_report)
		print()

		return vect_and_classifier, conf_m, clf_report

	def cluster_to_text_file(self, filename, myclusters):
		"""Get a list of clusters and write them to a file"""
		with open(filename,'w') as fw:
			for i,clst in enumerate(myclusters):
				if clst["cno"] == -1:
					continue
				fw.write("\nOrder of the cluster:"+str(i)+"\n")
				fw.write("CStr:"+clst['cstr']+"\n")
				fw.write("\n".join([" ".join(c[2].split("\n")) for c in clst['ctweettuplelist']])+"\n")
				fw.write("**********"*11)

	def create_clusters(self, tweetsDF,  my_token_pattern, min_dist_thres=0.6, min_max_diff_thres=0.4, max_dist_thres=0.8, iteration_no=1, min_clusters=1, printsize=True, nameprefix='',  selection=True, strout=False, user_identifier='screen_name', cluster_list=None):
		"""
		Have modes:
		mode1: get a certain number of clusters. Relax parameters for it. (This is the current Mode!)
		mode2: get clusters that comply with certain conditions.

		"min_max_diff_thres" should not be too small. Then You miss thresholds like: min 0.3 - min 0.7: The top is controlled by the maximum anyway. Do not fear from having it big: around 0.4

		"""
		min_clust_size = 5

		if min_dist_thres > 0.85 and max_dist_thres>0.99:
			logging.info("The parameter values are too high to allow a good selection. We just finish searching for clusters at that stage.")
			logging.info("Threshold Parameters are: \nmin_dist_thres="+str(min_dist_thres)+"\tmin_max_diff_thres:="+str(min_max_diff_thres)+ "\tmax_dist_thres="+str(max_dist_thres))
			return cluster_list


		len_clust_list = 0
		if cluster_list is None:
			cluster_list = []

		elif not selection and len(cluster_list)>0:
			return cluster_list
		else:
			len_clust_list = len(cluster_list)
			logging.info("Starting the iteration with:"+str(len_clust_list)+" clusters.")

			clustered_tweet_ids = []

			for clust_dict in cluster_list:
				clustered_tweet_ids += clust_dict["twids"]

			logging.info("Number of already clustered tweets are:"+str(len(clustered_tweet_ids)))

			logging.info("Tweet set size to be clustered:"+str(len(tweetsDF)))
			tweetsDF = tweetsDF[~tweetsDF.id_str.isin(clustered_tweet_ids)]
			logging.info("Tweet set size to be clustered(after elimination of the already clustered tweets):"+str(len(tweetsDF)))

			if len(tweetsDF)==0:
				logging.info("Please check that the id_str has a unique value for each item.")
				print("Please check that the id_str has a unique value for each item.")
				return cluster_list

		logging.info('Creating clusters was started!!')
		logging.info("Threshold Parameters are: \nmin_dist_thres="+str(min_dist_thres)+"\tmin_max_diff_thres:="+str(min_max_diff_thres)+ "\tmax_dist_thres="+str(max_dist_thres))
		cluster_bigram_cntr = Counter()

		freqcutoff = int(m.log(len(tweetsDF))/2)
		if freqcutoff == 0:
			freqcutoff = 1 # make it at least 1.

		#freqcutoff = int(m.log(len(tweetsDF))/2) # the bigger freq threshold is the quicker to find similar groups of tweets, although precision will decrease.
		logging.info("Feature extraction parameters are:\tfrequencyCutoff:"+str(freqcutoff))

		word_vectorizer = TfidfVectorizer(ngram_range=(1, 2), lowercase=False, norm='l2', min_df=freqcutoff, token_pattern=self.my_token_pattern)
		text_vectors = word_vectorizer.fit_transform(tweetsDF[self.active_column])
		# logging.info("Number of features:"+str(len(word_vectorizer.get_feature_names())))
		logging.info("Features are:"+str(word_vectorizer.get_feature_names()))

		#n_clust = int(m.sqrt(len(tweetsDF))/2)+iteration_no*(min_clusters-len_clust_list)*10 # The more clusters we need, the more clusters we will create.

		n_clust = int(m.sqrt(len(tweetsDF)))+iteration_no*(min_clusters-len_clust_list)*5
		if n_clust<(len(tweetsDF)/min_clust_size):
			logging.info("used: n_clust = int(m.sqrt(len(tweetsDF)))+iteration_no*(min_clusters-len_clust_list)*5")
		else:
			n_clust = int(m.sqrt(len(tweetsDF))/2)+iteration_no*(min_clusters-len_clust_list)*2

			if n_clust<(len(tweetsDF)/min_clust_size):
				logging.info("used: int(m.sqrt(len(tweetsDF))/2)+iteration_no*(min_clusters-len_clust_list)*2")
			else:
				n_clust = int(m.sqrt(len(tweetsDF))/2)+iteration_no
				logging.info("used: int(m.sqrt(len(tweetsDF))/2)+iteration_no*(min_clusters-len_clust_list)*2")

		n_initt = int(m.log10(len(tweetsDF)))+iteration_no  # up to 1 million, in KMeans setting, having many iterations is not a problem. # more iterations higher chance of having candidate clusters.

		logging.info("Clustering parameters are:\nnclusters="+str(n_clust)+"\tn_initt="+str(n_initt))


		if len(tweetsDF) < 1000000:
			km = KMeans(n_clusters=n_clust, init='k-means++', max_iter=500, n_init=n_initt)  # , n_jobs=16
			logging.info("The data set is small enough to use Kmeans")
		else:
			km = MiniBatchKMeans(n_clusters=n_clust, init='k-means++', max_iter=500, n_init=n_initt, batch_size=1000)
			logging.info("The data set is BIG, MiniBatchKMeans is used.")

		km.fit(text_vectors)

		# Cluster = namedtuple('Cluster', ['cno', 'cstr','tw_ids'])
		clustersizes = self.get_cluster_sizes(km, tweetsDF[self.active_column].values)

		logging.info("Cluster sizes are:"+str(clustersizes))

		for cn, csize in clustersizes.most_common():  # range(args.ksize):
			cn = int(cn)
			similar_indices = (km.labels_ == cn).nonzero()[0]
			similar = []
			similar_tuple_list = []
			for i in similar_indices:
				dist = sp.linalg.norm((km.cluster_centers_[cn] - text_vectors[i]))
				similar_tuple_list.append((dist, tweetsDF['id_str'].values[i], tweetsDF[self.active_column].values[i], tweetsDF[user_identifier].values[i]))
				if strout:
					similar.append(str(dist) + "\t" + tweetsDF['id_str'].values[i] + "\t" + tweetsDF[self.active_column].values[i] + "\t" + tweetsDF[user_identifier].values[i])

			similar_tuple_list = sorted(similar_tuple_list, key=itemgetter(0)) # sort based on the 0th, which is the distance from the center, element.
			# test sortedness!

			if strout:
				similar = sorted(similar, reverse=False)
			cluster_info_str = ''
			user_list = [t[3] for t in similar_tuple_list]  # t[3] means the third element in the similar_tuple_list.
			if selection:
				if (len(similar_tuple_list)>2) and (similar_tuple_list[0][0] < min_dist_thres) and (similar_tuple_list[-1][0] < max_dist_thres) and ((similar_tuple_list[0][0] + min_max_diff_thres) > similar_tuple_list[-1][0]):  # the smallest and biggest distance to the centroid should not be very different, we allow 0.4 for now!
					cluster_info_str += "cluster number and size are: " + str(cn) + '    ' + str(clustersizes[str(cn)]) + "\n"
					for txt in tweetsDF[self.active_column].values[similar_indices]:
						cluster_bigram_cntr.update(self.get_uni_bigrams(txt, self.my_token_pattern))  # regex.findall(r"\b\w+[-]?\w+\s\w+", txt, overlapped=True))
						# cluster_bigram_cntr.update(txt.split()) # unigrams
					frequency = reverse_index_frequency(cluster_bigram_cntr)
					if strout:
						topterms = [k+":" + str(v) for k, v in cluster_bigram_cntr.most_common() if k in word_vectorizer.get_feature_names()]
						cluster_info_str += "Top terms are:" + ", ".join(topterms) + "\n"
					if strout:
						cluster_info_str += "distance_to_centroid" + "\t" + "tweet_id" + "\t" + "tweet_text\n"
						if len(similar) > 20:
							cluster_info_str += 'First 10 documents:\n'
							cluster_info_str += "\n".join(similar[:10]) + "\n"
							# print(*similar[:10], sep='\n', end='\n')

							cluster_info_str += 'Last 10 documents:\n'
							cluster_info_str += "\n".join(similar[-10:]) + "\n"
						else:
							cluster_info_str += "Tweets for this cluster are:\n"
							cluster_info_str += "\n".join(similar) + "\n"
				else:
					logging.info("Cluster is not good. Smallest and largest distance to the cluster center and size are:"+str(similar_tuple_list[0][0])+"\t"+str(similar_tuple_list[-1][0])+"\t"+str(clustersizes[str(cn)]))
			else:
					cluster_info_str += "cluster number and size are: " + str(cn) + '    ' + str(clustersizes[str(cn)]) + "\n"
					cluster_bigram_cntr = Counter()
					for txt in tweetsDF[self.active_column].values[similar_indices]:
						cluster_bigram_cntr.update(self.get_uni_bigrams(txt, self.my_token_pattern))
					frequency = reverse_index_frequency(cluster_bigram_cntr)
					if strout:
						topterms = [k+":"+str(v) for k, v in cluster_bigram_cntr.most_common() if k in word_vectorizer.get_feature_names()]
						cluster_info_str += "Top terms are:" + ", ".join(topterms) + "\n"
					if strout:
						cluster_info_str += "distance_to_centroid" + "\t" + "tweet_id" + "\t" + "tweet_text\n"
						if len(similar) > 20:
							cluster_info_str += 'First 10 documents:\n'
							cluster_info_str += "\n".join(similar[:10]) + "\n"
							# print(*similar[:10], sep='\n', end='\n')

							cluster_info_str += 'Last 10 documents:\n'
							cluster_info_str += "\n".join(similar[-10:]) + "\n"
						else:
							cluster_info_str += "Tweets for this cluster are:\n"
							cluster_info_str += "\n".join(similar) + "\n"

			if len(cluster_info_str) > 0 and clustersizes[str(cn)]>min_clust_size:  # that means there is some information in the cluster.
				logging.info("\nCluster was appended. cluster_info_str:"+cluster_info_str+"\tmin_dist="+str(similar_tuple_list[0][0])+"\tmax_dist="+str(similar_tuple_list[-1][0]))
				cluster_list.append({'cno': cn, 'cnoprefix': nameprefix+str(cn), 'user_entropy': entropy(user_list), 'rif': frequency, 'cstr': cluster_info_str, 'ctweettuplelist': similar_tuple_list,  'twids': list(tweetsDF[np.in1d(km.labels_, [cn])]["id_str"].values)})  # 'user_ent':entropy(user_list),

		logging.info("length of cluster_list:"+str(len(cluster_list)))
		len_clust_list = len(cluster_list) # use to adjust the threshold steps for the next iteration. If you are closer to the target step smaller.
		if len_clust_list<min_clusters:
			logging.info("There is not enough clusters, call the create_clusters again with relaxed threshold parameters (recursively). Iteration no:"+str(iteration_no))

			factor = (min_clusters-len_clust_list)/1000 # if it needs more clusters, it will make a big step

			min_dist_thres2, max_dist_thres2, min_max_diff_thres2 = self.relax_parameters(min_dist_thres, max_dist_thres, min_max_diff_thres, factor)
			logging.info("Threshold step sizes are: \nmin_dist_thres="+str(min_dist_thres-min_dist_thres2)+"\tmax_dist_thres="+str(max_dist_thres-max_dist_thres2)+"\tmin_max_diff_thres="+str(min_max_diff_thres-min_max_diff_thres2))
			return self.create_clusters(tweetsDF,  self.my_token_pattern, min_dist_thres=min_dist_thres2, min_max_diff_thres=min_max_diff_thres2, max_dist_thres=max_dist_thres2,  \
				iteration_no=iteration_no+1, min_clusters=min_clusters, user_identifier=user_identifier, cluster_list=cluster_list)

		return cluster_list

	def create_clusters2(self, tweetsDF,  my_token_pattern, min_dist_thres=0.6, min_max_diff_thres=0.4, max_dist_thres=0.8, iteration_no=1, min_clusters=1, printsize=True, nameprefix='',  selection=True, strout=False, user_identifier='screen_name', cluster_list=None, custom_stop_words=None, myanalyzer='word', ngramrange=(1,2)):
		"""
		Have modes:
		mode1: get a certain number of clusters. Relax parameters for it. (This is the current Mode!)
		mode2: get clusters that comply with certain conditions.

		"min_max_diff_thres" should not be too small. Then You miss thresholds like: min 0.3 - min 0.7: The top is controlled by the maximum anyway. Do not fear from having it big: around 0.4

		"""
		min_clust_size = 5

		if min_dist_thres > 0.85 and max_dist_thres>0.99:
			logging.info("The parameter values are too high to allow a good selection. We just finish searching for clusters at that stage.")
			logging.info("Threshold Parameters are: \nmin_dist_thres="+str(min_dist_thres)+"\tmin_max_diff_thres:="+str(min_max_diff_thres)+ "\tmax_dist_thres="+str(max_dist_thres))

			for clust_dict in cluster_list:
				clustered_tweet_ids += clust_dict["twids"]
			tweetsDF = tweetsDF[~tweetsDF.id_str.isin(clustered_tweet_ids)]

			cluster_list.append({'cno':-1, "twids":list(tweetsDF.id_str.values)}) # these tweets are the rest.

			return cluster_list
		else:
			logging.info("The parameters has space to be relaxed.")


		len_clust_list = 0
		if cluster_list is None:
			cluster_list = []

		elif not selection and len(cluster_list)>0:
			return cluster_list
		else:
			len_clust_list = len(cluster_list)
			logging.info("Starting the iteration with:"+str(len_clust_list)+" clusters.")

			clustered_tweet_ids = []

			for clust_dict in cluster_list:
				clustered_tweet_ids += clust_dict["twids"]

			logging.info("Number of already clustered tweets are:"+str(len(clustered_tweet_ids)))

			logging.info("Tweet set size to be clustered:"+str(len(tweetsDF)))
			tweetsDF = tweetsDF[~tweetsDF.id_str.isin(clustered_tweet_ids)]
			logging.info("Tweet set size to be clustered(after elimination of the already clustered tweets):"+str(len(tweetsDF)))

			if len(tweetsDF)==0:
				logging.info("Please check that the id_str has a unique value for each item.")
				print("Please check that the id_str has a unique value for each item.")
				return cluster_list

		logging.info('Creating clusters was started!!')
		logging.info("Threshold Parameters are: \nmin_dist_thres="+str(min_dist_thres)+"\tmin_max_diff_thres:="+str(min_max_diff_thres)+ "\tmax_dist_thres="+str(max_dist_thres))
		cluster_bigram_cntr = Counter()

		freqcutoff = int(m.log(len(tweetsDF))/2)
		if freqcutoff == 0:
			freqcutoff = 1 # make it at least 1.

		#freqcutoff = int(m.log(len(tweetsDF))/2) # the bigger freq threshold is the quicker to find similar groups of tweets, although precision will decrease.
		if myanalyzer in ['char', 'char_wb']:
			word_vectorizer = TfidfVectorizer(stop_words=custom_stop_words, ngram_range=ngramrange, lowercase=False, norm='l2', min_df=freqcutoff*2, token_pattern=my_token_pattern, analyzer=myanalyzer)
			logging.info("The ngram_range is:"+str(ngramrange))
			logging.info("Feature extraction parameters are:\tfrequencyCutoff:"+str(freqcutoff*2)+"\tthe analyzer:"+myanalyzer)
		else:
			word_vectorizer = TfidfVectorizer(stop_words=custom_stop_words, ngram_range=(1, 2), lowercase=False, norm='l2', min_df=freqcutoff, token_pattern=my_token_pattern, analyzer=myanalyzer)
			logging.info("Feature extraction parameters are:\tfrequencyCutoff:"+str(freqcutoff)+"\tthe analyzer:"+myanalyzer)

		#print("tweetsDF.columns:", tweetsDF.columns)
		text_vectors = word_vectorizer.fit_transform(tweetsDF[self.active_column])
		# logging.info("Number of features:"+str(len(word_vectorizer.get_feature_names())))
		logging.info("Features are:"+str(word_vectorizer.get_feature_names()))

		#n_clust = int(m.sqrt(len(tweetsDF))/2)+iteration_no*(min_clusters-len_clust_list)*10 # The more clusters we need, the more clusters we will create.

		n_clust = int(m.sqrt(len(tweetsDF)))+iteration_no*(min_clusters-len_clust_list)*5
		if n_clust<(len(tweetsDF)/min_clust_size):
			logging.info("used: n_clust = int(m.sqrt(len(tweetsDF)))+iteration_no*(min_clusters-len_clust_list)*5")
		else:
			n_clust = int(m.sqrt(len(tweetsDF))/2)+iteration_no*(min_clusters-len_clust_list)*2

			if n_clust<(len(tweetsDF)/min_clust_size):
				logging.info("used: int(m.sqrt(len(tweetsDF))/2)+iteration_no*(min_clusters-len_clust_list)*2")
			else:
				n_clust = int(m.sqrt(len(tweetsDF))/2)+iteration_no
				logging.info("used: int(m.sqrt(len(tweetsDF))/2)+iteration_no*(min_clusters-len_clust_list)*2")

		n_initt = int(m.log10(len(tweetsDF)))+iteration_no  # up to 1 million, in KMeans setting, having many iterations is not a problem. # more iterations higher chance of having candidate clusters.

		logging.info("Clustering parameters are:\nnclusters="+str(n_clust)+"\tn_initt="+str(n_initt))


		if len(tweetsDF) < 1000000:
			km = KMeans(n_clusters=n_clust, init='k-means++', max_iter=500, n_init=n_initt)  # , n_jobs=16
			logging.info("The data set is small enough to use Kmeans")
		else:
			km = MiniBatchKMeans(n_clusters=n_clust, init='k-means++', max_iter=500, n_init=n_initt, batch_size=1000)
			logging.info("The data set is BIG, MiniBatchKMeans is used.")

		km.fit(text_vectors)

		# Cluster = namedtuple('Cluster', ['cno', 'cstr','tw_ids'])
		clustersizes = self.get_cluster_sizes(km, tweetsDF[self.active_column].values)

		logging.info("Cluster sizes are:"+str(clustersizes))

		for cn, csize in clustersizes.most_common():  # range(args.ksize):
			cn = int(cn)
			similar_indices = (km.labels_ == cn).nonzero()[0]
			similar = []
			similar_tuple_list = []
			for i in similar_indices:
				dist = sp.linalg.norm((km.cluster_centers_[cn] - text_vectors[i]))
				similar_tuple_list.append((dist, tweetsDF['id_str'].values[i], tweetsDF[self.active_column].values[i], tweetsDF[user_identifier].values[i]))
				if strout:
					similar.append(str(dist) + "\t" + tweetsDF['id_str'].values[i] + "\t" + tweetsDF[self.active_column].values[i] + "\t" + tweetsDF[user_identifier].values[i])

			similar_tuple_list = sorted(similar_tuple_list, key=itemgetter(0)) # sort based on the 0th, which is the distance from the center, element.
			# test sortedness!

			if strout:
				similar = sorted(similar, reverse=False)
			cluster_info_str = ''
			user_list = [t[3] for t in similar_tuple_list]  # t[3] means the third element in the similar_tuple_list.
			if selection:
				if (len(similar_tuple_list)>2) and (similar_tuple_list[0][0] < min_dist_thres) and (similar_tuple_list[-1][0] < max_dist_thres) and ((similar_tuple_list[0][0] + min_max_diff_thres) > similar_tuple_list[-1][0]):  # the smallest and biggest distance to the centroid should not be very different, we allow 0.4 for now!
					cluster_info_str += "cluster number and size are: " + str(cn) + '    ' + str(clustersizes[str(cn)]) + "\n"
					for txt in tweetsDF[self.active_column].values[similar_indices]:
						cluster_bigram_cntr.update(self.get_uni_bigrams(txt, my_token_pattern))  # regex.findall(r"\b\w+[-]?\w+\s\w+", txt, overlapped=True))
						# cluster_bigram_cntr.update(txt.split()) # unigrams
					frequency = self.reverse_index_frequency(cluster_bigram_cntr)
					if strout:
						topterms = [k+":" + str(v) for k, v in cluster_bigram_cntr.most_common() if k in word_vectorizer.get_feature_names()]
						cluster_info_str += "Top terms are:" + ", ".join(topterms) + "\n"
					if strout:
						cluster_info_str += "distance_to_centroid" + "\t" + "tweet_id" + "\t" + "tweet_text\n"
						if len(similar) > 20:
							cluster_info_str += 'First 10 documents:\n'
							cluster_info_str += "\n".join(similar[:10]) + "\n"
							# print(*similar[:10], sep='\n', end='\n')

							cluster_info_str += 'Last 10 documents:\n'
							cluster_info_str += "\n".join(similar[-10:]) + "\n"
						else:
							cluster_info_str += "Tweets for this cluster are:\n"
							cluster_info_str += "\n".join(similar) + "\n"
				else:
					logging.info("Cluster is not good. Smallest and largest distance to the cluster center and size are:"+str(similar_tuple_list[0][0])+"\t"+str(similar_tuple_list[-1][0])+"\t"+str(clustersizes[str(cn)]))
			else:
					cluster_info_str += "cluster number and size are: " + str(cn) + '    ' + str(clustersizes[str(cn)]) + "\n"
					cluster_bigram_cntr = Counter()
					for txt in tweetsDF[self.active_column].values[similar_indices]:
						cluster_bigram_cntr.update(self.get_uni_bigrams(txt, my_token_pattern))
					frequency = self.reverse_index_frequency(cluster_bigram_cntr)
					if strout:
						topterms = [k+":"+str(v) for k, v in cluster_bigram_cntr.most_common() if k in word_vectorizer.get_feature_names()]
						cluster_info_str += "Top terms are:" + ", ".join(topterms) + "\n"
					if strout:
						cluster_info_str += "distance_to_centroid" + "\t" + "tweet_id" + "\t" + "tweet_text\n"
						if len(similar) > 20:
							cluster_info_str += 'First 10 documents:\n'
							cluster_info_str += "\n".join(similar[:10]) + "\n"
							# print(*similar[:10], sep='\n', end='\n')

							cluster_info_str += 'Last 10 documents:\n'
							cluster_info_str += "\n".join(similar[-10:]) + "\n"
						else:
							cluster_info_str += "Tweets for this cluster are:\n"
							cluster_info_str += "\n".join(similar) + "\n"

			if len(cluster_info_str) > 0 and clustersizes[str(cn)]>min_clust_size:  # that means there is some information in the cluster.
				logging.info("\nCluster was appended. cluster_info_str:"+cluster_info_str+"\tmin_dist="+str(similar_tuple_list[0][0])+"\tmax_dist="+str(similar_tuple_list[-1][0]))
				cluster_list.append({'cno': cn, 'cnoprefix': nameprefix+str(cn), 'user_entropy': entropy(user_list), 'rif': frequency, 'cstr': cluster_info_str, 'ctweettuplelist': similar_tuple_list,  'twids': list(tweetsDF[np.in1d(km.labels_, [cn])]["id_str"].values)})  # 'user_ent':entropy(user_list),

		logging.info("length of cluster_list:"+str(len(cluster_list)))
		len_clust_list = len(cluster_list) # use to adjust the threshold steps for the next iteration. If you are closer to the target step smaller.
		if len_clust_list<min_clusters:
			logging.info("There is not enough clusters, call the create_clusters again with relaxed threshold parameters (recursively). Iteration no:"+str(iteration_no))

			factor = (min_clusters-len_clust_list)/5000 # if it needs more clusters, it will make a big step

			min_dist_thres2, max_dist_thres2, min_max_diff_thres2 = self.relax_parameters(min_dist_thres, max_dist_thres, min_max_diff_thres, factor)
			logging.info("Threshold step sizes are: \nmin_dist_thres="+str(min_dist_thres-min_dist_thres2)+"\tmax_dist_thres="+str(max_dist_thres-max_dist_thres2)+"\tmin_max_diff_thres="+str(min_max_diff_thres-min_max_diff_thres2))
			return self.create_clusters2(tweetsDF,  my_token_pattern, min_dist_thres=min_dist_thres2, min_max_diff_thres=min_max_diff_thres2, max_dist_thres=max_dist_thres2,  \
				iteration_no=iteration_no+1, min_clusters=min_clusters, user_identifier=user_identifier, cluster_list=cluster_list, custom_stop_words=custom_stop_words, myanalyzer=myanalyzer, ngramrange=ngramrange)

		else:
			clustered_tweet_ids = []
			for clust_dict in cluster_list:
				clustered_tweet_ids += clust_dict["twids"]
			tweetsDF = tweetsDF[~tweetsDF.id_str.isin(clustered_tweet_ids)]

			cluster_list.append({'cno':-1, "twids":list(tweetsDF.id_str.values)}) # these tweets are the rest.

			return cluster_list

	def relax_parameters(self, min_dist_thres,max_dist_thres,min_max_diff_thres,factor):
		min_dist_thres = min_dist_thres + min_dist_thres*(factor/2)  # As you are closer to the center distance change fast (Euclidean distance). Step a bit big.
		max_dist_thres = max_dist_thres + max_dist_thres*(factor/3) # If you are far from the center, there will be much variation in small differences of distance (Euclidean). Step small.
		min_max_diff_thres = min_max_diff_thres + min_max_diff_thres*(factor/4) # There is not much sense in increasing it much. Otherwise it will loose its meaning easily.

		return min_dist_thres, max_dist_thres, min_max_diff_thres

	def eliminate_duplicates_bucketwise(self, df, step=15000):
	    """
	    The actual near-duplicate detection algorithm is not memory-efficient enough. Therefore,
	    we mostly need to divide the data in the buckets, eliminate duplicates, merge the data, shuffle it, and repeat
	    the same cycle, until no-duplicate detected in any bucket. That may take long for big data sets. Conditions can
	    be relaxed to be quicker but leave a few duplicates.
	    """

	    logging.info("starting eliminate_duplicates_bucketwise, df length:"+str(len(df)))
	    logging.info("Step size:"+str(step))

	    df = df.reindex(np.random.permutation(df.index))
	    df.reset_index(inplace=True, drop=True)

	    tmp_df2 = pd.DataFrame()
	    for i in range(0, len(df), step):
	        tmp_unique = get_and_eliminate_near_duplicate_tweets(df[i:i+step], similarity_threshold=0.10, debug=False, debug_threshold=10000)
	        tmp_df2 = pd.concat([tmp_df2, tmp_unique], ignore_index=True)

	    if len(df) > len(tmp_df2):
	        logging.info(str(len(df) - len(tmp_df2))+" tweets were eliminated!")
	        return eliminate_duplicates_bucketwise(tmp_df2)

	    return df
