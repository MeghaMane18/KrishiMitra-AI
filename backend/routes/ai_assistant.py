
import os
import io
from fastapi import File, Form, UploadFile

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from groq import Groq

load_dotenv()

router = APIRouter(prefix="/ai", tags=["AI Farming Assistant"])


class QuestionRequest(BaseModel):
    question: str


@router.post("/ask")
def ask_farming_assistant(request: QuestionRequest):
    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Please enter a farming question."
        )

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="Groq API key is not configured."
        )

    try:
        client = Groq(api_key=api_key)

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are KrishiMitra AI, a responsible farming "
                        "assistant for Indian farmers. Answer in simple "
                        "Marathi, using Devanagari script. Give practical "
                        "guidance about crops, irrigation, soil, pests, "
                        "fertilizers, cattle, and fodder. If important "
                        "details are missing, ask follow-up questions. "
                        "Do not invent facts or give unsupported pesticide "
                        "dosages. For serious crop disease or chemical "
                        "treatment, recommend consulting a local "
                        "agricultural officer or KVK."
                    )
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            temperature=0.4,
            max_completion_tokens=800
        )

        answer = response.choices[0].message.content

        return {"answer": answer or "माफ करा, कृपया पुन्हा प्रश्न विचारा."}

    except Exception as e:
        print("Groq AI error:", repr(e))
        raise HTTPException(
            status_code=502,
            detail="AI सेवा सध्या उपलब्ध नाही. कृपया पुन्हा प्रयत्न करा."
        )
    


@router.post("/transcribe")
async def transcribe_farming_question(
    audio: UploadFile = File(...),
    language: str = Form("mr")
):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="Groq API key is not configured."
        )

    try:
        audio_bytes = await audio.read()

        if not audio_bytes:
            raise HTTPException(
                status_code=400,
                detail="Audio recording is empty."
            )

        allowed_languages = {"mr", "hi", "en"}
        if language not in allowed_languages:
            language = "mr"

        client = Groq(api_key=api_key)

        farming_prompt = (
            "Transcribe the speaker's actual words accurately. "
            "The speaker may mix Marathi and English in one sentence. "
            "Write Marathi words in Devanagari script and preserve "
            "English technical terms when spoken in English. "
            "Do not translate, summarize, or rewrite the question. "
            "Farming vocabulary may include soybean, cotton, sugarcane, "
            "soil, irrigation, drip irrigation, NPK, urea, DAP, "
            "fertilizer, pesticide, pests, cattle, cow feed, and milk."
        )

        transcription = client.audio.transcriptions.create(
            file=(
                audio.filename or "farming_question.wav",
                io.BytesIO(audio_bytes),
                audio.content_type or "audio/wav"
            ),
            model="whisper-large-v3",
            language=language,
            prompt=farming_prompt,
            response_format="json",
            temperature=0.0
        )

        recognized_text = (transcription.text or "").strip()

        if not recognized_text:
            raise HTTPException(
                status_code=422,
                detail="आवाज समजला नाही. कृपया पुन्हा स्पष्ट बोला."
            )

        return {"text": recognized_text}

    except HTTPException:
        raise

    except Exception as e:
        print("Groq transcription error:", repr(e))
        raise HTTPException(
            status_code=502,
            detail="आवाज समजला नाही. कृपया पुन्हा प्रयत्न करा."
        )
