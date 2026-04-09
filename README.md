# Docling Converter API

API para converter documentos em Markdown usando [Docling](https://github.com/DS4SD/docling).

## Formatos suportados

PDF, DOCX, PPTX, XLSX, PNG, JPG, JPEG, TIFF, BMP, HTML, MD, ADOC

## Executando com Docker

```bash
docker build -t docling-converter .
docker run -p 8000:8000 docling-converter
```

## Executando localmente

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Uso

### Endpoint

```
POST /converter
```

Envie um arquivo via `multipart/form-data` no campo `file`.

### Exemplo com curl

```bash
curl -X POST http://localhost:8000/converter \
  -F "file=@documento.pdf"
```

### Resposta

```json
{
  "data": {
    "name": "documento.pdf",
    "type": "application/pdf",
    "size": "1.25 MB"
  },
  "markdown": "# Título do documento\n\nConteúdo convertido..."
}
```

### Documentação interativa

Com o servidor rodando, acesse:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
