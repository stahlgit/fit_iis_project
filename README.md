# Projekt do Informačných systémov

- Prerekvizity:
  - Python 3.12
  - Poetry
  - Docker / Docker-Compose

## Tutorial:

### Docker

- docker kontajnery sa vždy **_pri každej zmene musia postaviť_**:
  - `docker compose build`
- po vytvorení kontajnerov ich vieme **_spustiť_**
  - `docker compose up`
- pre **_rýchle postavenie a sputenie_** kontajnerov vieme použiť buid flag
  - `docker compose up --build`
- ak si nežiadame vidieť logy z dockeru na terminály použijeme **_detach_** flag
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
    - `docker exec -it iis_database psql -U postgres -d your_db_name `

### Alembic

- alembic je lightweight nástroj pre migráciu DB. Využíva SQL Alchemy + robím versioning jednotlivých migrácií

#### Základné operácie

- vytvorenie migrácie `alembic revision -m "Popis zmien"`
  - odporúčam s autogenerate flagom výhradne `alembic revision --autogenerate -m "Popis zmien"`, **ALE** je potrebné skontrolovať, či autogenerovanie sa správne vygenerovalo
- aktualizovanie DB `alembic upgrade head` (najnovšia migrácia)
  - prípadne sa dá použiť špecifická migrácia s <revision_id>
- downgrade DN `alembic downgrade -1` (vráti stav DB na predošlý stav)
- história migrácii `alembic history`
- zobrazenie aktuálnej migrácie `alembic curret`

### Backend - Python

- Python aplikáciu vyvájame lokálne so spusteným PyEnvom pomocou Poetry
  - Pri nasadení celej aplikácie bude aj Python dockerizovaný, pre lokálny vývoj to ale nie je potreba
- Ak chceme pridať novú knižnicu, ktorá sa zatiaľ nenachádza v aplikácii použijeme nástroj **Poetry**

#### Poetry

- Poetry je nástroj na správu závislostí a balíčkovanie pre Python
- Poskytuje moderný spôsob správy knižníc a virtuálnych prostredí bez potreby používania requirements.txt (manuálne zapisovanie)alebo samostatných virtuálnych prostredí
- **_Inštalácia závisostí_** - stiahne a nainštaluje všetky knižnice v projekte uvedené v súbore pyproject.toml
  - `poetry install`
- **_Pridanie novej knižnice_** - pridá knižnicu do súboru pyproject.toml
  - `poetry add {knižnica}`
- **_vstup do virtuálneho prostredie Poetry_** - nemalo by to byť potrebné, keďže týmto vsúpime len do jedného kontajneru
  - `poetry shell`

#### FastAPI

- web framework budovanie API pre FE pomocou Pythonu.

#### Swagger (API docs)

- automaticky generuje interaktívnu dokumentáciu pre naše API endpointy.
- Po spustení aplikácie sa dokážeme pripjiť na: http://0.0.0.0:8000/docs, kde je prehľad všetkých dostupných endpointov a ich dokumentácia (JSON reprezentácia)

### Frontend

-
