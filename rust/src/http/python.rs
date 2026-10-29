//! Thin PyO3 wrapper around the Hermes HTTP client.
//!
//! Exposes `hermes._rust.http.HttpClient`, `HttpResponse`, and a
//! `HermesHttpError` exception. All network work happens in the core client,
//! never here.

use std::time::Duration;

use pyo3::create_exception;
use pyo3::exceptions::{PyException, PyValueError};
use pyo3::prelude::*;
use pyo3::types::{PyDict, PyList, PyModule, PyModuleMethods};

use crate::http::HermesHttpError as RustHttpError;
use crate::http::{HttpClient as CoreClient, Method, RetryPolicy};

create_exception!(_rust.http, HermesHttpError, PyException);

/// Raises `HermesHttpError` carrying the failure category and, for HTTP status
/// errors, the numeric status code. Attached as attributes so the Python layer
/// can classify without parsing error text.
fn to_py_err(py: Python<'_>, err: RustHttpError) -> PyErr {
    let ty = py.get_type::<HermesHttpError>();
    match ty.call1((err.to_string(),)) {
        Ok(instance) => {
            let category: &'static str = match &err {
                RustHttpError::InvalidUrl(_) => "InvalidUrl",
                RustHttpError::Dns(_) => "Dns",
                RustHttpError::Connection(_) => "Connection",
                RustHttpError::Timeout => "Timeout",
                RustHttpError::Tls(_) => "Tls",
                RustHttpError::TooManyRedirects => "TooManyRedirects",
                RustHttpError::Request(_) => "Request",
                RustHttpError::Response(_) => "Response",
                RustHttpError::Io(_) => "Io",
                RustHttpError::Json(_) => "Json",
                RustHttpError::Http { .. } => "Http",
            };
            let _ = instance.setattr("category", category);
            if let RustHttpError::Http { status, .. } = &err {
                let _ = instance.setattr("status_code", *status);
            }
            PyErr::from_value(instance)
        }
        Err(e) => e,
    }
}

/// Materialized response body so no underlying HTTP types leak across the FFI.
#[pyclass(name = "HttpResponse")]
#[derive(Clone)]
pub struct HttpResponse {
    status: u16,
    headers: Vec<(String, String)>,
    body: Vec<u8>,
}

#[pymethods]
impl HttpResponse {
    #[getter]
    fn status(&self) -> u16 {
        self.status
    }

    fn headers<'a>(&self, py: Python<'a>) -> PyResult<Bound<'a, PyDict>> {
        let dict = PyDict::new(py);
        for (name, value) in &self.headers {
            dict.set_item(name, value)?;
        }
        Ok(dict)
    }

    fn header(&self, name: &str) -> Option<String> {
        self.headers
            .iter()
            .find(|(key, _)| key.eq_ignore_ascii_case(name))
            .map(|(_, value)| value.clone())
    }

    fn bytes(&self) -> Vec<u8> {
        self.body.clone()
    }

    /// Decodes the body as UTF-8 text.
    fn text(&self) -> PyResult<String> {
        String::from_utf8(self.body.clone())
            .map_err(|e| PyValueError::new_err(format!("response body is not valid UTF-8: {e}")))
    }

    /// Parses the body as JSON.
    fn json<'a>(&self, py: Python<'a>) -> PyResult<Bound<'a, PyAny>> {
        let value: serde_json::Value = serde_json::from_slice(&self.body)
            .map_err(|e| PyValueError::new_err(format!("invalid JSON: {e}")))?;
        json_to_py(&value, py)
    }
}

/// Converts a `serde_json::Value` into a Python object.
fn json_to_py<'py>(value: &serde_json::Value, py: Python<'py>) -> PyResult<Bound<'py, PyAny>> {
    use pyo3::{IntoPyObject, IntoPyObjectExt};
    Ok(match value {
        serde_json::Value::Null => py.None().into_bound(py),
        serde_json::Value::Bool(b) => pyo3::types::PyBool::new(py, *b).into_bound_py_any(py)?,
        serde_json::Value::Number(n) => {
            if let Some(i) = n.as_i64() {
                i.into_pyobject(py)?.into_any()
            } else if let Some(u) = n.as_u64() {
                u.into_pyobject(py)?.into_any()
            } else {
                n.as_f64().unwrap_or(f64::NAN).into_pyobject(py)?.into_any()
            }
        }
        serde_json::Value::String(s) => s.into_pyobject(py)?.into_any(),
        serde_json::Value::Array(items) => {
            let list = PyList::empty(py);
            for item in items {
                list.append(json_to_py(item, py)?)?;
            }
            list.into_any()
        }
        serde_json::Value::Object(map) => {
            let dict = PyDict::new(py);
            for (key, item) in map {
                dict.set_item(key, json_to_py(item, py)?)?;
            }
            dict.into_any()
        }
    })
}

#[pyclass(name = "HttpClient")]
pub struct HttpClient {
    inner: CoreClient,
}

