"""
Generate visual test artifacts for all components.
Run with: python tests/generate_artifacts.py
"""
import os
import sys
from PIL import Image, ImageFont, ImageDraw

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Mock the meteocons font BEFORE importing weather module
class MockFont:
    """Mock font class for testing when actual font files aren't available."""
    def __init__(self, path, size):
        self.path = path
        self.size = size
        # Use a default font as fallback
        try:
            self.font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
        except:
            self.font = ImageFont.load_default()
    
    def getbbox(self, text, *args, **kwargs):
        return self.font.getbbox(text, *args, **kwargs)
    
    def getlength(self, text, *args, **kwargs):
        return self.font.getlength(text, *args, **kwargs)
    
    def getmetrics(self, *args, **kwargs):
        return self.font.getmetrics(*args, **kwargs)
    
    def getmask(self, text, *args, **kwargs):
        return self.font.getmask(text, *args, **kwargs)
    
    def __getattr__(self, name):
        # Delegate all other attributes to the underlying font
        return getattr(self.font, name)


# Create mock font instance
mock_icon_font = MockFont("./meteocons.ttf", 36)

# Patch ImageFont.truetype to return our mock for meteocons
original_truetype = ImageFont.truetype

def patched_truetype(font_path, size, *args, **kwargs):
    if "meteocons" in font_path:
        return mock_icon_font
    return original_truetype(font_path, size, *args, **kwargs)

ImageFont.truetype = patched_truetype

# Now import the components
from components.sensor import Sensor
from components.todo import Todo
from components.weather import Weather


# Test display dimensions (from config.example.toml)
DISPLAY_WIDTH = 250
DISPLAY_HEIGHT = 122
DISPLAY_DIMENSIONS = (DISPLAY_WIDTH, DISPLAY_HEIGHT)

# Output directory for test artifacts
ARTIFACT_DIR = os.path.join(os.path.dirname(__file__), 'artifacts')


# Mock classes for testing
class MockEntity:
    """Mock Home Assistant entity for testing."""
    def __init__(self, state, attributes=None):
        self.state = state
        self.attributes = attributes or {}


class MockClient:
    """Mock Home Assistant client for testing."""
    def get_state(self, entity_id):
        return MockEntity("21.5", {"friendly_name": "Temperature"})


class MockTodoDomain:
    """Mock todo domain for testing."""
    def __init__(self):
        self.get_items = MockGetItems()
        self.update_item = MockUpdateItem()


class MockGetItems:
    """Mock get_items service."""
    def trigger(self, entity_id):
        return {
            entity_id: {
                "items": [
                    {"uid": "1", "summary": "Buy groceries", "status": "needs_action"},
                    {"uid": "2", "summary": "Pay bills", "status": "completed"},
                ]
            }
        }


class MockUpdateItem:
    """Mock update_item service."""
    def trigger(self, entity_id, item, status):
        print(f"  Mock: Updated todo '{item}' to status '{status}'")


def setup_artifact_directory():
    """Create artifacts directory if it doesn't exist."""
    os.makedirs(ARTIFACT_DIR, exist_ok=True)


def save_artifact(image: Image.Image, filename: str):
    """Save a PIL Image as PNG artifact."""
    filepath = os.path.join(ARTIFACT_DIR, filename)
    image.save(filepath, 'PNG')
    print(f"  ✓ Artifact saved: {filepath}")
    return filepath


def generate_sensor_artifacts():
    """Generate artifacts for sensor component."""
    print("\nGenerating Sensor Artifacts:")
    
    # Test 1: Numeric value
    sensor = Sensor("sensor.temperature", DISPLAY_DIMENSIONS)
    sensor.entity = MockEntity("21.5", {"friendly_name": "Living Room Temp"})
    sensor._has_content = True
    image = sensor.render()
    save_artifact(image, "sensor_numeric.png")
    
    # Test 2: String value
    sensor = Sensor("sensor.weather_condition", DISPLAY_DIMENSIONS)
    sensor.entity = MockEntity("sunny", {"friendly_name": "Weather"})
    sensor._has_content = True
    image = sensor.render()
    save_artifact(image, "sensor_string.png")
    
    # Test 3: No content
    sensor = Sensor("sensor.empty", DISPLAY_DIMENSIONS)
    sensor._has_content = False
    image = sensor.render()
    save_artifact(image, "sensor_no_content.png")
    
    # Test 4: Rounded decimal
    sensor = Sensor("sensor.humidity", DISPLAY_DIMENSIONS)
    sensor.entity = MockEntity("45.678", {"friendly_name": "Humidity"})
    sensor._has_content = True
    image = sensor.render()
    save_artifact(image, "sensor_rounded_decimal.png")
    
    # Test 5: Whole number
    sensor = Sensor("sensor.count", DISPLAY_DIMENSIONS)
    sensor.entity = MockEntity("42", {"friendly_name": "Item Count"})
    sensor._has_content = True
    image = sensor.render()
    save_artifact(image, "sensor_whole_number.png")
    
    # Test 6: Centered text
    sensor = Sensor("sensor.center_test", DISPLAY_DIMENSIONS)
    sensor.entity = MockEntity("42", {"friendly_name": "Centered Sensor"})
    sensor._has_content = True
    image = sensor.render()
    save_artifact(image, "sensor_centered.png")


