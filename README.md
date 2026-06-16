# Local Transcriber: step-by-step install for WhisperX

This guide walks you through installing
[WhisperX](https://github.com/m-bain/whisperX) on a Windows PC so you can
transcribe audio files locally, with speaker labels. WhisperX is the work
of Max Bain; this repository contains a Windows installer script, a Python
entry point, a step-by-step guide, and a generic DPIA template, designed
to make WhisperX easier to pick up if you have never used a command line.

**What this is for.** Transcribing research audio (interviews, focus groups,
workshops) on your own computer. The audio never leaves the device.

**What you need.** A Windows PC with an NVIDIA graphics card that has at
least 8 GB of memory. Most gaming laptops from the last five years qualify.
If you are unsure, see [How do I check whether I have a suitable graphics
card?](#how-do-i-check-whether-i-have-a-suitable-graphics-card) at the bottom.

**How long it takes.** About half a working day if you follow the detailed
walkthrough below. About an hour if you just want it working and are
comfortable copy-pasting into a terminal.

---

## The fast version (if you just want it running)

If you do not want a tutorial and just want the commands to copy in order,
this is the whole install. Each line is explained in detail in Parts 1–5
below — come back to those if any step breaks.

```powershell
# 1. PREREQUISITES (do these once, each is a free, official download).
#    https://www.python.org/downloads/release/python-3119/  (tick "Add to PATH")
#    https://www.nvidia.com/Download/index.aspx             (latest driver)
#    Then in an *administrator* PowerShell:
winget install Gyan.FFmpeg

# 2. DOWNLOAD THIS REPO and unzip somewhere sensible:
#    https://github.com/DrIanKellar/whisperx-local-setup → green Code button → Download ZIP

# 3. INSTALL WHISPERX. Open a fresh PowerShell, cd into the unzipped folder, then:
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned   # type Y when prompted
.\setup.ps1                                            # 5–15 minutes, ~3 GB

# 4. HUGGING FACE.
#    a. Make a free account at https://huggingface.co/join
#    b. While signed in, accept the licence on all three pages
#       (click "Agree and access repository" on each):
#         https://huggingface.co/pyannote/segmentation-3.0
#         https://huggingface.co/pyannote/speaker-diarization-community-1
#         https://huggingface.co/pyannote/speaker-diarization-3.1
#    c. Make a Read token at https://huggingface.co/settings/tokens
#    d. Paste it into .env:
copy .env.example .env
notepad .env                                           # replace hf_replace_me with your token

# 5. TRANSCRIBE. Put your audio file in this folder, then:
.\venv\Scripts\Activate.ps1
python transcribe.py "your-audio-file.wav" --min-speakers 2 --max-speakers 8
```

That is the whole install. If you would rather walk through each step with
explanations and screenshots-worth of context, read on.

---

## Part 1: Three free downloads

You need three pieces of software installed before you can use this tool:
Python, ffmpeg, and the NVIDIA driver. Each is a free, official download. You
only do this once.

### 1.1 Install Python 3.11

1. Open your web browser and go to
   **https://www.python.org/downloads/release/python-3119/**
2. Scroll to the bottom of that page, to the section titled "Files".
3. Click **"Windows installer (64-bit)"**. The file downloads.
4. Open the downloaded file.
5. **Important.** At the bottom of the first installer window, tick the box
   that says **"Add python.exe to PATH"**. If you skip this, nothing else
   will work.
6. Click "Install Now". The installer takes about a minute.
7. When it says "Setup was successful", click "Close".

Do not install Python 3.12 or 3.13. The transcription tool only works with
3.11 at the moment.

### 1.2 Install ffmpeg

1. Open the Windows Start menu.
2. Type **PowerShell**.
3. Right-click "Windows PowerShell" in the search results and choose
   **"Run as administrator"**. A dark window opens. Click "Yes" if Windows
   asks for permission.
4. Copy the line below, paste it into the dark window (right-click to paste),
   and press Enter:

   ```powershell
   winget install Gyan.FFmpeg
   ```

5. The installer runs. When it finishes, **close that PowerShell window
   completely** and open a fresh one (normal, not as administrator). This
   refreshes the list of available commands.

### 1.3 NVIDIA driver

The NVIDIA driver is usually already installed if your laptop has an NVIDIA
graphics card. To check it is up to date:

1. Open the Start menu.
2. Type **"NVIDIA"**. If "GeForce Experience" or "NVIDIA Control Panel"
   appears, open it.
3. In GeForce Experience, go to the "Drivers" tab and click "Check for
   updates". Install whatever it offers.
4. If neither app is installed, go to
   **https://www.nvidia.com/Download/index.aspx**, pick your card from the
   dropdowns, and download the latest driver.

### 1.4 Check the three are working

1. Open a new PowerShell window (Start menu → type "PowerShell" → press
   Enter).
2. Copy these three lines, paste them in, and press Enter after each:

   ```powershell
   python --version
   ffmpeg -version
   nvidia-smi
   ```

You want to see:

- Something like `Python 3.11.x` for the first line.
- A long block of text starting with `ffmpeg version` for the second.
- A table showing your NVIDIA card's name for the third.

If any line says "not recognised", that piece of software did not install
correctly. Go back to its section and try again.

---

## Part 2: Download this tool

1. In your web browser, go to
   **https://github.com/DrIanKellar/whisperx-local-setup**
2. Click the green **"Code"** button near the top right.
3. Click **"Download ZIP"** at the bottom of the dropdown.
4. Open the downloaded ZIP file. Drag the folder inside out to a sensible
   location, for example your Documents folder.

You now have a folder containing all the tool's files. Make a note of where
it is; the next step needs the path.

---

## Part 3: Install WhisperX

This step uses the `setup.ps1` file in the folder you just downloaded. The
script does about fifteen minutes of work for you: it installs WhisperX, all
its dependencies, and the GPU-enabled version of PyTorch.

1. Open a new PowerShell window.
2. Type `cd ` (the letters c, d, then a space). Do not press Enter yet.
3. **Drag the folder you just downloaded into the PowerShell window.** It
   automatically types the path for you. Now press Enter.

   The prompt should now show that folder as the current location.

4. Copy these two lines and paste them in, then press Enter:

   ```powershell
   Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
   .\setup.ps1
   ```

5. The first line asks "Do you want to change the execution policy?". Type
   `Y` and press Enter. This is a one-time thing and lets Windows run local
   scripts.

   **If the execution policy is locked by your organisation** (common on
   university or work machines, you will get a "this policy is set by group
   policy" error), you cannot change it. Two ways round it:

   - **Run the script with a one-off bypass** (does not change the system
     setting):

     ```powershell
     powershell -ExecutionPolicy Bypass -File .\setup.ps1
     ```

   - **Or open `setup.ps1` in Notepad, copy its contents, and paste
     directly into PowerShell.** The commands run line by line without any
     script policy applying.

6. The setup script now runs. It will:
   - Check that Python, ffmpeg, and the NVIDIA driver are detected.
   - Create a "virtual environment". This is just a self-contained area for
     the tool, so it does not interfere with anything else on your computer.
   - Download and install WhisperX, faster-whisper, pyannote, and PyTorch.
     This is about 3 GB of downloads. Expect 5 to 15 minutes depending on
     your internet speed.
   - Print a final diagnostic confirming the GPU is detected.

7. When the script finishes, the last block of output should look like:

   ```
   torch:       2.8.0+cu128
   cuda avail:  True
   device:      (your GPU's name)
   ```

   If `cuda avail: True` is there, the install worked. If it says `False`,
   see [Troubleshooting](#troubleshooting).

---

## Part 4: Get a Hugging Face token

This is the one bit that needs an online account. Speaker labelling uses a
model you have to "agree to" before downloading. The model is free and
licensed for research use.

### 4.1 Create the account

1. Go to **https://huggingface.co/join**
2. Sign up with your email. It takes about thirty seconds.

### 4.2 Accept the model licences

While signed in to Hugging Face, visit each of the three pages below and
click the green **"Agree and access repository"** button. Each page updates
to say you have access. All three are free and licensed for research use.

1. **https://huggingface.co/pyannote/segmentation-3.0** — the voice activity
   detection model.
2. **https://huggingface.co/pyannote/speaker-diarization-community-1** —
   the speaker labelling model that current WhisperX uses by default.
3. **https://huggingface.co/pyannote/speaker-diarization-3.1** — an older
   diarisation model. Some versions of WhisperX fall back to this one;
   accept it now and you do not have to think about it later.

Accepting all three takes about a minute and saves you a confusing
authentication error during your first transcription.

### 4.3 Create the token

1. Go to **https://huggingface.co/settings/tokens**
2. Click **"Create new token"**.
3. Name it something like `local-transcriber`.
4. Choose token type **"Read"**. Not Write, not Fine-grained.
5. Click "Create token".
6. The token appears once. **Copy it now** by clicking the copy icon. It
   starts with `hf_`.

### 4.4 Save the token to the project folder

1. Open the project folder in Windows Explorer.
2. Find the file called `.env.example`.
3. Make a copy of it. Rename the copy to `.env` (delete the `.example` from
   the end). If Windows asks you to confirm, click yes.
4. Right-click `.env` and open it with Notepad.
5. Replace the placeholder text `hf_replace_me` with the token you copied.
   The line should look like:

   ```
   HF_TOKEN=hf_yourActualLongTokenHere
   ```

6. Save the file (Ctrl+S) and close.

**Do not share the `.env` file or upload it anywhere public.** It is your
personal access key.

---

## Part 5: Transcribe a recording

1. In a PowerShell window, navigate to the project folder if you are not
   already there (use the `cd` + drag trick from Part 3).
2. Type the following to activate the virtual environment:

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

   The prompt now starts with `(venv)`. This means the tool is ready.

3. Get your audio file ready. You can either:

   - **Copy the audio file into the project folder** (the same folder as
     `transcribe.py`). Then you only need the filename, e.g. `"interview.wav"`.
   - **Or leave it where it is**, and use the file's full address (path).
     The easiest way to get the full address is to find the file in
     Windows Explorer, hold Shift, right-click it, and choose
     **"Copy as path"**. Then paste it into PowerShell — the double quotes
     are already included.

4. Run one of the following, depending on which approach you picked:

   ```powershell
   # If the audio file is in the project folder
   python transcribe.py "interview.wav"

   # If the audio file is elsewhere — paste its full path
   python transcribe.py "C:\Users\You\Documents\interview.wav"
   ```

   Either way, **keep the double quotes around the filename or path** —
   they handle spaces and special characters.

5. **The first time you ever run this**, the tool downloads about 3 GB of
   model files. This takes 5 to 15 minutes. The progress bars are normal.
   Every subsequent run uses the cached copies and starts in seconds.

6. After processing (typical: one minute of audio takes about five to ten
   seconds on a recent GPU), three output files appear in a `transcripts`
   folder inside the project folder:

   - `your-audio-file.txt` — plain text transcript, grouped by speaker.
   - `your-audio-file.srt` — subtitle file with timestamps.
   - `your-audio-file.json` — structured data with word-level timing.

Open the `.txt` file in Notepad to read the transcript.

### Useful options

If you know how many speakers are in the recording, tell the tool. It
improves the labelling noticeably:

```powershell
# Two-speaker interview
python transcribe.py "audio.wav" --min-speakers 2 --max-speakers 2

# Group meeting with somewhere between 3 and 8 speakers
python transcribe.py "audio.wav" --min-speakers 3 --max-speakers 8
```

If the audio is not in English:

```powershell
# Let the tool detect the language for each file
python transcribe.py "audio.wav" --language auto

# Tell it directly: fr for French, de for German, etc.
python transcribe.py "audio.wav" --language fr
```

Type `python transcribe.py --help` to see every option.

---

## Troubleshooting

**The setup script says ffmpeg is not found, but I installed it.** Close the
PowerShell window completely and open a fresh one. ffmpeg needs Windows to
refresh its list of available commands.

**`cuda avail: False` at the end of setup.** The GPU PyTorch install did not
take. With the virtual environment activated, run:

```powershell
pip install --upgrade --force-reinstall --no-deps torch==2.8.0 torchaudio==2.8.0 torchvision==0.23.0 --index-url https://download.pytorch.org/whl/cu128
```

Then run `python -c "import torch; print(torch.cuda.is_available())"` again.
It should now say `True`.

**Diarisation says "0 speakers" or fails with an authentication error.**
Three things to check, in this order:

1. Did you click "Agree and access" on **all three** Hugging Face model
   pages? (`pyannote/segmentation-3.0`,
   `pyannote/speaker-diarization-community-1`, and
   `pyannote/speaker-diarization-3.1`.) If the error message names a
   specific model, that is the one you missed.
2. Did you create a Read-type token (not Write or Fine-grained)?
3. Is the `.env` file in the project folder (not the folder above), named
   exactly `.env` (not `.env.txt`), with the token pasted in correctly?

**Out of memory.** Add `--batch-size 4` (or 2) to the command. Your GPU is
being asked to do too much at once.

**Hallucinated repeating phrases at the end of long files.** Whisper
sometimes loops on silence. Use `--model large-v3-turbo` instead of
`large-v3`; it hallucinates less.

---

## How do I check whether I have a suitable graphics card?

1. Open the Start menu.
2. Type **"Device Manager"** and open it.
3. Expand the line "Display adapters".
4. Look at the names of the items underneath.

If any of them contains "NVIDIA", "GeForce", "RTX", or "GTX", you have a
suitable card. If the only items are "Intel" or "AMD" or "Radeon", you do
not — but your institution may have a research compute server that does, and
the install steps are essentially the same on Linux.

---

## Notes on research data

This toolchain is suitable for use with research interview data when:

- The host computer is an organisation-managed device with full-disk
  encryption.
- A DPIA has been approved before processing begins. See `DPIA_TEMPLATE.md`
  for a starting point you can adapt.
- Audio is held only for the time required to transcribe it and is destroyed
  afterwards.
- Transcripts are pseudonymised at creation and anonymised before any
  analysis or sharing.

For the longer explainer of why and when to use this tool, see `POST.md`.

---

## Credits and licences

This repository (installer scripts, Python wrapper, guides, DPIA template) is
MIT licensed. See `LICENSE`.

The transcription work itself is done by upstream open-source projects, each
downloaded by pip from its official distribution at install time:

- [WhisperX](https://github.com/m-bain/whisperX) by Max Bain — BSD-2-Clause.
- [Whisper](https://github.com/openai/whisper) by OpenAI — MIT.
- [faster-whisper](https://github.com/SYSTRAN/faster-whisper) by SYSTRAN — MIT.
- [pyannote.audio](https://github.com/pyannote/pyannote-audio) by Hervé Bredin and contributors — MIT.
