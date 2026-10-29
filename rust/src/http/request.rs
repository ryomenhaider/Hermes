//! Request building.

use crate::http::{Header, HermesHttpError, HttpClient, Response};

/// An HTTP method. `Other` allows arbitrary methods without a redesign.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Method {
    Get,
    Post,
    Put,
    Delete,
    Other(String),
}

impl Method {
    pub fn as_str(&self) -> &str {
        match self {
            Method::Get => "GET",
            Method::Post => "POST",
            Method::Put => "PUT",
            Method::Delete => "DELETE",
            Method::Other(m) => m,
        }
    }

    /// Retrying a request is only safe when the method is idempotent.
    pub(crate) fn is_idempotent(&self) -> bool {
        matches!(self, Method::Get | Method::Put | Method::Delete)
    }
}

/// A request body. The client stays agnostic about the payload format.
#[derive(Debug, Clone)]
pub enum Body {
    Bytes(Vec<u8>),
    Text(String),
}

impl From<&str> for Body {
    fn from(value: &str) -> Self {
        Body::Text(value.to_string())
    }
}

impl From<String> for Body {
    fn from(value: String) -> Self {
        Body::Text(value)
    }
}

impl From<&[u8]> for Body {
    fn from(value: &[u8]) -> Self {
        Body::Bytes(value.to_vec())
    }
}

impl From<Vec<u8>> for Body {
    fn from(value: Vec<u8>) -> Self {
        Body::Bytes(value)
    }
}

/// Builder for a single request. Produced by the client and executed via
/// [`RequestBuilder::send`].
#[derive(Debug, Clone)]
pub struct RequestBuilder {
    client: HttpClient,
    method: Method,
    url: String,
    headers: Vec<Header>,
    query: Vec<(String, String)>,
    body: Option<Body>,
}

impl RequestBuilder {
    pub(crate) fn new(client: HttpClient, method: Method, url: String) -> Self {
        RequestBuilder {
            client,
            method,
            url,
            headers: Vec::new(),
            query: Vec::new(),
            body: None,
        }
    }

    pub fn method(&self) -> &Method {
        &self.method
    }

    pub fn url(&self) -> &str {
        &self.url
    }

    pub fn query_params(&self) -> &[(String, String)] {
        &self.query
    }

    pub(crate) fn headers(&self) -> &[Header] {
        &self.headers
    }

    pub(crate) fn request_body(&self) -> Option<&Body> {
        self.body.as_ref()
    }

    pub fn header(mut self, name: impl Into<String>, value: impl Into<String>) -> Self {
        self.headers.push(Header {
            name: name.into(),
            value: value.into(),
        });
        self
    }

    pub fn query(mut self, name: impl Into<String>, value: impl Into<String>) -> Self {
        self.query.push((name.into(), value.into()));
        self
    }

    pub fn body(mut self, body: impl Into<Body>) -> Self {
        self.body = Some(body.into());
        self
    }

    /// Sends the request, returning the response.
    pub fn send(self) -> Result<Response, HermesHttpError> {
        self.client.execute_with_retry(&self)
    }
}
