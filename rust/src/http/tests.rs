//! Deterministic HTTP client tests against local servers. No internet access.

use std::io::{Read, Write};
use std::net::{IpAddr, TcpListener, TcpStream};
use std::sync::Arc;
use std::sync::atomic::{AtomicU32, Ordering};
use std::thread;
use std::time::Duration;

use crate::http::{HermesHttpError, HttpClient, Method, RetryPolicy};

fn listen() -> (TcpListener, String) {
    let listener = TcpListener::bind("127.0.0.1:0").unwrap();
    let url = format!("http://{}", listener.local_addr().unwrap());
    (listener, url)
}

/// Serves requests from the listener, calling `handler(request) -> response`
/// for each connection. Handlers decide what to return per request path.
fn serve(mut handler: impl FnMut(String) -> String + Send + 'static, listener: TcpListener) {
    thread::spawn(move || {
        for stream in listener.incoming() {
            let Ok(mut stream) = stream else { break };
            let request = read_request(&mut stream);
            let response = handler(request);
            let _ = stream.write_all(response.as_bytes());
        }
    });
}

/// Reads one HTTP request (headers + body per Content-Length).
fn read_request(stream: &mut TcpStream) -> String {
    let mut buf = Vec::new();
    let mut chunk = [0u8; 8192];
    loop {
        let n = stream.read(&mut chunk).unwrap_or(0);
        if n == 0 {
            break;
        }
        buf.extend_from_slice(&chunk[..n]);
        let text = String::from_utf8_lossy(&buf);
        if let Some(head_end) = text.find("\r\n\r\n").map(|pos| pos + 4) {
            let content_length = text[..head_end]
                .split("\r\n")
                .find_map(|line| {
                    let (name, value) = line.split_once(':')?;
                    name.trim()
                        .eq_ignore_ascii_case("content-length")
                        .then(|| value.trim().parse::<usize>().unwrap_or(0))
                })
                .unwrap_or(0);
            if buf.len() >= head_end + content_length {
                break;
            }
        }
    }
    String::from_utf8_lossy(&buf).to_string()
}

fn http_response(status: u16, reason: &str, headers: &[(&str, &str)], body: &str) -> String {
    let mut response = format!("HTTP/1.1 {status} {reason}\r\n");
    for (name, value) in headers {
        response.push_str(&format!("{name}: {value}\r\n"));
    }
    response.push_str(&format!(
        "Content-Length: {}\r\nConnection: close\r\n\r\n{}",
        body.len(),
        body
    ));
    response
}

#[test]
fn get_returns_status_body_and_headers() {
    let (listener, url) = listen();
    serve(
        move |request| {
            assert!(request.starts_with("GET /hello HTTP/1.1"), "got: {request}");
            http_response(200, "OK", &[("Content-Type", "text/plain")], "hello")
        },
        listener,
    );
    let client = HttpClient::new();
    let response = client.get(&format!("{url}/hello")).send().unwrap();
    assert_eq!(response.status(), 200);
    assert_eq!(response.status_text(), "OK");
    assert_eq!(response.header("content-type"), Some("text/plain"));
    let header_names: Vec<String> = response.headers().into_iter().map(|h| h.name).collect();
    assert!(header_names.iter().any(|n| n == "content-type"));
    assert_eq!(response.text().unwrap(), "hello");
}

#[test]
fn post_sends_body() {
    let (listener, url) = listen();
    serve(
        move |request| {
            assert!(request.starts_with("POST / HTTP/1.1"), "got: {request}");
            let body = request.split("\r\n\r\n").nth(1).unwrap_or("").to_string();
            http_response(200, "OK", &[], &body)
        },
        listener,
    );
    let client = HttpClient::new();
    let response = client.post(&url).body("payload=1").send().unwrap();
    assert_eq!(response.text().unwrap(), "payload=1");
}

#[test]
fn request_headers_are_sent() {
    let (listener, url) = listen();
    let seen = Arc::new(AtomicU32::new(0));
    let seen_thread = Arc::clone(&seen);
    serve(
        move |request| {
            let lower = request.to_lowercase();
            if lower.contains("x-custom: abc") && lower.contains("authorization: bearer tok") {
                seen_thread.store(1, Ordering::SeqCst);
            }
            http_response(200, "OK", &[], "")
        },
        listener,
    );
    let client = HttpClient::new();
    client
        .get(&url)
        .header("X-Custom", "abc")
        .header("Authorization", "Bearer tok")
        .send()
        .unwrap();
    assert_eq!(seen.load(Ordering::SeqCst), 1);
}

#[test]
fn default_headers_and_user_agent_are_sent() {
    let (listener, url) = listen();
    let seen = Arc::new(AtomicU32::new(0));
    let seen_thread = Arc::clone(&seen);
    serve(
        move |request| {
            let lower = request.to_lowercase();
            if lower.contains("accept: application/json")
                && lower.contains("user-agent: hermes-http")
            {
                seen_thread.store(1, Ordering::SeqCst);
            }
            http_response(200, "OK", &[], "")
        },
        listener,
    );
    let client = HttpClient::builder()
        .default_header("Accept", "application/json")
        .build();
    client.get(&url).send().unwrap();
    assert_eq!(seen.load(Ordering::SeqCst), 1);
}

