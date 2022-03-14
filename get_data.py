#
#
#
#
#
# ==> LIBRARY B.D.D.
# =================================
# On utilise contextlib pour ne pas afficher les messages des librairies lorqu'elles téléchargent leurs fonctions.
# On a ainsi un terminal tout propre après les installations
import contextlib
import os
#
#
#
with contextlib.redirect_stdout(open(os.devnull, 'w')):
    #
    # On met à jour la version de pip
    os.system("python.exe -m pip install --upgrade pip")
    #
    #
    # ==> COMMANDES NOTEBOOK
    # =================================
    # Installations pour un notebook:
    # !pip install wget
    # !pip install pandas
    # !pip install numpy
    # =================================
    # ==> COMMANDES NOTEBOOK
    #
    #
    try:  # WGET
        import wget
    #
    except ImportError:
        os.system("pip install wget")
    #
    #
    try:  # PANDAS
        import pandas
    except ImportError:
        os.system("pip install pandas")
    #
    #
    try:  # NUMPY
        import numpy
    except ImportError:
        os.system("pip install numpy")
    #
    #
    # =================================
    import wget
    import pandas as pd
    import numpy as np
    # =================================
    #
    #
#  => wget sert à télécharger du contenu via un URL
#  => pandas va permettre de gèrer rapidement nos bases de données
#  => numpy va être utiliser pour des modules usuels (np.nan, np.mean, np.sqrt et np.array)
# =================================
# ==> LIBRARY B.D.D.
#
#
#
#
#
# ==> INTRODUCTION
# =================================
# INTRODUCTION
#
# Dans ce code, nous allons chercher à mettre en relation plusieurs bases de données pour essayer de répondre à une
# problématique: ___LE CLIMAT A T'IL UNE INFLUENCE SUR LA FINANCE ET L'IMMOBILIER EN FRANCE?___
#
#
# COMMENT?
#
# le problème le plus dur est de trouver des bases de données intéressantes pour notre sujet.
# Après quelques recherches voici le résultat de nos choix:
if not (os.path.isfile("all_data.csv")):
    #
    #
    #
    #
    #
    # ==> B.D.D. PTZ
    print(" ==> B.D.D. PTZ START")
    # =================================
    #  => base de données sur les prêts à taux zéros (PTZ)
    #     (cf. https://www.data.gouv.fr/fr/datasets/base-de-donnees-ptz-prets-a-taux-zero/)
    #        | Nom de la variable | Format (Alphanumérique, Numérique) | Détails |
    #        |----------|----------|----------|
    #        | an | N | Année d’émission du PTZ |
    #        | type | N | Type d’opération {0: Ancien, 1: Neuf} |
    #        | region | A | Nom de la région |
    #        | dept | A | Numéro du département |
    #        | epci | A | Code SIREN de l’EPCI |
    #        | cins | A | Code commune |
    #        | zoco | A | Zonage effectif à la date d’émission du PTZ (A, B/B1, C/B2) |
    #        | pm2 | N | Prix au mètre carré de l’opération |
    #        | durt | N | Durée totale du PTZ (en mois) |
    #        | vtpz | N | Montant du PTZ |
    #        | vtpr | N | Montant de l’ensemble des prêts de l’opération |
    #        | dtpp | N | Durée du prêt principal (en mois) |
    #        | vtpp | N | Montant du prêt principal |
    #        | txno | N | Taux nominal annuel du prêt principal (en %) |
    #        | nbsmic | N | Revenu exprimé en nombre de SMIC par unité de consommation |
    #     NB. Le fichier ici présenté recense l’ensemble des PTZ émis depuis 1995 jusqu’en 2020.
    #
    # CODE:
    file = "ptz.txt"
    #
    # On télécharge si le fichier n'est pas présent
    if not (os.path.isfile(file)):
        url = "https://www.data.gouv.fr/fr/datasets/r/eac9a237-0907-45e7-a41e-ff2c171fe10d"
        wget.download(url, file)
    #
    # On le lit en UTF-8 avec pandas
    data_ptz = pd.read_csv(file, sep="\t", error_bad_lines=False, low_memory=False, encoding='cp1252')
    #
    # On supprime toutes les lignes sur lesquelles les communes ne sont pas présentes
    data_ptz_cins = data_ptz.dropna(subset=["cins"])
    #
    # On va ici faire la moyenne des valeurs par communes par années
    # On suppose que pour une commune les habitants suivent les mêmes règles
    result_ptz = pd.DataFrame()
    #
    # On regarde toutes les années
    for year in data_ptz_cins["an"].unique():
        data_year = data_ptz_cins[data_ptz_cins["an"] == year]
        #
        # On regroupe par communes
        result_ptz = result_ptz.append(data_year.groupby("cins").mean().reset_index())
    #
    # On a notre première base de données
    result_ptz = result_ptz.set_index('an').reset_index()
    print(" ==> B.D.D. PTZ END")
    # =================================
    # ==> B.D.D. PTZ
    #
    #
    #
    #
    #
    # ==> B.D.D. COMMUNE/LATITUDE/LONGITUDE
    print(" ==> B.D.D. COMMUNE/LATITUDE/LONGITUDE START")
    # =================================
    #  => base de données qui liste les communes
    #     (cf. https://www.data.gouv.fr/fr/datasets/communes-de-france-base-des-codes-postaux/#resources)
    #        | Nom de la variable | Détails |
    #        |----------|----------|
    #        | code_commune_INSEE | Le code commune INSEE |
    #        | nom_commune_postal | Le nom de la commune en MAJUSCULE |
    #        | code_postal | Le code postal |
    #        | libelle_acheminement | Le libellé d’acheminement |
    #        | ligne_5 | La ligne 5 de l'adresse |
    #        | latitude | la latitude GPS |
    #        | longitude | la longitude GPS |
    #        | code_commune | Le code de la commune |
    #        | article | L'article |
    #        | nom_commune | Le nom de la commune en Minuscule |
    #        | nom_commune_complet | Le nom complet de la commune en Minuscule |
    #        | code_departement | Le code département |
    #        | nom_departement | Le nom du département |
    #        | code_region | Le code région |
    #        | nom_region | Le nom de la région |
    #    NB. Ici on va extraire seulement les coordonnées GPS des communes ayant des données PTZ
    #
    # CODE:
    file = "communes-departement-region.csv"
    #
    # On télécharge si le fichier n'est pas présent
    if not (os.path.isfile(file)):
        url = "https://static.data.gouv.fr/resources/communes-de-france-base-des-codes-postaux/20200309-131459/communes-departement-region.csv"
        wget.download(url, file)
    #
    # On le lit en UTF-8 avec pandas
    communes_data = pd.read_csv(file, encoding='cp1252')
    #
    # On met les communes en entiers (coerce => defaut=NaN)
    communes_data["code_commune_INSEE"] = pd.to_numeric(communes_data["code_commune_INSEE"], errors='coerce')
    #
    # On met les données ptz en entiers pour pouvoir merge les deux DataFrame après
    result_ptz["cins"] = pd.to_numeric(result_ptz["cins"], errors='coerce')
    #
    # On supprime les lignes où les communes ne sont pas renseignées
    communes_data = communes_data.dropna(subset=["code_commune_INSEE"])
    #
    # On renomme la colonne de notre nouvelle base de données comme pout les ptz
    communes_data = communes_data.rename(columns={'code_commune_INSEE': 'cins'})
    #
    # On peut associer le tout
    # Nos ptz ont maintenant une latitude et une longitude pour les localiser facilement
    result_ptz_com = pd.merge(result_ptz, communes_data[["latitude", "longitude", "cins"]], on='cins')
    # =================================
    print(" ==> B.D.D. COMMUNE/LATITUDE/LONGITUDE END")
    # ==> B.D.D. COMMUNE/LATITUDE/LONGITUDE
    #
    #
    #
    #
    #
    # ==> B.D.D. DONNEES CLIMATOLOGIQUES
    print(" ==> B.D.D. DONNEES CLIMATOLOGIQUES START")
    # =================================
    #  => base de données d'observations issues des messages internationaux d’observation en surface (SYNOP)
    #     (cf. https://donneespubliques.meteofrance.fr/?fond=produit&id_produit=90&id_rubrique=32)
    #        | Nom de la variable | Type | Détails |
    #        |----------|----------|----------|
    #        | numer_sta | car | Indicatif OMM station |
    #        | date | car | Date (UTC) |
    #        | t | réel | Température |
    #        | u | réel | Humidité |
    #        | pres | int | Pression station |
    #        | tminsol | réel | Température minimale du sol sur 12 heures |
    #        | etat_sol | int | Etat du sol |
    #        | ht_neige | réel | Hauteur totale de la couche de neige, glace, autre au sol |
    #        | rr24 | réel | Précipitations dans les 24 dernières heures |
    #     NB. On n'a affiché que les valeurs qui nous intéresse et le reste est disponible sur le site:
    #         https://donneespubliques.meteofrance.fr/client/document/doc_parametres_synop_168.pdf
    #
    # CODE: Pour ne pas avoir un fichier trop lourd à charger à chaque fois, ici on va trier la base de données avant
    # de la sauvegarder. Faisons abstraction de notre problème pour se concentrer sur cette base de données,
    # nous la relirons à notre problème plus tard.
    #
    # Si on n'a pas fait ce tri, on le fait
    file = "data_meteo.csv"
    if not (os.path.isfile(file)):
        #
        # On crée une liste de format à télécharger sur internet que l'hébergeur va comprendre
        date = [str(annee) + str(mois) if mois >= 10 else str(annee) + "0" + str(mois)
                for annee in range(1996, 2022) for mois in range(1, 13)]
        #
        # L'URL de téléchargement aura donc le format suivant: start + data[i] + end
        start = "https://donneespubliques.meteofrance.fr/donnees_libres/Txt/Synop/Archive/synop."
        end = ".csv.gz"
        #
        # On enregistre les données dans un dossier car il y en a beaucoup (12 par an, de 1996 à 2021)
        dir_meteo = "synop"
        if not (os.path.isdir(dir_meteo)):
            os.mkdir(dir_meteo)
        #
        # On fait attention à ne pas prendre Novembre et Décembre 2021 qui n'ont pas encore réalisé
        for i in range(len(date) - 2):
            url_telechargement = start + date[i] + end
            file_dir = dir_meteo + "/" + date[i] + ".csv.gz"
            #
            # On vérifie que la date n'a pas déjà été téléchargée auparavant.
            if not (os.path.isfile(file_dir)):
                wget.download(url_telechargement, file_dir)
        print("    ==> B.D.D. DONNEES CLIMATOLOGIQUES DOWNLOADED")
        #
        # Il est maintenant temps de mettre toutes ces données dans une DataFrame
        data_meteo_df = pd.DataFrame()
        #
        # On ne séléctionne que les valeurs que l'on trouve intéressante, on supprime les autres
        list_to_drop = ["tend", "cod_tend", "dd", "ff", "td", "vv", "ww", "w1", "w2", "nbas", "hbas",
                        "cl", "cm", "ch", "tend24", "sw", "tw", "raf10", "rafper", "per", "ssfrai",
                        "perssfrai", "niv_bar", "geop", "rr1", "rr3", "rr6", "phenspe1", "phenspe2",
                        "phenspe3", "phenspe4", "nnuage1", "nnuage2", "nnuage3", "nnuage4", "ctype1",
                        "ctype2", "ctype3", "ctype4", "hnuage1", "hnuage2", "hnuage3", "hnuage4",
                        "Unnamed: 59", "tn12", "tx12", "rr12", "tn24", "tx24", "n", "pmer"]
        #
        # On les charge et les rajoute à data_meteo_df
        for i in range(len(date) - 2):
            file_dir = dir_meteo + "/" + date[i] + ".csv.gz"
            #
            meteo_df = pd.read_csv(file_dir, sep=";")
            #
            # On supprime les colonnes en trop
            meteo_df = meteo_df.drop(columns=list_to_drop)
            #
            # On ajoute les autres
            data_meteo_df = pd.concat([data_meteo_df, meteo_df])
        print("    ==> B.D.D. DONNEES CLIMATOLOGIQUES CONCATENATED")
        #
        # On met des NaN pour les données manquantes
        data_meteo_df = data_meteo_df.replace(["mq"], np.nan)
        #
        # On supprime toutes les lignes où la température est manquante car, c'est un paramètre important
        data_meteo_df = data_meteo_df.dropna(subset=["t"])
        #
        # On met la température sous forme d'entiers
        data_meteo_df["t"] = pd.to_numeric(data_meteo_df["t"], errors='coerce')
        #
        # On met en degrés Celsius
        data_meteo_df["t"] -= 273.15
        #
        # La date est sous un format détaillé (année, mois, jour, heure)
        # On ne veut garder que la date donc, que les quatre premiers caractères
        data_meteo_df["date"] = data_meteo_df["date"].astype(str)
        data_meteo_df["date"] = data_meteo_df["date"].str[:4]
        #
        # On enregistre la base de données déjà triée
        data_meteo_df.to_csv(file, index=False, sep=";")
    data_meteo_df = pd.read_csv(file, ";")
    # =================================
    print(" ==> B.D.D. DONNEES CLIMATOLOGIQUES END")
    # ==> B.D.D. DONNEES CLIMATOLOGIQUES
    #
    #
    #
    #
    #
    # ==> B.D.D. STATION/LATITUDE/LONGITUDE
    print(" ==> B.D.D. STATION/LATITUDE/LONGITUDE START")
    # =================================
    #  => base de données qui va permettre de récupérer les coordonnées des stations
    #     (cf. météo sur le site précédent)
    #        | Nom de la variable | Type | Détails |
    #        |----------|----------|----------|
    #        | ID | int | Indicatif OMM station |
    #        | Nom | car | Nom de la station en MAJUSCULE |
    #        | Latitude | réel | Latitude |
    #        | Longitude | réel | Longitude |
    #        | Altitude | int | Altitude |
    #     NB. On remarque que les coordonnées GPS sont un peu différentes que ci-dessus,
    #         on traitera ce problème dans un instant.
    #
    # CODE:
    file = "stations_synop.csv"
    #
    # On télécharge si le fichier n'est pas présent
    if not (os.path.isfile(file)):
        url = "https://donneespubliques.meteofrance.fr/donnees_libres/Txt/Synop/postesSynop.csv"
        wget.download(url, file)
    #
    stations = pd.read_csv(file, ";")
    #
    # On ignore le nom des stations
    stations = stations.drop(columns=["Nom"])
    #
    # On renomme le nom de la colonne comportant l'ID des stations
    stations = stations.rename(columns={'ID': 'numer_sta'})
    #
    # Le merge est de suite plus simple
    data_st = pd.merge(data_meteo_df, stations, on='numer_sta')
    # =================================
    print(" ==> B.D.D. STATION/LATITUDE/LONGITUDE END")
    # ==> B.D.D. STATION/LATITUDE/LONGITUDE
    #
    #
    #
    #
    #
    # ==> MOYENNE PAR COMMUNES PAR ANNEES
    print(" ==> MOYENNE PAR COMMUNES PAR ANNEES")
    # =================================
    # Toutes nos bases de données ont été téléchargées, on va se concentrer sur leurs exploitations.
    # On fait un nouveau tri pour simplifier nos bases de données.
    # On va faire une moyenne des données météologiques par stations.
    # En effet, la moyenne annuelle va largement suffir pour faire nos observations.
    #
    # CODE:
    # On fait un .groupby() par commune et année
    # On applique la moyenne de chaque paramètre avec la fonction numpy.mean()
    # On supprime l'ID des stations qui est arbitraire pour nous
    data_st = data_st.groupby(["numer_sta", "date"]).aggregate(np.mean).reset_index().drop(columns=["numer_sta"])
    #
    # Par ailleurs, on fait en sorte que les dates coïncident
    # On va avoir des valeurs de 1996 à 2020
    data_st = data_st[data_st["date"] != 2021]
    result_ptz_com = result_ptz_com[result_ptz_com["an"] != 1995]
    # =================================
    # ==> MOYENNE PAR COMMUNES PAR ANNEES
    #
    #
    #
    #
    #
    # ==> RAPPROCHEMENT STATIONS PTZ ET METEO
    print(" ==> RAPPROCHEMENT STATIONS PTZ ET METEO")
    # =================================
    # Le point le plus dur est de rassembler ces deux grosses bases de données. En
    # effet, nous avons remarqué que les ptz et les stations météos ne coïncident pas parfaitement. Cela veut dire
    # que les coordonnées GPS ne sont pas exactement pareilles. On va donc chercher la coordonnée la plus proche de
    # notre émission du PTZ, la différence de climat devrait être négligeable.
    #
    # Plusieurs possibilités s'offrent à nous, on choisit de calculer la distance euclidienne entre les coordonnées.
    # On va donc pour chaque station d'émission de PTZ regarder toutes les stations météo et prendre la plus proche.
    def distance_euclidienne(ptz_lat, ptz_lon, meteo_list_lat, meteo_list_lon):
        """
        Fonction qui calcule la station la plus proche d'une localisation donnée.
        On minimise la distance avec toutes les coordonnées dans la liste en paramètre.

        :param ptz_lat: latitude de la localisation fixée
        :param ptz_lon: longitude de la localisation fixée
        :param meteo_list_lat: liste des latitudes des stations à regarder
        :param meteo_list_lon: liste des longitudes des stations à regarder

        :return: indice de la station la plus proche dans la liste en paramètre
        """
        # On retournera l'indice de la station la plus proche dans ces listes
        meteo_list_lat = list(meteo_list_lat)
        meteo_list_lon = list(meteo_list_lon)
        #
        # Les coordonnées de la station la plus proche
        lat_proche, lon_proche = meteo_list_lat[0], meteo_list_lon[0]
        #
        # L'indice à retourner
        index = 0
        #
        # La distance entre les stations
        distance = np.sqrt((ptz_lat - lat_proche) ** 2 + (ptz_lon - lon_proche) ** 2)
        #
        for i_stat in range(1, len(meteo_list_lat)):
            lat2 = meteo_list_lat[i_stat]
            lon2 = meteo_list_lon[i_stat]
            distance_temp = np.sqrt((ptz_lat - lat2) ** 2 + (ptz_lon - lon2) ** 2)
            #
            if distance_temp < distance:
                distance = distance_temp
                index = i_stat
        return index
    # =================================
    # ==> RAPPROCHEMENT STATIONS PTZ ET METEO
    #
    #
    #
    #
    #
    # ==> FORMAT FINAL
    print(" ==> FORMAT FINAL START")
    # =================================
    # Après toutes ces étapes, on réalise l'étape ultime de la mise en commun.
    file = "all_data.csv"
    if not (os.path.isfile(file)):
        columns_name = list(result_ptz_com.columns) + list(data_st.columns)
        #
        # On supprime les colonnes qui sont en double
        columns_name.remove("date")
        columns_name.remove("Longitude")
        columns_name.remove("Latitude")
        #
        # On crée notre DataFrame avec les noms des colonnes
        all_data = pd.DataFrame(columns=columns_name)
        #
        # On parcourt toute la base de donnée pour appliquer la distance euclidienne
        for i in range(len(result_ptz_com.values)):
            #
            # On fait un petit affichage si c'est long
            if i % 5604 == 0:
                print("    ==> " + str(int(i / 5604) * 10) + "% parcouru")
            #
            # On stocke l'indice de la station la plus proche
            ival = distance_euclidienne(result_ptz_com.values[i][-2],
                                        result_ptz_com.values[i][-1],
                                        data_st[data_st["date"] == result_ptz_com.values[i][0]]["Latitude"],
                                        data_st[data_st["date"] == result_ptz_com.values[i][0]]["Longitude"])
            #
            # On récupère les données météos de la station la plus proche
            station_proc = pd.DataFrame(np.array(data_st[data_st["date"] == result_ptz_com.values[i][0]].drop(
                columns=["date", "Longitude", "Latitude"]))[ival]).T
            #
            # Et la ligne ptz à laquelle la météo correspond
            ptz_i = pd.DataFrame(result_ptz_com.values[i]).T
            #
            # On assemble enfin nos données
            enfin = pd.concat([ptz_i, station_proc], axis=1, join="inner").set_axis(columns_name, axis=1)
            all_data = all_data.append(enfin.reset_index(drop=True))
        print("    ==> 100%")
        #
        # On met bien les index
        all_data = all_data.reset_index(drop=True)
        #
        all_data = all_data.rename(columns={'an': 'year',
                                            'cins': 'commune',
                                            'type': 'type',
                                            'pm2': 'pm2',
                                            'durt': 'duree_ptz',
                                            'vtpz': 'montant_ptz',
                                            'vtpr': 'montant_tot',  # montant_operation
                                            'dtpp': 'duree_pp',  # duree_pret_principal
                                            'vtpp': 'montant_pp',  # montant_pret_principal
                                            'txno': 'taux_nom_pp',  # taux_nominal_pret_principal
                                            'nbsmic': 'nbsmic',
                                            'latitude': 'latitude',
                                            'longitude': 'longitude',
                                            't': 'temperature',
                                            'u': 'humidite',
                                            'pres': 'pression',
                                            'tminsol': 't_sol_min',  # temperature_min_sol
                                            'etat_sol': 'etat_sol',
                                            'ht_neige': 'neige',  # hauteur_neige
                                            'rr24': 'precip_mm',  # precipitation_mm
                                            'Altitude': 'altitude'
                                            })
        # Dernières rectifications
        all_data["t_sol_min"] -= 273.15
        all_data["year"] = all_data["year"].astype(int)
        all_data["commune"] = all_data["commune"].astype(int)
        all_data["altitude"] = all_data["altitude"].astype(int)
        all_data["neige"] = all_data["neige"] * 1000
        all_data.to_csv(file, index=False, sep=";")
    # =================================
    print(" ==> FORMAT FINAL END")
    # ==> FORMAT FINAL
#
# On a fini de générer notre base de données!
# =================================
# ==> INTRODUCTION
#
#
#
#
#
