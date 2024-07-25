# Data model

**Primary Tables**

**1**- *Organismes*:

Represents training organizations.

- Columns: **Nom** (name), **Siret** (unique identifier, primary key).
- Relationships: **formations** (one-to-many with Formations).


**2****- *Codes_Info*:

- Abstract base class for various code tables.
- Columns: **Code** (primary key), Libelle (label).

**3**- *NCP_Info*, *Formacodes_Info*, *RS_Info*, *NSF_Info*:

- Derived from Codes_Info.
- Each represents different types of codes with specific relationships.

**Core Association Tables**

**4**- *Formations*:

Represents training courses.

- Columns: **Id** (primary key), **Libelle** (label), **Siret_OF** (foreign key to Organismes), and other details.
- Relationships: Various relationships with code tables and Sessions.


**5-** *Sessions*:

Represents training sessions.

- Columns: **Formation_Id** (foreign key to Formations), **Code_Session**, and other session details.
- Relationships: formation (many-to-one with Formations).

**Secondary Association Tables**

**6-** *Codes_Formations*:

- Abstract base class for associations between codes and trainings.
- Columns: **Formation_Id** (foreign key to Formations).

**7-** *RNCP*, *Formacodes*, *RS*, *NSF*:

- Derived from Codes_Formations.
- Each represents associations between Formations and specific code tables.

**Auxiliary Association Tables**

*RNCP_Formacodes*, *RNCP_Codes_NSF*, *RS_Formacodes*, *RS_Codes_NSF*:

- Represents many-to-many relationships between different code tables.
- Columns: Foreign keys to the respective code tables.
- Relationships: Define the relationships between the code tables.