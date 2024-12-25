import os
import shutil
import logging
from typing import List, Tuple, Dict
from collections import Counter
import re
from pathlib import Path

# Setting up configuration for logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


class DataStorage:
    """Key-value storage with basic CRUD operations and logging."""

    def __init__(self):
        self._data: Dict[str, str] = {}
        logging.info("DataStorage initialized")

    def add(self, key: str, value: str) -> None:
        """Add or update a value for given key."""
        self._data[key] = value
        logging.info(f"Added/Updated key: {key}")

    def get(self, key: str) -> str:
        """Retrieve value for given key, return 'Key not found' if missing."""
        value = self._data.get(key, "Key not found")
        logging.info(f"Retrieved key: {key}")
        return value

    def delete(self, key: str) -> None:
        """Remove key-value pair if key exists."""
        if key in self._data:
            del self._data[key]
            logging.info(f"Deleted key: {key}")

    def list(self) -> Dict[str, str]:
        """Return copy of entire storage dictionary."""
        logging.info("Listed all data")
        return self._data.copy()


def find_top_k_frequent_words(text: str, k: int) -> List[Tuple[str, int]]:
    """
    Find k most frequent words in text.

    Args:
        text: Input text string
        k: Number of top frequent words to return

    Returns:
        List of tuples (word, frequency) sorted by frequency
    """
    # Extract words using regex, convert to lowercase
    words = re.findall(r'\b\w+\b', text.lower())

    # Count frequencies and return top k
    return Counter(words).most_common(k)


def check_polygon_collision(polygon1: List[Tuple[float, float]],
                            polygon2: List[Tuple[float, float]]) -> bool:
    """
    Check if two polygons intersect or one contains the other.

    Args:
        polygon1: List of (x, y) coordinates for first polygon
        polygon2: List of (x, y) coordinates for second polygon

    Returns:
        True if polygons collide or overlap, False otherwise
    """

    def point_in_polygon(point: Tuple[float, float],
                         polygon: List[Tuple[float, float]]) -> bool:
        """Ray casting algorithm to check if point is inside polygon."""
        x, y = point
        inside = False
        j = len(polygon) - 1

        for i in range(len(polygon)):
            if ((polygon[i][1] > y) != (polygon[j][1] > y) and
                    x < (polygon[j][0] - polygon[i][0]) * (y - polygon[i][1]) /
                    (polygon[j][1] - polygon[i][1]) + polygon[i][0]):
                inside = not inside
            j = i

        return inside

    def get_edges(polygon: List[Tuple[float, float]]) -> List[Tuple[Tuple[float, float],
    Tuple[float, float]]]:
        """Get list of edges as pairs of points."""
        return [(polygon[i], polygon[(i + 1) % len(polygon)])
                for i in range(len(polygon))]

    def line_segments_intersect(seg1: Tuple[Tuple[float, float], Tuple[float, float]],
                                seg2: Tuple[Tuple[float, float], Tuple[float, float]]) -> bool:
        """Check if two line segments intersect using CCW method."""

        def ccw(A: Tuple[float, float], B: Tuple[float, float],
                C: Tuple[float, float]) -> bool:
            return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

        A, B = seg1
        C, D = seg2
        return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)

    # Check if any point from either polygon is inside the other
    for point in polygon1:
        if point_in_polygon(point, polygon2):
            return True

    for point in polygon2:
        if point_in_polygon(point, polygon1):
            return True

    # Check if any edges intersect
    edges1 = get_edges(polygon1)
    edges2 = get_edges(polygon2)

    return any(line_segments_intersect(edge1, edge2)
               for edge1 in edges1
               for edge2 in edges2)


class FileProcessor:
    """Handle file system operations with logging."""

    @staticmethod
    def copy_directory(source_dir: str, target_dir: str) -> None:
        """
        Copy directory contents recursively.

        Args:
            source_dir: Path to source directory
            target_dir: Path to target directory

        Raises:
            FileNotFoundError: If source directory doesn't exist
        """
        source_path = Path(source_dir)
        target_path = Path(target_dir)

        if not source_path.exists():
            logging.error(f"Source directory not found: {source_dir}")
            raise FileNotFoundError(f"Source directory not found: {source_dir}")

        # Create target directory if it doesn't exist
        target_path.mkdir(parents=True, exist_ok=True)
        logging.info(f"Created/verified target directory: {target_dir}")

        # Copy all contents
        for item in source_path.iterdir():
            target_item = target_path / item.name

            if item.is_dir():
                FileProcessor.copy_directory(str(item), str(target_item))
            else:
                shutil.copy2(str(item), str(target_item))
                logging.info(f"Copied file: {item.name}")

    @staticmethod
    def process_files(directory: str, extensions: List[str]) -> List[Tuple[str, int]]:
        """
        Process files with given extensions and count lines.

        Args:
            directory: Path to directory to process
            extensions: List of file extensions to process (e.g., ['.txt', '.log'])

        Returns:
            List of tuples (filename, line_count)
        """
        result = []
        dir_path = Path(directory)

        # Walk through directory tree
        for file_path in dir_path.rglob('*'):
            if file_path.suffix in extensions:
                try:
                    line_count = sum(1 for _ in file_path.open('r'))
                    result.append((file_path.name, line_count))
                    logging.info(f"Processed file: {file_path.name}")
                except Exception as e:
                    logging.error(f"Error processing {file_path.name}: {str(e)}")

        return result


if __name__ == "__main__":
    # Test DataStorage
    storage = DataStorage()
    storage.add("key1", "value1")
    storage.add("key2", "value2")
    print(storage.list())
    print(storage.get("key1"))
    storage.delete("key1")

    # Test word frequency
    text = "Hello world! Hello everyone. This is a simple test. Test, test, hello."
    print(find_top_k_frequent_words(text, 2))

    # Test polygon collision
    polygon1 = [(0, 0), (4, 0), (4, 4), (0, 4)]
    polygon2 = [(2, 2), (6, 2), (6, 6), (2, 6)]
    print(check_polygon_collision(polygon1, polygon2))

    # Test file operations
    source_dir = "./source_dir"  # Replace with your path
    target_dir = "./target_dir"  # Replace with your path

    try:
        FileProcessor.copy_directory(source_dir, target_dir)
        result = FileProcessor.process_files(source_dir, [".txt", ".log"])
        print(result)
    except FileNotFoundError as e:
        logging.error(f"File operation error: {str(e)}")