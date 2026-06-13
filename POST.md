# Whisper for research audio: running it on your own laptop

If you record interviews for research, you have probably used a cloud transcription tool, or paid someone to do it. There is a third option that nobody mentions: you can run essentially the same speech-recognition technology on your own laptop, free of charge, with no internet involvement at all, and the data protection argument becomes much easier.

This is a short explainer. The actual install lives in the repository linked at the bottom and is a half-day job. The setup script does the heavy lifting.

## Three reasons it is worth doing

**Data protection is much easier.** Recorded voices of identifiable people are biometric data under UK GDPR. They are special category data, alongside health information, political opinions, and religious beliefs. Sending them to a cloud transcription service is allowed but means a third-party contract, questions about where in the world the data is stored, and a harder DPIA conversation. Running the transcription on your own device means the audio never leaves your computer. There is no third party to contract with, no international transfer question, and the DPIA argument essentially writes itself.

**It is free.** No per-minute charges. One-off setup, then unlimited recordings.

**It does not change.** Cloud tools update terms of service, deprecate features, and adjust pricing. A local install does what it did the day you set it up, for as long as you keep using it.

## What you get out

You feed in an audio file. A few minutes later you have a plain text transcript labelled by speaker (Speaker 0, Speaker 1, etc.), a subtitle file with timestamps, and a structured data file with every word's exact timing. On a recent gaming-class laptop, an hour of audio takes about six minutes to process. On a more modest setup, twenty to thirty minutes.

## The DPIA argument, simplified

A DPIA is the form you fill in for any project involving personal data and AI or machine learning. The screening question that catches transcription work is usually phrased as "are you using innovative or novel technology to process personal data". Speech-recognition models qualify, which is why a full DPIA is normally required.

The argument is the same every time, and it is the cleanest case you can make. Audio is recorded onto an organisation-managed device. It moves straight to your encrypted research drive. It is transcribed locally, with no internet connection needed for the processing step. The audio is destroyed as soon as the transcript exists. The transcript is anonymised before anyone analyses it. The combination of "no third party" and "audio destroyed immediately" lands well with Data Protection Officers because it removes most of the categories of risk they would normally have to write about.

The repository includes a generic DPIA template you can adapt, with example answers drawn from a real successful application.

## What the tool is

The tool is called **WhisperX**, written by Max Bain ([github.com/m-bain/whisperX](https://github.com/m-bain/whisperX)). It bundles three open-source pieces together: OpenAI's Whisper speech-recognition model, the faster-whisper runtime, and pyannote for speaker labelling, with word-level timestamp alignment on top. Max's work is what actually does the transcribing. The repository linked below is a Windows installer, a Python entry point, a step-by-step guide, and a generic DPIA template, designed to make WhisperX easier to pick up for researchers who would otherwise bounce off the install pain.

## What installing it actually looks like

The shape of the install is:

1. Install three free pieces of software (Python, ffmpeg, an up-to-date NVIDIA graphics driver). Each is one download from the official site.
2. Run a setup script that does the rest. The script handles the trickier bits — WhisperX 3.8 has a couple of dependency-version traps that would otherwise eat an hour. The script has the right fixes baked in.
3. Create a free Hugging Face account to get an access token for the speaker-labelling model, which is licensed for research use.
4. Run one line to transcribe each recording.

You need a Windows laptop or desktop with an NVIDIA graphics card, ideally with 8 GB of memory or more. Most gaming laptops from the last five years qualify. If you do not have one, your IT department can usually run this on a research server for you; the principle is identical.

The repository README walks through every step in the level of detail required if you have never used a command line before.

## Honest limits

Two things to know.

Whisper occasionally invents words during long silences or unusual audio, and sometimes mishears domain-specific terms (acronyms in particular). A human pass on the transcript before you analyse it is not optional.

Speaker labels (Speaker 0, Speaker 1, and so on) are assigned per file. If you have several recordings from the same focus group, the same person may be labelled differently in each. Matching voices across files is a manual step.

Neither of these is a deal-breaker. They are limits worth knowing about, not reasons to avoid the approach.

## Try it

WhisperX (the actual transcription tool, by Max Bain): https://github.com/m-bain/whisperX

Installer, step-by-step guide, and DPIA template (this repository): https://github.com/DrIanKellar/whisperx-local-setup
