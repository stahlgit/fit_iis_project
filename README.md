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
 - ak máme súbor/priečinok, ktorý nechceme mať vo vybuildovanej aplikácii je **dôložité tento súbor vložiť do .dockerignore** 

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
  - Python aplikácia je spojaná spolu so zvyškom kontajnerov pomocou docker networkingu 
  - Ak chceme pridať novú knižnicu, ktorá sa zatiaľ nenachádza v aplikácii použijeme nástroj **Poetry**

#### Poetry
  - Poetry je nástroj na správu závislostí a balíčkovanie pre Python
  - Poskytuje moderný spôsob správy knižníc a virtuálnych prostredí bez potreby používania requirements.txt (manuálne zapisovanie)alebo samostatných virtuálnych prostredí
  - ***Inštalácia závisostí*** - stiahne a nainštaluje všetky knižnice v projekte uvedené v súbore pyproject.toml
    - `poetry install`
  - ***Pridanie novej knižnice*** - pridá knižnicu do súboru pyproject.toml
    - `poetry add {knižnica}`
  - ***vstup do virtuálneho prostredie Poetry*** - nemalo by to byť potrebné, keďže týmto vsúpime len do jedného kontajneru 
    - `poetry shell`
#### FastAPI
  - web framework budovanie API pre FE pomocou Pythonu. 
#### Swagger (API docs)
  - automaticky generuje interaktívnu dokumentáciu pre naše API endpointy. 
  - Po spustení aplikácie sa dokážeme pripjiť na: http://0.0.0.0:8000/docs, kde je prehľad všetkých dostupných endpointov a ich dokumentácia (JSON reprezentácia)
### Frontend
  - 