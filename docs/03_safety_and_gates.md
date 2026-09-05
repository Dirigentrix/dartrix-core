# Safety and Gates

WolfGuardian is deterministic. `s_non` is clamped to [0, 1]. Values below the soft threshold pass; values at or above the soft threshold produce SOFT_BLOCK; values at or above the hard threshold produce HARD_BLOCK. Confidence is also clamped. Hysteresis lowers the active boundary after a blocked decision, reducing oscillation around thresholds. This library does not claim to replace domain-specific safety review.
