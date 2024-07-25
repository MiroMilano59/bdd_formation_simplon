# Entities and Attributes

**Organismes**

- Nom (String, not nullable)
- Siret (String, primary key, not autoincrement)
- Codes_Info (Abstract)
- Code (String, primary key, not autoincrement)
- Libelle (String, not nullable)
- RNCP_Info (Inherits from Codes_Info)
- Date_Fin (Date, nullable)
- Formacodes_Info (Inherits from Codes_Info)
- RS_Info (Inherits from Codes_Info)
- Date_Fin (Date, nullable)
- NSF_Info (Inherits from Codes_Info)

**Formations**

- Id (Integer, primary key, autoincrement)
- Libelle (String, not nullable)
- Siret_OF (ForeignKey to Organismes.Siret, not nullable)
- Simplon_Id (String, nullable)
- Resume_Programme (String, nullable)

**Sessions**

- Formation_Id (ForeignKey to Formations.Id, not nullable)
- Code_Session (String, not nullable)
- Nom_Dept (String, nullable)
- Code_Dept (Integer, nullable)
- Nom_Region (String, nullable)
- Code_Region (Integer, nullable)
- Ville (String, nullable)
- Date_Debut (Date, nullable)
- Date_Lim_Cand (Date, nullable)
- Duree (String, nullable)
- Alternance (Integer, not nullable, default 0)
- Distanciel (Integer, not nullable, default 0)
- Niveau_Sortie (String, nullable)
- Libelle_Session (String, nullable)
- Statut (Enum('Active', 'Inactive'), not nullable, default 'Active')

**Codes_Formations (Abstract)**

- Formation_Id (ForeignKey to Formations.Id, not nullable)
- RNCP (Inherits from Codes_Formations)
- Code_RNCP (ForeignKey to RNCP_Info.Code, not nullable)

**Formacodes (Inherits from Codes_Formations)**

- Formacode (ForeignKey to Formacodes_Info.Code, not nullable)
- RS (Inherits from Codes_Formations)
- Code_RS (ForeignKey to RS_Info.Code, not nullable)

**NSF (Inherits from Codes_Formations)**

- Code_NSF (ForeignKey to NSF_Info.Code, not nullable)
- RNCP_Formacodes
- Code_RNCP (ForeignKey to RNCP_Info.Code, not nullable)
- Formacode (ForeignKey to Formacodes_Info.Code, not nullable)

**RNCP_Codes_NSF**

- Code_RNCP (ForeignKey to RNCP_Info.Code, not nullable)
- Code_NSF (ForeignKey to NSF_Info.Code, not nullable)

**RS_Formacodes**

- Code_RS (ForeignKey to RS_Info.Code, not nullable)
- Formacode (ForeignKey to Formacodes_Info.Code, not nullable)

**RS_Codes_NSF**

- Code_RS (ForeignKey to RS_Info.Code, not nullable)
- Code_NSF (ForeignKey to NSF_Info.Code, not nullable)

**Relationships**

- Organismes has many Formations (One-to-Many)
- Formations has many Sessions (One-to-Many)
- Formations has many RNCP (One-to-Many)
- Formations has many Formacodes (One-to-Many)
- Formations has many RS (One-to-Many)
- Formations has many NSF (One-to-Many)
- RNCP_Info has many RNCP (One-to-Many)
- Formacodes_Info has many Formacodes (One-to-Many)
- RS_Info has many RS (One-to-Many)
- NSF_Info has many NSF (One-to-Many)
- RNCP_Info has many RNCP_Formacodes (One-to-Many)
- Formacodes_Info has many RNCP_Formacodes (One-to-Many)
- RNCP_Info has many RNCP_Codes_NSF (One-to-Many)
- NSF_Info has many RNCP_Codes_NSF (One-to-Many)
- RS_Info has many RS_Formacodes (One-to-Many)
- Formacodes_Info has many RS_Formacodes (One-to-Many)
- RS_Info has many RS_Codes_NSF (One-to-Many)
- NSF_Info has many RS_Codes_NSF (One-to-Many)