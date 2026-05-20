# ZIP CODE INPUT - QUICK REFERENCE CARD

## Three Ways to Provide a Zip Code

### ⭐ METHOD 1: Command Line (Fastest)
```bash
python az_fndry_agent.py <ZIP_CODE>
```

**Examples:**
```bash
python az_fndry_agent.py 10001    # New York
python az_fndry_agent.py 90210    # Los Angeles
python az_fndry_agent.py 60601    # Chicago
python az_fndry_agent.py 94105    # San Francisco
python az_fndry_agent.py 75201    # Dallas
```

---

### METHOD 2: Environment Variable
```bash
export ZIP_CODE=<ZIP_CODE>
python az_fndry_agent.py
```

**Examples:**
```bash
export ZIP_CODE=10001 && python az_fndry_agent.py
export ZIP_CODE=90210 && python az_fndry_agent.py
export ZIP_CODE=60601 && python az_fndry_agent.py
```

---

### METHOD 3: Interactive Prompt
```bash
python az_fndry_agent.py
# Then type zip code when prompted
```

**Example:**
```
$ python az_fndry_agent.py
Enter a zip code (or press Enter to skip): 10001
```

---

## Cheat Sheet

| What You Want | Command |
|---------------|---------|
| Quick NYC weather | `python az_fndry_agent.py 10001` |
| Quick LA weather | `python az_fndry_agent.py 90210` |
| Quick Chicago weather | `python az_fndry_agent.py 60601` |
| Manual entry | `python az_fndry_agent.py` (then type) |
| Set for session | `export ZIP_CODE=10001` then `python az_fndry_agent.py` |
| Batch process | `python az_fndry_agent.py 10001 && python az_fndry_agent.py 90210` |
| Query multiple | `for z in 10001 90210 60601; do python az_fndry_agent.py $z; done` |

---

## Output Format

When you provide a zip code, the script shows:

```
✓ Zip code from command line: 10001
📝 Sending to agent: Tell me the weather for zip code 10001. What can you help with?
Response output: [Agent response here]
```

---

## Priority (if multiple sources provided)

1. Command line argument → Highest priority
2. Environment variable → Medium priority  
3. Interactive prompt → Lowest priority

**Example:** This uses 10001, ignoring the environment variable:
```bash
export ZIP_CODE=90210
python az_fndry_agent.py 10001  # Uses 10001
```

---

**Last Updated:** May 14, 2026
