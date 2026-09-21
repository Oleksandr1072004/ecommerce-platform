flowchart TB
    subgraph Clients
        W[Web SPA]
        M[Mobile App]
        A[Admin Panel]
    end

    LB[Load Balancer<br/>Nginx]

    subgraph Backend["Backend API (FastAPI)"]
        API1[API Instance 1]
        API2[API Instance 2]
        API3[API Instance N]
    end

    subgraph Data["Data Layer"]
        CACHE[(Redis<br/>Cache + Sessions)]
        DB[(PostgreSQL<br/>Primary - Writes)]
        REPL[(PostgreSQL<br/>Replica - Reads)]
    end

    subgraph Async["Async Workers (future labs)"]
        Q[(Message Queue<br/>RabbitMQ / Kafka)]
        WK[Workers<br/>emails, reports]
    end

    W --> LB
    M --> LB
    A --> LB
    LB --> API1
    LB --> API2
    LB --> API3

    API1 --> CACHE
    API2 --> CACHE
    API3 --> CACHE

    API1 --> DB
    API2 --> DB
    API3 --> DB

    API1 --> REPL
    API2 --> REPL
    API3 --> REPL

    API1 -.-> Q
    Q -.-> WK
