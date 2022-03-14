# Dashboard: Influence du climat sur les finances
*Le contexte :* 
    
Depuis Août, le GIEC, Groupe d’experts intergouvernemental sur l’évolution du climat, a publié le premier volet de son sixième rapport. c’est le tableau le plus complet, le plus précis et le plus à jour de la situation climatique mondiale. Nous savons tous pertinemment que le réchauffement climatique impacte fortement notre planète. Le rapport a alors alarmé beaucoup de monde mais ceux sur lesquels nous auriont voulu nous pencher sont les institutions financières. En effet, cette nouvelle publication pourrait nous permettre de voir en quoi les institutions financières peuvent être impactées par les grands changements à venir. Elles doivent réagir vite pour prendre des mesures nécéssaires.

Dans ce Dashboard, nous avons donc voulu reproduire un rapport du GIEC pour analyser les différents impacts qu'a la température sur notre planète pour permettre aux Institutions financières de prendre des mesures pour le futur. Il a été réalisé à l'aide de données que nous pouvions trouver publiquement et facilement.

Pour ce faire, nous avons récupéré les données d'observations issues des messages internationaux d’observation en surface (SYNOP) circulant sur le système mondial de télécommunication (SMT) de l’Organisation Météorologique Mondiale (OMM). Nous avons pu y trouver des paramètres atmosphériques mesurés tels que la température, l'humidité, la pression atmosphérique, ou autres paramètres. A côté de celle-ci, nous avons récupéré des données sur data.gouv pour trouver des données financières. Le problème est que souvent, les données intéressantes ne sont pas publiques et restent dans les banques ou autres instituts financières. Notre choix est donc tourné vers des données plus immobilières mais qui seront en lien fort avec notre sujet. Ainsi, les prêts à taux zéros guideront notre comparaison avec des données telles le prix au mètre carré ou autres.


### User Guide
*Comment on déploie le Dasboard ?*

Le programme principal s'intitule ***main.py***.

1) Cloner tout le projet à partir du GIT.
`git clone https://git.esiee.fr/galagain-et-batut/notreprojetpython.git`

2) Télécharger les librairies sur la machine. Deux possibilités :
*  `python -m pip install -r requirements.txt` # python3 sur Linux et MacOS
*  Juste lancer le programme principal python, le programme installe avec `os.system()` les librairies avec pip automatiquement

Toutes les librairies utiles sont maintenant installées:
* wget 
* pandas
* numpy
* dash
* dash_bootstrap_components
* plotly
* plotly-express
* ipywidgets
* scikit-learn

3) On va créer la base de données **all_data.csv** pour notre DashBoard si il n'est pas déjà présent dans le dossier :
* Exécuter le fichier qui crée le fichier en question `python get_data.py`
* Juste lancer le programme principal qui le télécharge si on ne l'a pas encore fait
* Si un des liens n'est plus fonctionnel, la base de données peut se télécharger [et se voir ici](https://galagain.com/projects/dataptz/all_data.csv)

