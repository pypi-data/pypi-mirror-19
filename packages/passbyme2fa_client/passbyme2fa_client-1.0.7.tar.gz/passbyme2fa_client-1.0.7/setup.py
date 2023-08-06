from setuptools import setup
import sys

if sys.version_info < (2, 7, 9):
    sys.exit('Sorry, Python < 2.7.9 is not supported')

setup(
        name             = "passbyme2fa_client",
        version          = "1.0.7",
        author           = "Microsec ltd.",
        author_email     = "development@passbyme.com",
        description      = "Messaging SDK for PassBy[ME] Mobile ID solution",
        url              = "https://www.passbyme.com/",
        download_url     = "https://github.com/microsec/passbyme2fa-client-python",
        license          = "MIT",
        packages         = ["passbyme2fa_client"],
        package_data     = {"passbyme2fa_client": ["truststore.pem"]},
        tests_require    = [
            "httpretty",
        ],
        install_requires = [
            "arrow",
        ],
        test_suite       = "test",
)
