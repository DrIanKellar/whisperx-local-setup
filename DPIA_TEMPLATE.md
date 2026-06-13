# DPIA Template: Local Audio Transcription with WhisperX

A starting point for a Data Protection Impact Assessment (DPIA) covering research projects that use locally-run Whisper-based transcription. The structure below is the one used by most UK universities; the exact format your organisation requires may differ. Substitute your organisation's template if you have one. The substance should still be useful as reference text.

Each section lists the standard DPIA question, then an example answer drawn from a real DPIA written for this use case. Adapt the examples to your project.

This template assumes:

- Audio is recorded onto an organisation-managed device.
- Transcription happens entirely locally; no cloud transcription service is used.
- Anonymised transcripts are what get retained; raw audio is destroyed once transcribed.

If any of those assumptions does not hold, your DPIA will need to be different. See the appendix at the bottom.

---

## Step 1: Project details

**Name of project / proposed activity.** The name of your study.

**Description of proposed activity.**

> Example: The aim of this study is to investigate [research question]. Data will be collected via one-to-one interviews / focus groups / workshops with [participant group], lasting approximately [duration]. Interview audio will be transcribed locally using a Python package called WhisperX, which combines the Whisper speech-recognition model with pyannote speaker diarisation. The package runs entirely offline on an organisation-managed device with no internet connection required during processing.

**Project Lead / Principal Investigator.** Name, job title.

**Department Responsible.** Your department or school.

**Background and reason a DPIA was required.**

> Example: The research collects interview audio that will be transcribed using a machine-learning model. The use of machine learning to process audio of identifiable people was flagged by the data protection screening process as requiring a full DPIA. The screening criterion typically triggered is "use of innovative or novel technology to process personal data".

---

## Step 2: Describe the processing

**What type of personal data will be involved?**

> Example: Audio recordings of interview participants are biometric data under UK GDPR and constitute special category personal data. Once transcribed, the audio is destroyed and the transcript is anonymised. Only the anonymised transcript is retained for analysis and storage.

**Will the project involve sensitive / special category personal data?**

> Example: Yes, briefly. Voice recordings are biometric data. The recordings exist only for the time required to transcribe them, after which they are destroyed.

**Who does the personal data relate to?**

> Example: Research participants recruited via [recruitment channel]. The total number expected is approximately [N] individuals.

**Does this include children or other vulnerable groups?**

> Example: [Yes / No, with explanation. If yes, additional safeguards will be required; consult your data protection team.]

**How much data will you be collecting and using?**

> Example: 15 to 20 interviews of approximately one hour each.

**What is the source of the data?**

> Example: Data is collected directly from participants via a digital recorder during in-person or video-conferenced interviews. Participants are informed about the recording before taking part and confirm consent in writing.

**What information will you give data subjects?**

> Example: A Participant Information Sheet (PIS) approved by the relevant ethics committee. The sheet explains what the data will be used for, how it will be processed (specifically including the use of WhisperX for local transcription), how long it will be kept, and the participant's rights. Participants are asked to confirm they are happy with the interview at the end of the session, before the audio is processed.

**Subject Access Requests and right to erasure.**

> Example: Participants may exercise SAR rights up to the point at which their audio has been transcribed and the transcript anonymised. After that point, the audio no longer exists and the transcript cannot be linked back to the individual, so deletion is not technically possible. This boundary is explained on the Participant Information Sheet so participants can make an informed decision before taking part.

**How will you store the data?**

> Example: Audio is held temporarily on an encrypted, organisation-managed drive for the time required to transcribe. Anonymised transcripts are then stored on the same encrypted drive for the duration of the project. Access is restricted to the named research team.

**How long will you retain the data?**

