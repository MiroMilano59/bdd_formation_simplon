# Schema

[Here to Display Schema](simplondb.png)

```mermaid
erDiagram

    Organismes {
        String Nom
        String Siret PK
    }

    Codes_Info {
        String Code PK
        String Libelle
    }

    RNCP_Info {
        String Code PK
        String Libelle
        Date Date_Fin
    }

    Formacodes_Info {
        String Code PK
        String Libelle
    }

    RS_Info {
        String Code PK
        String Libelle
        Date Date_Fin
    }

    NSF_Info {
        String Code PK
        String Libelle
    }

    Formations {
        Integer Id PK
        String Libelle
        String Siret_OF FK
        String Simplon_Id
        String Resume_Programme
    }

    Sessions {
        Integer Formation_Id FK
        String Code_Session
        String Nom_Dept
        Integer Code_Dept
        String Nom_Region
        Integer Code_Region
        String Ville
        Date Date_Debut
        Date Date_Lim_Cand
        String Duree
        Integer Alternance
        Integer Distanciel
        String Niveau_Sortie
        String Libelle_Session
        Enum Statut
    }

    RNCP {
        Integer Formation_Id FK
        String Code_RNCP FK
    }

    Formacodes {
        Integer Formation_Id FK
        String Formacode FK
    }

    RS {
        Integer Formation_Id FK
        String Code_RS FK
    }

    NSF {
        Integer Formation_Id FK
        String Code_NSF FK
    }

    RNCP_Formacodes {
        String Code_RNCP FK
        String Formacode FK
    }

    RNCP_Codes_NSF {
        String Code_RNCP FK
        String Code_NSF FK
    }
    
    RS_Formacodes {
        String Code_RS FK
        String Formacode FK
    }

    RS_Codes_NSF {
        String Code_RS FK
        String Code_NSF FK
    }

    Organismes ||--o{ Formations : "formations"
    Formations ||--o{ Sessions : "sessions"
    Formations ||--o{ RNCP : "codes_rncp"
    Formations ||--o{ Formacodes : "formacodes"
    Formations ||--o{ RS : "codes_rs"
    Formations ||--o{ NSF : "codes_nsf"
    RNCP_Info ||--o{ RNCP : "formations"
    Formacodes_Info ||--o{ Formacodes : "formations"
    RS_Info ||--o{ RS : "formations"
    NSF_Info ||--o{ NSF : "formations"
    RNCP_Info ||--o{ RNCP_Formacodes : "formacodes"
    Formacodes_Info ||--o{ RNCP_Formacodes : "codes_rncp"
    RNCP_Info ||--o{ RNCP_Codes_NSF : "codes_nsf"
    NSF_Info ||--o{ RNCP_Codes_NSF : "codes_rncp"
    RS_Info ||--o{ RS_Formacodes : "formacodes"
    Formacodes_Info ||--o{ RS_Formacodes : "codes_rs"
    RS_Info ||--o{ RS_Codes_NSF : "codes_nsf"
    NSF_Info ||--o{ RS_Codes_NSF : "codes_rs"
```