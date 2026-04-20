import httpx # Você precisará instalar: pip install httpx
from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import DocumentStream
from fastapi import FastAPI, UploadFile, File, HTTPException
import io

app = FastAPI()

converter = DocumentConverter()

ALLOWED_EXTENSIONS = {
    ".pdf", ".docx", ".pptx", ".xlsx", 
    ".png", ".jpg", ".jpeg", ".tiff", ".bmp",
    ".html", ".md", ".adoc"
}


@app.post("/converter-url")
async def convert_url(url: str):
    try:
        # 1. A API baixa o arquivo do link
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code != 200:
                raise HTTPException(status_code=400, detail="Não foi possível baixar o arquivo do link.")
            
            conteudo = response.content

        # 2. Processo de conversão idêntico ao anterior
        file_name = url.split("/")[-1].split("?")[0] or "arquivo_remoto"
        content_type = response.headers.get("content-type", "application/octet-stream")
        file_size_mb = len(conteudo) / (1024 * 1024)

        buf = io.BytesIO(conteudo)
        source = DocumentStream(name=file_name, stream=buf)
        
        result = converter.convert(source)
        
        return {
            "data": {
                "name": file_name,
                "type": content_type,
                "size": f"{file_size_mb:.2f} MB"
            },
            "markdown": result.document.export_to_markdown()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro: {str(e)}")