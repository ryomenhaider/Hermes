//! Retry policy for the HTTP client.

use std::time::Duration;

/// Simple, explicit retry configuration.
///
/// Defaults to no retries; enable by setting `max_retries > 0`. Retries only
/// apply to idempotent methods and only for retryable transport errors or
/// 5xx status codes.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct RetryPolicy {
    pub max_retries: u32,
    pub base_backoff_ms: u64,
}

impl Default for RetryPolicy {
    fn default() -> Self {
        RetryPolicy {
            max_retries: 0,
            base_backoff_ms: 200,
        }
    }
}

impl RetryPolicy {
    /// Base backoff multiplied exponentially per attempt, capped to avoid huge
    /// sleeps on high retry counts.
    pub(crate) fn backoff(&self, attempt: u32) -> Duration {
        Duration::from_millis(self.base_backoff_ms.saturating_mul(1u64 << attempt.min(10)))
    }

    pub(crate) fn is_retryable_status(status: u16) -> bool {
        matches!(status, 500 | 502 | 503 | 504)
    }
}
