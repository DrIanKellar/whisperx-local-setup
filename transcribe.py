"""
Local transcription with WhisperX + pyannote diarisation.

Usage:
    python transcribe.py path/to/audio.mp3
    python transcribe.py path/to/audio.mp3 --model large-v3-turbo --language en
    python transcribe.py path/to/audio.mp3 --no-diarize
    python transcribe.py path/to/audio.mp3 --min-speakers 2 --max-speakers 4

Outputs (next to the audio file, in an `out/` folder by default):
    <name>.srt    subtitle format with timestamps and speaker labels
    <name>.txt    plain text with [SPEAKER_XX] tags
    <name>.json   full WhisperX result with word-level timing
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import warnings
from pathlib import Path

from dotenv import load_dotenv

# Quiet known cosmetic warnings before any heavy imports.
# Use module= filters where possible since some messages start with a
# newline and `.*` doesn't cross newlines.
warnings.filterwarnings("ignore", module="pyannote.audio.core.io")
warnings.filterwarnings("ignore", module="pyannote.audio.utils.reproducibility")
warnings.filterwarnings("ignore", module="pyannote.audio.models.blocks.pooling")
warnings.filterwarnings("ignore", message=".*TensorFloat-32.*")
warnings.filterwarnings("ignore", message=r".*std\(\):.*")
warnings.filterwarnings("ignore", message=".*degrees of freedom.*")
# Logger silencing — Lightning's checkpoint upgrade and whisperx INFO chatter
for name in (
    "lightning",
    "lightning.pytorch",
    "lightning.pytorch.utilities",
    "lightning.pytorch.utilities.migration",
    "lightning.fabric",
    "pytorch_lightning",
    "pytorch_lightning.utilities",
    "pytorch_lightning.utilities.migration",
    "speechbrain",
    "whisperx",
    "whisperx.asr",
    "whisperx.vads",
    "whisperx.vads.pyannote",
    "whisperx.diarize",
):
    logging.getLogger(name).setLevel(logging.ERROR)

# Defer heavy imports until after argparse so --help is fast
def _lazy_imports():
    import torch
    # Re-enable TF32: pyannote disables it on import for reproducibility;
    # on Ampere+ this is ~20-30% faster on diarisation with no meaningful
    # accuracy cost for ASR/diar work.
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cudnn.allow_tf32 = True
    import whisperx
    return torch, whisperx


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Transcribe + diarise audio locally with WhisperX.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("audio", type=Path, help="Path to audio file (mp3, wav, m4a, etc.)")
    p.add_argument("--model", default="large-v3", help="Whisper model size")
    p.add_argument(
        "--language",
        default="en",
        help="ISO code. Default 'en'. Pass --language auto to autodetect, or e.g. --language fr.",
    )
    p.add_argument("--device", default="cuda", choices=["cuda", "cpu"], help="Compute device")
    p.add_argument(
        "--compute-type",
        default="float16",
        choices=["float16", "float32", "int8", "int8_float16"],
        help="float16 for GPU, int8 for low-VRAM or CPU",
    )
    p.add_argument("--batch-size", type=int, default=16, help="Lower this if you hit OOM")
    p.add_argument("--no-diarize", action="store_true", help="Skip speaker diarisation")
    p.add_argument("--min-speakers", type=int, default=None, help="Hint for diarisation")
    p.add_argument("--max-speakers", type=int, default=None, help="Hint for diarisation")
    p.add_argument(
        "--out-dir",
        type=Path,
        default=None,
        help="Output directory (default: ./out next to the audio file)",
    )
    return p.parse_args()


def fmt_ts(seconds: float) -> str:
    """SRT timestamp format: HH:MM:SS,mmm"""
    if seconds is None:
        seconds = 0.0
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def write_srt(segments: list[dict], path: Path) -> None:
    lines = []
    for i, seg in enumerate(segments, start=1):
        speaker = seg.get("speaker", "")
        text = seg.get("text", "").strip()
        if speaker:
            text = f"[{speaker}] {text}"
        lines.append(str(i))
        lines.append(f"{fmt_ts(seg.get('start'))} --> {fmt_ts(seg.get('end'))}")
        lines.append(text)
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_txt(segments: list[dict], path: Path) -> None:
    lines = []
    current_speaker = None
    for seg in segments:
        speaker = seg.get("speaker", "UNKNOWN")
        text = seg.get("text", "").strip()
        if not text:
            continue
        if speaker != current_speaker:
            if current_speaker is not None:
                lines.append("")
            lines.append(f"[{speaker}]")
            current_speaker = speaker
        lines.append(text)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_json(result: dict, path: Path) -> None:
    path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> int:
    args = parse_args()
    load_dotenv()

    audio_path: Path = args.audio.expanduser().resolve()
    if not audio_path.exists():
        print(f"ERROR: audio not found at {audio_path}", file=sys.stderr)
        return 2

    # Default output: <project>/transcripts/. Override with TRANSCRIPTS_DIR in
    # .env, or --out-dir at the command line.
    default_out = Path(
        os.environ.get("TRANSCRIPTS_DIR") or Path(__file__).resolve().parent / "transcripts"
    )
    out_dir = (args.out_dir or default_out).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = audio_path.stem

    hf_token = os.environ.get("HF_TOKEN")
    if not args.no_diarize and (not hf_token or hf_token == "hf_replace_me"):
        print(
            "ERROR: HF_TOKEN is missing. Put it in .env, or pass --no-diarize.",
            file=sys.stderr,
        )
        return 2

    torch, whisperx = _lazy_imports()

    device = args.device
    if device == "cuda" and not torch.cuda.is_available():
        print("WARN: CUDA not available; falling back to CPU.", file=sys.stderr)
        device = "cpu"
        if args.compute_type in ("float16", "int8_float16"):
            args.compute_type = "int8"

    print(f"Device: {device}  Compute: {args.compute_type}  Model: {args.model}")
    print(f"Audio:  {audio_path}")
    print(f"Out:    {out_dir}")

    # 1. Load audio (resamples to 16k mono)
    audio = whisperx.load_audio(str(audio_path))

    # 2. Transcribe
    print("Transcribing...")
    # asr_options: condition_on_previous_text=False reduces compounding
    # hallucinations on long audio (Whisper sometimes locks onto a phrase
    # and repeats it). suppress_numerals discourages digit hallucinations.
    asr_options = {
        "condition_on_previous_text": False,
        "suppress_numerals": False,
    }
    # `--language auto` means let whisperx detect per file
    lang_arg = None if args.language == "auto" else args.language
    asr_model = whisperx.load_model(
        args.model,
        device,
        compute_type=args.compute_type,
        language=lang_arg,
        asr_options=asr_options,
    )
    result = asr_model.transcribe(audio, batch_size=args.batch_size)
    detected_lang = result.get("language", args.language or "unknown")
    print(f"Detected language: {detected_lang}")
    # Free VRAM before loading the next model
    del asr_model
    if device == "cuda":
        torch.cuda.empty_cache()

    # 3. Align for word-level timestamps
    print("Aligning...")
    try:
        align_model, align_meta = whisperx.load_align_model(
            language_code=detected_lang, device=device
        )
        result = whisperx.align(
            result["segments"],
            align_model,
            align_meta,
            audio,
            device,
            return_char_alignments=False,
        )
        del align_model
        if device == "cuda":
            torch.cuda.empty_cache()
    except Exception as e:
        print(f"WARN: alignment failed ({e}); continuing without word-level timing.")

    # 4. Diarise
    if not args.no_diarize:
        print("Diarising...")
        try:
            from whisperx.diarize import DiarizationPipeline  # whisperx >= 3.1.2
        except ImportError:
            DiarizationPipeline = whisperx.DiarizationPipeline  # older API

        # whisperx 3.8+ uses `token`; older versions use `use_auth_token`
        try:
            diarize_model = DiarizationPipeline(token=hf_token, device=device)
        except TypeError:
            diarize_model = DiarizationPipeline(use_auth_token=hf_token, device=device)
        diar_kwargs = {}
        if args.min_speakers is not None:
            diar_kwargs["min_speakers"] = args.min_speakers
        if args.max_speakers is not None:
            diar_kwargs["max_speakers"] = args.max_speakers
        diarize_segments = diarize_model(audio, **diar_kwargs)
        result = whisperx.assign_word_speakers(diarize_segments, result)

    # 5. Write outputs
    segments = result.get("segments", [])
    srt_path = out_dir / f"{stem}.srt"
    txt_path = out_dir / f"{stem}.txt"
    json_path = out_dir / f"{stem}.json"
    write_srt(segments, srt_path)
    write_txt(segments, txt_path)
    write_json(result, json_path)

    print(f"\nWrote:\n  {srt_path}\n  {txt_path}\n  {json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
