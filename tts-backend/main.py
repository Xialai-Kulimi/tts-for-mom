from os import getenv, remove, mkdir

from dotenv import load_dotenv

load_dotenv()

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from rich.console import Console
from pydantic import BaseModel
from typing import Literal, Union
from uuid import uuid4
from pathlib import Path
from starlette.responses import FileResponse


console = Console()

app = FastAPI()

output_path = Path("output")

try:
    mkdir(output_path)
except FileExistsError:
    ...

for filepath in output_path.iterdir():
    remove(filepath)


@app.exception_handler(HTTPException)
async def custom_exception_handler(request, exc):
    status_code = 500

    if isinstance(exc, HTTPException):
        status_code = exc.status_code
        return JSONResponse(
            content=Payload.error(str(exc.detail)).model_dump(), status_code=status_code
        )
    return JSONResponse(
        content=Payload.error("未知的錯誤").model_dump(), status_code=status_code
    )


@app.exception_handler(404)
async def not_found_exception_handler(request, exc):
    return JSONResponse(
        content=Payload.error(
            f"未知的路徑或資源 {request.method} {request.url}"
        ).model_dump(),
        status_code=404,
    )


@app.exception_handler(500)
async def unknown_exception_handler(request, exc):
    return JSONResponse(
        content=Payload.error(f"{exc}").model_dump(),
        status_code=500,
    )


@app.exception_handler(405)
async def wrong_method_exception_handler(request, exc):
    return JSONResponse(
        content=Payload.error(
            f"未知的方法 {request.method} {request.url}"
        ).model_dump(),
        status_code=504,
    )


class Payload(BaseModel):
    status: Literal["error", "warning", "success", "info"]
    message: str | None = None
    data: list | dict | str | None = None

    @classmethod
    def success(cls, message: str, data: Union[dict, list] = None):
        return Payload(status="success", message=message, data=data)

    @classmethod
    def info(cls, message: str, data: Union[dict, list] = None):
        return Payload(status="info", message=message, data=data)

    @classmethod
    def warning(cls, message: str, data: Union[dict, list] = None):
        return Payload(status="warning", message=message, data=data)

    @classmethod
    def error(cls, message: str, data: Union[dict, list] = None):
        return Payload(status="error", message=message, data=data)


class SoundPayload(BaseModel):
    text: str
    speed: float
    split: bool = False


from gtts import gTTS
from pydub import AudioSegment


def tts(text: str, speed: float):
    file_id = str(uuid4())
    filename = Path(output_path, f"{file_id}.mp3")
    tts = gTTS(text=text.strip(), lang="zh", slow=False)
    tts.save(filename)
    if speed != 1:
        audio = AudioSegment.from_mp3(open(filename, "rb"))
        speed_audio = audio.speedup(playback_speed=speed)
        speed_audio.export(filename, format="mp3")
    return file_id


allow_list = []


@app.get("/download/{file_id}")
async def download_file(file_id: str):
    if file_id in allow_list:
        return FileResponse(
            Path(output_path, f"{file_id}.mp3"), headers={"Content-Type": "audio/mpeg"}
        )
    return Payload.error("不存在此檔案")


class AudioPair(BaseModel):
    text: str
    fileId: str


def gen_tts(text: str, speed: float):
    file_id = tts(text, speed)
    allow_list.append(file_id)
    while len(allow_list) > 10000:
        old_file_id = allow_list.pop(0)
        remove(Path(output_path, f"{old_file_id}.mp3"))
    return file_id


@app.post("/sound")
async def test_endpoint(payload: SoundPayload):
    console.log(payload)
    if not payload.text:
        return Payload.error("請輸入文字")
    if payload.split:
        return Payload.success(
            "成功建立批次語音",
            [
                AudioPair(text=text, fileId=gen_tts(text, speed=payload.speed)).model_dump()
                for text in payload.text.split("\n")
                if text.strip()
            ],
        )

    else:
        file_id = gen_tts(payload.text, payload.speed)
        return Payload.success("成功建立語音", AudioPair(text=payload.text, fileId=file_id).model_dump())

    # return Payload(status="success", message="成功建立語音", data=str(file_id))


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="127.0.0.1",
        port=int(getenv("PORT", 8000)),
        reload=True,
    )
