"""
Unit tests for Visualizer.
"""

from models.visualizer import Visualizer


def test_visualizer_init():
    viz = Visualizer()
    assert viz is not None