def generate_todo_artifacts():
    """Generate artifacts for todo component."""
    print("\nGenerating Todo Artifacts:")
    
    # Test 1: With items
    todo = Todo("todo.shopping", DISPLAY_DIMENSIONS)
    todo.entity = MockEntity("2", {})
    todo.todo_domain = MockTodoDomain()
    todo.todos = {
        "items": [
            {"uid": "1", "summary": "Buy milk and eggs", "status": "needs_action"},
            {"uid": "2", "summary": "Get bread", "status": "needs_action"},
        ]
    }
    todo._has_content = True
    image = todo.render()
    save_artifact(image, "todo_with_items.png")
    
    # Test 2: No content
    todo = Todo("todo.empty", DISPLAY_DIMENSIONS)
    todo._has_content = False
    image = todo.render()
    save_artifact(image, "todo_no_content.png")
    
    # Test 3: All completed
    todo = Todo("todo.completed", DISPLAY_DIMENSIONS)
    todo.entity = MockEntity("0", {})
    todo.todo_domain = MockTodoDomain()
    todo.todos = {
        "items": [
            {"uid": "1", "summary": "Task 1", "status": "completed"},
            {"uid": "2", "summary": "Task 2", "status": "completed"},
        ]
    }
    todo._has_content = False
    image = todo.render()
    save_artifact(image, "todo_all_completed.png")
    
    # Test 4: Long text
    todo = Todo("todo.long", DISPLAY_DIMENSIONS)
    todo.entity = MockEntity("1", {})
    todo.todo_domain = MockTodoDomain()
    todo.todos = {
        "items": [
            {
                "uid": "1",
                "summary": "This is a very long todo item that should wrap to multiple lines",
                "status": "needs_action"
            },
        ]
    }
    todo._has_content = True
    image = todo.render()
    save_artifact(image, "todo_long_text.png")


def generate_weather_artifacts():
    """Generate artifacts for weather component."""
    print("\nGenerating Weather Artifacts:")
    
    # Test 1: With data
    weather = Weather("weather.home", DISPLAY_DIMENSIONS)
    weather.entity = MockEntity(
        "sunny",
        {
            "friendly_name": "Home Weather",
            "temperature": 22.5,
            "temperature_unit": "°C",
        }
    )
    weather.forecast = {
        "weather.home": {
            "forecast": [
                {"condition": "sunny", "temperature": 22, "datetime": "2024-01-01T12:00:00"},
                {"condition": "partlycloudy", "temperature": 20, "datetime": "2024-01-01T13:00:00"},
                {"condition": "cloudy", "temperature": 18, "datetime": "2024-01-01T14:00:00"},
                {"condition": "rainy", "temperature": 15, "datetime": "2024-01-01T15:00:00"},
            ]
        }
    }
    weather._has_content = True
    image = weather.render()
    save_artifact(image, "weather_with_data.png")
    
    # Test 2: No content
    weather = Weather("weather.empty", DISPLAY_DIMENSIONS)
    weather._has_content = False
    image = weather.render()
    save_artifact(image, "weather_no_content.png")


def main():
    """Generate all test artifacts."""
    print("\n" + "="*70)
    print("Generating Component Visual Test Artifacts")
    print("="*70)
    
    setup_artifact_directory()
    
    generate_sensor_artifacts()
    generate_todo_artifacts()
    generate_weather_artifacts()
    
    print("\n" + "="*70)
    print(f"✓ All artifacts saved to: {os.path.abspath(ARTIFACT_DIR)}")
    print("="*70 + "\n")
    
    # List all generated files
    print("Generated files:")
    for filename in sorted(os.listdir(ARTIFACT_DIR)):
        filepath = os.path.join(ARTIFACT_DIR, filename)
        size = os.path.getsize(filepath)
        print(f"  - {filename} ({size} bytes)")
    print()


if __name__ == "__main__":
    main()
