use pyo3::prelude::*;

pub mod cli;
pub mod er;
pub mod http;
pub mod utils;

#[pyfunction]
fn version() -> &'static str {
    "0.1.0"
}

#[pymodule]
fn _rust(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(version, m)?)?;
    http::register(m)?;

    let cli_mod = PyModule::new(m.py(), "cli")?;
    cli::register(&cli_mod)?;
    m.add_submodule(&cli_mod)?;
    Ok(())
}
