# simpleCOMPLEXITY

**Torus Topology and Vortex Dynamics for AI Attention Mechanisms**

A research framework exploring the intersection of torus topology, vortex dynamics, and attention mechanisms in neural networks.

## Overview

simpleCOMPLEXITY investigates how complex mathematical structures (torus topology, vortex flows) can create emergent simple behaviors in AI systems - hence the name.

## Core Concepts

### Torus Topology in Attention

```
    Torus Surface: S¹ × S¹
    
         ╭─────────────────────╮
        ╱                       ╲
       │    ↻ Major Circle      │
       │    (sequence flow)     │
       │                        │
       │  ↺ Minor Circle        │
       │  (head interaction)    │
        ╲                       ╱
         ╰─────────────────────╯
```

The torus provides a natural topology for:
- **Bidirectional attention** along major axis
- **Cross-head communication** along minor axis
- **Cyclic boundary conditions** (no edge effects)

### Vortex Dynamics

```
    Vortex Field: ω = ∇ × v
    
    Information flows like fluid vortices:
    - Clockwise spirals (compression)
    - Counter-clockwise spirals (expansion)
    - Vortex shedding (attention dropout)
```

## Mathematical Foundation

### Torus Coordinates

```
Position: (θ, φ) ∈ [0, 2π) × [0, 2π)
Embedding: x = (R + r·cos(φ))·cos(θ)
           y = (R + r·cos(φ))·sin(θ)  
           z = r·sin(φ)
```

### Vorticity Attention

```
Attention(Q, K, V) = softmax(QKᵀ/√d + Ω)V

Where Ω is the vorticity bias matrix derived from torus geometry
```

## Relation to Other Repos

| Repo | Connection |
|------|------------|
| **[torus-attention](https://github.com/GitMonsters/torus-attention)** | Full Rust implementation of these concepts |
| **[torus-collider](https://github.com/GitMonsters/torus-collider)** | Anomaly detection using torus topology |
| **[TRANSCENDPLEXITY](https://github.com/GitMonsters/TRANSCENDPLEXITY)** | Advanced ML architecture |

## Key Ideas

1. **Simplicity from Complexity** - Complex topological structures enable simple emergent behaviors
2. **Natural Periodicity** - Torus handles cyclic patterns without boundary artifacts
3. **Vortex Attention** - Fluid dynamics metaphor for information flow
4. **8-Stream Architecture** - 8 distinct flows on the torus surface

## Applications

- Long-range sequence modeling
- Bidirectional context understanding
- Circular/periodic data (time series, rotations)
- Multi-scale attention patterns

## Part of GitMonsters AGI Ecosystem

This repository contains theoretical foundations implemented in:
- **Rust**: [torus-attention](https://github.com/GitMonsters/torus-attention)
- **Python**: [octotetrahedral-agi](https://github.com/GitMonsters/octotetrahedral-agi)

## License

MIT License
