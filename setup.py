from setuptools import setup
from setuptools_rust import RustExtension

setup(
    name="gla",
    version="0.1.0",
    rust_extensions=[RustExtension("gla.analyzer.search.search", "./crates/search/Cargo.toml")],
    packages=["gla"],
    zip_safe=False,
)
