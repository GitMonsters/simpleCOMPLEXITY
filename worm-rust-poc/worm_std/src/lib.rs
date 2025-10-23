//! Worm Std - Security-Hardened Rust Standard Library
//!
//! This library provides a restricted version of Rust's standard library
//! that removes all network capabilities while preserving all other functionality.
//!
//! # Security Features
//!
//! - ❌ **No Network Access** - std::net module is completely removed
//! - ✅ **File I/O** - All file operations work normally
//! - ✅ **Collections** - All data structures available
//! - ✅ **Threading** - Safe concurrency primitives
//! - ⚠️  **Process** - Restricted subprocess with command filtering
//!
//! # Usage
//!
//! Replace your standard library imports:
//!
//! ```rust,ignore
//! // Instead of:
//! // use std::prelude::*;
//!
//! // Use:
//! use worm_std::prelude::*;
//! ```
//!
//! # Example
//!
//! ```rust
//! use worm_std::fs;
//!
//! fn main() -> worm_std::io::Result<()> {
//!     // This works - file I/O is allowed
//!     let contents = fs::read_to_string("input.txt")?;
//!     fs::write("output.txt", contents.to_uppercase())?;
//!     Ok(())
//! }
//! ```
//!
//! ```rust,compile_fail
//! use worm_std::net::TcpStream;  // ERROR: module `net` not found
//! ```

// Re-export most of std, excluding network modules
pub use std::{
    any,
    array,
    ascii,
    borrow,
    boxed,
    cell,
    char,
    clone,
    cmp,
    collections,
    convert,
    default,
    env,
    error,
    f32,
    f64,
    ffi,
    fmt,
    fs,
    future,
    hash,
    hint,
    i8,
    i16,
    i32,
    i64,
    i128,
    io,
    isize,
    iter,
    marker,
    mem,
    num,
    ops,
    option,
    os,
    panic,
    path,
    pin,
    primitive,
    ptr,
    rc,
    result,
    slice,
    str,
    string,
    sync,
    task,
    thread,
    time,
    u8,
    u16,
    u32,
    u64,
    u128,
    usize,
    vec,
};

// ============================================================================
// NETWORK MODULES - INTENTIONALLY NOT INCLUDED
// ============================================================================
//
// The following std modules are NOT re-exported:
//
// - std::net          - All network functionality (TcpStream, UdpSocket, etc.)
//
// Attempting to use these will result in compile-time errors:
//
//   error[E0432]: unresolved import `worm_std::net`
//
// This is the PRIMARY SECURITY FEATURE - network access is impossible
// at compile time, not just blocked at runtime.

// ============================================================================
// RESTRICTED PROCESS MODULE
// ============================================================================

pub mod process;

// ============================================================================
// WORM-SPECIFIC MODULES
// ============================================================================

/// Error types specific to Worm Rust
pub mod worm_error {
    use std::fmt;

    #[derive(Debug, Clone)]
    pub enum WormError {
        /// Attempted to execute a network command (curl, wget, etc.)
        NetworkCommandBlocked(String),

        /// Detected URL pattern in command arguments
        UrlPatternDetected(String),

        /// Generic security violation
        SecurityViolation(String),
    }

    impl fmt::Display for WormError {
        fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
            match self {
                WormError::NetworkCommandBlocked(cmd) => {
                    write!(f, "Network command blocked: '{}' - Worm Rust does not allow network commands", cmd)
                }
                WormError::UrlPatternDetected(url) => {
                    write!(f, "URL pattern detected: '{}' - possible network access attempt", url)
                }
                WormError::SecurityViolation(msg) => {
                    write!(f, "Security violation: {}", msg)
                }
            }
        }
    }

    impl std::error::Error for WormError {}
}

pub use worm_error::WormError;

// ============================================================================
// PRELUDE
// ============================================================================

/// The Worm Rust Prelude
///
/// Import this instead of std::prelude::*
pub mod prelude {
    pub use std::prelude::v1::*;

    // Make WormError available
    pub use crate::WormError;
}

// ============================================================================
// VERSION INFO
// ============================================================================

/// Check if running under Worm Rust
pub fn is_worm_rust() -> bool {
    std::env::var("WORM_RUST").is_ok()
}

/// Get Worm Rust version
pub const VERSION: &str = env!("CARGO_PKG_VERSION");

/// Print Worm Rust banner
pub fn print_banner() {
    eprintln!("🔒 Worm Rust v{} - Security-Hardened Rust", VERSION);
    eprintln!("   Network access: DISABLED");
    eprintln!("   Process spawn: FILTERED");
    eprintln!();
}
