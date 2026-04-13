import sys
import types


def _import_estimator_module():
    deepface_stub = types.ModuleType("deepface")
    deepface_stub.DeepFace = type("DeepFace", (), {"analyze": staticmethod(lambda **_: [])})
    sys.modules.setdefault("deepface", deepface_stub)

    from src import demographic_estimator

    return demographic_estimator


def test_passes_confidence_helper():
    estimator = _import_estimator_module()
    assert estimator._passes_confidence({"face_confidence": 0.95}, 0.9)
    assert not estimator._passes_confidence({"face_confidence": 0.2}, 0.9)
    assert estimator._passes_confidence({"face_confidence": 0.2}, 0.0)


def test_analyze_image_applies_confidence_filter(monkeypatch, tmp_path):
    estimator = _import_estimator_module()
    image_path = tmp_path / "sample.jpg"
    image_path.write_bytes(b"jpg")

    def fake_analyze(**kwargs):
        return [
            {
                "age": 30,
                "dominant_gender": "Man",
                "dominant_race": "white",
                "face_confidence": 0.95,
            },
            {
                "age": 20,
                "dominant_gender": "Woman",
                "dominant_race": "asian",
                "face_confidence": 0.3,
            },
        ]

    monkeypatch.setattr(estimator.DeepFace, "analyze", fake_analyze)

    filtered = estimator.analyze_image(
        image_path, detector_backend="retinaface", min_confidence=0.9
    )
    unfiltered = estimator.analyze_image(
        image_path, detector_backend="retinaface", min_confidence=0.0
    )

    assert len(filtered) == 1
    assert filtered[0]["confidence"] == 0.95
    assert len(unfiltered) == 2
