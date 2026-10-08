# Component Visual Tests

This directory contains tests that generate PNG artifacts for visual verification of component rendering.

## Quick Start

Generate all component artifacts:

```bash
python tests/generate_artifacts.py
```

This will create PNG images in the `tests/artifacts/` directory showing how each component looks with different data.

## Generated Artifacts

### Sensor Component
- `sensor_numeric.png` - Sensor with numeric value (21.5)
- `sensor_string.png` - Sensor with string value ("sunny")
- `sensor_no_content.png` - Sensor with no content
- `sensor_rounded_decimal.png` - Sensor with decimal that gets rounded (45.678)
- `sensor_whole_number.png` - Sensor with whole number (42)
- `sensor_centered.png` - Sensor with centered title and value

### Todo Component
- `todo_with_items.png` - Todo with multiple unchecked items
- `todo_no_content.png` - Todo with no content
- `todo_all_completed.png` - Todo where all items are completed
- `todo_long_text.png` - Todo with long text that wraps

### Weather Component
- `weather_with_data.png` - Weather with current conditions and forecast
- `weather_no_content.png` - Weather with no content

## Requirements

- Python 3.x
- Pillow library (`pip install Pillow`)

## Adding New Tests

To add a new test case:

1. Create a new test function in `generate_artifacts.py`
2. Set up the component with mock data
3. Call `render()` to generate the image
4. Call `save_artifact(image, "filename.png")` to save it

Example:

```python
def test_new_feature():
    print("\nTesting new feature:")
    component = MyComponent("entity.id", DISPLAY_DIMENSIONS)
    # Set up mock data
    component.data = mock_data
    component._has_content = True
    
    image = component.render()
    save_artifact(image, "new_feature.png")
```

## Notes

- The weather component uses a custom `meteocons.ttf` font. The test uses a mock font that falls back to DejaVuSans.
- All artifacts are generated at the display dimensions specified in `config.example.toml` (250x122 pixels).
- Artifacts are useful for quick visual verification without deploying to the e-paper device.