#[pymethods]
impl HttpClient {
    #[new]
    #[pyo3(signature = (timeout_secs=Some(30.0), user_agent=None, max_redirects=None, retries=None))]
    fn new(
        timeout_secs: Option<f64>,
        user_agent: Option<String>,
        max_redirects: Option<u32>,
        retries: Option<u32>,
    ) -> PyResult<Self> {
        let mut builder = CoreClient::builder();
        if let Some(secs) = timeout_secs {
            // `from_secs_f64` panics on out-of-range input, which would surface
            // as an opaque PanicException; validate and raise a clean error.
            builder = builder.timeout(Duration::try_from_secs_f64(secs).map_err(|_| {
                PyValueError::new_err(format!(
                    "invalid timeout_secs: {secs} (must be a finite, non-negative number of seconds)"
                ))
            })?);
        }
        if let Some(user_agent) = user_agent {
            builder = builder.user_agent(&user_agent);
        }
        if let Some(max_redirects) = max_redirects {
            builder = builder.max_redirects(max_redirects);
        }
        if let Some(max_retries) = retries {
            builder = builder.retry(RetryPolicy {
                max_retries,
                ..Default::default()
            });
        }
        Ok(HttpClient {
            inner: builder.build(),
        })
    }

    /// Verbatim body decoding, suitable for response bodies that are not UTF-8.
    #[pyo3(signature = (url, headers=None, query=None))]
    fn get<'py>(
        &self,
        py: Python<'py>,
        url: &str,
        headers: Option<Vec<(String, String)>>,
        query: Option<Vec<(String, String)>>,
    ) -> PyResult<HttpResponse> {
        self.dispatch(py, "GET", url, None, headers, query)
    }

    #[pyo3(signature = (url, body=None, headers=None, query=None))]
    fn post<'py>(
        &self,
        py: Python<'py>,
        url: &str,
        body: Option<String>,
        headers: Option<Vec<(String, String)>>,
        query: Option<Vec<(String, String)>>,
    ) -> PyResult<HttpResponse> {
        self.dispatch(py, "POST", url, body, headers, query)
    }

    #[pyo3(signature = (url, body=None, headers=None, query=None))]
    fn put<'py>(
        &self,
        py: Python<'py>,
        url: &str,
        body: Option<String>,
        headers: Option<Vec<(String, String)>>,
        query: Option<Vec<(String, String)>>,
    ) -> PyResult<HttpResponse> {
        self.dispatch(py, "PUT", url, body, headers, query)
    }

    #[pyo3(signature = (url, headers=None, query=None))]
    fn delete<'py>(
        &self,
        py: Python<'py>,
        url: &str,
        headers: Option<Vec<(String, String)>>,
        query: Option<Vec<(String, String)>>,
    ) -> PyResult<HttpResponse> {
        self.dispatch(py, "DELETE", url, None, headers, query)
    }

    #[pyo3(signature = (method, url, body=None, headers=None, query=None))]
    fn request<'py>(
        &self,
        py: Python<'py>,
        method: &str,
        url: &str,
        body: Option<String>,
        headers: Option<Vec<(String, String)>>,
        query: Option<Vec<(String, String)>>,
    ) -> PyResult<HttpResponse> {
        self.dispatch(py, method, url, body, headers, query)
    }
}

impl HttpClient {
    fn dispatch(
        &self,
        py: Python<'_>,
        method: &str,
        url: &str,
        body: Option<String>,
        headers: Option<Vec<(String, String)>>,
        query: Option<Vec<(String, String)>>,
    ) -> PyResult<HttpResponse> {
        let method = match method.to_ascii_uppercase().as_str() {
            "GET" => Method::Get,
            "POST" => Method::Post,
            "PUT" => Method::Put,
            "DELETE" => Method::Delete,
            other => Method::Other(other.to_string()),
        };
        let mut builder = self.inner.request(method, url);
        if let Some(headers) = headers {
            for (name, value) in headers {
                builder = builder.header(name, value);
            }
        }
        if let Some(query) = query {
            for (name, value) in query {
                builder = builder.query(name, value);
            }
        }
        if let Some(body) = body {
            builder = builder.body(body);
        }
        // Release the GIL while doing blocking I/O so other Python threads
        // (and any asyncio loop on a worker thread) keep running.
        let sent = py.detach(|| builder.send());
        let response = sent.map_err(|e| to_py_err(py, e))?;
        let status = response.status();
        let headers = response
            .headers()
            .into_iter()
            .map(|h| (h.name, h.value))
            .collect();
        let read = py.detach(|| response.bytes());
        let body = read.map_err(|e| to_py_err(py, e))?;
        Ok(HttpResponse {
            status,
            headers,
            body,
        })
    }
}

pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    let http = PyModule::new(m.py(), "http")?;
    http.add_class::<HttpClient>()?;
    http.add_class::<HttpResponse>()?;
    http.add("HermesHttpError", m.py().get_type::<HermesHttpError>())?;
    m.add_submodule(&http)?;
    Ok(())
}
