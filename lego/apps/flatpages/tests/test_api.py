from lego.apps.flatpages.models import Page
from lego.apps.users.tests.utils import create_normal_user, create_super_user
from lego.utils.test_utils import BaseAPITestCase


class PageAPITestCase(BaseAPITestCase):
    fixtures = ["test_pages.yaml"]

    def setUp(self):
        self.pages = Page.objects.all().order_by("created_at")

    def test_get_pages(self):
        response = self.client.get("/api/v1/pages/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["results"]), 4)
        first = response.json()["results"][0]
        self.assertEqual(first["title"], self.pages.first().title)
        self.assertEqual(first["slug"], self.pages.first().slug)
        self.assertFalse("content" in first)

    def test_get_page_with_id(self):
        slug = "webkom"
        response = self.client.get("/api/v1/pages/{0}/".format(slug))
        expected = self.pages.get(slug=slug)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], expected.title)
        self.assertEqual(response.json()["slug"], expected.slug)
        self.assertEqual(response.json()["content"], expected.content)

    def test_non_existing_retrieve(self):
        response = self.client.get("/api/v1/pages/badslug/")
        self.assertEqual(response.status_code, 404)

    def test_unauthenticated(self):
        slug = "webkom"
        methods = ["post", "patch", "put", "delete"]
        for method in methods:
            call = getattr(self.client, method)
            response = call("/api/v1/pages/{0}/".format(slug))
            self.assertEqual(response.status_code, 401)

    def test_unauthorized(self):
        slug = "webkom"
        methods = ["post", "patch", "put", "delete"]
        user = create_normal_user()
        self.client.force_authenticate(user)
        for method in methods:
            call = getattr(self.client, method)
            response = call("/api/v1/pages/{0}/".format(slug))
            self.assertEqual(response.status_code, 403)

    def test_create_page(self):
        page = {"title": "cat", "content": "hei"}

        user = create_super_user()
        self.client.force_authenticate(user)
        response = self.client.post("/api/v1/pages/", data=page)
        self.assertEqual(response.status_code, 201)
