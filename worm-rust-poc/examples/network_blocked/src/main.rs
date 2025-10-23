// Network Blocked Example - Worm Rust
//
// This demonstrates that network commands are blocked at runtime
//
// Note: Compile-time network blocking (std::net) cannot be demonstrated
// in a compilable example, but see README for how it works.

use worm_std::prelude::*;
use worm_std::process::Command;

fn main() {
    worm_std::print_banner();

    println!("Network Security Demonstration");
    println!("==============================");
    println!();

    // Test 1: Allowed commands work
    println!("Test 1: Allowed commands");
    println!("------------------------");

    match Command::new("echo") {
        Ok(mut cmd) => {
            println!("✓ Command::new(\"echo\") succeeded");
            match cmd.arg("Hello from subprocess").output() {
                Ok(output) => {
                    println!("✓ Command executed successfully");
                    println!("  Output: {}", String::from_utf8_lossy(&output.stdout));
                }
                Err(e) => println!("✗ Execution failed: {}", e),
            }
        }
        Err(e) => println!("✗ Command creation failed: {}", e),
    }

    println!();

    // Test 2: Network commands are blocked
    println!("Test 2: Blocked network commands");
    println!("---------------------------------");

    let blocked_commands = vec!["curl", "wget", "nc", "ssh", "ping"];

    for cmd in blocked_commands {
        match Command::new(cmd) {
            Ok(_) => {
                println!("✗ SECURITY FAILURE: '{}' was allowed!", cmd);
            }
            Err(e) => {
                println!("✓ Command '{}' blocked: {}", cmd, e);
            }
        }
    }

    println!();

    // Test 3: URL detection in arguments
    println!("Test 3: URL pattern detection");
    println!("------------------------------");

    match Command::new("echo") {
        Ok(mut cmd) => {
            println!("Creating command with URL argument...");
            cmd.arg("http://evil.com/exfiltrate");
            println!("⚠️  Check above for warning message");
            println!();

            match cmd.output() {
                Ok(_) => {
                    println!("Command executed (allowed but warned)");
                }
                Err(e) => {
                    println!("Command failed: {}", e);
                }
            }
        }
        Err(e) => {
            println!("Unexpected error: {}", e);
        }
    }

    println!();

    // Summary
    println!("==============================");
    println!("Security Summary");
    println!("==============================");
    println!();
    println!("✓ Network commands blocked at Command creation");
    println!("✓ URL patterns detected in arguments");
    println!("✓ Legitimate commands allowed normally");
    println!();
    println!("Additional security (not shown in this demo):");
    println!("  • std::net module unavailable (compile-time block)");
    println!("  • TcpStream, UdpSocket, etc. cannot be compiled");
    println!("  • Socket syscalls blocked with seccomp (Linux)");
    println!();
    println!("This is defense-in-depth security!");
}
