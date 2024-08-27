### Working Notes

Create migrations:
```bash
flask --app backend.app db migrate --rev-id $(ls backend/migrations/versions | wc -1) -m"Linking between Players and Users" -d "backend/migrations"
```