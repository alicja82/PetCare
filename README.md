# PetCare

System zarządzania opieką nad zwierzętami domowymi

## Funkcjonalności

- **Autoryzacja użytkowników** - rejestracja i logowanie z JWT
- **Zarządzanie zwierzętami** - CRUD operations, przesyłanie zdjęć
- **Harmonogramy karmienia** - planowanie posiłków dla zwierząt
- **Historia wizyt weterynaryjnych** - śledzenie wizyt i zabiegów
- **Walidacja danych** - sprawdzanie poprawności wprowadzanych danych
- **Testy jednostkowe i integracyjne** - pokrycie testami backend i frontend

## Technologie

### Backend (Flask)
- **Flask** - framework webowy
- **Flask-SQLAlchemy** - ORM do bazy danych
- **Flask-Migrate** - migracje bazy danych
- **Flask-Bcrypt** - hashowanie haseł
- **Flask-JWT-Extended** - autoryzacja JWT
- **Flask-CORS** - obsługa CORS
- **pytest** - testy jednostkowe i integracyjne

### Frontend (Vue 3)
- **Vue 3** - framework JavaScript
- **Pinia** - zarządzanie stanem aplikacji
- **Vue Router** - routing
- **Axios** - komunikacja HTTP
- **Bootstrap 5** - stylowanie UI
- **Vitest** - testy jednostkowe i integracyjne

## Instalacja

### Backend

```bash
cd backend
pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
npm install
```

## Uruchomienie

### Backend

```bash
cd backend
python app.py
```

API będzie dostępne pod adresem: `http://localhost:5000`

### Frontend

```bash
cd frontend
npm run dev
```

Aplikacja będzie dostępna pod adresem: `http://localhost:5173`

## Uruchomienie testów

### Backend

```bash
cd backend
python -m pytest tests/ -v
```

**Testy:**
- 3 testy jednostkowe (AuthService, PetService, ScheduleService)
- 3 testy integracyjne (auth endpoints, pets endpoints, schedule endpoints)

### Frontend

```bash
cd frontend
npm test
```

**Testy:**
- 3 testy jednostkowe (authStore, petStore, scheduleStore)
- 3 testy integracyjne (Pets, Login, Schedules)

## API Endpoints

### Autoryzacja
- `POST /api/auth/register` - rejestracja użytkownika
- `POST /api/auth/login` - logowanie użytkownika
- `GET /api/auth/me` - informacje o zalogowanym użytkowniku

### Zwierzęta
- `GET /api/pets/` - lista zwierząt użytkownika
- `POST /api/pets/` - dodanie nowego zwierzęcia
- `GET /api/pets/<id>` - szczegóły zwierzęcia
- `PUT /api/pets/<id>` - edycja zwierzęcia
- `DELETE /api/pets/<id>` - usunięcie zwierzęcia

### Harmonogramy karmienia
- `GET /api/pets/<id>/schedule` - harmonogramy dla zwierzęcia
- `POST /api/pets/<id>/schedule` - dodanie harmonogramu
- `PUT /api/schedule/<id>` - edycja harmonogramu
- `DELETE /api/schedule/<id>` - usunięcie harmonogramu

### Wizyty weterynaryjne
- `GET /api/pets/<id>/visits` - wizyty dla zwierzęcia
- `POST /api/pets/<id>/visits` - dodanie wizyty
- `PUT /api/visits/<id>` - edycja wizyty
- `DELETE /api/visits/<id>` - usunięcie wizyty

## Architektura

### Service Layer Pattern
Backend wykorzystuje wzorzec Service Layer dla separacji logiki biznesowej od warstwy HTTP:
- **Routes** - obsługa requestów HTTP, walidacja
- **Services** - logika biznesowa, operacje na danych
- **Models** - definicje modeli bazy danych
- **Middlewares** - autoryzacja, weryfikacja własności zasobów

### State Management
Frontend wykorzystuje Pinia do centralnego zarządzania stanem:
- Jeden store na domenę (auth, pets, schedules, visits)
- Akcje async dla komunikacji z API
- Reaktywny stan współdzielony między komponentami

## Zasady

- **SOLID** - separacja odpowiedzialności (Service Layer)
- **DRY** - brak duplikacji kodu
- **Walidacja** - po stronie backendu i frontendu
- **Bezpieczeństwo** - hashowanie haseł, JWT tokens
- **Testowanie** - pokrycie testami unit i integration
