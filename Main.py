from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from googletrans import Translator
import uvicorn

app = FastAPI()
translator = Translator()

# Drapeaux emoji pour quelques langues
lang_info = {
    "fr": {"name": "French", "flag": "🇫🇷"},
    "en": {"name": "English", "flag": "🇬🇧"},
    "es": {"name": "Spanish", "flag": "🇪🇸"},
    "mg": {"name": "Malagasy", "flag": "🇲🇬"},
    "de": {"name": "German", "flag": "🇩🇪"},
    "ja": {"name": "Japanese", "flag": "🇯🇵"},
    "ko": {"name": "Korean", "flag": "🇰🇷"},
    # Ajouter d'autres langues avec leurs noms complets et drapeaux emoji ici
}

# Définition du modèle de la requête
class TranslationRequest(BaseModel):
    text_to_translate: str
    dest: str

# Fonction pour obtenir les informations sur la langue
def get_language_info(language_code):
    lang = lang_info.get(language_code.lower())
    if lang:
        return f"{lang['flag']} {lang['name']}"
    else:
        return f"Unknown Language ({language_code})"

# Endpoint pour la traduction
@app.post("/translate")
async def translate_text(request: TranslationRequest):
    try:
        translated_text = translator.translate(request.text_to_translate, dest=request.dest)

        # Obtenir les informations sur les langues source et cible
        source_lang = get_language_info(translated_text.src)
        dest_lang = get_language_info(request.dest)

        translation_result = f"{source_lang} ➜ {dest_lang}"

        return {"translation": translated_text.text, "translation_info": translation_result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

@app.get("/ping")
async def healthcheck():
    return {"status": "API is running smoothly"}

# Lancement du serveur
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4555)
