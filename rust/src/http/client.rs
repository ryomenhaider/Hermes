//! The Hermes synchronous HTTP client.

use std::sync::Arc;
use std::time::Duration;

use ureq::OrAnyStatus;

use crate::http::retry::RetryPolicy;
use crate::http::{Body, Header, HermesHttpError, Method, RequestBuilder, Response};

/// A reusable synchronous HTTP client, built from an [`HttpClientBuilder`].
///
/// The client owns connection configuration (timeout, user agent, default
/// headers, retry policy) and applies it to every request.
#[derive(Debug, Clone)]
pub struct HttpClient {
    agent: ureq::Agent,
    retry: RetryPolicy,
    default_headers: Vec<Header>,
}

/// Configuration for an [`HttpClient`].
#[derive(Clone)]
pub struct HttpClientBuilder {
    timeout: Duration,
    user_agent: Option<String>,
    max_redirects: u32,
    retry: RetryPolicy,
    default_headers: Vec<Header>,
    tls_config: Option<Arc<rustls::ClientConfig>>,
}

impl Default for HttpClientBuilder {
    fn default() -> Self {
        HttpClientBuilder {
            timeout: Duration::from_secs(30),
            user_agent: Some(format!("hermes-http/{}", env!("CARGO_PKG_VERSION"))),
            max_redirects: 10,
            retry: RetryPolicy::default(),
            default_headers: Vec::new(),
            tls_config: None,
        }
    }
}

impl HttpClientBuilder {
    /// Whole-request timeout, including reading the response.
    pub fn timeout(mut self, timeout: Duration) -> Self {
        self.timeout = timeout;
        self
    }

    pub fn user_agent(mut self, user_agent: &str) -> Self {
        self.user_agent = Some(user_agent.to_string());
        self
    }

    /// Maximum number of redirects the client will follow.
    pub fn max_redirects(mut self, max_redirects: u32) -> Self {
        self.max_redirects = max_redirects;
        self
    }

    pub fn retry(mut self, retry: RetryPolicy) -> Self {
        self.retry = retry;
        self
    }

    pub fn default_header(mut self, name: &str, value: &str) -> Self {
        self.default_headers.push(Header {
            name: name.to_string(),
            value: value.to_string(),
        });
        self
    }

    /// Overrides the TLS configuration, e.g. to trust a private CA.
    pub fn tls_config(mut self, config: Arc<rustls::ClientConfig>) -> Self {
        self.tls_config = Some(config);
        self
    }

    pub fn build(self) -> HttpClient {
        let mut agent = ureq::AgentBuilder::new()
            .timeout(self.timeout)
            .timeout_connect(self.timeout)
            .timeout_read(self.timeout)
            .timeout_write(self.timeout)
            .redirects(self.max_redirects);
        if let Some(user_agent) = &self.user_agent {
            agent = agent.user_agent(user_agent);
        }
        if let Some(tls_config) = self.tls_config {
            agent = agent.tls_config(tls_config);
        }
        HttpClient {
            agent: agent.build(),
            retry: self.retry,
            default_headers: self.default_headers,
        }
    }
}

impl Default for HttpClient {
    fn default() -> Self {
        Self::new()
    }
}

impl HttpClient {
    /// A client with default configuration (30s timeout, no retries).
    pub fn new() -> HttpClient {
        HttpClient::builder().build()
    }

    pub fn builder() -> HttpClientBuilder {
        HttpClientBuilder::default()
    }

    pub fn get(&self, url: &str) -> RequestBuilder {
        self.request(Method::Get, url)
    }

    pub fn post(&self, url: &str) -> RequestBuilder {
        self.request(Method::Post, url)
    }

    pub fn put(&self, url: &str) -> RequestBuilder {
        self.request(Method::Put, url)
    }

    pub fn delete(&self, url: &str) -> RequestBuilder {
        self.request(Method::Delete, url)
    }

    pub fn request(&self, method: Method, url: &str) -> RequestBuilder {
        RequestBuilder::new(self.clone(), method, url.to_string())
    }

    pub(crate) fn execute_with_retry(
        &self,
        rb: &RequestBuilder,
    ) -> Result<Response, HermesHttpError> {
        let mut attempt = 0u32;
        loop {
            let result = self.execute(rb);
            let retryable = match &result {
                Ok(resp) => RetryPolicy::is_retryable_status(resp.status()),
                Err(err) => err.is_retryable(),
            };
            if !(rb.method().is_idempotent() && attempt < self.retry.max_retries && retryable) {
                return result;
            }
            std::thread::sleep(self.retry.backoff(attempt));
            attempt += 1;
        }
    }

    fn execute(&self, rb: &RequestBuilder) -> Result<Response, HermesHttpError> {
        let mut req = self.agent.request(rb.method().as_str(), rb.url());
        for header in self.default_headers.iter().chain(rb.headers()) {
            req = req.set(&header.name, &header.value);
        }
        for (name, value) in rb.query_params() {
            req = req.query(name, value);
        }

        let result: Result<ureq::Response, ureq::Error> = match rb.request_body() {
            None => req.call(),
            Some(Body::Bytes(bytes)) => req.send_bytes(bytes),
            Some(Body::Text(text)) => req.send_string(text),
        };
        // Non-2xx responses are still responses: callers inspect `status`.
        result
            .or_any_status()
            .map(Response::from_ureq)
            .map_err(HermesHttpError::from)
    }
}
