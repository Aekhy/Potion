# Potion

Le but du jeu est de faire des potions !
Vous devrez essayer de comprendres comment les éléments du jeu
intéragissent les uns avec les autres trouver ces précieux elexirs.

Important: Lire "Avant de commencer" pour éviter de perdre votre progression.

## Touches
### Clavier : 
        "o" - ouvrir/fermer le menu d'accueil
        "tab" - ouvrir/fermer le menu de gestion
        "i" - ouvrir/fermer l'inventaire (n'est pas souvent disponible voir pas du tout)
        "echappe" - revenir à la page Chaudron/Outils depuis le menu Chaudron ou le menu Outils (page temporaire)

### Souris :
        cliquer :
            "left click"/"LMB" - Activer l'effet d'un bouton, selectionner un onglet.
        maintenir:
            "left click"/"LMB" - Drag / Tenir UN item
            "right click"/"RMB" - Drag / Tenir le "stack" d'item
        relacher:
            Si vous tenez un item, relacher le bouton pose l'item au niveau de votre curseur. Si l'item ne peut pas être posé à cette endroit, il revient à sa position d'origine.
                        
## Avant de commencer.

    Le système de sauvegarde de ce jeu sauvegarde uniquement les points suivants:

    1. Les items dans votre inventaire
    2. L'état de vos connaissances

    Remarque:
        Si vous déposer un item dans le chaudron, un outils ou tout slot autre qu'un slot de votre inventaire et que vous quitter le jeu, cet item sera perdu.

    Remarque:
        Si le jeu crash, considérez votre progression depuis votre dernière sauvegarde (ie la dernière fois que vous avez fermé le jeu sans crash) perdue.


Lancez le programme.
Vous arrivez sur la page d'accueil.


## Accueil - "o"
    Cliquez sur "JOUER" pour lancer/continuer votre partie.
    Cliquer sur "PARAMETRE" ou "POTION" ne fait rien.
    Cliquez sur "QUITTER" pour sauvegarder et quitter le jeu

    Affiché sur certains menu : "RETOUR AU MENU PRINCIPAL"
    Cliquez pour revenir à ce menu.

    Vous pouvez utiliser les flèches directionnels pour choisir l'option et appuyer sur la touche "ENTREE" pour valider votre choix.



si cliquer sur "JOUER" ne fait rien, réessayer encore une fois.

## Page Chaudron / Outils
    Cette page (qui est temporaire) permet de choisir le menu qu'on souhaite ouvrir.
    Cliquer sur "CHAUDRON" ou "OUTILS"


## Page Chaudron

    La partie 'gauche' laisse place à votre inventaire.
    La partie du 'milieu' (carré rouge) est votre chaudron.
    La partie de 'droite' permet de manipuler les recettes.
    La partie 'en bas à gauche' permet d'aller sur le menu outils en cliquant sur "OUTILS"

## Inventaire

    Votre inventaire est divisé en quatre onglets.
    Chaque onglet contient un certains nombre de pages (d'autres onglet numeroté).
    Chaque page contient une grille de slot pour stoquer vos items.
    Un slot spécifique est dédié à la déstruction d'item. Pour l'utiliser il suffit de déposer
    l'item à détruire dans le slot et de cliquer sur "DETRUIRE L'ITEM"

    Remarque: Pour drop un item dans votre inventaire, vérifier que l'onglet séléctionné (en gris foncé)
    correspond au type de votre item. Si ce n'est pas le cas, l'item retournera à son emplacement d'origine.


### Ingredients
    Contient vos ingredients
### Mixtures
    Contient vos mixtures élémentaires et astrales
### Potions
    Contient vos mixtures étranges, potion raté et finie
### Recettes
    Contient votre papier, vos recette


## Chaudron

    Le Chaudron à pour but de mélanger vos ingredients et/ou vos mixtures astrales/élémentaires
    afin de creer des mixtures étranges ou des potions finies.

    Pour ajouter des choses dans le chaudron, il suffit de drag & drop l'item au dessus du carré rouge.
    Les items que vous pouvez mettre dans le chaudron dépendent de ce qui est déjà présent dans le chaudron
    et de l'item en question.
    Pour récupérer le contenu du chaudron, cliquez sur "FINIR".
    Le résultat apparaitra dans la case au dessus.
    Vous pourrez alors récupérer le contenu avec un drag & drop dans votre inventaire

## Recettes

    Vous pouvez voir une recette dans cette partie.

    Pour voir le contenu d'une recette sans modification, drag & drop une recette dans la case grise
    en dessous de "VISUALISER"
    Ceci affichera toujours le contenu de ce qu'il y a dans cette case.

    Pour écrire / réécrire une recette, drag & drop du papier ou une recette déjà écrite dans la case en dessous de 
    "ECRIRE"
    Sera affiché la recette en cours d'écriture, ie le contenu actuel de votre chaudron (jusqu'a ce que vous récupérer le contenu du chaudron, dans ce cas le contenu précédent restera affiché).

    Vous pouvez placer à tout moment du papier une recette dans les deux cases.

    Important : Comprenez que tout ce qui est dans la case en dessous de "ECRIRE" effacera les données de l'item et repartira avec le contenu du chaudron.

    Remarque : Si vous avez des items dans les deux cases, ce sera l'item dans "VISUALISER" qui sera affiché.

    Remarque : Une recette n'est pas le contenue de votre chaudron. Une fois que vous avez mis la recette dans votre inventaire, n'oubliez pas de récupérer le contenu du chaudron.

