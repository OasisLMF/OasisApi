import string
from tempfile import TemporaryDirectory

from django.test import override_settings
from hypothesis import given
from hypothesis.extra.django import TestCase
from hypothesis.strategies import text
from pathlib2 import Path

from ...auth.tests.fakes import fake_user
from ..tasks import run_analysis_success, record_run_analysis_failure, generate_input_success, record_generate_input_failure
from .fakes import fake_analysis


class RunAnalysisSuccess(TestCase):
    @given(output_location=text(min_size=1, max_size=10, alphabet=string.ascii_letters))
    def test_output_file_and_status_are_updated(self, output_location):
        with TemporaryDirectory() as d:
            with override_settings(MEDIA_ROOT=d):
                Path(d, output_location).touch()

                initiator = fake_user()
                analysis = fake_analysis()

                run_analysis_success(output_location, analysis.pk, initiator.pk)

                analysis.refresh_from_db()

                self.assertEqual(analysis.output_file.file.name, output_location)
                self.assertEqual(analysis.output_file.content_type, 'application/gzip')
                self.assertEqual(analysis.output_file.creator, initiator)
                self.assertEqual(analysis.status, analysis.status_choices.RUN_COMPLETED)


class RunAnalysisFailure(TestCase):
    @given(traceback=text(min_size=1, max_size=10, alphabet=string.ascii_letters))
    def test_output_tracebackfile__and_status_are_updated(self, traceback):
        with TemporaryDirectory() as d:
            with override_settings(MEDIA_ROOT=d):
                initiator = fake_user()
                analysis = fake_analysis()

                record_run_analysis_failure(analysis.pk, initiator.pk, traceback)

                analysis.refresh_from_db()

                self.assertEqual(analysis.run_traceback_file.file.read(), traceback.encode())
                self.assertEqual(analysis.run_traceback_file.content_type, 'text/plain')
                self.assertEqual(analysis.run_traceback_file.creator, initiator)
                self.assertEqual(analysis.status, analysis.status_choices.RUN_ERROR)


class GenerateInputsSuccess(TestCase):
    @given(
        input_location=text(min_size=1, max_size=10, alphabet=string.ascii_letters),
        input_error_location=text(min_size=1, max_size=10, alphabet=string.ascii_letters),
    )
    def test_input_file_input_errors_file_and_status_are_updated(self, input_location, input_error_location):
        with TemporaryDirectory() as d:
            with override_settings(MEDIA_ROOT=d):
                Path(d, input_location).touch()
                Path(d, input_error_location).touch()

                initiator = fake_user()
                analysis = fake_analysis()

                generate_input_success((input_location, input_error_location), analysis.pk, initiator.pk)

                analysis.refresh_from_db()

                self.assertEqual(analysis.input_file.file.name, input_location)
                self.assertEqual(analysis.input_file.content_type, 'application/gzip')
                self.assertEqual(analysis.input_file.creator, initiator)
                self.assertEqual(analysis.input_errors_file.file.name, input_error_location)
                self.assertEqual(analysis.input_errors_file.content_type, 'text/csv')
                self.assertEqual(analysis.input_errors_file.creator, initiator)
                self.assertEqual(analysis.status, analysis.status_choices.READY)


class GenerateInputsFailure(TestCase):
    @given(traceback=text(min_size=1, max_size=10, alphabet=string.ascii_letters))
    def test_input_generation_traceback_file_and_status_are_updated(self, traceback):
        with TemporaryDirectory() as d:
            with override_settings(MEDIA_ROOT=d):
                initiator = fake_user()
                analysis = fake_analysis()

                record_generate_input_failure(analysis.pk, initiator.pk, traceback)

                analysis.refresh_from_db()

                self.assertEqual(analysis.input_generation_traceback_file.file.read(), traceback.encode())
                self.assertEqual(analysis.input_generation_traceback_file.content_type, 'text/plain')
                self.assertEqual(analysis.input_generation_traceback_file.creator, initiator)
                self.assertEqual(analysis.status, analysis.status_choices.INPUTS_GENERATION_ERROR)
