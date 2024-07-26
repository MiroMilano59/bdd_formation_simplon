# Introduction

SimplonDB is a SQLAlchemy-based ORM (Object-Relational Mapping) framework designed to manage and interact with a database schema for educational and training organizations. This framework includes various models representing different entities and their relationships within the database.


**Primary Tables**: Organismes, Formations, Sessions.

**Code Tables**: RNCP_Info, Formacodes_Info, RS_Info, NSF_Info.

**Association Tables**: RNCP, Formacodes, RS, NSF.

**Auxiliary Association Tables**: RNCP_Formacodes, RNCP_Codes_NSF, RS_Formacodes, RS_Codes_NSF.

These models define a comprehensive schema for managing training organizations, courses, and various associated codes, with relationships and constraints to ensure data integrity.