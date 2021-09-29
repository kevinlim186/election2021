import pandas as pd

#array(['Special Provinces', 'NCR', 'CAR', 'Region I', 'Region II',
#       'Region III', 'Region IV-A', 'Region IV-B', 'Region V',
#       'Region VI', 'Region VII', 'Region VIII', 'Region IX', 'Region X',
#       'Region XI', 'Region XII', 'CARAGA', 'ARMM'], dtype=object)

#Index(['region', 'province', 'city_or_municipality_including_districts',
#       'registered_voter', 'male', 'female', '17-19', '20-24', '25-29',
#       '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64',
#       '65-above', 'literacy', 'indigenous_people', 'person_with_disability',
#       'single', 'married', 'widow', 'legally_seperated'],
#      dtype='object')

demographic = pd.read_csv('./data/election_demographic.csv')

#demographic['region']
#clean up
demographic.loc[demographic['region']=='Region I','region']='1'
demographic.loc[demographic['region']=='Region II','region']='2'
demographic.loc[demographic['region']=='Region III','region']='3'
demographic.loc[demographic['region']=='Region IV-A','region']='4A'
demographic.loc[demographic['region']=='Region IV-B','region']='4B'
demographic.loc[demographic['region']=='Region V','region']='5'
demographic.loc[demographic['region']=='Region VI','region']='6'
demographic.loc[demographic['region']=='Region VII','region']='7'
demographic.loc[demographic['region']=='Region VIII','region']='8'
demographic.loc[demographic['region']=='Region IX','region']='9'
demographic.loc[demographic['region']=='Region X','region']='10'
demographic.loc[demographic['region']=='Region XI','region']='11'
demographic.loc[demographic['region']=='Region XII','region']='12'
demographic.loc[demographic['region']=='CARAGA','region']='13'


##uncategorized due to mismatching of region designation
demographic.loc[demographic['region']=='Special Provinces','region']='Others'


#array(['NCR', 'CAR', '1', '2', '3', '4A', '4B', '5', '6', '7', '8', '9',
#       '10', '11', '12', '13', 'NIR', 'ARMM', nan], dtype=object)
# Index(['Regions', 'Duterte', 'Roxas', 'Poe', 'Binay', 'Santiago']
results = pd.read_csv('./data/election_results.csv')
#results['Regions']
results.loc[results['Regions']=='NIR','Regions']='Others'
results=results[results['Regions'].notna()]
results['Duterte']=results['Duterte'].astype('int32') 
results['Roxas']= results['Roxas'].astype('int32') 
results['Poe']= results['Poe'].astype('int32') 
results['Binay'] = results['Binay'].astype('int32') 
results['Santiago'] = results['Santiago'].astype('int32')


results['total']= results['Duterte'] + results['Roxas']+ results['Poe'] + results['Binay'] + results['Santiago']


#array(['N. C. R.', 'CAR', 'REGION  I', 'REGION  II', 'REGION  III',
#       'REGION  IV-A', 'REGION  IV-B', 'REGION  V', 'REGION  VI',
#       'REGION  VII', 'REGION  VIII', 'REGION  IX', 'REGION  X',
#       'REGION XI', 'REGION  XII', 'CARAGA', 'A.R.M.M.'], dtype=object)

#Index(['REGION', 'PROVINCE', 'NUM_OF_CLUSTERED_PREC_FUNCTIONED', 'REG_VOTERS',
#       'VOTERS_WHO_ACTUALLY_VOTED', 'VOTER_TURNOUT'],
#      dtype='object')
      
turn_out = pd.read_csv('./data/election_turnout.csv')
#turn_out['REGION']
turn_out.loc[turn_out['REGION']=='N. C. R.', 'REGION']='NCR'
turn_out.loc[turn_out['REGION']=='A.R.M.M.', 'REGION']='ARMM'
turn_out.loc[turn_out['REGION']=='REGION  I', 'REGION']='1'
turn_out.loc[turn_out['REGION']=='REGION  II', 'REGION']='2'
turn_out.loc[turn_out['REGION']=='REGION  III', 'REGION']='3'
turn_out.loc[turn_out['REGION']=='REGION  IV-A','REGION']='4A'
turn_out.loc[turn_out['REGION']=='REGION  IV-B','REGION']='4B'
turn_out.loc[turn_out['REGION']=='REGION  V','REGION']='5'
turn_out.loc[turn_out['REGION']=='REGION  VI', 'REGION']='6'
turn_out.loc[turn_out['REGION']=='REGION  VII', 'REGION']='7'
turn_out.loc[turn_out['REGION']=='REGION  VIII', 'REGION']='8'
turn_out.loc[turn_out['REGION']=='REGION  IX', 'REGION']='9'
turn_out.loc[turn_out['REGION']=='REGION  X', 'REGION']='10'
turn_out.loc[turn_out['REGION']=='REGION  XI', 'REGION']='11'
turn_out.loc[turn_out['REGION']=='REGION  XII', 'REGION']='12'
turn_out.loc[turn_out['REGION']=='CARAGA', 'REGION']='13'



####Reasonableness tests #####
#check if total votes tallies 
turn_out_per_region = turn_out.groupby(['REGION'])['VOTERS_WHO_ACTUALLY_VOTED'].sum().reset_index()
res_turn = turn_out_per_region.merge(results, left_on='REGION', right_on='Regions')
res_turn = res_turn.rename(columns={'VOTERS_WHO_ACTUALLY_VOTED':'turn_out_data', 'total':'results_data', })
res_turn['difference'] =res_turn['turn_out_data']-res_turn['results_data']

res_turn=res_turn[['REGION', 'turn_out_data', 'results_data', 'difference']]
res_turn = res_turn.sort_values(by=['REGION'])


