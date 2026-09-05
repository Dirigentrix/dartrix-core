# DARTRIX Core Architecture

DARTRIX Core is a small, deterministic Python kernel. State flows through Touch (input capture), Whisper (context enrichment), Resonance (108 Hz normalization), WolfGuardian (safety gate), and Djinn (output operator). Each stage is independently testable and has no network dependency.

The `State` object carries input, intent, resonance metadata, safety score, confidence, and output.
