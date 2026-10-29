mod commands;

use clap::{Parser, Subcommand};
use std::ffi::OsString;

/// Hermes command-line interface.
///
/// This module only parses arguments, dispatches commands, formats output,
/// and reports exit codes. All real work happens in the Hermes Rust core.
/// Both the native `hermes` binary and the Python `_rust.cli` module funnel
/// through [`run_from`].
#[derive(Parser)]
#[command(name = "hermes", version, about = "Hermes command-line interface")]
pub struct Cli {
    #[command(subcommand)]
    pub command: Command,
}

#[derive(Subcommand, Debug, Clone, Copy)]
pub enum Command {
    /// Fetch data from a source
    Fetch,
    /// Inspect data
    Inspect,
    /// Manage datasets
    Dataset,
    /// Work with entities
    Entity,
}

/// Run the CLI against the process arguments, returning the exit code.
pub fn run() -> i32 {
    run_from(std::env::args_os())
}

/// Run the CLI against an explicit argv (`argv[0]` first), returning the exit code.
pub fn run_from<I, T>(args: I) -> i32
where
    I: IntoIterator<Item = T>,
    T: Into<OsString> + Clone,
{
    match Cli::try_parse_from(args) {
        Ok(cli) => commands::exec(cli.command),
        Err(err) => {
            // clap already formats the help/version/usage-error message itself.
            let _ = err.print();
            match err.kind() {
                clap::error::ErrorKind::DisplayHelp | clap::error::ErrorKind::DisplayVersion => 0,
                _ => 2,
            }
        }
    }
}

/// Python entry point: `_rust.cli.main(argv)` -> exit code.
#[pyo3::pyfunction]
fn main(args: Vec<String>) -> i32 {
    run_from(args.into_iter())
}

pub fn register(m: &pyo3::prelude::Bound<'_, pyo3::prelude::PyModule>) -> pyo3::PyResult<()> {
    use pyo3::types::PyModuleMethods;
    m.add_function(pyo3::wrap_pyfunction!(main, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parses_version_and_help_flags() {
        assert_eq!(run_from(["hermes", "--version"]), 0);
        assert_eq!(run_from(["hermes", "--help"]), 0);
    }

    #[test]
    fn parses_every_subcommand() {
        for name in ["fetch", "inspect", "dataset", "entity"] {
            let args = ["hermes".to_string(), name.to_string()];
            Cli::try_parse_from(args).unwrap_or_else(|e| panic!("{name} should parse: {e}"));
        }
    }

    #[test]
    fn invalid_subcommand_is_a_usage_error() {
        assert_eq!(run_from(["hermes", "bogus"]), 2);
    }

    #[test]
    fn unimplemented_commands_exit_nonzero() {
        for cmd in [
            Command::Fetch,
            Command::Inspect,
            Command::Dataset,
            Command::Entity,
        ] {
            assert_eq!(commands::exec(cmd), 1);
        }
    }
}
