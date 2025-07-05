import pytest
from src.iteration_tracker import IterationTracker, IterationStatus

def test_iteration_tracker_initialization():
    tracker = IterationTracker()
    assert tracker.current_iteration == 0
    assert tracker.status == IterationStatus.INITIALIZED

def test_start_iteration():
    tracker = IterationTracker()
    tracker.start_iteration()
    assert tracker.current_iteration == 1
    assert tracker.status == IterationStatus.IN_PROGRESS

def test_complete_iteration():
    tracker = IterationTracker()
    tracker.start_iteration()
    tracker.complete_iteration()
    assert tracker.status == IterationStatus.COMPLETED

def test_failed_iteration():
    tracker = IterationTracker()
    tracker.start_iteration()
    tracker.complete_iteration(success=False)
    assert tracker.status == IterationStatus.FAILED

def test_max_iterations_limit():
    tracker = IterationTracker(max_iterations=2)
    tracker.start_iteration()  # 1st iteration
    tracker.complete_iteration()
    tracker.start_iteration()  # 2nd iteration
    tracker.complete_iteration()
    
    with pytest.raises(RuntimeError):
        tracker.start_iteration()  # Should raise an error

def test_metadata_management():
    tracker = IterationTracker()
    tracker.start_iteration()
    
    # Add metadata
    tracker.add_metadata('learning_rate', 0.01)
    tracker.add_metadata('batch_size', 32)
    
    # Retrieve metadata
    assert tracker.get_metadata('learning_rate') == 0.01
    assert tracker.get_metadata('batch_size') == 32
    assert tracker.get_metadata('nonexistent', 'default') == 'default'

def test_reset():
    tracker = IterationTracker()
    tracker.start_iteration()
    tracker.add_metadata('test', 'value')
    
    tracker.reset()
    assert tracker.current_iteration == 0
    assert tracker.status == IterationStatus.INITIALIZED
    assert tracker.get_metadata('test') is None