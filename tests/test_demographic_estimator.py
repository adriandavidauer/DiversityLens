from unittest.mock import patch, MagicMock

from src.demographic_estimator import analyze_image, analyze_video


def _mock_deepface_result():
    return [
        {
            "age": 30,
            "dominant_gender": "Man",
            "dominant_race": "white",
            "face_confidence": 0.95,
            "region": {"x": 0, "y": 0, "w": 100, "h": 100},
        }
    ]


class TestAnalyzeImage:
    def test_nonexistent_file(self):
        result = analyze_image("nonexistent/image.png")
        assert result == []

    @patch("src.demographic_estimator.DeepFace")
    def test_returns_demographics(self, mock_deepface, tmp_path):
        img = tmp_path / "test.png"
        img.write_bytes(b"\x89PNG\r\n\x1a\n")

        mock_deepface.analyze.return_value = _mock_deepface_result()

        result = analyze_image(img)
        assert len(result) == 1
        assert result[0]["age"] == 30
        assert result[0]["gender"] == "Man"
        assert result[0]["race"] == "white"
        assert result[0]["confidence"] == 0.95

    @patch("src.demographic_estimator.DeepFace")
    def test_no_face_detected(self, mock_deepface, tmp_path):
        img = tmp_path / "test.png"
        img.write_bytes(b"\x89PNG\r\n\x1a\n")

        mock_deepface.analyze.return_value = [{"region": {"x": 0, "y": 0, "w": 0, "h": 0}}]

        result = analyze_image(img)
        assert result == []

    @patch("src.demographic_estimator.DeepFace")
    def test_multiple_faces(self, mock_deepface, tmp_path):
        img = tmp_path / "test.png"
        img.write_bytes(b"\x89PNG\r\n\x1a\n")

        mock_deepface.analyze.return_value = _mock_deepface_result() + [
            {
                "age": 25,
                "dominant_gender": "Woman",
                "dominant_race": "asian",
                "face_confidence": 0.88,
            }
        ]

        result = analyze_image(img)
        assert len(result) == 2

    @patch("src.demographic_estimator.DeepFace")
    def test_accepts_string_path(self, mock_deepface, tmp_path):
        img = tmp_path / "test.png"
        img.write_bytes(b"\x89PNG\r\n\x1a\n")
        mock_deepface.analyze.return_value = _mock_deepface_result()

        result = analyze_image(str(img))
        assert len(result) == 1


class TestAnalyzeVideo:
    def test_nonexistent_file(self):
        result = analyze_video("nonexistent/video.mp4")
        assert result == []

    @patch("src.demographic_estimator.cv2")
    @patch("src.demographic_estimator.DeepFace")
    def test_unopenable_video(self, _mock_deepface, mock_cv2, tmp_path):
        vid = tmp_path / "test.mp4"
        vid.write_bytes(b"\x00")

        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = False
        mock_cv2.VideoCapture.return_value = mock_cap

        result = analyze_video(vid)
        assert result == []

    @patch("src.demographic_estimator.cv2")
    @patch("src.demographic_estimator.DeepFace")
    def test_video_analysis(self, mock_deepface, mock_cv2, tmp_path):
        vid = tmp_path / "test.mp4"
        vid.write_bytes(b"\x00")

        mock_cap = MagicMock()
        mock_cap.isOpened.return_value = True
        mock_cap.get.return_value = 30.0
        # Return one frame then stop
        mock_cap.read.side_effect = [
            (True, MagicMock()),
            (False, None),
        ]
        mock_cv2.VideoCapture.return_value = mock_cap
        mock_cv2.COLOR_BGR2RGB = 4
        mock_cv2.cvtColor.return_value = MagicMock()
        mock_cv2.CAP_PROP_FPS = 5

        mock_deepface.analyze.return_value = _mock_deepface_result()

        result = analyze_video(vid, skip_frames=1)
        assert len(result) == 1
        assert result[0]["age"] == 30
