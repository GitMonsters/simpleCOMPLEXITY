//! Restricted Process Module
//!
//! This module provides a filtered version of std::process that blocks
//! network-related commands while allowing safe local operations.

use crate::WormError;
use std::ffi::OsStr;
use std::io;

// Re-export safe types from std::process
pub use std::process::{Child, ChildStderr, ChildStdin, ChildStdout, ExitStatus, Output, Stdio};

/// List of blocked commands that could be used for network access
const BLOCKED_COMMANDS: &[&str] = &[
    // Network clients
    "curl",
    "wget",
    "nc",
    "netcat",
    "telnet",
    "ssh",
    "scp",
    "sftp",
    "ftp",
    "lftp",
    // Network tools
    "ping",
    "ping6",
    "traceroute",
    "traceroute6",
    "nmap",
    "ncat",
    // DNS tools
    "nslookup",
    "dig",
    "host",
    // HTTP tools
    "httpie",
    "http",
    "fetch",
    // Other
    "socat",
    "rsync", // Can use network
];

/// URL patterns that might indicate network access
const URL_PATTERNS: &[&str] = &["http://", "https://", "ftp://", "ssh://", "tcp://", "udp://"];

/// Check if a command is blocked
fn is_blocked_command(program: &str) -> bool {
    let program_lower = program.to_lowercase();
    let base_cmd = std::path::Path::new(&program_lower)
        .file_name()
        .and_then(|s| s.to_str())
        .unwrap_or(&program_lower);

    BLOCKED_COMMANDS.contains(&base_cmd)
}

/// Check if a string contains URL patterns
fn contains_url_pattern(s: &str) -> bool {
    URL_PATTERNS.iter().any(|pattern| s.contains(pattern))
}

/// A restricted version of std::process::Command
///
/// This command builder blocks execution of network-related commands
/// and warns about URL patterns in arguments.
pub struct Command {
    inner: std::process::Command,
    program: String,
    has_url_warning: bool,
}

impl Command {
    /// Creates a new Command with security checks
    ///
    /// # Errors
    ///
    /// Returns `WormError::NetworkCommandBlocked` if the command is in the blocklist
    ///
    /// # Example
    ///
    /// ```rust
    /// use worm_std::process::Command;
    ///
    /// // This works
    /// let output = Command::new("ls").unwrap().output();
    ///
    /// // This fails at creation
    /// let result = Command::new("curl");
    /// assert!(result.is_err());
    /// ```
    pub fn new<S: AsRef<OsStr>>(program: S) -> Result<Command, WormError> {
        let program_str = program.as_ref().to_string_lossy().to_string();

        // Security check: block network commands
        if is_blocked_command(&program_str) {
            return Err(WormError::NetworkCommandBlocked(program_str));
        }

        Ok(Command {
            inner: std::process::Command::new(program),
            program: program_str,
            has_url_warning: false,
        })
    }

    /// Adds an argument to the command
    ///
    /// Warns if the argument contains URL patterns
    pub fn arg<S: AsRef<OsStr>>(&mut self, arg: S) -> &mut Command {
        let arg_str = arg.as_ref().to_string_lossy();

        // Warning: check for URLs in arguments
        if contains_url_pattern(&arg_str) {
            if !self.has_url_warning {
                eprintln!(
                    "⚠️  WORM WARNING: URL pattern detected in command '{}': {}",
                    self.program, arg_str
                );
                eprintln!("   This may be attempting network access");
                self.has_url_warning = true;
            }
        }

        self.inner.arg(arg);
        self
    }

    /// Adds multiple arguments
    pub fn args<I, S>(&mut self, args: I) -> &mut Command
    where
        I: IntoIterator<Item = S>,
        S: AsRef<OsStr>,
    {
        for arg in args {
            self.arg(arg);
        }
        self
    }

    /// Sets the working directory
    pub fn current_dir<P: AsRef<std::path::Path>>(&mut self, dir: P) -> &mut Command {
        self.inner.current_dir(dir);
        self
    }

    /// Sets an environment variable
    pub fn env<K, V>(&mut self, key: K, val: V) -> &mut Command
    where
        K: AsRef<OsStr>,
        V: AsRef<OsStr>,
    {
        self.inner.env(key, val);
        self
    }

    /// Clears all environment variables
    pub fn env_clear(&mut self) -> &mut Command {
        self.inner.env_clear();
        self
    }

    /// Removes an environment variable
    pub fn env_remove<K: AsRef<OsStr>>(&mut self, key: K) -> &mut Command {
        self.inner.env_remove(key);
        self
    }

    /// Configures stdin
    pub fn stdin<T: Into<Stdio>>(&mut self, cfg: T) -> &mut Command {
        self.inner.stdin(cfg);
        self
    }

    /// Configures stdout
    pub fn stdout<T: Into<Stdio>>(&mut self, cfg: T) -> &mut Command {
        self.inner.stdout(cfg);
        self
    }

    /// Configures stderr
    pub fn stderr<T: Into<Stdio>>(&mut self, cfg: T) -> &mut Command {
        self.inner.stderr(cfg);
        self
    }

    /// Spawns the command
    pub fn spawn(&mut self) -> io::Result<Child> {
        self.inner.spawn()
    }

    /// Executes the command and waits for completion
    pub fn output(&mut self) -> io::Result<Output> {
        self.inner.output()
    }

    /// Executes the command and waits for it to finish
    pub fn status(&mut self) -> io::Result<ExitStatus> {
        self.inner.status()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_allowed_commands() {
        // These should all succeed
        assert!(Command::new("ls").is_ok());
        assert!(Command::new("cat").is_ok());
        assert!(Command::new("echo").is_ok());
        assert!(Command::new("grep").is_ok());
        assert!(Command::new("find").is_ok());
    }

    #[test]
    fn test_blocked_commands() {
        // These should all fail
        assert!(Command::new("curl").is_err());
        assert!(Command::new("wget").is_err());
        assert!(Command::new("nc").is_err());
        assert!(Command::new("ssh").is_err());
        assert!(Command::new("ping").is_err());
    }

    #[test]
    fn test_url_detection() {
        assert!(contains_url_pattern("http://example.com"));
        assert!(contains_url_pattern("https://evil.com"));
        assert!(contains_url_pattern("ftp://server.com"));
        assert!(!contains_url_pattern("normal string"));
    }
}
