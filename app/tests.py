from django.test import TestCase
from app.models import Content, ContentDetails, Channel


class ContentTestCase(TestCase):
    def testPost(self):
        content = ContentDetails(title="My Title", description_detail="desc", is_active=True, slug="mytitle", votes=1)
        self.assertEqual(content.title, "My Title")
        self.assertEqual(content.description_detail, "desc")
        self.assertEqual(content.is_active, True)
        self.assertEqual(content.slug, "mytitle")
        self.assertEqual(content.votes, 1)
