# README projet DevOps

Déploiment d'un API Pokedex Pokemon sur AWS (Utilisation de service **Gratuit**).

## Pour commencer

### Pré-requis

- Avoir un compte [Amazon AWS](https://aws.amazon.com/)
    - Avoir un utilisateur **AWS IAM** (Access key & Secret key) avec la permission (**AmazonEC2FullAccess**)
- Avoir votre système d'exploitation sous **Linux** _(Pas obligatoire mais fortement conseillé)_
    - Avoir [Terraform](https://www.terraform.io/) installé sur votre machine
    - Avoir [Python 3](https://www.python.org/) installé sur votre machine
        - Avoir le paquets Ansible d'installé `pip install ansible`

### Connexion depuis le terminal à AWS

    export AWS_ACCESS_KEY_ID="Votre identifiant"
    export AWS_SECRET_ACCESS_KEY="Votre clé secrète"

## Mise en place d'une machine virtuelle sous Ubuntu 22.04

### Recherche de l'AMI ID

> [!NOTE]
> Une Amazon Machine Image (AMI) est une image fournie par AWS qui fournit les informations requises pour lancer une instance.

Lancer la commande ci-dessous pour récupérer l'ami de la version d'Ubuntu 22.04 : 

    aws ec2 describe-images --owners 099720109477 --filters "Name=name,Values=ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*" --query "Images[*].[ImageId,Name]" --region eu-west-3 --output table
    
> *Canonical (distributeur de Ubuntu) id : 099720109477*

> [!WARNING]
> Pensez à changer la variable --region par la region que vous utilisé

Cela retournera un tableau comme ceci :

> [!TIP]
> |        ImageId        |                              Name                              |
> |:----------------------|:---------------------------------------------------------------|
> | ami-00983e8a26e4c9bd9 | ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-20230919 |
> | ami-0e7bc13af71a7ace1 | ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-20240629 |
> | ami-0b61e714d0fd856cc | ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-20230428 |
> | ami-01bfa142c445a5d49 | ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-20231117 |

Copié la première **ImageId** et collé la dans le fichier **main.tf** : `ami = "ImageId"`

### Crée votre clé EC2

Dans votre AWS Console aller dans EC2.
Aller dans le menu vertical à gauche **Network & Security** -> **Key Pairs** puis cliqué sur **Create key pair**.
Nommez votre clé et choisissez le type, **RSA** ou **ED25519** _(ED25519 uniquement pour les instances Linux et Mac)_. 
Sélectionnez le format **.pem**, puis validez la création en cliquant sur **Create key pair**.

Une nouvelle fenêtre va s'ouvrir, vous invitant à sauvegarder la clé dans votre système. 
Placez-la dans le répertoire du projet à l'emplacement suivant : `~/Projet_DevOps/.ssh/` 
et dans le fichier **main.tf** coller le nom ici : `key_name = "Le nom de votre clé sans l'extension"`

>[!IMPORTANT]
> Pour plus de sécurité, il est conseillé de modifier les permissions de votre clé.
>
>     chmod 400 ~/Projet_DevOps/.ssh/<LeNomDeVotreClé.pem>

### Crée un **Security Groups**

Dans votre AWS Console, allez dans EC2. 
Dans le menu vertical à gauche, sélectionnez **Network & Security -> Security Groups** 
puis cliquez sur **Create security group**. 
Remplissez la section **Basic details** comme vous le souhaitez. 

Dans la section **Inbound rules** :
- Ajouter une règle pour accéder à votre service depuis un navigateur internet avec les détails suivants :
    - **Type** : HTTP
    - **Protocole** : TCP
    - **Port** : 80
    - **Source** : Anywhere-IPv4 0.0.0.0/0 _(ou une plage d'IP spécifique si vous voulez restreindre l'accès)_

- Ajouter une autre règle pour accéder à votre Ubuntu serveur depuis un CMD :
    - **Type** -> SSH
    - **Protocole** : TCP _(automatiquement remplie)_
    - **Port** : 22 _(automatiquement remplie)_
    - **Source** : Anywhere-IPv4 0.0.0.0/0 _(pour plus de sécurité, préférez My IP avec votre IP)_

Une fois cela terminé, cliquez sur **Create security group**.

Maintenant que vous avez votre **Security Group**, copiez son **Security group ID** 
et collez-le dans le fichier **main.tf** : `vpc_security_group_ids = ["Security group ID"]`

### Exécution de Terraform

    terraform init
    terraform apply

> [!NOTE]
> Vous devriez avoir en sortie :
> ```
> Outputs:
> 
> instance_ip = "xx.xx.xxx.xxx"
> ```
> Gardez l'ip pour plus tard

## Mise à jour d'Ubuntu et installation de Docker

Pour mettre à jour Ubuntu et installer Docker, il faut exécuter le **playbook Ansible**. 
Mais pour nous faciliter la tâche on va remplire un fichier **inventory**. 

> [!NOTE]
> Un fichier d'inventaire dans Ansible est un fichier qui liste les hôtes (serveurs) sur lesquels Ansible exécutera les tâches définies dans les playbooks.
> Il s'agit d'un élément clé de l'infrastructure d'Ansible, permettant de définir et d'organiser les groupes de serveurs.

### Modifier le fichier "inventory"

Remplire avec votre ip affiché à la suite de l'exécution de la commande `terraform apply` 
Remplacer aussi la position et/ou le nom de votre fichier de clé EC2 crée plus haut.
Le fichier **inventory** doit resembler à cela : 
```
[webserver]
<instance_ip> ansible_user=ubuntu ansible_ssh_private_key_file=~/Projet_DevOps/.ssh/<LeNomDeVotreClé.pem>
```

### Création de l'archive de l'application

Pour déployer l'application sur le serveur, vous devez d'abord créer une archive de celle-ci à l'aide de Docker.

Commencez par vous rendre dans le répertoire de l'application :

    cd app

Ensuite, exécutez la commande suivante pour créer une archive locale de l'application :

    tar -czvf ../app.tar.gz *

Maintenant que l'archive est créée, vous devez vérifier que le chemin dans le fichier **playbook.yml** pointe bien vers l'archive qui sera copiée sur le serveur. 

Pour ce faire, retournez dans le répertoire principal du projet :

    cd ../

Lancez ensuite la commande suivante :

    realpath app.tar.gz

Cette commande vous retournera le chemin complet de l'archive. Ouvrez le fichier **playbook.yml** et vérifiez que la variable src dans l'action intitulée **Copy application archive to the remote host** correspond bien au chemin renvoyé par la commande précédente.

### Exécution du playbook Ansible

Installez la collection **community.docker**:

    ansible-galaxy collection install community.docker

Puis, exécutez le playbook Ansible :

    ansible-playbook -i inventory playbook.yml

## Vérification

Si tout fonctionne correctement, vous devriez pouvoir accéder à la page principale de l'application en entrant l'adresse IP de votre instance `<instance_ip>` dans un navigateur web.