#[test]
fn query_parameters_are_url_encoded() {
    let (listener, url) = listen();
    serve(
        move |request| {
            let line = request.lines().next().unwrap_or("").to_string();
            http_response(200, "OK", &[], &line)
        },
        listener,
    );
    let client = HttpClient::new();
    let response = client
        .get(&format!("{url}/search"))
        .query("limit", "100")
        .query("symbol", "AAPL")
        .query("q", "a b&c=d")
        .send()
        .unwrap();
    let request_line = response.text().unwrap();
    assert!(request_line.contains("limit=100"), "{request_line}");
    assert!(request_line.contains("symbol=AAPL"), "{request_line}");
    assert!(request_line.contains("q=a+b%26c%3Dd"), "{request_line}");
}

#[test]
fn duplicate_response_headers_are_all_returned() {
    let (listener, url) = listen();
    serve(
        move |_| {
            http_response(
                200,
                "OK",
                &[("Set-Cookie", "a=1"), ("Set-Cookie", "b=2")],
                "",
            )
        },
        listener,
    );
    let client = HttpClient::new();
    let response = client.get(&url).send().unwrap();
    let headers = response.headers();
    let cookies: Vec<&str> = headers
        .iter()
        .filter(|h| h.name.eq_ignore_ascii_case("set-cookie"))
        .map(|h| h.value.as_str())
        .collect();
    assert_eq!(cookies, ["a=1", "b=2"]);
}

#[test]
fn non_2xx_status_is_reported_with_body() {
    let (listener, url) = listen();
    serve(
        move |_| http_response(404, "Not Found", &[], "missing"),
        listener,
    );
    let client = HttpClient::new();
    let response = client.get(&url).send().unwrap();
    assert_eq!(response.status(), 404);
    assert!(matches!(
        response.error_for_status(),
        Err(HermesHttpError::Http { .. })
    ));
    assert_eq!(response.text().unwrap(), "missing");
}

#[test]
fn json_body_is_parsed() {
    let (listener, url) = listen();
    serve(
        move |_| {
            http_response(
                200,
                "OK",
                &[("Content-Type", "application/json")],
                r#"{"a": 1, "b": [true, null]}"#,
            )
        },
        listener,
    );
    let client = HttpClient::new();
    let value: serde_json::Value = client.get(&url).send().unwrap().json().unwrap();
    assert_eq!(value["a"], 1);
    assert_eq!(value["b"][0], true);
}

#[test]
fn times_out_when_server_is_unresponsive() {
    let (listener, url) = listen();
    serve(
        move |_| {
            thread::sleep(Duration::from_secs(5));
            http_response(200, "OK", &[], "late")
        },
        listener,
    );
    let client = HttpClient::builder()
        .timeout(Duration::from_millis(150))
        .build();
    let err = client.get(&url).send().unwrap_err();
    assert!(matches!(err, HermesHttpError::Timeout), "got {err:?}");
}

#[test]
fn invalid_url_is_rejected() {
    let client = HttpClient::new();
    let err = client.get("not a url").send().unwrap_err();
    assert!(matches!(err, HermesHttpError::InvalidUrl(_)), "got {err:?}");
    let err = client.get("ftp://example").send().unwrap_err();
    assert!(matches!(err, HermesHttpError::InvalidUrl(_)), "got {err:?}");
}

#[test]
fn connection_failure_is_reported() {
    let listener = TcpListener::bind("127.0.0.1:0").unwrap();
    let addr = listener.local_addr().unwrap();
    drop(listener);
    let client = HttpClient::new();
    let err = client.get(&format!("http://{addr}/")).send().unwrap_err();
    assert!(matches!(err, HermesHttpError::Connection(_)), "got {err:?}");
}

#[test]
fn redirects_are_followed() {
    let (listener, url) = listen();
    let location = format!("{url}/final");
    serve(
        move |request| {
            if request.contains("/final") {
                http_response(200, "OK", &[], "done")
            } else {
                http_response(302, "Found", &[("Location", location.as_str())], "")
            }
        },
        listener,
    );
    let client = HttpClient::new();
    let response = client.get(&url).send().unwrap();
    assert_eq!(response.status(), 200);
    assert_eq!(response.text().unwrap(), "done");
}

#[test]
fn retries_idempotent_requests_on_5xx() {
    let (listener, url) = listen();
    let calls = Arc::new(AtomicU32::new(0));
    let calls_thread = Arc::clone(&calls);
    serve(
        move |_| {
            if calls_thread.fetch_add(1, Ordering::SeqCst) == 0 {
                http_response(500, "Internal Server Error", &[], "")
            } else {
                http_response(200, "OK", &[], "ok")
            }
        },
        listener,
    );
    let client = HttpClient::builder()
        .retry(RetryPolicy {
            max_retries: 2,
            base_backoff_ms: 10,
        })
        .build();
    let response = client.get(&url).send().unwrap();
    assert_eq!(response.status(), 200);
    assert_eq!(calls.load(Ordering::SeqCst), 2);
}

