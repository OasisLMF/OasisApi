import json
import mimetypes
import string
from tempfile import NamedTemporaryFile

from backports.tempfile import TemporaryDirectory
from django.core.files import File
from django.test import override_settings
from django.urls import reverse
from django_webtest import WebTestMixin
from hypothesis import given
from hypothesis.extra.django import TestCase
from hypothesis.strategies import text, binary, sampled_from
from mock import patch
from pathlib2 import Path
from rest_framework_simplejwt.tokens import AccessToken

from ...files.tests.fakes import fake_related_file
from ...analysis_models.tests.fakes import fake_analysis_model
from ...portfolios.tests.fakes import fake_portfolio
from ...auth.tests.fakes import fake_user
from ..models import Analysis
from .fakes import fake_analysis


class AnalysisApi(WebTestMixin, TestCase):
    def test_user_is_not_authenticated___response_is_401(self):
        analysis = fake_analysis()

        response = self.app.get(analysis.get_absolute_url(), expect_errors=True)

        self.assertEqual(401, response.status_code)

    def test_user_is_authenticated_object_does_not_exist___response_is_404(self):
        user = fake_user()
        analysis = fake_analysis()

        response = self.app.get(
            reverse('analysis-detail', args=[analysis.pk + 1]),
            expect_errors=True,
            headers={
                'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
            }
        )

        self.assertEqual(404, response.status_code)

    def test_name_is_not_provided___response_is_400(self):
        user = fake_user()

        response = self.app.post(
            reverse('analysis-list'),
            expect_errors=True,
            headers={
                'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
            },
            params={},
            content_type='application/json',
        )

        self.assertEqual(400, response.status_code)

    @given(name=text(alphabet=' \t\n\r', max_size=10))
    def test_cleaned_name_is_empty___response_is_400(self, name):
        user = fake_user()

        response = self.app.post(
            reverse('analysis-list'),
            expect_errors=True,
            headers={
                'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
            },
            params=json.dumps({'name': name}),
            content_type='application/json'
        )

        self.assertEqual(400, response.status_code)

    @given(name=text(alphabet=string.ascii_letters, max_size=10, min_size=1))
    def test_cleaned_name_portfolio_and_model_are_present___object_is_created(self, name):
        user = fake_user()
        model = fake_analysis_model()
        portfolio = fake_portfolio()

        response = self.app.post(
            reverse('analysis-list'),
            headers={
                'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
            },
            params=json.dumps({'name': name, 'portfolio': portfolio.pk, 'model': model.pk}),
            content_type='application/json'
        )
        self.assertEqual(201, response.status_code)

        analysis = Analysis.objects.get(pk=response.json['id'])
        response = self.app.get(
            analysis.get_absolute_url(),
            headers={
                'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
            },
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual({
            'created': analysis.created.strftime('%y-%m-%dT%H:%M:%S.%f%z'),
            'modified': analysis.modified.strftime('%y-%m-%dT%H:%M:%S.%f%z'),
            'id': analysis.pk,
            'name': name,
            'portfolio': portfolio.pk,
            'model': model.pk,
            'settings_file': response.request.application_url + analysis.get_absolute_settings_file_url(),
            'input_file': response.request.application_url + analysis.get_absolute_input_file_url(),
            'input_errors_file': response.request.application_url + analysis.get_absolute_input_errors_file_url(),
            'input_generation_traceback_file': response.request.application_url + analysis.get_absolute_input_generation_traceback_file_url(),
            'output_file': response.request.application_url + analysis.get_absolute_output_file_url(),
            'run_traceback_file': response.request.application_url + analysis.get_absolute_run_traceback_file_url(),
            'status': Analysis.status_choices.NEW,
        }, response.json)

    def test_model_does_not_exist___response_is_400(self):
        user = fake_user()
        analysis = fake_analysis()
        model = fake_analysis_model()

        response = self.app.patch(
            analysis.get_absolute_url(),
            headers={
                'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
            },
            params=json.dumps({'model': model.pk + 1}),
            content_type='application/json',
            expect_errors=True,
        )

        self.assertEqual(400, response.status_code)

    def test_model_does_exist___response_is_200(self):
        user = fake_user()
        analysis = fake_analysis()
        model = fake_analysis_model()

        response = self.app.patch(
            analysis.get_absolute_url(),
            headers={
                'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
            },
            params=json.dumps({'model': model.pk}),
            content_type='application/json',
            expect_errors=True,
        )

        analysis.refresh_from_db()

        self.assertEqual(200, response.status_code)
        self.assertEqual(analysis.model, model)


class AnalysisRun(WebTestMixin, TestCase):
    def test_user_is_not_authenticated___response_is_401(self):
        analysis = fake_analysis()

        response = self.app.post(analysis.get_absolute_run_url(), expect_errors=True)

        self.assertEqual(401, response.status_code)

    def test_user_is_authenticated_object_does_not_exist___response_is_404(self):
        user = fake_user()
        analysis = fake_analysis()

        response = self.app.post(
            reverse('analysis-run', args=[analysis.pk + 1]),
            expect_errors=True,
            headers={
                'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
            }
        )

        self.assertEqual(404, response.status_code)

    def test_user_is_authenticated_object_exists___run_is_called(self):
        with patch('src.server.oasisapi.analyses.models.Analysis.run', autospec=True) as run_mock:
            user = fake_user()
            analysis = fake_analysis()

            self.app.post(
                analysis.get_absolute_run_url(),
                headers={
                    'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
                }
            )

            run_mock.assert_called_once_with(analysis, user)


class AnalysisCancel(WebTestMixin, TestCase):
    def test_user_is_not_authenticated___response_is_401(self):
        analysis = fake_analysis()

        response = self.app.post(analysis.get_absolute_cancel_url(), expect_errors=True)

        self.assertEqual(401, response.status_code)

    def test_user_is_authenticated_object_does_not_exist___response_is_404(self):
        user = fake_user()
        analysis = fake_analysis()

        response = self.app.post(
            reverse('analysis-cancel', args=[analysis.pk + 1]),
            expect_errors=True,
            headers={
                'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
            }
        )

        self.assertEqual(404, response.status_code)

    def test_user_is_authenticated_object_exists___cancel_is_called(self):
        with patch('src.server.oasisapi.analyses.models.Analysis.cancel', autospec=True) as cancel_mock:
            user = fake_user()
            analysis = fake_analysis()

            self.app.post(
                analysis.get_absolute_cancel_url(),
                headers={
                    'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
                }
            )

            cancel_mock.assert_called_once_with(analysis)


class AnalysisGenerateInputs(WebTestMixin, TestCase):
    def test_user_is_not_authenticated___response_is_401(self):
        analysis = fake_analysis()

        response = self.app.post(analysis.get_absolute_generate_inputs_url(), expect_errors=True)

        self.assertEqual(401, response.status_code)

    def test_user_is_authenticated_object_does_not_exist___response_is_404(self):
        user = fake_user()
        analysis = fake_analysis()

        response = self.app.post(
            reverse('analysis-generate-inputs', args=[analysis.pk + 1]),
            expect_errors=True,
            headers={
                'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
            }
        )

        self.assertEqual(404, response.status_code)

    def test_user_is_authenticated_object_exists___generate_inputs_is_called(self):
        with patch('src.server.oasisapi.analyses.models.Analysis.generate_inputs', autospec=True) as generate_inputs_mock:
            user = fake_user()
            analysis = fake_analysis()

            self.app.post(
                analysis.get_absolute_generate_inputs_url(),
                headers={
                    'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
                }
            )

            generate_inputs_mock.assert_called_once_with(analysis, user)


class AnalysisCancelInputsGeneration(WebTestMixin, TestCase):
    def test_user_is_not_authenticated___response_is_401(self):
        analysis = fake_analysis()

        response = self.app.post(analysis.get_absolute_cancel_inputs_generation_url(), expect_errors=True)

        self.assertEqual(401, response.status_code)

    def test_user_is_authenticated_object_does_not_exist___response_is_404(self):
        user = fake_user()
        analysis = fake_analysis()

        response = self.app.post(
            reverse('analysis-cancel-generate-inputs', args=[analysis.pk + 1]),
            expect_errors=True,
            headers={
                'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
            }
        )

        self.assertEqual(404, response.status_code)

    def test_user_is_authenticated_object_exists___generate_inputs_generation_is_called(self):
        with patch('src.server.oasisapi.analyses.models.Analysis.cancel_generate_inputs', autospec=True) as cancel_generate_inputs:
            user = fake_user()
            analysis = fake_analysis()

            self.app.post(
                analysis.get_absolute_cancel_inputs_generation_url(),
                headers={
                    'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
                }
            )

            cancel_generate_inputs.assert_called_once_with(analysis)


class AnalysisCopy(WebTestMixin, TestCase):
    def test_user_is_not_authenticated___response_is_401(self):
        analysis = fake_analysis()

        response = self.app.post(analysis.get_absolute_copy_url(), expect_errors=True)

        self.assertEqual(401, response.status_code)

    def test_user_is_authenticated_object_does_not_exist___response_is_404(self):
        user = fake_user()
        analysis = fake_analysis()

        response = self.app.post(
            reverse('analysis-copy', args=[analysis.pk + 1]),
            expect_errors=True,
            headers={
                'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
            }
        )

        self.assertEqual(404, response.status_code)

    def test_new_object_is_created(self):
        user = fake_user()
        analysis = fake_analysis()

        response = self.app.post(
            analysis.get_absolute_copy_url(),
            headers={
                'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
            }
        )

        self.assertNotEqual(analysis.pk, response.json['id'])

    @given(name=text(min_size=1, max_size=10, alphabet=string.ascii_letters))
    def test_no_new_name_is_provided___copy_is_appended_to_name(self, name):
        user = fake_user()
        analysis = fake_analysis(name=name)

        response = self.app.post(
            analysis.get_absolute_copy_url(),
            headers={
                'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
            }
        )

        self.assertEqual(Analysis.objects.get(pk=response.json['id']).name, '{} - Copy'.format(name))

    @given(orig_name=text(min_size=1, max_size=10, alphabet=string.ascii_letters), new_name=text(min_size=1, max_size=10, alphabet=string.ascii_letters))
    def test_new_name_is_provided___new_name_is_set_on_new_object(self, orig_name, new_name):
        user = fake_user()
        analysis = fake_analysis(name=orig_name)

        response = self.app.post(
            analysis.get_absolute_copy_url(),
            headers={
                'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
            },
            params=json.dumps({'name': new_name}),
            content_type='application/json'
        )

        self.assertEqual(Analysis.objects.get(pk=response.json['id']).name, new_name)

    @given(status=sampled_from(list(Analysis.status_choices._db_values)))
    def test_state_is_reset(self, status):
        user = fake_user()
        analysis = fake_analysis(status=status)

        response = self.app.post(
            analysis.get_absolute_copy_url(),
            headers={
                'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
            }
        )

        self.assertEqual(Analysis.objects.get(pk=response.json['id']).status, Analysis.status_choices.NEW)

    def test_creator_is_set_to_caller(self):
        user = fake_user()
        analysis = fake_analysis()

        response = self.app.post(
            analysis.get_absolute_copy_url(),
            headers={
                'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
            }
        )

        self.assertEqual(Analysis.objects.get(pk=response.json['id']).creator, user)

    @given(task_id=text(min_size=1, max_size=10, alphabet=string.ascii_letters))
    def test_run_task_id_is_reset(self, task_id):
        user = fake_user()
        analysis = fake_analysis(run_task_id=task_id)

        response = self.app.post(
            analysis.get_absolute_copy_url(),
            headers={
                'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
            }
        )

        self.assertEqual(Analysis.objects.get(pk=response.json['id']).run_task_id, '')

    @given(task_id=text(min_size=1, max_size=10, alphabet=string.ascii_letters))
    def test_generate_inputs_task_id_is_reset(self, task_id):
        user = fake_user()
        analysis = fake_analysis(generate_inputs_task_id=task_id)

        response = self.app.post(
            analysis.get_absolute_copy_url(),
            headers={
                'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
            }
        )

        self.assertEqual(Analysis.objects.get(pk=response.json['id']).generate_inputs_task_id, '')

    def test_portfolio_is_not_supplied___portfolio_is_copied(self):
        user = fake_user()
        analysis = fake_analysis()

        response = self.app.post(
            analysis.get_absolute_copy_url(),
            headers={
                'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
            }
        )

        self.assertEqual(Analysis.objects.get(pk=response.json['id']).portfolio, analysis.portfolio)

    def test_portfolio_is_supplied___portfolio_is_replaced(self):
        user = fake_user()
        analysis = fake_analysis()
        new_portfolio = fake_portfolio()

        response = self.app.post(
            analysis.get_absolute_copy_url(),
            headers={
                'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
            },
            params=json.dumps({'portfolio': new_portfolio.pk}),
            content_type='application/json',
        )

        self.assertEqual(Analysis.objects.get(pk=response.json['id']).portfolio, new_portfolio)

    def test_model_is_not_supplied___model_is_copied(self):
        user = fake_user()
        analysis = fake_analysis()

        response = self.app.post(
            analysis.get_absolute_copy_url(),
            headers={
                'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
            }
        )

        self.assertEqual(Analysis.objects.get(pk=response.json['id']).model, analysis.model)

    def test_model_is_supplied___model_is_replaced(self):
        user = fake_user()
        analysis = fake_analysis()
        new_model = fake_analysis_model()

        response = self.app.post(
            analysis.get_absolute_copy_url(),
            headers={
                'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
            },
            params=json.dumps({'model': new_model.pk}),
            content_type='application/json',
        )

        self.assertEqual(Analysis.objects.get(pk=response.json['id']).model, new_model)

    def test_settings_file_is_not_supplied___settings_file_is_copied(self):
        with TemporaryDirectory() as d:
            with override_settings(MEDIA_ROOT=d):
                user = fake_user()
                analysis = fake_analysis(settings_file=fake_related_file(file='{}'))

                response = self.app.post(
                    analysis.get_absolute_copy_url(),
                    headers={
                        'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
                    }
                )

                self.assertEqual(Analysis.objects.get(pk=response.json['id']).settings_file.pk, analysis.settings_file.pk)

    def test_input_file_is_not_supplied___input_file_is_copied(self):
        with TemporaryDirectory() as d:
            with override_settings(MEDIA_ROOT=d):
                user = fake_user()
                analysis = fake_analysis(input_file=fake_related_file())

                response = self.app.post(
                    analysis.get_absolute_copy_url(),
                    headers={
                        'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
                    }
                )

                self.assertEqual(Analysis.objects.get(pk=response.json['id']).input_file, analysis.input_file)

    def test_input_errors_file_is_cleared(self):
        with TemporaryDirectory() as d:
            with override_settings(MEDIA_ROOT=d):
                user = fake_user()
                analysis = fake_analysis(input_errors_file=fake_related_file())

                response = self.app.post(
                    analysis.get_absolute_copy_url(),
                    headers={
                        'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
                    },
                )

                self.assertIsNone(Analysis.objects.get(pk=response.json['id']).input_errors_file)

    def test_output_file_is_cleared(self):
        with TemporaryDirectory() as d:
            with override_settings(MEDIA_ROOT=d):
                user = fake_user()
                analysis = fake_analysis(output_file=fake_related_file())

                response = self.app.post(
                    analysis.get_absolute_copy_url(),
                    headers={
                        'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
                    },
                )

                self.assertIsNone(Analysis.objects.get(pk=response.json['id']).output_file)


class AnalysisSettingsFile(WebTestMixin, TestCase):
    def test_user_is_not_authenticated___response_is_401(self):
        analysis = fake_analysis()

        response = self.app.get(analysis.get_absolute_settings_file_url(), expect_errors=True)

        self.assertEqual(401, response.status_code)

    def test_settings_file_is_not_present___get_response_is_404(self):
        user = fake_user()
        analysis = fake_analysis()

        response = self.app.get(
            analysis.get_absolute_settings_file_url(),
            headers={
                'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
            },
            expect_errors=True,
        )

        self.assertEqual(404, response.status_code)

    def test_settings_file_is_not_present___delete_response_is_404(self):
        user = fake_user()
        analysis = fake_analysis()

        response = self.app.delete(
            analysis.get_absolute_settings_file_url(),
            headers={
                'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
            },
            expect_errors=True,
        )

        self.assertEqual(404, response.status_code)

    def test_settings_file_is_not_a_valid_format___response_is_400(self):
        with TemporaryDirectory() as d:
            with override_settings(MEDIA_ROOT=d):
                user = fake_user()
                analysis = fake_analysis()

                response = self.app.post(
                    analysis.get_absolute_settings_file_url(),
                    headers={
                        'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
                    },
                    upload_files=(
                        ('file', 'file.tar', b'content'),
                    ),
                    expect_errors=True,
                )

                self.assertEqual(400, response.status_code)

    @given(file_content=binary(min_size=1))
    def test_settings_file_is_uploaded___file_can_be_retrieved(self, file_content):
        with TemporaryDirectory() as d:
            with override_settings(MEDIA_ROOT=d):
                user = fake_user()
                analysis = fake_analysis()

                self.app.post(
                    analysis.get_absolute_settings_file_url(),
                    headers={
                        'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
                    },
                    upload_files=(
                        ('file', 'file.json', file_content),
                    ),
                )

                response = self.app.get(
                    analysis.get_absolute_settings_file_url(),
                    headers={
                        'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
                    },
                )

                self.assertEqual(response.body, file_content)
                self.assertEqual(response.content_type, 'application/json')


class AnalysisInputFile(WebTestMixin, TestCase):
    def test_user_is_not_authenticated___response_is_401(self):
        analysis = fake_analysis()

        response = self.app.get(analysis.get_absolute_input_file_url(), expect_errors=True)

        self.assertEqual(401, response.status_code)

    def test_input_file_is_not_present___get_response_is_404(self):
        user = fake_user()
        analysis = fake_analysis()

        response = self.app.get(
            analysis.get_absolute_input_file_url(),
            headers={
                'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
            },
            expect_errors=True,
        )

        self.assertEqual(404, response.status_code)

    @given(file_content=binary(min_size=1), content_type=sampled_from(['application/x-gzip', 'application/gzip', 'application/x-tar', 'application/tar']))
    def test_input_file_is_present___file_can_be_retrieved(self, file_content, content_type):
        with TemporaryDirectory() as d:
            with override_settings(MEDIA_ROOT=d):
                user = fake_user()
                analysis = fake_analysis(input_file=fake_related_file(file=file_content, content_type=content_type))

                response = self.app.get(
                    analysis.get_absolute_input_file_url(),
                    headers={
                        'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
                    },
                )

                self.assertEqual(response.body, file_content)
                self.assertEqual(response.content_type, content_type)


class AnalysisInputErrorsFile(WebTestMixin, TestCase):
    def test_user_is_not_authenticated___response_is_401(self):
        analysis = fake_analysis()

        response = self.app.get(analysis.get_absolute_input_errors_file_url(), expect_errors=True)

        self.assertEqual(401, response.status_code)

    def test_input_errors_file_is_not_present___get_response_is_404(self):
        user = fake_user()
        analysis = fake_analysis()

        response = self.app.get(
            analysis.get_absolute_input_errors_file_url(),
            headers={
                'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
            },
            expect_errors=True,
        )

        self.assertEqual(404, response.status_code)

    def test_input_errors_file_is_not_present___delete_response_is_404(self):
        user = fake_user()
        analysis = fake_analysis()

        response = self.app.delete(
            analysis.get_absolute_input_errors_file_url(),
            headers={
                'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
            },
            expect_errors=True,
        )

        self.assertEqual(404, response.status_code)

    @given(file_content=binary(min_size=1), content_type=sampled_from(['text/csv', 'application/json']))
    def test_input_errors_file_is_present___file_can_be_retrieved(self, file_content, content_type):
        with TemporaryDirectory() as d:
            with override_settings(MEDIA_ROOT=d):
                user = fake_user()
                analysis = fake_analysis(input_errors_file=fake_related_file(file=file_content, content_type=content_type))

                response = self.app.get(
                    analysis.get_absolute_input_errors_file_url(),
                    headers={
                        'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
                    },
                )

                self.assertEqual(response.body, file_content)
                self.assertEqual(response.content_type, content_type)


class AnalysisInputGenerationTracebackFile(WebTestMixin, TestCase):
    def test_user_is_not_authenticated___response_is_401(self):
        analysis = fake_analysis()

        response = self.app.get(analysis.get_absolute_input_generation_traceback_file_url(), expect_errors=True)

        self.assertEqual(401, response.status_code)

    def test_input_generation_traceback_file_is_not_present___get_response_is_404(self):
        user = fake_user()
        analysis = fake_analysis()

        response = self.app.get(
            analysis.get_absolute_input_generation_traceback_file_url(),
            headers={
                'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
            },
            expect_errors=True,
        )

        self.assertEqual(404, response.status_code)

    def test_input_generation_traceback_file_is_not_present___delete_response_is_404(self):
        user = fake_user()
        analysis = fake_analysis()

        response = self.app.delete(
            analysis.get_absolute_input_generation_traceback_file_url(),
            headers={
                'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
            },
            expect_errors=True,
        )

        self.assertEqual(404, response.status_code)

    @given(file_content=binary(min_size=1))
    def test_input_generation_traceback_file_is_present___file_can_be_retrieved(self, file_content):
        with TemporaryDirectory() as d:
            with override_settings(MEDIA_ROOT=d):
                user = fake_user()
                analysis = fake_analysis(input_generation_traceback_file=fake_related_file(file=file_content, content_type='text/plain'))

                response = self.app.get(
                    analysis.get_absolute_input_generation_traceback_file_url(),
                    headers={
                        'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
                    },
                )

                self.assertEqual(response.body, file_content)
                self.assertEqual(response.content_type, 'text/plain')


class AnalysisOutputFile(WebTestMixin, TestCase):
    def test_user_is_not_authenticated___response_is_401(self):
        analysis = fake_analysis()

        response = self.app.get(analysis.get_absolute_output_file_url(), expect_errors=True)

        self.assertEqual(401, response.status_code)

    def test_output_file_is_not_present___get_response_is_404(self):
        user = fake_user()
        analysis = fake_analysis()

        response = self.app.get(
            analysis.get_absolute_output_file_url(),
            headers={
                'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
            },
            expect_errors=True,
        )

        self.assertEqual(404, response.status_code)

    def test_output_file_is_not_present___delete_response_is_404(self):
        user = fake_user()
        analysis = fake_analysis()

        response = self.app.delete(
            analysis.get_absolute_output_file_url(),
            headers={
                'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
            },
            expect_errors=True,
        )

        self.assertEqual(404, response.status_code)

    def test_output_file_is_not_valid_format___post_response_is_405(self):
        with TemporaryDirectory() as d:
            with override_settings(MEDIA_ROOT=d):
                user = fake_user()
                analysis = fake_analysis()

                response = self.app.post(
                    analysis.get_absolute_output_file_url(),
                    headers={
                        'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
                    },
                    upload_files=(
                        ('file', 'file.csv', b'content'),
                    ),
                    expect_errors=True,
                )

                self.assertEqual(405, response.status_code)

    @given(file_content=binary(min_size=1), content_type=sampled_from(['application/x-gzip', 'application/gzip', 'application/x-tar', 'application/tar']))
    def test_output_file_is_present___file_can_be_retrieved(self, file_content, content_type):
        with TemporaryDirectory() as d:
            with override_settings(MEDIA_ROOT=d):
                user = fake_user()
                analysis = fake_analysis(output_file=fake_related_file(file=file_content, content_type=content_type))

                response = self.app.get(
                    analysis.get_absolute_output_file_url(),
                    headers={
                        'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
                    },
                )

                self.assertEqual(response.body, file_content)
                self.assertEqual(response.content_type, content_type)


class AnalysisRunTracebackFile(WebTestMixin, TestCase):
    def test_user_is_not_authenticated___response_is_401(self):
        analysis = fake_analysis()

        response = self.app.get(analysis.get_absolute_run_traceback_file_url(), expect_errors=True)

        self.assertEqual(401, response.status_code)

    def test_run_traceback_file_is_not_present___get_response_is_404(self):
        user = fake_user()
        analysis = fake_analysis()

        response = self.app.get(
            analysis.get_absolute_run_traceback_file_url(),
            headers={
                'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
            },
            expect_errors=True,
        )

        self.assertEqual(404, response.status_code)

    def test_run_traceback_file_is_not_present___delete_response_is_404(self):
        user = fake_user()
        analysis = fake_analysis()

        response = self.app.delete(
            analysis.get_absolute_run_traceback_file_url(),
            headers={
                'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
            },
            expect_errors=True,
        )

        self.assertEqual(404, response.status_code)

    def test_run_traceback_file_is_not_valid_format___post_response_is_405(self):
        with TemporaryDirectory() as d:
            with override_settings(MEDIA_ROOT=d):
                user = fake_user()
                analysis = fake_analysis()

                response = self.app.post(
                    analysis.get_absolute_run_traceback_file_url(),
                    headers={
                        'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
                    },
                    upload_files=(
                        ('file', 'file.csv', b'content'),
                    ),
                    expect_errors=True,
                )

                self.assertEqual(405, response.status_code)

    @given(file_content=binary(min_size=1), content_type=sampled_from(['application/x-gzip', 'application/gzip', 'application/x-tar', 'application/tar']))
    def test_run_traceback_file_is_present___file_can_be_retrieved(self, file_content, content_type):
        with TemporaryDirectory() as d:
            with override_settings(MEDIA_ROOT=d):
                user = fake_user()
                analysis = fake_analysis(run_traceback_file=fake_related_file(file=file_content, content_type=content_type))

                response = self.app.get(
                    analysis.get_absolute_run_traceback_file_url(),
                    headers={
                        'Authorization': 'Bearer {}'.format(AccessToken.for_user(user))
                    },
                )

                self.assertEqual(response.body, file_content)
                self.assertEqual(response.content_type, content_type)
