// Hello Worm - Basic Worm Rust Example
//
// This demonstrates that normal Rust code works fine in Worm Rust

use worm_std::prelude::*;

fn main() {
    // Print banner to show we're running under Worm Rust
    worm_std::print_banner();

    println!("Hello from Worm Rust!");
    println!();

    // All normal operations work
    println!("✓ Printing works");
    println!("✓ String operations work: {}", "test".to_uppercase());
    println!("✓ Math works: 2 + 2 = {}", 2 + 2);
    println!("✓ Collections work");

    let mut vec = Vec::new();
    vec.push(1);
    vec.push(2);
    vec.push(3);
    println!("  Vec: {:?}", vec);

    let mut map = std::collections::HashMap::new();
    map.insert("key", "value");
    println!("  HashMap: {:?}", map);

    println!();
    println!("What DOESN'T work:");
    println!("  ✗ Network access (compile-time error)");
    println!("  ✗ Network commands like curl, wget (runtime error)");
    println!();
    println!("This is a security feature!");
}