Quatre bases de données sont donc téléchargées:
* [base de données sur les prêts à taux zéros (PTZ)](https://www.data.gouv.fr/fr/datasets/r/eac9a237-0907-45e7-a41e-ff2c171fe10d)
* [base de données qui liste les communes](https://static.data.gouv.fr/resources/communes-de-france-base-des-codes-postaux/20200309-131459/communes-departement-region.csv)
* [base de données d'observations issues des messages internationaux d’observation en surface (SYNOP)](https://donneespubliques.meteofrance.fr/?fond=produit&id_produit=90&id_rubrique=32)
* [base de données qui va permettre de récupérer les coordonnées des stations](https://donneespubliques.meteofrance.fr/donnees_libres/Txt/Synop/postesSynop.csv)

4) Il ne reste plus qu'à executer le programme principal: `python main.py` # python3 sur Linux et MacOS

5) Connectez vous à l'adresse créée par le DashBoard: [http://127.0.0.1:8050/](http://127.0.0.1:8050/)

Vous pouvez maintenant naviguer dessus, vous allez pouvoir y retrouver différents graphiques intéractifs, car il vous sera possible de choisir de nombreux paramètres

**NB.** le [*main.py*](https://galagain.com/projects/dataptz/main.py) permet d'installer automatiquement les paquets et la base de données. Il se suffit donc à lui même...


### Developper Guide
*Comment est organiser le code ?*

Toutes les étapes sont **présentes et décrites en détails dans le code**.
Ainsi, toutes les fonctions sont détaillées et chaque ligne de code du programme est expliqué pour comprendre son fonction.

#### La première partie se charge donc de télécharger la base de données.

Les librairies utilisées ont des utilités différentes.
-   => wget sert à télécharger du contenu via un URL
-   => pandas va permettre de gèrer rapidement nos bases de données
-   => numpy va être utiliser pour des modules usuels (np.nan, np.mean, np.sqrt et np.array)

Dans les grandes lignes on télécharge notre base de données sur les prêts à taux zéros en faisant attention à lire les données en UTF-8. On regroupe les données par communes car on suppose que pour une commune les habitants suivent les mêmes règles. On va ensuite mettre des coordonnées à ces communes. On va faire un `pandas.merge()` qui va permettre de rassembler nos deux bases de données sur la colonne choisie. 

Ensuite, on télécharge les données climatologiques. Celles-ci sont très nombreuses et sont lourdes. En soit, ce n'est pas un problème mais, quand on va vouloir des interactions avec nos courbes, cela va être lent. On supprime donc les colonnes que l'on ignore. Sur les colonnes restantes, on fait la moyenne des observations par communes et par années. Comme précédemment, on trouve les coordonnées géographiques sur une autre base de données, il nous suffit juste à les rassembler.

Ensuite, il faut rassembler ces deux grosses parties. Donc, la démarche choisie a été de calculer la distance euclidienne entre les stations qui ont fait les émissions des prêts et les stations qui ont fait les enregistrements météo. Pour chaque "agence de prêt" on associe la météo la plus proche.

Il suffit de mettre les noms des colonnes qui nous interesse et le tour est joué.


#### La deuxième partie se charge de gérer le DashBoard.

Les librairies utilisées ont des utilités différentes.
- dash permet de créer une application Web de ML et DataScience facilement
   => `dcc.Input()`
   => `dcc.RadioItems()`
   => `dcc.Graph()`
   => `dcc.RangeSlider()`
   => `dcc.Slider()`
   => `html.Div()`
   => `html.H1()`
   => `html.Br()`
   => `Output()`
   => `Input()`
- dash_bootstrap_components permet de faire un affichage plus propre du DashBoard en lignes et colonnes
   => `dbc.Col()`
   => `dbc.Row()`
   => `dbc.Card()`
- plotly permet de faire des tracés interactifs
   => `go.Figure()`
   => `go.Surface()`
   => `go.Scatter()`
   => `go.Surface()`
   => `go.FigureWidget()`
   => `go.Heatmap()`
   => `go.Histogram()`
   => `px.scatter()`
   => `px.scatter_mapbox()`
- sklearn permet ICI d'importer des fonctions et modèles mathématiques tout fait
   => `train_test_split()`
   => `PolynomialFeatures()`
   => `LinearRegression()`
   => `SVR()`
- json va nous permettre de decompresser des fonctions enregistrées en str
   => `json.loads()`
   => `json.dumps()`

Pour l'affichage de nos données, toutes les fonctions peuvent être modifiées à la guise de l'utilisateur. Il est donc facile pour un développeur de mettre ses propres affichages.

Les fonctions créées sont ainsi:
- `plot3d(data_df, x, y, year_predict)` est une fonction qui crée un affichage 3D de nos paramètres en réalisant un modèle de prédiction SVR
- `predict_polynom(data_df, val, nb_year_predict, degree_predict)` est une fonction qui crée les modèles polynomials
- `heatmap_gen(data_df)` est une fonction qui génère la matrice de corrélation
- `histo_count(data_df, x, bins, typey)` est une fonction qui crée les histogrammes
- `scatter_map_year(data_df, year, colonne)` est une fonction qui génère les cartes


Une fois le DashBoard créé, les `@callback()` arrivent et mettent à jour les figures.
- `clic_data(clickData, bins, typex, year, year_predict)` est la fonction du callback qui crée le DashBoard par défaut et qui met à jour en fonction des clics
- `polynom(value, degree, year_predict)` est une fonction qui permet de mettre à jour les prédictions polynomiales

Des extensions du code intéressantes pourraient être d'automatiser les prédictions. Il faudrait faire une sorte de descente de gradient en fonction des paramètres qui influencent le plus les finances. Avec cette base de données, le résultat amènerait à savoir dans quelles communes acheter et faire des **placements immobiliers** en comprenant l'évolution climatique et l'impact que cela aura sur nos prêts et sur les paramètres immobiliers. Avec des données plus poussées, les **possibilités sont immenses** mais de nombreuses données sont privées... Néanmoins ce travail est une recherche scolaire et n'est pas à but lucratif !

### Rapport d'analyse
*Que pouvons nous conclure de ce Dashboard ?*

La mise en relation de ces deux bases de données est très intéressante. La première observation est la matrice de corrélation que l'on voit en détails (sur le DashBoard ou [**en détails sur ce pdf**](https://galagain.com/projects/dataptz/corr.pdf).
Il faut regarder les coefficients les plus loins de 0. Si on se rapproche de 1, l'augmentation d'un paramètre entraine une augmentation de l'autre paramètre et inversement. Si on se rapproche de -1, l'augmentation d'un paramètre entraine une diminution de l'autre paramètre et inversement.

Les résultats obtenus peuvent se comprendre de façons différentes en fonction des connaissances que l'on a sur les sujets. Voici donc nos explications de la matrice de corrélation.

#### Matrice de corrélation

Les observations amènent :
- un lien positif apparait entre la température et {le prix au mètre carré, la durée nécessaire pour faire le prêt, le montant du prêt effectué}
- le même lien mais négativement entre l'humidité et ces paramètres et entre l'état du sol et ces paramètres
- un lien positif entre la température du sol et {la durée nécessaire pour faire le prêt, le montant du prêt effectué}

Ce qui peut s'expliquer de la façon suivante :
La température d'une ville est effectivement un facteur de choix pour acheter une maison. Pour une maison de vacances, l'on va chercher à trouver une région chaude. Cette catégorie de la population a donc des moyens supérieurs à la moyenne pour faire cet achat. Le montant du prêt peut donc être plus grand. Les impacts sont direct sur le prix au mètre carré, c'est le marché de l'offre et de la demande. Donc plus un quartier est chaud, plus il est prisé. Et il y a une forte correlation entre le prix au mètre carré et le montant du prêt (0.67), la durée du prêt (0.38) et le taux nominal annuel (-0.41). L'influence de l'un implique les autres. Par ailleurs, on confirme que plus le prix au mètre carré est cher plus la population est riche car, la corrélation avec le revenu exprimé en nombre de SMIC par unité de consommation est de 0.5. "La chaleur attire les riches".

L'humidité est corrélée à la température (-0.41). Donc si l'humidité augmente, la température diminue. Donc en admettant l'explication précédente, si l'humidité augmente, le prix au mètre carré diminue.

Ceci est pareil avec l'état du sol, plus la température augmente, plus le sol change (-0.44). Donc, on fait la même conclusion que l'humidité.

Enfin, il peut être intéressant de remarquer que l'année et la température sont liées. Le rechauffement climatique trouve de brèves formes sur la matrice de corrélation du pdf. Le prix au mètre carré augmente donc, dans les mêmes supputations et argumentations précédentes.


#### Les cartes

Les cartes ont une utilité évidente dans le sens où elles permettent d'observer facilement les zones que l'on étudie et l'évolution de nos paramètres dans l'espace.

Par exemple, on remarque que le prix au mètre carré est le plus fort dans la capitale (ce qui s'ajoute à nos observations de la matrice de corrélation). Mais les populations les plus riches se dirigent au fil des années vers les côtes chaudes entrainant un impact sur les données immobilières.

D'un point de vue météologique, on peut faire pleins d'observations qui s'éloignent de notre sujet. Par exemple, on peut remarquer que chaque année la neige évolue et disparait petit à petit et n'est présente qu'en petite quantite dans des zones restreintes...


#### Les histogrammes

Ils permettent de comprendre la répartition des paramètres. On observe des repartitions gaussiennes de la population pour de nombreux paramètres et nous permettent de faire des reflexions supplémentaires sur les paramètres. (des violin plot auraient pu être ajoutés si besoin)


#### Les prédictions

Cette partie est la partie expérimentale de notre recherche. En effet, en faisant des modèles simples, on peut essayer de spéculer sur l'évolution de nos paramètres dans les prochaines années.

D'une part l'on voit l'évolution de notre paramètre depuis 1996, et on se projette avec des polynômes de degrés variables. Des réseaux simples de ML sous Keras amèneraient rapidement des résultats plus réalistes mais, là on ne s'y intéresse pas.

D'autre part, l'affichage 3D permet de visualiser nos paramètres dans le plan. On pourrait par exemple chercher à maximiser les revenus (en z) si l'on créait une colonne prenant en compte les paramètres qui les affectent en x et y. Ce graphique permet de faire une représentation différente mais aussi intéressante de nos valeurs dans le futur et dans le temps.




.....

###### Fin du README