import os
import json
import httpx
from typing import Any, Dict, List, Optional
from fastmcp.exceptions import ToolError
from .models import MinutelyForecastInput, MinutelyForecastOutput, SummaryWindow


def _bool_will_rain(summary_phrase: Optional[str], summaries: List[Dict[str, Any]]) -> bool:
    for s in summaries or []:
        stype = (s.get("Type") or "").upper()
        if (stype == "RAIN" or s.get("TypeId") == 1) and (s.get("CountMinute") or 0) > 0:
            return True
    if summary_phrase:
        p = summary_phrase.lower()
        if "rain" in p or "shower" in p:
            return True
    for s in summaries or []:
        txt = (s.get("MinuteText") or "").lower()
        if "rain" in txt or "shower" in txt:
            return True
    return False

def _first_rain_minute(summaries: List[Dict[str, Any]]) -> Optional[int]:
    best: Optional[int] = None
    for s in summaries or []:
        stype = (s.get("Type") or "").upper()
        if (stype == "RAIN" or s.get("TypeId") == 1) and (s.get("CountMinute") or 0) > 0:
            start = s.get("StartMinute")
            if isinstance(start, int):
                best = start if best is None else min(best, start)
    if best is not None:
        return best
    for s in summaries or []:
        txt = (s.get("MinuteText") or "").lower()
        if "rain" in txt or "shower" in txt:
            start = s.get("StartMinute")
            if isinstance(start, int):
                best = start if best is None else min(best, start)
    return best

def _normalize_summaries(summaries: List[Dict[str, Any]], cutoff_minutes: int) -> List[SummaryWindow]:
    out: List[SummaryWindow] = []
    for s in summaries or []:
        try:
            start = int(s.get("StartMinute", 0))
            end = int(s.get("EndMinute", start))
            count = int(s.get("CountMinute", max(1, end - start + 1)))
            txt = s.get("MinuteText")
        except Exception:
            continue
        if start > cutoff_minutes:
            continue
        end = min(end, cutoff_minutes)
        out.append(SummaryWindow(
            start_minute=start,
            end_minute=end,
            count_minute=count,
            text_template=txt,
        ))
    out.sort(key=lambda w: (w.start_minute, w.end_minute))
    return out

async def get_minutely_forecast(req: MinutelyForecastInput) -> MinutelyForecastOutput:
    key = os.getenv("ACCUWEATHER_API_KEY")
    url = os.getenv("ACCUWEATHER_API_URL") 
    if not key or not url:
        raise ToolError("Defina ACCUWEATHER_API_KEY e ACCUWEATHER_API_URL")

    params = {"q": f"{req.lat},{req.lon}", "apikey": key}

    last_exc: Optional[Exception] = None
    for attempt in (1, 2):
        try:
            async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
                r = await client.get(
                    url,
                    params=params,
                    headers={"Accept": "application/json"},
                )
            status = r.status_code
            ctype = (r.headers.get("content-type") or "").lower()
            body_preview = (r.text or "")[:400].replace("\n", " ")
            diag = f"status={status} ctype={ctype} len={len(r.content)} url={getattr(r.request, 'url', '<n/a>')}"

            if status >= 400 or not r.content:
                if attempt == 1:
                    last_exc = ToolError(f"AccuWeather sem payload utilizável ({diag}). Body: {body_preview!r}")
                    continue
                raise ToolError(f"AccuWeather sem payload utilizável ({diag}). Body: {body_preview!r}")

            if "application/json" not in ctype:
                if attempt == 1:
                    last_exc = ToolError(f"AccuWeather retornou conteúdo não-JSON ({diag}). Body: {body_preview!r}")
                    continue
                raise ToolError(f"AccuWeather retornou conteúdo não-JSON ({diag}). Body: {body_preview!r}")

            try:
                data = r.json()
            except json.JSONDecodeError as e:
                if attempt == 1:
                    last_exc = ToolError(f"JSON inválido do AccuWeather ({diag}). Erro: {e}. Body: {body_preview!r}")
                    continue
                raise ToolError(f"JSON inválido do AccuWeather ({diag}). Erro: {e}. Body: {body_preview!r}")

            summary = data.get("Summary") or {}
            summaries = data.get("Summaries") or []

            phrase = summary.get("Phrase")
            will_rain = _bool_will_rain(phrase, summaries)
            rain_start = _first_rain_minute(summaries)
            windows = _normalize_summaries(summaries, cutoff_minutes=req.minutes)

            return MinutelyForecastOutput(
                lat=req.lat,
                lon=req.lon,
                will_rain=bool(will_rain),
                rain_start_in_min=rain_start,
                phrase=phrase,
                summaries=windows,
                confidence=0.7,
            )
        except httpx.RequestError as e:
            last_exc = ToolError(f"Erro de rede ao chamar AccuWeather: {e.__class__.__name__}: {e}")
            if attempt == 2:
                raise last_exc

    if last_exc:
        raise last_exc
    raise ToolError("Falha desconhecida ao obter previsão por minuto (sem exceção capturada).")