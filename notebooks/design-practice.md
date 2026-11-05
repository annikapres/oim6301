```mermaid
erDiagram
    SHOWS {
        int id PK
        string title
        int year
        int episodes
    }
    PEOPLE {
        int id PK
        string name
        int birth
    }
    GENRES {
        int show_id PK, FK
        string genre PK
    }
    STARS {
        int show_id PK, FK
        int person_id PK, FK
    }
    WRITERS {
        int show_id PK, FK
        int person_id PK, FK
    }
    RATINGS {
        int show_id PK, FK
        float rating
        int votes
    }

    SHOWS ||--o{ GENRES : has
    SHOWS ||--o{ STARS : features
    PEOPLE ||--o{ STARS : stars_in
    SHOWS ||--o{ WRITERS : credits
    PEOPLE ||--o{ WRITERS : writes
    SHOWS ||--o| RATINGS : receives
```
