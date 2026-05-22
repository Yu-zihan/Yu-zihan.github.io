# Project Runbook

Canonical site root:
- `/Users/yzh/Desktop/Code/Blog/Blog`

Use this config only:
- `/Users/yzh/Desktop/Code/Blog/Blog/Kodama.toml`

Content lives in:
- `/Users/yzh/Desktop/Code/Blog/Blog/trees`

Run preview (from Kodama source checkout):
```bash
cd /Users/yzh/Desktop/Code/Blog/Blog/kodama
cargo run -- serve -c ../Kodama.toml -v
```

Build static output:
```bash
cd /Users/yzh/Desktop/Code/Blog/Blog/kodama
cargo run -- build -c ../Kodama.toml -v
```

Notes:
- Ignore temporary preview workspace `/tmp/kodama-academic-preview`.
- Current homepage/about/blog style is driven by academic mode in `Kodama.toml`.
- Math rendering is enabled via `/Users/yzh/Desktop/Code/Blog/Blog/import-math.html`.
