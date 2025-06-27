# Aquarium

Aquarium is a fish simulation using BOIDS movements written in Python.

## How to launch it

### 🐍 Local launch

```bash
pip install -r requirements.txt
python main.py
```

### 🐳 Docker launch

```bash
docker build -t aquarium
docker run -it --rm aquarium
```
*To show graphic window, Docker must be configured for X11*

## Structure

- `main.py`: Main loop
- `boid.py`: BOIDS entity logic
- `config.py`: General settings

## License

This projet is fully open-source. Check the LICENSE file for further informations.

## Screenshot






