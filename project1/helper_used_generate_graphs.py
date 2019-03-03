agent1 = pd.read_csv('random_agent.csv',sep='\t')
agent2 = pd.read_csv('only_shooting_agent.csv',sep='\t')
agent3 = pd.read_csv('perceiving_agent.csv',sep='\t')
combine_data = pd.concat([agent1,agent2,agent3],axis=1)
#score 
score = combine_data.drop(['actions known', 'actions performed', 'environment knowledeg',
       'actions known', 'actions performed', 'environment knowledeg',
       'levels cleared'],axis=1)
score.columns = ['random agent','only shooting agent','perceving agent']
plot = sns.boxplot(data=score,linewidth=2.5)
plot.set_title('Score')
plt.savefig('scores.png')
plt.show()
#levels cleared 
levels = combine_data.drop(['action_performed','actions known', 'actions performed', 'environment knowledeg','score'],axis=1)
levels.columns = ['random agent','only shooting agent','perceving agent']
levels = sns.boxplot(data=score,linewidth=2.5)
levels.set_title('levels cleared')
plt.savefig('levels.png')
plt.show()
#'actions performed',
action_performed = combine_data.drop(['actions known',  'environment knowledeg','levels cleared','score'],axis=1)
action_performed.columns = ['random agent','only shooting agent','perceving agent']
#action_performed.plot(kind='box',figsize=(8,8),title='Actions Performed',grid=True)
plot = sns.boxplot(data=action_performed,linewidth=2.5)
plot.set_title('Actions Performed')
plt.savefig('actions_performed.png')
plt.show()

#data.plot(y='score',kind='bar',figsize=(12,9))
#plt.savefig('skip_selection.jpg',dpi=600)
skip_selection = pd.read_csv('skip_selection_data.csv',sep='\t')
skip_selection.drop(['actions known', 'actions performed', 'environment knowledeg',
       'levels cleared'],axis = 1, inplace = True)
sns.barplot(data=skip_selection,y=score)
plt.show()