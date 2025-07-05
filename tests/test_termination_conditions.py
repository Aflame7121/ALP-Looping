import pytest
from src.termination_conditions import (
    MaxIterationTerminationCondition, 
    TerminationConditionError
)


def test_max_iteration_termination_condition_initialization():
    """Test initialization of MaxIterationTerminationCondition."""
    condition = MaxIterationTerminationCondition(max_iterations=10)
    assert condition.max_iterations == 10


def test_max_iteration_termination_condition_invalid_initialization():
    """Test invalid initialization raises ValueError."""
    with pytest.raises(ValueError, match="max_iterations must be a positive integer"):
        MaxIterationTerminationCondition(max_iterations=0)
    
    with pytest.raises(ValueError, match="max_iterations must be a positive integer"):
        MaxIterationTerminationCondition(max_iterations=-5)


def test_max_iteration_termination_condition_evaluation():
    """Test termination condition evaluation logic."""
    condition = MaxIterationTerminationCondition(max_iterations=5)
    
    # Test iterations below max
    assert not condition.evaluate(current_iteration=4)
    
    # Test iterations at max
    assert condition.evaluate(current_iteration=5)
    
    # Test iterations beyond max
    assert condition.evaluate(current_iteration=6)


def test_termination_condition_error_handling():
    """Test error handling in termination condition."""
    # Simulate a condition that might raise an unexpected error
    class BrokenTerminationCondition(MaxIterationTerminationCondition):
        def evaluate(self, current_iteration: int, **kwargs):
            raise RuntimeError("Simulated evaluation error")
    
    broken_condition = BrokenTerminationCondition(max_iterations=10)
    
    with pytest.raises(TerminationConditionError) as exc_info:
        broken_condition.evaluate(current_iteration=5)
    
    # Verify exception details
    assert "Error in max iteration termination condition" in str(exc_info.value)
    assert exc_info.value.context.get("current_iteration") == 5