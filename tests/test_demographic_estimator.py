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


def test_analyze_video_respects_frame_step_and_confidence(monkeypatch, tmp_path):
    estimator = _import_estimator_module()
    video_path = tmp_path / "sample.mp4"
    video_path.write_bytes(b"mp4")

    frames = ["frame0", "frame1", "frame2"]

    class FakeCapture:
        def __init__(self, video_path_str):
            self.video_path_str = video_path_str
            self.index = 0

        def isOpened(self):
            return True

        def read(self):
            if self.index >= len(frames):
                return False, None
            frame = frames[self.index]
            self.index += 1
            return True, frame

        def release(self):
            return None

    analyzed_frames = []

    def fake_analyze(**kwargs):
        analyzed_frames.append(kwargs["img_path"])
        return {
            "age": 30,
            "dominant_gender": "Man",
            "dominant_race": "white",
            "face_confidence": 0.95,
        }

    monkeypatch.setattr(estimator.cv2, "VideoCapture", FakeCapture)
    monkeypatch.setattr(estimator.cv2, "cvtColor", lambda frame, _: frame)
    monkeypatch.setattr(estimator.DeepFace, "analyze", fake_analyze)

    results = estimator.analyze_video(
        video_path,
        skip_frames=2,
        detector_backend="retinaface",
        min_confidence=0.9,
    )

    assert analyzed_frames == ["frame0", "frame2"]
    assert len(results) == 2
