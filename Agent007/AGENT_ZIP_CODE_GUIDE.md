# How to Provide a Zip Code to the Azure Foundry Agent

Your Azure Foundry agent script now supports **3 different ways** to provide a zip code through the terminal!

---

## 🎯 Method 1: Command Line Arguments (Easiest)

Pass the zip code directly as an argument:

```bash
python az_fndry_agent.py 90210
```

**Example:**
```bash
python az_fndry_agent.py 10001
```

**Output:**
```
✓ Zip code from command line: 10001
📝 Sending to agent: Tell me the weather for zip code 10001. What can you help with?
Response output: ...
```

**Advantages:**
- ✅ Simplest to use
- ✅ Easy to script
- ✅ Perfect for one-off queries

---

## 🎯 Method 2: Environment Variables

Set an environment variable before running:

```bash
export ZIP_CODE=90210
python az_fndry_agent.py
```

**Example:**
```bash
export ZIP_CODE=94105
python az_fndry_agent.py
```

**Output:**
```
✓ Zip code from environment variable: 94105
📝 Sending to agent: Tell me the weather for zip code 94105. What can you help with?
Response output: ...
```

**Advantages:**
- ✅ Good for repeated runs
- ✅ Works with shell scripts
- ✅ Useful for CI/CD pipelines

**Clear the variable:**
```bash
unset ZIP_CODE
```

---

## 🎯 Method 3: Interactive Terminal Prompt

Run the script without arguments and it will ask:

```bash
python az_fndry_agent.py
```

**Example:**
```
================================================================================
🌍 Enter Zip Code
================================================================================
Enter a zip code (or press Enter to skip): 10001

✓ Zip code from user input: 10001
📝 Sending to agent: Tell me the weather for zip code 10001. What can you help with?
Response output: ...
```

**Advantages:**
- ✅ Interactive and user-friendly
- ✅ Good for testing
- ✅ Optional (can skip by pressing Enter)

---

## 📊 Comparison Table

| Method | Command | Best For | Speed |
|--------|---------|----------|-------|
| **Command Line** | `python az_fndry_agent.py 10001` | Quick queries | ⚡⚡⚡ |
| **Environment** | `export ZIP_CODE=10001 && python az_fndry_agent.py` | Repeated runs | ⚡⚡ |
| **Interactive** | `python az_fndry_agent.py` (then enter zip) | Testing | ⚡ |

---

## 🔄 Advanced Examples

### **Run multiple queries with different zip codes:**
```bash
python az_fndry_agent.py 10001
python az_fndry_agent.py 90210
python az_fndry_agent.py 60601
```

### **Use in a shell script:**
```bash
#!/bin/bash
for zip in 10001 90210 60601 75201; do
  echo "Querying zip code: $zip"
  python az_fndry_agent.py $zip
  echo "---"
done
```

### **Use with environment variables in a shell script:**
```bash
#!/bin/bash
export ZIP_CODE=10001
python az_fndry_agent.py

export ZIP_CODE=90210
python az_fndry_agent.py

export ZIP_CODE=60601
python az_fndry_agent.py
```

### **Get zip code from user and pass to agent:**
```bash
read -p "Enter a zip code: " zip_code
python az_fndry_agent.py $zip_code
```

### **Pipe output to file:**
```bash
python az_fndry_agent.py 10001 > response_10001.txt
python az_fndry_agent.py 90210 > response_90210.txt
```

---

## 💡 Tips & Tricks

### **Tip 1: View what's being sent**
The script prints the message before sending:
```
📝 Sending to agent: Tell me the weather for zip code 10001. What can you help with?
```

### **Tip 2: Skip the zip code**
Press Enter at the prompt:
```
Enter a zip code (or press Enter to skip): [press Enter]
```

### **Tip 3: Combine methods (Priority Order)**
The script tries in this order:
1. Command line argument (highest priority)
2. Environment variable (medium priority)
3. Interactive prompt (lowest priority)

Example (uses command line argument):
```bash
export ZIP_CODE=90210
python az_fndry_agent.py 10001  # Uses 10001, ignores environment variable
```

### **Tip 4: Use in production with defaults**
```bash
# Set default, then allow override
export ZIP_CODE=${1:-10001}
python az_fndry_agent.py
```

---

## 🔍 How It Works Internally

**The script does this:**

1. **Checks command line arguments**
   ```bash
   if len(sys.argv) > 1:
       zip_code = sys.argv[1]
   ```

2. **If not found, checks environment variable**
   ```bash
   zip_code = os.getenv("ZIP_CODE")
   ```

3. **If still not found, asks user**
   ```bash
   zip_code = input("Enter a zip code: ")
   ```

4. **Builds the message**
   ```bash
   user_message = f"Tell me the weather for zip code {zip_code}. What can you help with?"
   ```

5. **Sends to agent**
   ```bash
   response = openai_client.responses.create(
       input=[{"role": "user", "content": user_message}],
       extra_body={...}
   )
   ```

---

## ✅ Examples You Can Try Right Now

### **Example 1: New York (10001)**
```bash
python az_fndry_agent.py 10001
```

### **Example 2: Los Angeles (90210)**
```bash
python az_fndry_agent.py 90210
```

### **Example 3: San Francisco (94105)**
```bash
python az_fndry_agent.py 94105
```

### **Example 4: Chicago (60601)**
```bash
python az_fndry_agent.py 60601
```

### **Example 5: No zip code (skip)**
```bash
python az_fndry_agent.py
# Then press Enter at the prompt
```

---

## 🐛 Troubleshooting

### **Problem: "No zip code provided"**
```
No zip code provided, using default query
```

**Solution:** Provide a zip code using one of the three methods above.

### **Problem: "Invalid zip code"**
The script accepts any input. If the agent doesn't recognize it, you'll see:
```
Response output: I don't recognize that zip code...
```

**Solution:** Use a valid US zip code like 10001, 90210, 60601, etc.

### **Problem: Need to change the zip code in environment**
```bash
# Current
export ZIP_CODE=10001

# Change it
export ZIP_CODE=90210

# Or unset it
unset ZIP_CODE
```

---

## 📞 Need More Help?

### **View the code:**
```bash
cat az_fndry_agent.py | grep -A 30 "GET ZIP CODE"
```

### **See what methods are available:**
```bash
python az_fndry_agent.py --help  # (if you add help)
```

### **Test each method:**
```bash
# Method 1: Command line
python az_fndry_agent.py 10001

# Method 2: Environment
export ZIP_CODE=90210 && python az_fndry_agent.py

# Method 3: Interactive
python az_fndry_agent.py
# Enter: 60601
```

---

## 🎯 Summary

You now have **3 ways** to provide a zip code:

| # | Method | Command | Example |
|---|--------|---------|---------|
| 1 | **Command Line** | `python az_fndry_agent.py <zip>` | `python az_fndry_agent.py 10001` |
| 2 | **Environment** | `export ZIP_CODE=<zip> && python az_fndry_agent.py` | `export ZIP_CODE=90210 && python az_fndry_agent.py` |
| 3 | **Interactive** | `python az_fndry_agent.py` (then type zip) | Run script and enter at prompt |

**Pick the method that works best for your use case!**

---

**Last Updated:** May 14, 2026  
**Status:** ✅ READY TO USE
