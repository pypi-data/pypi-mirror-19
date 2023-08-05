import unittest

from pyramid import testing


class TestDepsjs(unittest.TestCase):

    def __setup(self, settings):  # noqa
        import pyramid_closure
        config = testing.setUp(settings=settings)
        config.include(pyramid_closure.includeme)
        config.add_static_view(
            name='static',
            path='pyramid_closure:tests/fixtures/static')
        return config

    def tearDown(self):  # noqa
        testing.tearDown()

    def test_roots_with_prefix_structured(self):
        settings = {
            'pyramid_closure': {
                'roots_with_prefix': [
                    [
                        'pyramid_closure:tests/fixtures/static/js',
                        'pyramid_closure/tests/fixtures/static/js',
                    ]
                ]
            }
        }
        self.__setup(settings)
        from pyramid_closure.views import depsjs
        request = testing.DummyRequest()
        resp = depsjs(request)
        self.assertEqual(resp, """goog.addDependency('http://example.com/static/js/appmodule.js', ['app'], [], false);
goog.addDependency('http://example.com/static/js/main.js', ['app_main'], [], false);
goog.addDependency('http://example.com/static/js/maincontroller.js', ['app.MainController'], ['app'], false);
""")

    def test_roots_with_prefix_unstructured(self):
        roots_with_prefix = \
            'pyramid_closure:tests/fixtures/static/js ' \
            'pyramid_closure/tests/fixtures/static/js'
        settings = {
            'pyramid_closure.roots_with_prefix': roots_with_prefix
        }
        self.__setup(settings)
        from pyramid_closure.views import depsjs
        request = testing.DummyRequest()
        resp = depsjs(request)
        self.assertEqual(resp, """goog.addDependency('http://example.com/static/js/appmodule.js', ['app'], [], false);
goog.addDependency('http://example.com/static/js/main.js', ['app_main'], [], false);
goog.addDependency('http://example.com/static/js/maincontroller.js', ['app.MainController'], ['app'], false);
""")