> Example: Audio is destroyed within [N] days of the interview taking place, once transcription is complete and a quality check has been performed. Anonymised transcripts are retained for [your institution's standard retention period, often 10 years] in line with the organisational records management policy, and (where applicable) deposited in an open research repository at the end of the project after a final anonymisation check.

**How will the data be destroyed when no longer required?**

> Example: Audio files are securely deleted from the encrypted drive once transcription is complete. Transcripts are deleted from the encrypted drive at the end of the retention period.

---

## Step 3: Data sharing, processors, and international transfers

**Will you be sharing data with anyone outside the organisation?**

> Example: The final anonymised transcripts will be deposited in an open research repository in line with funder data-sharing requirements at the end of the project. Identifiable raw data is not shared at any point.

**Which IT systems or third parties will be used to store, share, or process the data?**

> Example: The WhisperX Python package is used to transcribe audio. It is installed and run entirely on a locally-managed device. No cloud transcription service is used at any point. Model weights are downloaded once from the Hugging Face Hub during initial setup and are then cached on the local device; no audio or transcript content is sent to Hugging Face or anywhere else during transcription.

**Current state of technology / novelty.**

> Example: Open-source speech-recognition models such as Whisper have been publicly available since 2022 and are widely used in academic and commercial research. Running the model locally on a managed device, with no internet involvement during transcription, is the most privacy-preserving deployment available. No known security flaws apply to the local-only deployment.

**International data transfers.**

> Example: None. Audio and transcripts remain on the organisation's managed infrastructure throughout the project.

**Technical security measures.**

> Example: Audio and transcripts are stored on encrypted organisation storage. Transcripts are pseudonymised at creation and anonymised before any analysis or sharing. Demographic data (job role, department, age, gender, education level) is stored in a separate file with no link to the transcripts, so the combination cannot be used to identify participants.

**How will you ensure that they comply with these measures?**

> Example: The named PI is responsible for ensuring all measures are followed and reviewed at appropriate points during the project.

**Do you have a contract / agreement in place with any third parties?**

> Example: No third-party processors are involved.

---

## Step 4: Consultation process

**How will you seek individuals' views?**

> Example: Participants are fully informed about the methods used in this study via the Participant Information Sheet and have the opportunity to ask questions before consenting.

**Who else do you need to involve within the organisation?**

> Example: [Information Security Team / IT Services / ethics committee — list the consultations you have done.]

**Have you consulted the Information Security Team?**

> Example: Yes.

**Have you recorded the processing activity on your department's Information Asset Register?**

> Example: Yes.

---

## Step 5: Lawful basis for processing

For personal data (Article 6 UK GDPR), the standard basis for university research is:

- **Article 6(1)(e) — Public task.** Research conducted as part of the public research function of the organisation.

For special category data (Article 9 UK GDPR), the standard basis for research with appropriate safeguards is:

- **Article 9(2)(j) — Archiving in the public interest, scientific or historical research, or statistical purposes.** This must be combined with the safeguards required by Article 89(1).

The Article 89(1) safeguards are data minimisation, pseudonymisation where possible, secure storage, and processing for genuinely research-driven purposes. All of these are normally satisfied by the standard research-design practices described elsewhere in this DPIA.

You will also need to identify a condition under Schedule 1 of the Data Protection Act 2018 — typically Condition 4 (research) — and confirm this with your data protection team.

---

## Step 6: Identifying, assessing, and mitigating risks

Risks are normally scored on three dimensions: likelihood (Remote / Possible / Probable), severity (Minimal / Significant / Severe), and overall risk (Low / Medium / High).

### Risk 1: Audio recordings leaked to people outside the research team

- Likelihood: Remote
- Severity: Minimal
- Overall risk: Low
- **Mitigation:** All audio is transferred to the organisation's encrypted drive immediately after recording, and deleted from the digital recorder. Audio is held only for the time required to transcribe it. No copies are ever stored on personal devices or in cloud services. The transcription tool runs entirely offline; no copy is ever sent off the device during processing.
- Residual risk: zero.

### Risk 2: Demographic data combined to identify participants

- Likelihood: Remote
- Severity: Significant
- Overall risk: Low
- **Mitigation:** All data is separated into individual files so combinations cannot be made in practice. Demographic data is stored separately from transcript data; both are pseudonymised with a participant code. No personally identifiable information (such as names or email addresses) is kept.
- Residual risk: zero.

### Additional risks to consider depending on your study design

- **Re-identification through residual content in transcripts** (specific quotes, named places, occupations). Mitigation: anonymisation pass on every transcript before it is stored or shared, with a second pass before publication.
- **Device theft or loss.** Mitigation: full-disk encryption on the host device, organisation-managed device controls.
- **Hallucinated content attributed to a real participant.** Whisper occasionally invents or repeats text. Mitigation: a human quality-check pass on every transcript before it is used for analysis.
- **Hugging Face token leakage.** Mitigation: token stored in an `.env` file outside any version-controlled folder; never committed to a public code repository.

---

## Step 7: Sign off and record outcomes

Complete this section per your organisation's process.

- DPIA Approved (Yes / No)
- Name of Data Protection Team officer
- Date of approval / rejection
- Comments / summary of advice
- DPIA to be kept under review by (name, date of agreement to keep DPIA under review)

If processing is not approved at the first review, follow your organisation's DPO, SIRO, and executive-board escalation route as required.

---

## Appendix: when this template does not apply

This template assumes the case where local Whisper is the answer. If any of the following apply, the case is more complicated and you should talk to your data protection team before adapting this template:

- You plan to send audio to a cloud transcription service at any point in the workflow.
- You plan to share raw (non-anonymised) audio with collaborators at other institutions.
- The audio includes children or other groups requiring additional safeguarding measures.
- The audio includes content that is itself special category data beyond the voice (for example, recorded clinical assessments).
- The project is being delivered as a commercial contract for an external client rather than as part of the public research mission of your institution.
- You plan to retain raw audio for longer than the time required to transcribe and quality-check.
