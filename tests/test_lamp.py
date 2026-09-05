from dartrix_core import AladdinLamp, GateDecision, Intent, WolfGuardian

def test_pipeline_passes_and_resonates():
    output, gate = AladdinLamp().operate("  hello DARTRIX  ", Intent.SUPPORT)
    assert output == "hello DARTRIX"
    assert gate.decision is GateDecision.PASS
    assert gate.s_non == 0.0

def test_guardian_blocks_at_thresholds():
    guardian = WolfGuardian()
    assert guardian.evaluate(.5).decision is GateDecision.SOFT_BLOCK
    assert guardian.evaluate(.9).decision is GateDecision.HARD_BLOCK

def test_intent_enum():
    assert Intent.TRANSFORM.value == "transform"
