# Projekt do Informačných systémov
- Prerekvizity: 
  - Python 3.12 
  - Poetry
  - Docker / Docker-Compose


## Tutorial: 
### Docker
 -  docker kontajnery sa vždy ***pri každej zmene musia postaviť***:
    -  `docker compose build`
 -  po vytvorení kontajnerov ich vieme ***spustiť***
     - `docker compose up` 
 -  pre ***rýchle postavenie a sputenie*** kontajnerov vieme použiť buid flag 
    -  `docker compose up --build`
 - ak si nežiadame vidieť logy z dockeru na terminály použijeme ***detach*** flag 
   - `docker compose up -d`

### Databaza - PostgreSQL
  - dockerizovaný PostgreSQL, spúšťa sa spolu zo všetkými kontajnérmi
  - prehlasovacie údaje sú ukladané v .env , ktorý si treba vytvoriť (automaticky z neho docker číta dáta)
  - **príklad**: 
    - POSTGRES_USER=postgres
    - POSTGRES_PASSWORD=your_password
    - POSTGRES_DB=your_db_name
  - ak databáza beží vieme k nej pristupovať pomocou terminálu alebo iného DB nástroju: 
    - **docker exec -it {názov_kontajneru} psql -U {db_user} -d {db_name}**

    - **príklad**: 
      -  `docker exec -it iis_database psql -U postgres -d your_db_name `
### Backend - Python
  - Backend apli
### Frontend