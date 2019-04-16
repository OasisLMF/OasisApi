import json
import mimetypes
import string
from tempfile import TemporaryDirectory

from django.test import override_settings
from django.urls import reverse
from django_webtest import WebTestMixin
from hypothesis import given, settings
from hypothesis.extra.django import TestCase
from hypothesis.strategies import text, binary, sampled_from

from rest_framework_simplejwt.tokens import AccessToken

from ...auth.tests.fakes import fake_user
from ..models import ComplexModelDataFile
from .fakes import fake_complex_model_file


class ComplexModelFilesApi(WebTestMixin, TestCase):
    @given(
        file_name=text(alphabet=string.ascii_letters, min_size=1, max_size=10),
        file_description=text(alphabet=string.whitespace, min_size=0, max_size=10),
    )
    def test_file_type_is_missing___response_is_400(self, file_name, file_description):
        user = fake_user()

        response = self.app.post(
            reverse('complex-model-data-file-list', kwargs={'version': 'v1'}),
            expect_errors=True,
            headers={
                'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
            },
            params=json.dumps({
                'file_name': file_name,
                'file_description': file_description,
            }),
            content_type='application/json',
        )

        self.assertEqual(400, response.status_code)
        self.assertFalse(ComplexModelDataFile.objects.exists())

    @given(
        file_name=text(alphabet=string.whitespace, min_size=0, max_size=10),
        file_description=text(alphabet=string.ascii_letters, min_size=1, max_size=10),
    )
    def test_file_name_is_missing___response_is_400(self, file_name, file_description):
        user = fake_user()

        response = self.app.post(
            reverse('complex-model-data-file-list', kwargs={'version': 'v1'}),
            expect_errors=True,
            headers={
                'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
            },
            params=json.dumps({
                'file_name': file_name,
                'file_description': file_description,
            }),
            content_type='application/json',
        )

        self.assertEqual(400, response.status_code)
        self.assertFalse(ComplexModelDataFile.objects.exists())

    @given(
        file_name=text(alphabet=string.ascii_letters, min_size=1, max_size=10),
        file_description=text(alphabet=string.ascii_letters, min_size=1, max_size=10),
    )
    @settings(deadline=None)
    def test_data_is_valid___object_is_created(self, file_name, file_description):
        user = fake_user()

        response = self.app.post(
            reverse('complex-model-data-file-list', kwargs={'version': 'v1'}),
            headers={
                'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
            },
            params=json.dumps({
                'file_name': file_name,
                'file_description': file_description,
            }),
            content_type='application/json',
        )

        model = ComplexModelDataFile.objects.first()

        self.assertEqual(201, response.status_code)
        self.assertEqual(model.file_name, file_name)
        self.assertEqual(model.file_description, file_description)


class ComplexModelFileDataFile(WebTestMixin, TestCase):
    def test_user_is_not_authenticated___response_is_401(self):
        cmf = fake_complex_model_file()

        response = self.app.get(cmf.get_absolute_data_file_url(), expect_errors=True)

        self.assertEqual(401, response.status_code)

    def test_data_file_is_not_present___get_response_is_404(self):
        user = fake_user()
        cmf = fake_complex_model_file()

        response = self.app.get(
            cmf.get_absolute_data_file_url(),
            headers={
                'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
            },
            expect_errors=True,
        )

        self.assertEqual(404, response.status_code)

    def test_data_file_is_not_present___delete_response_is_404(self):
        user = fake_user()
        cmf = fake_complex_model_file()

        response = self.app.delete(
            cmf.get_absolute_data_file_url(),
            headers={
                'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
            },
            expect_errors=True,
        )

        self.assertEqual(404, response.status_code)

    def test_data_file_is_unknown_format___response_is_200(self):
        with TemporaryDirectory() as d:
            with override_settings(MEDIA_ROOT=d):
                user = fake_user()
                cmf = fake_complex_model_file()

                response = self.app.post(
                    cmf.get_absolute_data_file_url(),
                    headers={
                        'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
                    },
                    upload_files=(
                        ('file', 'file.tar', b'an-unknown-mime-format'),
                    ),
                )

                self.assertEqual(200, response.status_code)

    @given(file_content=binary(min_size=1), content_type=sampled_from(['text/csv', 'application/json', 'application/octet-stream', 'image/tiff']))
    @settings(deadline=None)
    def test_data_file_is_uploaded___file_can_be_retrieved(self, file_content, content_type):
        with TemporaryDirectory() as d:
            with override_settings(MEDIA_ROOT=d):
                user = fake_user()
                cmf = fake_complex_model_file()

                self.app.post(
                    cmf.get_absolute_data_file_url(),
                    headers={
                        'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
                    },
                    upload_files=(
                        ('file', 'file{}'.format(mimetypes.guess_extension(content_type)), file_content),
                    ),
                )

                response = self.app.get(
                    cmf.get_absolute_data_file_url(),
                    headers={
                        'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
                    },
                )

                self.assertEqual(response.body, file_content)
                self.assertEqual(response.content_type, content_type)
