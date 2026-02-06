# Contributing

## How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Development Setup

```bash
# Clone repository
git clone https://github.com/yourusername/weather-transit-analysis.git

# Install dependencies
pip install -r requirements.txt

# Setup database
psql -U postgres -f config/setup_postgres.sql

# Start Airflow
cd airflow && docker-compose up -d
```

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add comments for complex logic
- Write docstrings for functions

## Testing

Run tests before submitting PR:
```bash
python -m pytest tests/
```

## Questions?

Open an issue or contact the maintainers.
