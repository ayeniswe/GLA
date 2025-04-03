use pyo3::prelude::*;
use str_match::StrMatch;

mod str_match;
mod ahocorasick;

#[pymodule]
fn search(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<StrMatch>()?;
    Ok(())
}
