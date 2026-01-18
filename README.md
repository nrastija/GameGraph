# GameGraph – Sustav za preporuku video igara

GameGraph je web aplikacija za preporuku video igara temeljena na grafičkoj bazi podataka Neo4j i javno dostupnim podacima s RAWG Video Games Database API-ja. Sustav omogućuje pohranu, analizu i preporuku video igara na temelju njihovih atributa i međusobnih odnosa, poput žanrova, oznaka, platformi, razvojnih studija i izdavača.

Projekt je razvijen u Python programskom jeziku i koristi slojevitu arhitekturu koja jasno razdvaja prezentacijski sloj, poslovnu logiku i podatkovni sloj.

---

## Opis sustava

Sustav GameGraph implementira content-based pristup preporukama video igara. Na temelju jedne ili više odabranih igara, sustav analizira sličnosti u grafu (žanrovi, oznake, platforme i ostali povezani entiteti) te predlaže relevantne preporuke korisniku.

Podaci o igrama dohvaćaju se s RAWG platforme i pohranjuju u Neo4j grafičku bazu podataka u normaliziranom obliku.

---

## Tehnologije

- Python 3.11  
- Neo4j Graph Database  
- Neo4j Python Driver  
- NiceGUI (FastAPI, Vue.js, Quasar)  
- RAWG Video Games Database API  
- Requests  
- python-dotenv  

---

## Struktura projekta

```text
gamegraph/
├── api/                 RAWG API klijent
├── database/            Neo4j konekcija i Cypher upiti
├── ui/                  Web sučelje aplikacije
├── scripts/             Skripte za uvoz i obradu podataka
├── tests/               Jedinični i integracijski testovi
├── config.py            Konfiguracija aplikacije
├── main.py              Ulazna točka aplikacije
└── requirements.txt     Popis ovisnosti
```

---

## Preduvjeti

Prije pokretanja sustava potrebno je osigurati sljedeće:

- Instaliran Python 3.11 ili noviji
- Pokrenuta Neo4j baza podataka (lokalno ili udaljeno)
- RAWG API ključ (besplatan račun)
- Git (skidanje i setupanje repozitorija)

---

## Instalacija i postavljanje

### 1. Kloniranje repozitorija:

```bash
git clone https://github.com/your-username/gamegraph.git
cd gamegraph
```

### 2. Instalacija potrebnih ovisnosti:
```bash
pip install -r requirements.txt
```

### 3. Konfiguracija varijabli okoline

U korijenu projekta potrebno je kreirati datoteku .env.py sa sljedećim sadržajem:

```text
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_neo4j_password

RAWG_API_KEY=your_rawg_api_key

DEBUG=True
LOG_LEVEL=INFO
```

### 4. Pokretanje sustava

Web aplikacija pokreće se naredbom:
```bash
python main.py
```
Nakon uspješnog pokretanja, aplikacija je dostupna putem web preglednika na lokalnoj adresi koju ispisuje NiceGUI (zadano http://localhost:8080).

### 5. Uvoz podataka iz RAWG API-ja

Prije korištenja sustava preporuka potrebno je napuniti bazu podataka igrama.

Pokretanje skripte za uvoz:
```bash
python scripts/import_data.py
```
Skripta omogućuje odabir količine podataka za uvoz:

- 100 igara (mali skup podataka)
- 500 igara (srednji skup podataka)
- 1000 igara (veliki skup podataka)
- proizvoljan broj igara

Podaci se privremeno spremaju u lokalni cache kako bi se smanjio broj poziva prema RAWG API-ju.

### 6. Testiranje (opcionalno)

Testovi se nalaze u direktoriju tests/ i mogu se pokrenuti pomoću alata pytest:
```text
pytest
```
Testovi obuhvaćaju provjeru konekcije na Neo4j bazu, komunikaciju s RAWG API-jem i osnovnu logiku preporuka.

Napomene

- Sustav je namijenjen edukativnim i istraživačkim svrhama.
- RAWG API ima ograničenja broja poziva, stoga se preporučuje korištenje cache mehanizma.
- Performanse sustava ovise o količini podataka i dostupnim resursima Neo4j baze podataka.

---

## Korištenje aplikacije

Nakon pokretanja aplikacije korisnik kroz web sučelje može pregledavati dostupne video igre, pretraživati igre po nazivu te pristupiti detaljima pojedine igre. Sustav omogućuje generiranje preporuka na temelju jedne ili više odabranih igara, kao i preporuke temeljene na žanrovima. Sve preporuke generiraju se analizom povezanosti u Neo4j grafičkoj bazi podataka.

## Licenca

Ovaj projekt razvijen je u edukativne svrhe. Slobodno se može koristiti, prilagođavati i proširivati uz navođenje izvora.