#[test]
fn does_not_retry_non_idempotent_requests() {
    let (listener, url) = listen();
    let calls = Arc::new(AtomicU32::new(0));
    let calls_thread = Arc::clone(&calls);
    serve(
        move |_| {
            calls_thread.fetch_add(1, Ordering::SeqCst);
            http_response(500, "Internal Server Error", &[], "")
        },
        listener,
    );
    let client = HttpClient::builder()
        .retry(RetryPolicy {
            max_retries: 3,
            base_backoff_ms: 10,
        })
        .build();
    let response = client.post(&url).body("payload").send().unwrap();
    assert_eq!(response.status(), 500);
    assert_eq!(calls.load(Ordering::SeqCst), 1);
}

#[test]
fn arbitrary_methods_are_supported() {
    let (listener, url) = listen();
    serve(
        move |request| {
            assert!(request.starts_with("PATCH / HTTP/1.1"), "got: {request}");
            http_response(200, "OK", &[], "patched")
        },
        listener,
    );
    let client = HttpClient::new();
    let response = client
        .request(Method::Other("PATCH".to_string()), &url)
        .send()
        .unwrap();
    assert_eq!(response.text().unwrap(), "patched");
}

// --- HTTPS via a local rustls server -------------------------------------

fn make_tls_keypair() -> (rcgen::Certificate, rcgen::KeyPair) {
    let mut params = rcgen::CertificateParams::new(Vec::new()).unwrap();
    params.subject_alt_names = vec![rcgen::SanType::IpAddress(IpAddr::from([127, 0, 0, 1]))];
    let key_pair = rcgen::KeyPair::generate().unwrap();
    let cert = params.self_signed(&key_pair).unwrap();
    (cert, key_pair)
}

/// Starts a one-shot HTTPS server answering with "allowed". Returns the URL,
/// the certificate, and the key pair used so tests can decide on trust.
fn start_https_server() -> (String, rcgen::Certificate, rcgen::KeyPair) {
    // rustls 0.23 needs an explicit process default crypto provider; ring is
    // what ureq already enables, so reuse it. Installing twice is harmless.
    let _ =
        rustls::crypto::CryptoProvider::install_default(rustls::crypto::ring::default_provider());
    let listener = TcpListener::bind("127.0.0.1:0").unwrap();
    let url = format!("https://{}/", listener.local_addr().unwrap());
    let (cert, key_pair) = make_tls_keypair();

    let server_config = rustls::ServerConfig::builder()
        .with_no_client_auth()
        .with_single_cert(
            vec![cert.der().clone()],
            rustls::pki_types::PrivatePkcs8KeyDer::from(key_pair.serialize_der()).into(),
        )
        .unwrap();

    thread::spawn(move || {
        let (mut tcp, _) = listener.accept().unwrap();
        let mut conn = rustls::ServerConnection::new(std::sync::Arc::new(server_config)).unwrap();
        let mut request = Vec::new();
        let mut buf = [0u8; 4096];
        loop {
            if conn.complete_io(&mut tcp).is_err() {
                break;
            }
            loop {
                match conn.reader().read(&mut buf) {
                    Ok(0) | Err(_) => break,
                    Ok(n) => request.extend_from_slice(&buf[..n]),
                }
            }
            if String::from_utf8_lossy(&request).contains("\r\n\r\n") {
                break;
            }
        }
        let response = "HTTP/1.1 200 OK\r\nContent-Length: 7\r\nConnection: close\r\n\r\nallowed";
        if conn.writer().write_all(response.as_bytes()).is_ok() {
            let _ = conn.writer().flush();
            let _ = conn.complete_io(&mut tcp);
        }
    });
    (url, cert, key_pair)
}

#[test]
fn https_rejects_untrusted_certificate() {
    let (url, _, _) = start_https_server();
    let client = HttpClient::new();
    let err = client.get(&url).send().unwrap_err();
    assert!(matches!(err, HermesHttpError::Tls(_)), "got {err:?}");
}

#[test]
fn https_succeeds_with_trusted_certificate() {
    let _ =
        rustls::crypto::CryptoProvider::install_default(rustls::crypto::ring::default_provider());
    let (url, cert, _) = start_https_server();
    let mut roots = rustls::RootCertStore::empty();
    roots.add(cert.der().clone()).unwrap();
    let client_config = rustls::ClientConfig::builder()
        .with_root_certificates(roots)
        .with_no_client_auth();
    let client = HttpClient::builder()
        .tls_config(Arc::new(client_config))
        .build();
    let response = client.get(&url).send().unwrap();
    assert_eq!(response.text().unwrap(), "allowed");
}
