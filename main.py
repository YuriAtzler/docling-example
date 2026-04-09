from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import DocumentStream
from fastapi import FastAPI, UploadFile, File, HTTPException
import io

app = FastAPI()

ALLOWED_EXTENSIONS = {
    ".pdf", ".docx", ".pptx", ".xlsx", 
    ".png", ".jpg", ".jpeg", ".tiff", ".bmp",
    ".html", ".md", ".adoc"
}

@app.post("/converter")
async def convert(file: UploadFile = File(...)):
    file_name = file.filename.lower()
    extension = f".{file_name.split('.')[-1]}" if "." in file_name else ""
    
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400, 
            detail=f"Extensão {extension} não suportada. Use: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    content = await file.read()
    file_size_mb = len(content) / (1024 * 1024)
    
    try:
        buf = io.BytesIO(content)
        source = DocumentStream(name=file.filename, stream=buf)
        
        converter = DocumentConverter()
        result = converter.convert(source)
        
        return {
            "data": {
                "name": file.filename,
                "type": file.content_type,
                "size": f"{file_size_mb:.2f} MB"
            },
            "markdown": result.document.export_to_markdown()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao converter documento: {str(e)}")