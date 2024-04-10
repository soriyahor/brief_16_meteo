# brief_16_meteo Mateo

## Creation sur Azure

Création d'un registre de conteneur soriyab16 (avec la creation de groupe de ressource grsoriya) sur azure portal

Il faudra installer azure cli via ce lien : 

https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-linux?view=azure-cli-latest&pivots=apt

## S'authentifier sur azure via terminal

```az acr login --name soriyab16 --expose-token```

```docker login soriyab16.azurecr.io  -u 00000000-0000-0000-0000-000000000000 -p token```

## Construction postgres

### image postgres

A la racine du dossier brief_16_meteo, on crée l'image :
```docker build -t postgres -f Dockerfile_postgres . ```

ensuite on le tague :
```docker tag postgres:latest soriyab16.azurecr.io/postgres:latest```

et on le push sur azure :

```docker push soriyab16.azurecr.io/postgres:latest```

### conteneur

Avec un fichier yaml :

``` az container create --resource-group grsoriya --file deploy-postgres.yaml --registry-username soriyab16 --registry-password pwd ```


## Construction batch

### image batch

Dans le dossier functions, on crée l'image :
```docker build -t meteobatch -f Dockerfile_batch . ```

ensuite on le tague :
```docker tag meteobatch:latest soriyab16.azurecr.io/meteobatch:latest```

et on le push sur azure :

```docker push soriyab16.azurecr.io/meteobatch:latest```

### conteneur

On créé l'instance de conteneur sur azure 

## Construction fastfront

1. image fastapi nlp

Obtenir une Key de EdenAI
https://docs.edenai.co/reference/start-your-ai-journey-with-edenai

Dans un fichier config.py, indiquez la clé obtenue auprès de edenai
API_KEY = "xxxxxxxxxxxxxx....xxxxxxxxxxxxxxxxxxx"

Dans le dossier front, on crée l'image :
```docker build -t fastapimeteo -f Dockerfile . ```

ensuite on le tague :
```docker tag fastapimeteo:latest soriyab16.azurecr.io/fastapimeteo:latest```

et on le push sur azure :

```docker push soriyab16.azurecr.io/fastapimeteo:latest```

2. image front

Dans le dossier front, on crée l'image :
```docker build -t frontmeteo -f Dockerfile . ```

ensuite on le tague :
```docker tag frontmeteo:latest soriyab16.azurecr.io/frontmeteo:latest```

et on le push sur azure :

```docker push soriyab16.azurecr.io/frontmeteo:latest```

3. Conteneur fastfront

Pour creer plusieurs conteneurs dans une instance de conteneur :

https://learn.microsoft.com/en-us/azure/container-instances/container-instances-multi-container-yaml

Avec un fichier yaml :

``` az container create --resource-group grsoriya --file deploy-aci.yaml --registry-username soriyab16 --registry-password pwd ```



## executer les instances de conteneurs :

Dans l'ordre :

    1. postgres : connexion à la base de donnée
    2. batch : insertion de données
    3. fastfront : fonctionnement du back-end et front-end

Pour voir les logs :

``` az container attach --resource-group grsoriya --name soriyab16fastfront ```

Fastapi:
http://soriyab16-fastfront.francecentral.azurecontainer.io:8020/docs

Front : 
http://soriyab16-fastfront.francecentral.azurecontainer.io:8001/



