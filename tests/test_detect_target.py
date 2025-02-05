"""
TODO: PointsAndTime
"""
import copy

import cv2
import numpy as np
import pytest

from modules.detect_target import detect_target
from modules import frame_and_time


MODEL_PATH =                    "tests/model_example/yolov8s_ultralytics_pretrained_default.pt"
IMAGE_BUS_PATH =                "tests/model_example/bus.jpg"
IMAGE_BUS_ANNOTATED_PATH =      "tests/model_example/bus_annotated.png"
IMAGE_ZIDANE_PATH =             "tests/model_example/zidane.jpg"
IMAGE_ZIDANE_ANNOTATED_PATH =   "tests/model_example/zidane_annotated.png"


@pytest.fixture()
def detector():
    detector = detect_target.DetectTarget(MODEL_PATH)
    yield detector

@pytest.fixture()
def image_bus():
    image = cv2.imread(IMAGE_BUS_PATH)
    image_bus = frame_and_time.FrameAndTime(image)
    yield image_bus

@pytest.fixture()
def image_zidane():
    image = cv2.imread(IMAGE_ZIDANE_PATH)
    image_zidane = frame_and_time.FrameAndTime(image)
    yield image_zidane


class TestDetector:
    """
    Tests DetectTarget.run()
    """

    def test_single_bus_image(self,
                              detector: detect_target.DetectTarget,
                              image_bus: frame_and_time.FrameAndTime):
        """
        Bus image
        """
        # Setup
        expected = cv2.imread(IMAGE_BUS_ANNOTATED_PATH)
        assert expected is not None

        # Run
        result, actual = detector.run(image_bus)

        # Test
        assert result
        assert actual is not None
        np.testing.assert_array_equal(actual, expected)

    def test_single_zidane_image(self,
                                 detector: detect_target.DetectTarget,
                                 image_zidane: frame_and_time.FrameAndTime):
        """
        Zidane image
        """
        # Setup
        expected = cv2.imread(IMAGE_ZIDANE_ANNOTATED_PATH)
        assert expected is not None

        # Run
        result, actual = detector.run(image_zidane)

        # Test
        assert result
        assert actual is not None
        np.testing.assert_array_equal(actual, expected)

    def test_multiple_zidane_image(self,
                                   detector: detect_target.DetectTarget,
                                   image_zidane: frame_and_time.FrameAndTime):
        """
        Multiple Zidane images
        """
        IMAGE_COUNT = 4

        # Setup
        expected = cv2.imread(IMAGE_ZIDANE_ANNOTATED_PATH)
        assert expected is not None

        input_images = []
        for _ in range(0, IMAGE_COUNT):
            input_image = copy.deepcopy(image_zidane)
            input_images.append(input_image)

        # Run
        outputs = []
        for i in range(0, IMAGE_COUNT):
            output = detector.run(input_images[i])
            outputs.append(output)

        # Test
        for i in range(0, IMAGE_COUNT):
            output: "tuple[bool, np.ndarray | None]" = outputs[i]
            result, actual = output
            assert result
            assert actual is not None
            np.testing.assert_array_equal(actual, expected)
