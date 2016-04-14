import os
import subprocess
import uranium
from uranium.rules import rule, Once


@uranium.task_requires("install_swagger_ui")
def main(build):
    build.packages.install(".", develop=True)


def test(build):
    main(build)
    build.packages.install("jedi")
    build.packages.install("sphinx")
    build.packages.install("pytest")
    build.packages.install("pytest-cov")
    pytest = os.path.join(build.root, "bin", "py.test")
    subprocess.call([
        pytest, "--cov", "web_transmute",
        "web_transmute/tests",
        "--cov-report", "term-missing"
    ] + build.options.args)


def distribute(build):
    """ distribute the uranium package """
    build.packages.install("wheel")
    build.executables.run([
        "python", "setup.py",
        "sdist", "upload"
    ])


@rule(Once())
def install_swagger_ui(build):
    import io
    import shutil
    import tarfile
    version = "2.1.4"
    PATH = "https://github.com/swagger-api/swagger-ui/archive/v{0}.tar.gz".format(version)
    TARGET_PATH = os.path.join(build.root, "web_transmute", "swagger", "static")
    EXTRACTED_TOP_LEVEL_DIRNAME = "swagger-ui-{0}".format(version)
    build.packages.install("requests")
    import requests
    r = requests.get(PATH, stream=True)
    stream = io.BytesIO()
    stream.write(r.content)
    stream.seek(0)
    tf = tarfile.TarFile.open(fileobj=stream)
    tf.extractall(path=TARGET_PATH)
    # move the files under the top level directory.
    for name in os.listdir(os.path.join(TARGET_PATH, EXTRACTED_TOP_LEVEL_DIRNAME, "dist")):
        shutil.move(
            os.path.join(TARGET_PATH, EXTRACTED_TOP_LEVEL_DIRNAME, "dist", name),
            TARGET_PATH
        )
