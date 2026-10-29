//! Hermes HTTP response wrapper.

use std::fmt;
use std::io::Read;

use crate::http::HermesHttpError;

/// A single HTTP header (request or response).
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Header {
    pub name: String,
    pub value: String,
}

/// An HTTP response. Owns the received body and hides the underlying library.
pub struct Response {
    inner: ureq::Response,
}

impl fmt::Debug for Response {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "Response(status: {})", self.status())
    }
}

impl Response {
    pub(crate) fn from_ureq(inner: ureq::Response) -> Self {
        Response { inner }
    }

    pub fn status(&self) -> u16 {
        self.inner.status()
    }

    pub fn status_text(&self) -> &str {
        self.inner.status_text()
    }

    /// Reads a single response header by name (case-insensitive).
    pub fn header(&self, name: &str) -> Option<&str> {
        self.inner.header(name)
    }

    /// Returns all response headers. Repeated headers (e.g. `Set-Cookie`)
    /// appear once per value, in received order.
    pub fn headers(&self) -> Vec<Header> {
        // `headers_names()` lists one entry per header line, so a repeated
        // header shows up multiple times; dedupe while keeping first-seen
        // order, then collect every value for each unique name.
        let mut names: Vec<String> = Vec::new();
        for name in self.inner.headers_names() {
            if !names.contains(&name) {
                names.push(name);
            }
        }
        names
            .into_iter()
            .flat_map(|name| {
                self.inner.all(&name).into_iter().map(move |value| Header {
                    name: name.clone(),
                    value: value.to_string(),
                })
            })
            .collect()
    }

    /// Errors only if the response has a non-2xx status code.
    pub fn error_for_status(&self) -> Result<(), HermesHttpError> {
        let status = self.inner.status();
        if (200..300).contains(&status) {
            Ok(())
        } else {
            Err(HermesHttpError::Http {
                status,
                message: self.inner.status_text().to_string(),
            })
        }
    }

    /// Consumes the response, returning a reader for incremental body access.
    pub fn reader(self) -> Box<dyn Read + Send + Sync + 'static> {
        self.inner.into_reader()
    }

    /// Consumes the response and reads the entire body into memory.
    pub fn bytes(self) -> Result<Vec<u8>, HermesHttpError> {
        let mut reader = self.inner.into_reader();
        let mut buf = Vec::new();
        reader
            .read_to_end(&mut buf)
            .map_err(|e| HermesHttpError::Response(format!("failed reading response body: {e}")))?;
        Ok(buf)
    }

    /// Consumes the response and decodes the body as UTF-8 text.
    pub fn text(self) -> Result<String, HermesHttpError> {
        let bytes = self.bytes()?;
        String::from_utf8(bytes).map_err(|e| {
            HermesHttpError::Response(format!("response body is not valid UTF-8: {e}"))
        })
    }

    /// Consumes the response and parses the body as JSON.
    pub fn json<T: serde::de::DeserializeOwned>(self) -> Result<T, HermesHttpError> {
        let bytes = self.bytes()?;
        serde_json::from_slice(&bytes).map_err(HermesHttpError::from)
    }
}