## Page Outil

    La partie 'gauche' laisse place à votre inventaire.
    La partie 'droite' répertorie les outils.

### Utiliser un outils
    Vous pouvez drag & drop une mixture (astrale, élémentaire ou étrange) sur un des carré de couleur représentant un outils.
    Si l'item revient à sa position d'origine c'est que l'outil ne peut etre utilise sur celui-ci (c'est le cas si l'on met une mixture
    astrale dans un outils ne fonctionnant que sur des mixtures élémentaires ou inversement)
    Une fois l'item dans l'outils, vous pouvez cliquer sur le texte décrivant l'effet (détaillé plus bas) pour l'appliquer à votre item.
    Celui ci s'affiche alors dans la case grise correspondant à l'outil.


## Ce qu'est une potion
### Etats d'une potion
    Dans ce jeu une potion à trois états possibles :
        1. Une potion finie, elle porte un nom unique et identifiable.
        2. Une potion raté, décrite comme tel.
        3. Une mixture étrange, c'est presque une potion mais il manque un petit quelque chose...
### Composition d'une potion
    Ainsi, une potion finie ou raté est composé de trois éléments :
        1. Une mixture astrale 
        2. Une mixture élémentaire
        3. Une propriété alchimique

        La combinaison de ces trois facteurs détermine le résultat final.

### Mixture astrale/élémentaire   
    Une mixture (astrale ou élémentaire) est un mélange d'ingredient de même type.
    On en obtient en mettant des ingredients dans le chaudron.

    Dans le jeu, vous devrez découvrir quels ingredient font partie de quelle catégorie afin de les mélanger ensemble
    pour creer la mixture souhaité.

### Mixture astrale

    Certains ingredients mélangé ensemble donnerons une mixture astrale.
    Par défault, ce sera la mixture astrale "ORIGINE"
    Avec une combinaison d'ingredient approprié vous obtiendrez une mixture astrale du nom d'une planète.

### Mixture élémentaire

    Certains ingredients mélangé ensemble donnerons une mixture élémentaire.
    Par défault, ce sera la mixture astrale "NEUTRE"
    Avec une combinaison d'ingredient approprié vous obtiendrez une mixture élémentaire du nom d'un élément.

### Effet
    Un effet est l'action d'un outil sur une mixture (astrale, élémentaire ou étrange)
    Un effet est appliquable soit sur une mixture astrale soit sur une mixture élémentaire (pas les deux).
    Un seul effet peut être appliqué par mixture.
    Un effet ne peut pas être retiré.

### Propriété alchimique
    Une propriété alchimique est une combinaison d'un effet d'une mixture astrale et d'un effet d'une mixture élémentaire.
    Toutes les combinaisons correspondent à une propriété alchimique, mais ce ne sera peut etre pas celle qui permettra d'obtenir
    une potion finie.


## Faire une potion
### Première méthode
    Une premiere approche est de creer vos mixtures astrales et élémentaires séparement, de leurs appliquer un effet
    puis de les mélanger dans votre chaudron pour obtenir une potion finie ou raté.

### Seconde méthode
    La seconde méthode consiste à mélanger tous vos ingredients en une seule fois dans le chaudron, vous obtiendrez alors
    une mixture étrange.
    Il reste ensuite à appliquer une propriété alchimique sur celle-ci : pour cela, il faut appliquer une combinaison de deux effets
    à votre mixture étrange. Les effets s'appliqueront directement à la mixture (astrale ou élémentaire) correspondante.
    Vous aurez alors une potion finie, ou raté.

### Quel méthode ?

    La première est plus "longue" mais permet d'avoir une meilleur comprehension des potions et d'obtenir la recette complète.
    La seconde est plus "rapide" mais requiert une meilleure connaissance et ne permet pas d'obtenir la recette complète 
    (en effet, on ne peut pas encore ajouter une recette au outils, on obtient donc une rectte complète en combinant une mixture astrale
    avec effet et une mixture élémentaire avec effet dans le chaudron pendant qu'un papier/recette est entrain d'être écris.)


## Obtenir la bonne mixture astrale/élémentaire

    Chaque ingredient possède des caractéristiques.
    En ajoutant un ingredient, vous ajoutez ces caractéristiques à l'astre/l'élément réprésenté dans votre chaudron.
    Cela vous emmene sur un autre astre/élément ou ne change rien.

    Une connaissance de chaque ingredient permet de savoir quelle caractéristique intéragit avec quelle caractéristiques, vous pourrez
    alors remplacer une combinaison d'ingredients par une autre combinaisons à caractéristique équivalente, ce qui permet de creer une 
    meme potion finie avec plusieurs recettes différentes.


## Trouver la bonne combinaison de mixtures astrales, élémentaire et propriété alchimique

    Sur ce point, il n'y a pour l'instant aucune aide dans le jeu.
    (Vous avez cependant accès au contenu du jeu via ce repository...)