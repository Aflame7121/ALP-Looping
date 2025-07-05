from typing import Optional, Dict, Any
from dataclasses import dataclass, field
from enum import Enum, auto

class IterationStatus(Enum):
    """Enum representing the status of an iteration."""
    INITIALIZED = auto()
    IN_PROGRESS = auto()
    COMPLETED = auto()
    FAILED = auto()

@dataclass
class IterationMetadata:
    """Metadata for tracking iteration details."""
    iteration_number: int = 0
    status: IterationStatus = IterationStatus.INITIALIZED
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    duration: Optional[float] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)

class IterationTracker:
    """
    A comprehensive iteration tracking mechanism for the Adaptive Learning Process.
    
    Tracks iteration count, status, timing, and provides extensible metadata management.
    
    Key Features:
    - Track current iteration number
    - Manage iteration status
    - Record timing and performance metrics
    - Support for additional metadata
    - Error handling and state management
    """
    
    def __init__(self, max_iterations: Optional[int] = None):
        """
        Initialize the iteration tracker.
        
        Args:
            max_iterations (Optional[int]): Maximum number of iterations allowed. 
                                            None means unlimited iterations.
        """
        self._max_iterations = max_iterations
        self._current_iteration = IterationMetadata()
    
    @property
    def current_iteration(self) -> int:
        """Get the current iteration number."""
        return self._current_iteration.iteration_number
    
    @property
    def status(self) -> IterationStatus:
        """Get the current iteration status."""
        return self._current_iteration.status
    
    def start_iteration(self) -> None:
        """
        Start a new iteration, incrementing the iteration count and updating status.
        
        Raises:
            RuntimeError: If max iterations limit is reached.
        """
        # Check iteration limit
        if (self._max_iterations is not None and 
            self._current_iteration.iteration_number >= self._max_iterations):
            raise RuntimeError(f"Maximum iterations ({self._max_iterations}) reached.")
        
        # Increment iteration
        self._current_iteration.iteration_number += 1
        self._current_iteration.status = IterationStatus.IN_PROGRESS
        
        # You could add more complex initialization logic here
    
    def complete_iteration(self, success: bool = True) -> None:
        """
        Mark the current iteration as complete.
        
        Args:
            success (bool): Whether the iteration completed successfully.
        """
        self._current_iteration.status = (
            IterationStatus.COMPLETED if success 
            else IterationStatus.FAILED
        )
    
    def add_metadata(self, key: str, value: Any) -> None:
        """
        Add additional metadata to the current iteration.
        
        Args:
            key (str): Metadata key
            value (Any): Metadata value
        """
        self._current_iteration.additional_data[key] = value
    
    def get_metadata(self, key: str, default: Optional[Any] = None) -> Any:
        """
        Retrieve metadata for the current iteration.
        
        Args:
            key (str): Metadata key
            default (Optional[Any]): Default value if key not found
        
        Returns:
            Any: Metadata value or default
        """
        return self._current_iteration.additional_data.get(key, default)
    
    def reset(self) -> None:
        """Reset the iteration tracker to its initial state."""
        self._current_iteration = IterationMetadata()