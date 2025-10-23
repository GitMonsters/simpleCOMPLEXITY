// File Processing Example - Worm Rust
//
// Demonstrates that file I/O works normally in Worm Rust

use worm_std::prelude::*;
use worm_std::fs;
use worm_std::io::Write;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    worm_std::print_banner();

    println!("File Processing Example");
    println!("=======================");
    println!();

    // Create a sample input file
    println!("Creating input.txt...");
    let input_data = "Hello, Worm Rust!\nThis is a test file.\nNetwork access is blocked.";
    fs::write("input.txt", input_data)?;
    println!("✓ Created input.txt");

    // Read the file
    println!();
    println!("Reading input.txt...");
    let contents = fs::read_to_string("input.txt")?;
    println!("✓ Read {} bytes", contents.len());
    println!();
    println!("Contents:");
    println!("{}", contents);

    // Process the file
    println!();
    println!("Processing...");
    let processed = contents
        .lines()
        .enumerate()
        .map(|(i, line)| format!("{}. {}", i + 1, line.to_uppercase()))
        .collect::<Vec<_>>()
        .join("\n");

    // Write output
    println!("Writing output.txt...");
    fs::write("output.txt", &processed)?;
    println!("✓ Created output.txt");

    // Show output
    println!();
    println!("Output:");
    println!("{}", processed);

    // Append to file
    println!();
    println!("Appending to output.txt...");
    let mut file = fs::OpenOptions::new()
        .append(true)
        .open("output.txt")?;
    writeln!(file, "\n--- END OF FILE ---")?;
    println!("✓ Appended");

    // Clean up
    println!();
    println!("Cleaning up...");
    fs::remove_file("input.txt")?;
    fs::remove_file("output.txt")?;
    println!("✓ Cleaned up temporary files");

    println!();
    println!("Success! All file operations work in Worm Rust.");
    println!();
    println!("Security note:");
    println!("  ✓ All operations were local");
    println!("  ✓ No network access possible");
    println!("  ✓ Files cannot be exfiltrated");

    Ok(())
}
