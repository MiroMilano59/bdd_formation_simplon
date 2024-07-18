# brief_scraping_scrapy

## Contexte
...

## Objectifs
 - ...
 - ...
## Les données à scrapper
...

## Définition du modèle MCD (Modèle Conceptuel des Données)
### Les concepts
La prmière étape consiste à définr notre MCD, nous avons 

```mermaid
---
title: MCD Concepts
---
erDiagram
    Formation {}
    
    Session {}
    
    FormaCode {}
    
    CodeNfs {}

    Organisme {}

    Region {}

    Departement {}

```

### Les attributs
Définition des attributs

```mermaid
---
title: MCD Concepts & Attributs
---
erDiagram
    Formation {
        int IdFormation PK
        str NiveauSortie
        str ResumeProgramme
        int CodeRNCP
        int CodeRS      
    }
    
    Session {
        int IdSession PK
        int IdFormation
        str TypeFormation
        date DateSession
        int CodeDepartement
        int CodeRegion
        str VilleSession
        int IdOrganisme
    }
    
    FormaCode {
        int IdFormation FK
        str FormaCode
    }
    
    CodeNfs {
        int IdFormation FK
        str CodeNfs
    }
    
    Organisme {
        int IdOrganisme
        int SIRET
        str NomOrganisme
        str CodeRegion FK
        str CodeDepartement FK
    }

    Region {
        int CodeRegion PK
        str NomRegion
    }

    Departement {
        int CodeDepartement PK
        str NomDepartement
    }
```


## Les associations
 ****

```mermaid
---
title: MCD Associations
---
erDiagram
    Formation {
        int IdFormation PK
        str NiveauSortie
        str ResumeProgramme
        int CodeRNCP
        int CodeRS      
    }
    
    Session {
        int IdSession PK
        int IdFormation
        str TypeFormation
        date DateSession
        int CodeDepartement
        int CodeRegion
        str VilleSession
        int IdOrganisme
    }
    
    FormaCode {
        int IdFormation FK
        str FormaCode
    }
    
    CodeNfs {
        int IdFormation FK
        str CodeNfs
    }
    
    Organisme {
        int IdOrganisme
        int SIRET
        str NomOrganisme
        str CodeRegion FK
        str CodeDepartement FK
    }

    Region {
        int CodeRegion PK
        str NomRegion
    }

    Departement {
        int CodeDepartement PK
        str NomDepartement
    }
Formation ||--|{ FormaCode : a
Formation ||--|{ CodeNfs : a
Formation ||--o{ Session : ouverte
Session ||--o{ Organisme : par
Organisme ||--|{ Region : au
Organisme ||--|{ Departement : au

```