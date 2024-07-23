# README projet DevOps

Déploiment d'un API Pokedex Pokemon sur AWS (Utilisation de service **Gratuit**).

## Pour commencer

### Pré-requis

- Avoir un compte [Amazon AWS](https://aws.amazon.com/fr/)
- Avoir un utilisateur **AWS IAM** (Access key & Secret key) avec la permission (**AmazonEC2FullAccess**)

### Connexion depuis le terminal à AWS

    export AWS_ACCESS_KEY_ID="Votre identifiant"
    export AWS_SECRET_ACCESS_KEY="Votre clé secrète"


## Mise en place d'une machine virtuelle sous Ubuntu 22.04

### Recherche de l'AMI ID

> [!NOTE]
> Une Amazon Machine Image (AMI) est une image fournie par AWS qui fournit les informations requises pour lancer une instance.

Lancer la commande ci-dessous pour récupérer l'ami de la version d'Ubuntu 22.04

*Canonical (distributeur de Ubuntu) id : 099720109477*

    aws ec2 describe-images --owners 099720109477 --filters "Name=name,Values=ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*" --query "Images[*].[ImageId,Name]" --region eu-west-3 --output table

Cela retournera un tableau comme ceci :

> [!TIP]
> |        ImageId        |                              Name                              |
> |----------------------:|----------------------------------------------------------------|
> | ami-00983e8a26e4c9bd9 | ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-20230919 |
> | ami-0e7bc13af71a7ace1 | ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-20240629 |
> | ami-0b61e714d0fd856cc | ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-20230428 |
> | ami-01bfa142c445a5d49 | ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-20231117 |

Copié la première **ImageId** et collé la dans le fichier **main.tf**

## Crée un **Security Groups**

Dans votre AWS Console, allez dans EC2. 
Dans le menu vertical à gauche, sélectionnez **Network & Security -> Security Groups** 
puis cliquez sur **Create security group**. 
Remplissez la section **Basic details** selon vos besoins sans modifier le **VPC**. 
Pour les catégories **Inbound rules** et **Outbound rules**, choisissez **Type -> SSH**. 
La partie **Protocol** et **Port range** sera automatiquement remplie. 
Pour la **Source**, sélectionnez **Anywhere-IPv4**, mais pour plus de sécurité, préférez **My IP**.

Une fois cela terminé, cliquez sur **Create security group**.

Maintenant que vous avez votre **Security Group**, copiez son **Security group ID** 
et collez-le dans le fichier **main.tf**.

## Exécution de Terraform

    terraform init
    terraform apply

## Crée votre clé EC2

Dans votre AWS Console aller dans EC2.
Aller dans le menu vertical à gauche **Network & Security** -> **Key Pairs** puis cliqué sur **Create key pair**.

## Modifier le fichier "inventory"

Remplire avec votre IP affiché à la suite de l'exécution de la commande terraform apply
Remplacer aussi la position de votre fichier de clé EC2 crée plus haut