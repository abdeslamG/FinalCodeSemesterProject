
#### Imports

import os
import nltk

import pandas as pd
from ProcessEntropy.CrossEntropy import pairwise_information_flow
import numpy as np
import time

from Preprocessing import *

import warnings
warnings.filterwarnings('ignore')

### 
### Files and paths

SP_path = '/Users/abdeslamguessous/Documents/GitHub/SemesterProject/'
PE_path = SP_path + 'ProcessEntropy-master/'
depandancies = PE_path + 'Pycharm_files_V3/'
results_path = PE_path + 'Results_V3/'

tweets = pd.read_csv(depandancies + 'Tweets_filtered_V3.csv')
users_peers = pd.read_csv(depandancies + 'Peers_V3.csv')


### Functions

def peers_IF (users_peers, tweets):	
	
	print('len of users_peers', len(users_peers))
	print('Len of Tweets', len(tweets))
	print('Number of users', len(tweets.author_id.unique() ) )
	# Loop to avoid kernel crash- user split oriented
	result = []
	start_value = 0
	peers_not_found =  set()

	for idx in range(8122, len(users_peers) ):
		end_value = idx 

	#	users_chunk = users_peers.iloc[start_value : end_value]
		tweets_loop = tweets[tweets['author_id'].isin( users_peers.iloc[idx])]
		print('IDX', idx, 'Len of tweets_loop', len(tweets_loop), 'Number of authors', len(tweets_loop.author_id.unique()) )
    
		if len(tweets_loop.author_id.unique()) == 1 :
			peers_not_found.add(users_peers.iloc[idx]['User 0'])
			peers_not_found.add(users_peers.iloc[idx]['User 1'])
			print('Only one User , -> User 0  : ',users_peers.iloc[idx]['User 0'] , users_peers.iloc[idx]['User 1'])  
			continue 
			
			
		trials = 20
		if len(result) == 0 :
			while trials > 0:
				try :
					result = pairwise_information_flow(tweets_loop, text_col = 'text', label_col = 'author_id', time_col = 'created_at')
					trials = -1
				except :
					print('Trial number ' , trials) 
					trials = trials - 1
			
		#result = result.append(pairwise_information_flow(tweets_loop, text_col = 'text', label_col = 'author_id', time_col = 'created_at'))
    
		if len(result)>1 :
			result.to_csv(results_path + '/Results_ ' + str(idx) +'.csv')
		result = []
		#	time.sleep(10)
        
		time.sleep(0.5)
		start_value = idx
		
	#result.to_csv(results_path + '/Results_final_16_47.csv')
	return peers_not_found

  # tweets_iter = tweets_filtered
  # result.append(pairwise_information_flow(tweets_filtered, text_col = 'text', label_col = 'author_id', time_col = 'created_at')

	
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    peers_not_found = peers_IF(users_peers, tweets)
