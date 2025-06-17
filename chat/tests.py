from django.test import TestCase, Client
from django.urls import reverse

class ChatViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_chat_ui_renders(self):
        """Test that the chat UI page loads successfully."""
        response = self.client.get(reverse('chat_ui'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Marvin')  # Check for chat header

    def test_stream_endpoint_no_message(self):
        """Test the stream endpoint with no message (should still respond)."""
        response = self.client.get(reverse('chat_stream'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/event-stream', response['Content-Type'])

    def test_stream_endpoint_with_message(self):
        """Test the stream endpoint with a sample message (mocked)."""
        # This test will not hit the real LocalAI backend, but will check the endpoint works
        response = self.client.get(reverse('chat_stream'), {'message': 'Hello'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/event-stream', response['Content-Type'])
        # The response should yield at least one line (could be error if LocalAI is not running)
        lines = list(response.streaming_content)
        self.assertTrue(any(b'data:' in line for line in lines))

    def test_fail_always(self):
        """This test is designed to fail. Comment it out to pass all tests."""
        self.assertEqual(1, 2, "This test always fails!")
