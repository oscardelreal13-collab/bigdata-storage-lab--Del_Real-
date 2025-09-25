
# en la raíz del repo
mkdir -p src
# mueve los archivos si están en otro sitio
# ej. si están en la raíz y quieres que queden en src:
git mv validate.py src/ 2>/dev/null || true
git mv transform.py src/ 2>/dev/null || true
git mv ingest.py src/ 2>/dev/null || true

# crea __init__.py
printf "# paquete src\n" > src/__init__.py

git add src/__init__.py src/validate.py src/transform.py src/ingest.py || true
git commit -m "chore: add src package and move modules" || true
git push
