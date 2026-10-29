//! Hermes-specific HTTP error types.

use std::error::Error;
use std::fmt;
use std::io;

/// Classifies failures that can occur while making an HTTP request.
///
/// The client maps the underlying library's errors onto these categories so
/// callers never have to depend on a particular HTTP implementation.
#[derive(Debug)]
pub enum HermesHttpError {
    InvalidUrl(String),
    Dns(String),
    Connection(String),
    Timeout,
    Tls(String),
    TooManyRedirects,
    Request(String),
    Response(String),
    Io(String),
    Json(String),
    Http { status: u16, message: String },
}

impl HermesHttpError {
    /// True when a retry might reasonably succeed. Produced before a response
    /// was received, so retrying is only safe for idempotent methods.
    pub(crate) fn is_retryable(&self) -> bool {
        matches!(
            self,
            HermesHttpError::Connection(_)
                | HermesHttpError::Dns(_)
                | HermesHttpError::Io(_)
                | HermesHttpError::Timeout
        )
    }
}

impl fmt::Display for HermesHttpError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            HermesHttpError::InvalidUrl(m) => write!(f, "invalid URL: {m}"),
            HermesHttpError::Dns(m) => write!(f, "DNS lookup failed: {m}"),
            HermesHttpError::Connection(m) => write!(f, "connection failed: {m}"),
            HermesHttpError::Timeout => f.write_str("request timed out"),
            HermesHttpError::Tls(m) => write!(f, "TLS failure: {m}"),
            HermesHttpError::TooManyRedirects => f.write_str("too many redirects"),
            HermesHttpError::Request(m) => write!(f, "invalid request: {m}"),
            HermesHttpError::Response(m) => write!(f, "invalid response: {m}"),
            HermesHttpError::Io(m) => write!(f, "I/O error: {m}"),
            HermesHttpError::Json(m) => write!(f, "invalid JSON: {m}"),
            HermesHttpError::Http { status, message } => {
                write!(f, "HTTP status {status}: {message}")
            }
        }
    }
}

impl Error for HermesHttpError {}

impl From<ureq::Error> for HermesHttpError {
    fn from(err: ureq::Error) -> Self {
        match err {
            ureq::Error::Status(status, response) => HermesHttpError::Http {
                status,
                message: response.status_text().to_string(),
            },
            ureq::Error::Transport(t) => t.into(),
        }
    }
}

impl From<ureq::Transport> for HermesHttpError {
    fn from(t: ureq::Transport) -> Self {
        let message = t.message().unwrap_or("").to_string();
        match t.kind() {
            ureq::ErrorKind::InvalidUrl | ureq::ErrorKind::UnknownScheme => {
                HermesHttpError::InvalidUrl(message)
            }
            ureq::ErrorKind::Dns => HermesHttpError::Dns(message),
            ureq::ErrorKind::ConnectionFailed | ureq::ErrorKind::ProxyConnect => {
                if has_rustls_source(&t) {
                    HermesHttpError::Tls(t.to_string())
                } else {
                    HermesHttpError::Connection(message)
                }
            }
            ureq::ErrorKind::Io => {
                if timed_out(&t) {
                    HermesHttpError::Timeout
                } else if has_rustls_source(&t) {
                    HermesHttpError::Tls(t.to_string())
                } else {
                    HermesHttpError::Io(t.to_string())
                }
            }
            ureq::ErrorKind::TooManyRedirects => HermesHttpError::TooManyRedirects,
            ureq::ErrorKind::InsecureRequestHttpsOnly | ureq::ErrorKind::InvalidProxyUrl => {
                HermesHttpError::Request(message)
            }
            ureq::ErrorKind::BadStatus
            | ureq::ErrorKind::BadHeader
            | ureq::ErrorKind::ProxyUnauthorized => HermesHttpError::Response(t.to_string()),
            ureq::ErrorKind::HTTP => HermesHttpError::Http {
                status: 0,
                message: t.to_string(),
            },
        }
    }
}

impl From<serde_json::Error> for HermesHttpError {
    fn from(err: serde_json::Error) -> Self {
        HermesHttpError::Json(err.to_string())
    }
}

/// True if any error in the chain is an `io::Error` signalling a timeout.
fn timed_out(t: &ureq::Transport) -> bool {
    each_source(t, |err| {
        err.downcast_ref::<io::Error>().is_some_and(|io_err| {
            matches!(
                io_err.kind(),
                io::ErrorKind::TimedOut | io::ErrorKind::WouldBlock
            )
        })
    })
}

/// True if any error in the chain originates from the TLS layer (rustls).
fn has_rustls_source(t: &ureq::Transport) -> bool {
    each_source(t, |err| {
        if err.downcast_ref::<rustls::Error>().is_some() {
            return true;
        }
        // rustls::Error is often buried as the payload of an io::Error, which
        // `source()` does not surface; `get_ref()` does.
        err.downcast_ref::<io::Error>().is_some_and(|io_err| {
            io_err
                .get_ref()
                .is_some_and(|inner| inner.downcast_ref::<rustls::Error>().is_some())
        })
    })
}

/// Walks the transport's source chain (plus each `io::Error`'s own payload).
fn each_source(
    t: &ureq::Transport,
    f: impl Fn(&(dyn std::error::Error + 'static)) -> bool,
) -> bool {
    let mut current = t.source();
    while let Some(source) = current {
        if f(source) {
            return true;
        }
        current = source.source();
    }
    false
}
