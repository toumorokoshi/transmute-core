import os
import subprocess
import uranium
from uranium.rules import rule, Once


@uranium.task_requires("install_swagger_ui")
def main(build):
    build.packages.install(".", develop=True)
    # we install flask to allow testing the example.
    build.packages.install("flask")


def test(build):
    if not build.history.get("test_deps"):
        main(build)
        build.packages.install("pytest")
        build.packages.install("pytest-cov")
        build.packages.install("flake8")
        build.history["test_deps"] = True
    build.executables.run([
        "py.test", "--cov", "transmute_core",
        "transmute_core/tests",
        "--cov-report", "term-missing"
    ] + build.options.args)


def publish(build):
    """ publish the uranium package """
    build.packages.install("wheel")
    build.executables.run([
        "python", "setup.py",
        "sdist", "bdist_wheel", "--universal", "upload", "--release"
    ])


def changelog(build):
    """ create a changelog """
    build.packages.install("gitchangelog")
    changelog_text = subprocess.check_output(["gitchangelog", "show", "^v0.2.9"])
    with open(os.path.join(build.root, "CHANGELOG"), "wb+") as fh:
        fh.write(changelog_text)


def build_docs(build):
    changelog(build)
    build.packages.install("Babel")
    build.packages.install("Sphinx")
    build.packages.install("sphinx_rtd_theme")
    build.packages.install("sphinxcontrib-programoutput")
    return build.executables.run([
        "sphinx-build", "docs",
        os.path.join("docs", "_build")
    ] + build.options.args)[0]


@rule(Once())
def install_swagger_ui(build):
    import io
    import shutil
    import tarfile
    version = "2.2.8"
    PATH = "https://github.com/swagger-api/swagger-ui/archive/v{0}.tar.gz".format(version)
    TARGET_PATH = os.path.join(build.root, "transmute_core", "swagger", "static")
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
