# API Reference

## P Problems Module

### SortingAlgorithms
```python
class SortingAlgorithms:
    def bubble_sort(self, arr: List[int]) -> Tuple[List[int], int]
    def quick_sort(self, arr: List[int]) -> Tuple[List[int], int]
    def merge_sort(self, arr: List[int]) -> Tuple[List[int], int]
    def heap_sort(self, arr: List[int]) -> Tuple[List[int], int]
    def measure_performance(self, algorithm: str, arr_size: int = 1000) -> Dict
