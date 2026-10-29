//! Synchronous HTTP client. The core lives in this module; `python` is a thin
//! PyO3 shim so Python never sees `ureq` types.

mod client;
mod error;
mod python;
mod request;
mod response;
mod retry;
#[cfg(test)]
mod tests;

pub use client::{HttpClient, HttpClientBuilder};
pub use error::HermesHttpError;
pub use request::{Body, Method, RequestBuilder};
pub use response::{Header, Response};
pub use retry::RetryPolicy;

pub(crate) use python::register;
