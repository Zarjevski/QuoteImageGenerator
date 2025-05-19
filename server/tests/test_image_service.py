import unittest
from services.image_service import generate_image

class TestImageGeneration(unittest.TestCase):
    def test_generate_preview_valid_input(self):
        data = {
            "quote": "חיים הם מה שקורה כשאתה עסוק בלתכנן תוכניות אחרות.",
            "thinker": "ExampleThinker",
            "image": "example.jpg"
        }
        try:
            result = generate_image(data)
            self.assertIn("preview_url", result)
            self.assertIn("filename", result)
        except Exception as e:
            self.fail(f"Image generation raised an exception: {e}")

if __name__ == "__main__":
    unittest.main()
