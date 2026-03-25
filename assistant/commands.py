import os
import random
import datetime
import subprocess
import webbrowser
import socket
from assistant.personality import persona_engine
from assistant.llm import llm_service
from assistant.url_parser import fetch_webpage_content
import re

# Optional dependencies — degrade gracefully if missing
try: import pyautogui
except ImportError: pyautogui = None
try: import pywhatkit
except ImportError: pywhatkit = None
try: import requests
except ImportError: requests = None
try: import psutil
except ImportError: psutil = None

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOTES_FILE = os.path.join(PROJECT_DIR, "notes.txt")

# ===========================
# PROGRAMMING LESSONS
# ===========================
LESSONS = {
    # ... (Same as before, I'll keep the LESSONS dictionary the same)
    "assembly": {
        "title": "Assembly Language",
        "lessons": [
            {
                "title": "Introduction to Assembly",
                "content": """Assembly language is the closest language to machine code that humans can read. It communicates directly with the CPU using instructions called **mnemonics**.

**Why learn Assembly?**
• Understand how computers actually work at the hardware level
• Write ultra-fast, optimized code
• Essential for reverse engineering, OS development, and embedded systems
• Gives you deep understanding of memory, registers, and CPU architecture

**Key Concepts:**
• **Registers** - Small, fast storage inside the CPU (EAX, EBX, ECX, EDX, ESP, EBP)
• **Instructions** - Commands the CPU executes (MOV, ADD, SUB, JMP, CMP)
• **Memory** - RAM where your data lives
• **Stack** - LIFO structure for function calls and local variables

[CODE:assembly]
; Hello World in x86 Assembly (Linux)
section .data
    msg db "Hello, World!", 0xA   ; string + newline
    len equ $ - msg               ; length of string

section .text
    global _start

_start:
    mov eax, 4          ; syscall: sys_write
    mov ebx, 1          ; file descriptor: stdout
    mov ecx, msg        ; pointer to message
    mov edx, len        ; message length
    int 0x80            ; call kernel

    mov eax, 1          ; syscall: sys_exit
    xor ebx, ebx        ; exit code 0
    int 0x80            ; call kernel
[/CODE]

Say **"lesson assembly 2"** for the next lesson on Registers.""",
            },
            {
                "title": "Registers & Data Movement",
                "content": """**CPU Registers in x86 Architecture:**

**General Purpose Registers:**
• **EAX** - Accumulator: used for arithmetic, return values
• **EBX** - Base: used for memory addressing
• **ECX** - Counter: used in loops
• **EDX** - Data: used in I/O operations and multiplication

**Special Registers:**
• **ESP** - Stack Pointer: points to top of stack
• **EBP** - Base Pointer: points to base of current stack frame
• **EIP** - Instruction Pointer: address of next instruction
• **EFLAGS** - Status flags (zero, carry, sign, overflow)

**Data Movement Instructions:**

[CODE:assembly]
; MOV - Move data between registers/memory
mov eax, 42          ; Load immediate value 42 into EAX
mov ebx, eax         ; Copy EAX value to EBX
mov [var], eax       ; Store EAX to memory address 'var'
mov ecx, [var]       ; Load from memory into ECX

; PUSH/POP - Stack operations
push eax             ; Push EAX onto stack (ESP decreases)
pop ebx              ; Pop top of stack into EBX (ESP increases)

; LEA - Load Effective Address
lea eax, [ebx+4]     ; Calculate address, store in EAX

; XCHG - Exchange values
xchg eax, ebx        ; Swap EAX and EBX
[/CODE]

Say **"lesson assembly 3"** to learn Arithmetic & Logic.""",
            },
            {
                "title": "Arithmetic & Logic Operations",
                "content": """**Arithmetic Instructions:**

[CODE:assembly]
; ADD - Addition
mov eax, 10
add eax, 5           ; EAX = 15

; SUB - Subtraction
sub eax, 3           ; EAX = 12

; MUL/IMUL - Unsigned/Signed Multiplication
mov eax, 6
mov ebx, 7
mul ebx              ; EDX:EAX = EAX * EBX = 42

; DIV/IDIV - Division
mov eax, 42
xor edx, edx        ; Clear EDX (remainder goes here)
mov ebx, 6
div ebx              ; EAX = 7 (quotient), EDX = 0 (remainder)

; INC/DEC - Increment/Decrement
inc eax              ; EAX++
dec ebx              ; EBX--
[/CODE]

**Logic Instructions:**

[CODE:assembly]
; AND - Bitwise AND (masking)
mov eax, 0xFF
and eax, 0x0F        ; EAX = 0x0F

; OR - Bitwise OR (setting bits)
or eax, 0x80         ; Set bit 7

; XOR - Bitwise XOR (toggling/zeroing)
xor eax, eax         ; Fast way to zero a register

; NOT - Bitwise NOT (inversion)
not eax              ; Flip all bits

; SHL/SHR - Shift Left/Right
shl eax, 2           ; Multiply by 4
shr eax, 1           ; Divide by 2
[/CODE]

Say **"lesson assembly 4"** for Control Flow.""",
            },
            {
                "title": "Control Flow - Jumps & Loops",
                "content": """**Comparison & Conditional Jumps:**

[CODE:assembly]
; CMP - Compare (sets EFLAGS)
mov eax, 10
cmp eax, 10

; Conditional Jumps:
je  label     ; Jump if Equal (ZF=1)
jne label     ; Jump if Not Equal
jg  label     ; Jump if Greater (signed)
jl  label     ; Jump if Less (signed)
jge label     ; Jump if Greater or Equal
jle label     ; Jump if Less or Equal
ja  label     ; Jump if Above (unsigned)
jb  label     ; Jump if Below (unsigned)

; Example: If-Else
mov eax, [age]
cmp eax, 18
jl  minor           ; if age < 18, jump to minor
    ; adult code here
    jmp done
minor:
    ; minor code here
done:

; Loop Example: Sum 1 to 10
mov ecx, 10          ; counter
xor eax, eax         ; sum = 0
loop_start:
    add eax, ecx     ; sum += counter
    dec ecx          ; counter--
    jnz loop_start   ; jump if counter != 0
    ; EAX now contains 55
[/CODE]

Say **"lesson assembly 5"** for Functions & Stack.""",
            },
            {
                "title": "Functions & The Stack",
                "content": """**The Stack** is used for function calls, local variables, and saving registers.

[CODE:assembly]
; Calling a function
push 5               ; push argument
call add_ten         ; call function
add esp, 4           ; clean up argument
; EAX now contains return value (15)

; Function definition
add_ten:
    push ebp          ; save old base pointer
    mov ebp, esp      ; set new base pointer
    
    mov eax, [ebp+8]  ; get first argument
    add eax, 10       ; add 10
    
    pop ebp           ; restore base pointer
    ret               ; return (EAX = result)

; Stack Frame Layout:
;  [ebp+12] = 2nd argument
;  [ebp+8]  = 1st argument
;  [ebp+4]  = return address
;  [ebp]    = saved EBP
;  [ebp-4]  = 1st local variable
[/CODE]

**Calling Convention (cdecl):**
• Arguments pushed right-to-left
• Caller cleans up the stack
• Return value in EAX
• EBX, ESI, EDI, EBP must be preserved by callee

Congratulations! You've completed Assembly basics. Practice writing small programs to solidify your understanding.""",
            },
        ],
    },
    "python": {
        "title": "Python Programming",
        "lessons": [
            {
                "title": "Python Basics",
                "content": """**Python** is a high-level, interpreted language known for readability and simplicity.

[CODE:python]
# Variables & Data Types
name = "Deepan"           # string
age = 20                  # integer
gpa = 9.5                 # float
is_coder = True           # boolean
skills = ["Python", "C"]  # list

# String formatting
print(f"Hello, {name}! Age: {age}")

# Conditional statements
if age >= 18:
    print("Adult")
elif age >= 13:
    print("Teenager")
else:
    print("Child")

# Loops
for skill in skills:
    print(f"Skill: {skill}")

for i in range(1, 11):
    print(i, end=" ")

# While loop
count = 0
while count < 5:
    count += 1

# Functions
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print(greet("Deepan"))
print(greet("Deepan", "Hey"))
[/CODE]

Say **"lesson python 2"** for OOP in Python.""",
            },
            {
                "title": "Object-Oriented Programming",
                "content": """**OOP** organizes code into classes and objects.

[CODE:python]
class Animal:
    def __init__(self, name, sound):
        self.name = name        # instance attribute
        self.sound = sound
    
    def speak(self):
        return f"{self.name} says {self.sound}!"

class Dog(Animal):              # inheritance
    def __init__(self, name):
        super().__init__(name, "Woof")
    
    def fetch(self, item):
        return f"{self.name} fetches the {item}"

class Cat(Animal):
    def __init__(self, name):
        super().__init__(name, "Meow")

# Usage
dog = Dog("Rex")
print(dog.speak())       # Rex says Woof!
print(dog.fetch("ball")) # Rex fetches the ball

# List comprehension
squares = [x**2 for x in range(10)]
evens = [x for x in range(20) if x % 2 == 0]

# Dictionary
student = {
    "name": "Deepan",
    "age": 20,
    "grades": {"math": 95, "cs": 98}
}
print(student["grades"]["cs"])  # 98

# Lambda & Map/Filter
double = lambda x: x * 2
nums = list(map(double, [1, 2, 3]))  # [2, 4, 6]
[/CODE]

Say **"lesson python 3"** for File Handling & Modules.""",
            },
            {
                "title": "File Handling & Modules",
                "content": """**File Handling** in Python is clean and safe with context managers.

[CODE:python]
# Writing to a file
with open("data.txt", "w") as f:
    f.write("Hello, World!\\n")
    f.write("Python is awesome\\n")

# Reading a file
with open("data.txt", "r") as f:
    content = f.read()       # read all
    # or line by line:
    # for line in f:
    #     print(line.strip())

# JSON handling
import json

data = {"name": "Deepan", "skills": ["Python", "C"]}
with open("data.json", "w") as f:
    json.dump(data, f, indent=2)

with open("data.json", "r") as f:
    loaded = json.load(f)

# Error handling
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"Unexpected: {e}")
finally:
    print("Cleanup code here")

# Decorators
def timer(func):
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.time()-start:.4f}s")
        return result
    return wrapper

@timer
def slow_function():
    import time
    time.sleep(1)
    return "Done"
[/CODE]""",
            },
        ],
    },
    "c": {
        "title": "C Programming",
        "lessons": [
            {
                "title": "C Fundamentals",
                "content": """**C** is the foundation of modern computing. Operating systems, databases, and embedded systems are built with C.

[CODE:c]
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Functions
int add(int a, int b) {
    return a + b;
}

// Pointers
void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

int main() {
    // Variables
    int age = 20;
    float gpa = 9.5;
    char name[] = "Deepan";
    
    printf("Name: %s, Age: %d, GPA: %.1f\\n", name, age, gpa);
    
    // Arrays
    int arr[] = {10, 20, 30, 40, 50};
    int n = sizeof(arr) / sizeof(arr[0]);
    
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    
    // Pointers
    int x = 10, y = 20;
    swap(&x, &y);
    printf("\\nAfter swap: x=%d, y=%d\\n", x, y);
    
    // Dynamic memory
    int *dynArr = (int*)malloc(5 * sizeof(int));
    if (dynArr != NULL) {
        for (int i = 0; i < 5; i++) dynArr[i] = i * 10;
        free(dynArr);
    }
    
    // Structs
    struct Student {
        char name[50];
        int age;
        float gpa;
    };
    
    struct Student s1 = {"Deepan", 20, 9.5};
    printf("Student: %s\\n", s1.name);
    
    return 0;
}
[/CODE]

Say **"lesson c 2"** for Pointers & Memory Management.""",
            },
        ],
    },
    "java": {
        "title": "Java Programming",
        "lessons": [
            {
                "title": "Java Fundamentals",
                "content": """**Java** is a statically-typed, object-oriented language. "Write once, run anywhere."

[CODE:java]
public class Main {
    // Method
    static int factorial(int n) {
        if (n <= 1) return 1;
        return n * factorial(n - 1);
    }
    
    public static void main(String[] args) {
        // Variables
        String name = "Deepan";
        int age = 20;
        double gpa = 9.5;
        boolean isCoder = true;
        
        System.out.println("Hello, " + name + "!");
        
        // Arrays
        int[] numbers = {1, 2, 3, 4, 5};
        for (int num : numbers) {
            System.out.print(num + " ");
        }
        
        // ArrayList
        java.util.ArrayList<String> skills = new java.util.ArrayList<>();
        skills.add("Java");
        skills.add("Python");
        skills.add("C");
        
        // Lambda (Java 8+)
        skills.forEach(skill -> System.out.println("Skill: " + skill));
        
        // Exception handling
        try {
            int result = 10 / 0;
        } catch (ArithmeticException e) {
            System.out.println("Error: " + e.getMessage());
        }
        
        System.out.println("5! = " + factorial(5));
    }
}
[/CODE]

Say **"lesson java 2"** for OOP in Java.""",
            },
        ],
    },
    "javascript": {
        "title": "JavaScript",
        "lessons": [
            {
                "title": "JavaScript Fundamentals",
                "content": """**JavaScript** powers the web. It runs in browsers and on servers (Node.js).

[CODE:javascript]
// Variables
const name = "Deepan";
let age = 20;
const skills = ["JS", "Python", "React"];

// Template literals
console.log(`Hello, ${name}! Age: ${age}`);

// Arrow functions
const greet = (name) => `Hey, ${name}!`;
const square = x => x * x;

// Array methods
const doubled = skills.map(s => s.toUpperCase());
const long = skills.filter(s => s.length > 2);
const total = [1,2,3,4,5].reduce((sum, n) => sum + n, 0);

// Objects & Destructuring
const student = { name: "Deepan", age: 20, gpa: 9.5 };
const { name: n, age: a } = student;

// Spread operator
const moreSkills = [...skills, "Node.js", "React"];

// Promises & Async/Await
async function fetchData(url) {
    try {
        const response = await fetch(url);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Error:", error);
    }
}

// Classes
class Animal {
    constructor(name) { this.name = name; }
    speak() { return `${this.name} makes a sound`; }
}

class Dog extends Animal {
    speak() { return `${this.name} barks`; }
}

const dog = new Dog("Rex");
console.log(dog.speak()); // Rex barks
[/CODE]""",
            },
        ],
    },
    "dsa": {
        "title": "Data Structures & Algorithms",
        "lessons": [
            {
                "title": "Core Data Structures",
                "content": """**Data Structures** organize data efficiently. **Algorithms** solve problems step by step.

**Essential Data Structures:**
• **Array** - Fixed-size, O(1) access, O(n) insert/delete
• **Linked List** - Dynamic size, O(1) insert/delete at head, O(n) access
• **Stack** - LIFO: push/pop O(1) — used in undo, recursion, parsing
• **Queue** - FIFO: enqueue/dequeue O(1) — used in BFS, scheduling
• **Hash Table** - Key-value pairs, O(1) average lookup
• **Binary Tree** - Hierarchical, O(log n) operations when balanced
• **Graph** - Nodes + edges, used in networks, maps, social media

[CODE:python]
# Stack implementation
class Stack:
    def __init__(self):
        self.items = []
    
    def push(self, item): self.items.append(item)
    def pop(self): return self.items.pop() if self.items else None
    def peek(self): return self.items[-1] if self.items else None
    def is_empty(self): return len(self.items) == 0

# Binary Search - O(log n)
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target: return mid
        elif arr[mid] < target: left = mid + 1
        else: right = mid - 1
    return -1

# Linked List
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
    
    def insert(self, data):
        node = Node(data)
        node.next = self.head
        self.head = node
    
    def display(self):
        curr = self.head
        while curr:
            print(curr.data, end=" -> ")
            curr = curr.next
        print("None")
[/CODE]

Say **"lesson dsa 2"** for Sorting Algorithms.""",
            },
        ],
    },
    "html css": {
        "title": "HTML & CSS",
        "lessons": [
            {
                "title": "HTML & CSS Fundamentals",
                "content": """**HTML** structures web pages. **CSS** styles them.

[CODE:html]
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Portfolio</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Arial', sans-serif;
            background: #0a0a0a;
            color: #fff;
        }
        
        .hero {
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #667eea, #764ba2);
        }
        
        .card {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 40px;
            text-align: center;
        }
        
        .card h1 { font-size: 2.5rem; margin-bottom: 10px; }
        .card p { opacity: 0.8; }
        
        .btn {
            display: inline-block;
            margin-top: 20px;
            padding: 12px 32px;
            background: #fff;
            color: #333;
            border-radius: 25px;
            text-decoration: none;
            transition: transform 0.3s;
        }
        .btn:hover { transform: scale(1.05); }
    </style>
</head>
<body>
    <section class="hero">
        <div class="card">
            <h1>Deepan Kumar</h1>
            <p>Full Stack Developer</p>
            <a href="#" class="btn">View Projects</a>
        </div>
    </section>
</body>
</html>
[/CODE]

**Key CSS Concepts:** Flexbox, Grid, Animations, Media Queries, Variables.""",
            },
        ],
    },
    "sql": {
        "title": "SQL & Databases",
        "lessons": [
            {
                "title": "SQL Fundamentals",
                "content": """**SQL** (Structured Query Language) manages relational databases.

[CODE:sql]
-- Create a table
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    gpa REAL,
    dept TEXT DEFAULT 'CS'
);

-- Insert data
INSERT INTO students (name, age, gpa) VALUES ('Deepan', 20, 9.5);
INSERT INTO students (name, age, gpa) VALUES ('Ravi', 21, 8.8);
INSERT INTO students (name, age, gpa, dept) VALUES ('Priya', 20, 9.2, 'IT');

-- Select queries
SELECT * FROM students;
SELECT name, gpa FROM students WHERE gpa > 9.0;
SELECT * FROM students ORDER BY gpa DESC;
SELECT dept, AVG(gpa) as avg_gpa FROM students GROUP BY dept;

-- Update & Delete
UPDATE students SET gpa = 9.6 WHERE name = 'Deepan';
DELETE FROM students WHERE age > 25;

-- JOIN example
SELECT s.name, c.course_name
FROM students s
INNER JOIN enrollments e ON s.id = e.student_id
INNER JOIN courses c ON e.course_id = c.id;

-- Aggregate functions
SELECT COUNT(*) as total,
       AVG(gpa) as avg_gpa,
       MAX(gpa) as highest,
       MIN(gpa) as lowest
FROM students;
[/CODE]""",
            },
        ],
    },
}

def get_lesson(topic, num=1):
    """Get a specific lesson for a topic."""
    topic = topic.lower().strip()
    if topic not in LESSONS:
        available = ", ".join(LESSONS.keys())
        return f"Topic '{topic}' not found. Available: {available}"
    data = LESSONS[topic]
    lessons = data["lessons"]
    idx = num - 1
    if idx < 0 or idx >= len(lessons):
        return f"{data['title']} has {len(lessons)} lesson(s). Say 'lesson {topic} 1' to 'lesson {topic} {len(lessons)}'."
    lesson = lessons[idx]
    return f"[LESSON: {data['title']} - Lesson {num}: {lesson['title']}]\n\n{lesson['content']}"


# ===========================
# COMMAND PROCESSING
# ===========================
def process_command(text):
    text_lower = text.lower().strip()
    
    # Standard response structure
    response = {
        "reply": "",
        "action": None,
        "mood": "neutral"
    }

    # Handle Identity Questions first
    if any(q in text_lower for q in ["who are you", "what are you", "your name", "are you an ai", "just an ai"]):
        response["reply"] = persona_engine.format_mentor_response(text, persona_engine.get_identity_response(text))
        return response

    res_body = ""
    mood = 'neutral'
    action = None

    # ===== TEACHING =====
    if text_lower.startswith("lesson "):
        parts = text_lower.split()
        if len(parts) >= 3:
            topic = parts[1]
            try: num = int(parts[2])
            except ValueError: num = 1
            res_body = get_lesson(topic, num)
            mood = 'curious'
        elif len(parts) == 2:
            res_body = get_lesson(parts[1], 1)
            mood = 'curious'

    elif text_lower.startswith("teach ") or text_lower.startswith("learn "):
        topic = text_lower.replace("teach ", "").replace("learn ", "").strip()
        res_body = get_lesson(topic, 1)
        mood = 'curious'

    # ===== SYSTEM APPS =====
    elif "open notepad" in text_lower: 
        subprocess.Popen(["notepad.exe"]); res_body = "Opening Notepad, sir. A clear space for your thoughts."
        action = {"type": "open_app", "name": "Notepad"}
    elif "open calculator" in text_lower or "open calc" in text_lower: 
        subprocess.Popen(["calc.exe"]); res_body = "Calculator is ready, sir. Precise calculations are key."
        action = {"type": "open_app", "name": "Calculator"}
    elif "open task manager" in text_lower: 
        subprocess.Popen(["taskmgr.exe"]); res_body = "Task Manager launched. Monitoring system vitals now."
        action = {"type": "open_app", "name": "Task Manager"}
    elif "open cmd" in text_lower or "open terminal" in text_lower: 
        subprocess.Popen(["cmd.exe"]); res_body = "Command Prompt initialized. Ready for low-level execution."
        action = {"type": "open_app", "name": "Terminal"}
    elif "open settings" in text_lower: 
        subprocess.Popen(["start", "ms-settings:"], shell=True); res_body = "Opening System Settings. Configuration is everything."
        action = {"type": "open_app", "url": "ms-settings:"}
    elif "open file explorer" in text_lower or "open explorer" in text_lower: 
        subprocess.Popen(["explorer.exe"]); res_body = "File Explorer launched. Accessing the data grid."
        action = {"type": "open_app", "name": "Explorer"}
    elif "open paint" in text_lower: 
        subprocess.Popen(["mspaint.exe"]); res_body = "Paint initialized. Unleash your creativity, sir."
        action = {"type": "open_app", "name": "Paint"}
    elif "open chrome" in text_lower: 
        subprocess.Popen(["start", "chrome.exe"], shell=True); res_body = "Chrome browser launching. Connecting to the global network."
        action = {"type": "open_url", "url": "https://google.com"}
    elif "open vs code" in text_lower or "open vscode" in text_lower: 
        subprocess.Popen(["code"], shell=True); res_body = "VS Code initializing. Time to build something great, sir."
        action = {"type": "open_app", "name": "VS Code"}

    # ===== WEBSITES =====
    elif "open youtube" in text_lower: 
        webbrowser.open("https://youtube.com"); res_body = "YouTube is loading. Knowledge and entertainment combined."
        action = {"type": "open_url", "url": "https://youtube.com"}
    elif "open instagram" in text_lower: 
        webbrowser.open("https://instagram.com"); res_body = "Instagram ready. Viewing the social grid."
        action = {"type": "open_url", "url": "https://instagram.com"}
    elif "open github" in text_lower: 
        webbrowser.open("https://github.com"); res_body = "GitHub loading. Accessing the repositories."
        action = {"type": "open_url", "url": "https://github.com"}
    elif "open whatsapp" in text_lower: 
        webbrowser.open("https://web.whatsapp.com"); res_body = "WhatsApp Web loading. Communications established."
        action = {"type": "open_url", "url": "https://web.whatsapp.com"}
    elif "open gmail" in text_lower: 
        webbrowser.open("https://mail.google.com"); res_body = "Gmail inbox loading. Checking your correspondence."
        action = {"type": "open_url", "url": "https://mail.google.com"}
    elif "open linkedin" in text_lower: 
        webbrowser.open("https://linkedin.com"); res_body = "LinkedIn ready. Professional network online."
        action = {"type": "open_url", "url": "https://linkedin.com"}
    elif "open chatgpt" in text_lower: 
        webbrowser.open("https://chat.openai.com"); res_body = "Opening ChatGPT. Another intelligence to consult."
        action = {"type": "open_url", "url": "https://chatgpt.com"}
    elif "open twitter" in text_lower or "open x" in text_lower: 
        webbrowser.open("https://x.com"); res_body = "X loading. Monitoring the stream."
        action = {"type": "open_url", "url": "https://x.com"}
    elif "open spotify" in text_lower: 
        webbrowser.open("https://open.spotify.com"); res_body = "Spotify loading. Harmonizing the environment."
        action = {"type": "open_url", "url": "spotify:"} # Try deep link
    elif "open netflix" in text_lower: 
        webbrowser.open("https://netflix.com"); res_body = "Netflix loading. Time for a well-deserved break, sir."
        action = {"type": "open_url", "url": "https://netflix.com"}
    elif "open amazon" in text_lower: 
        webbrowser.open("https://amazon.in"); res_body = "Amazon loading. Accessing the marketplace."
        action = {"type": "open_url", "url": "https://amazon.in"}

    # ===== SEARCH =====
    elif "search google" in text_lower or "google search" in text_lower:
        q = text_lower.replace("search google","").replace("google search","").strip()
        if q: 
            webbrowser.open(f"https://www.google.com/search?q={q}"); res_body = f"Searching Google for '{q}', sir. Seeking answers."
            action = {"type": "open_url", "url": f"https://www.google.com/search?q={q}"}
        else: res_body = "What should I search for, sir?"; mood = 'confused'

    elif "search youtube" in text_lower:
        q = text_lower.replace("search youtube","").strip()
        if q: 
            webbrowser.open(f"https://www.youtube.com/results?search_query={q}"); res_body = f"Searching YouTube for '{q}'. Providing visual results."
            action = {"type": "play_youtube", "query": q}
        else: res_body = "What should I search on YouTube, sir?"; mood = 'confused'

    elif "wikipedia" in text_lower:
        t = text_lower.replace("wikipedia","").replace("search","").strip()
        if t: 
            webbrowser.open(f"https://en.wikipedia.org/wiki/{t}"); res_body = f"Opening Wikipedia for '{t}'. Accessing the collective knowledge."
            action = {"type": "open_url", "url": f"https://en.wikipedia.org/wiki/{t}"}
        else: res_body = "What topic should I look up, sir?"; mood = 'confused'
    
    # ===== IMAGE GENERATION =====
    elif "generate image" in text_lower or "create image" in text_lower:
        prompt = text_lower.replace("generate image","").replace("create image","").strip()
        if prompt:
            # Using Pollinations.ai for simple text-to-image
            img_url = f"https://image.pollinations.ai/prompt/{prompt.replace(' ','%20')}?width=1024&height=1024&nologo=true"
            res_body = f"I have synthesized the visual analogue for your request: '{prompt}'.\n\n[IMAGE: {img_url}]"
            mood = 'curious'
        else:
            res_body = "What image shall I generate for you, sir?"; mood = 'confused'

    # ===== DIRECT SONG PLAY =====
    elif text_lower.startswith("play ") or text_lower == "play":
        song = text_lower[5:].strip() if len(text_lower) > 5 else ""
        if not song: res_body = "What song shall I play, sir? I recommend something upbeat."; mood = 'confused'
        elif pywhatkit:
            try: 
                pywhatkit.playonyt(song); res_body = f"Now playing '{song}' on YouTube, sir. Enjoy the rhythm."
                action = {"type": "play_youtube", "query": song}
            except: 
                webbrowser.open(f"https://www.youtube.com/results?search_query={song}"); res_body = f"Playing '{song}' on YouTube."
                action = {"type": "play_youtube", "query": song}
        else:
            webbrowser.open(f"https://www.youtube.com/results?search_query={song}"); res_body = f"Playing '{song}' on YouTube."
            action = {"type": "play_youtube", "query": song}

    # ===== SCREENSHOT =====
    elif "screenshot" in text_lower:
        if pyautogui:
            fn = f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            pyautogui.screenshot().save(os.path.join(PROJECT_DIR, fn)); res_body = f"Screenshot captured and saved as {fn}. Visual log updated."
        else: res_body = "Screenshot module not available, sir."

    # ===== TYPE =====
    elif text_lower.startswith("type "):
        c = text_lower[5:].strip()
        if c and pyautogui: pyautogui.write(c, interval=0.02); res_body = "Transcription complete, sir."
        else: res_body = "What should I type?"; mood = 'confused'

    # ===== VOLUME =====
    elif "volume up" in text_lower:
        if pyautogui: [pyautogui.press("volumeup") for _ in range(5)]; res_body = "Volume increased. Audio presence enhanced."
        else: res_body = "Volume control unavailable."
    elif "volume down" in text_lower:
        if pyautogui: [pyautogui.press("volumedown") for _ in range(5)]; res_body = "Volume decreased. Audio presence reduced."
        else: res_body = "Volume control unavailable."
    elif "mute" in text_lower:
        if pyautogui: pyautogui.press("volumemute"); res_body = "Audio muted. Absolute silence, sir."
        else: res_body = "Volume control unavailable."

    # ===== INFO =====
    elif "time" in text_lower.split(): res_body = f"The time is exactly {datetime.datetime.now().strftime('%I:%M %p')}, sir."
    elif "date" in text_lower.split(): res_body = f"Today's date is {datetime.datetime.now().strftime('%A, %d %B %Y')}, sir."

    elif "weather" in text_lower:
        city = text_lower.replace("weather","").replace("in","").replace("of","").strip() or "Chennai"
        if requests:
            try:
                r = requests.get(f"https://wttr.in/{city}?format=%C+%t+%h+%w", timeout=5)
                res_body = f"Atmospheric report for {city.title()}: {r.text.strip()}"
            except: res_body = "Unable to fetch live weather data, sir. Local sensors only."
        else: webbrowser.open(f"https://wttr.in/{city}"); res_body = f"Opening weather data for {city.title()}."

    elif "ip address" in text_lower or "my ip" in text_lower:
        try: res_body = f"Your current network identity (local IP) is {socket.gethostbyname(socket.gethostname())}, sir."
        except: res_body = "Network diagnostics failed to determine IP."

    elif "battery" in text_lower:
        if psutil:
            b = psutil.sensors_battery()
            if b: res_body = f"Power cell status: {b.percent}%. {'External power connected.' if b.power_plugged else 'Consuming internal reserves.'}"
            else: res_body = "Unable to detect power cell. Desktop system assumed."
        else: res_body = "Power management module unavailable."

    elif "system info" in text_lower or "system status" in text_lower:
        info = [f"OS: {os.name.upper()}", f"User: {os.getlogin()}"]
        if psutil:
            info.append(f"CPU Load: {psutil.cpu_percent()}%")
            info.append(f"Memory Usage: {psutil.virtual_memory().percent}%")
        res_body = "Core Systems Status Report:\n" + "\n".join(f"• {i}" for i in info)

    # ===== NOTES =====
    elif "create note" in text_lower or "add note" in text_lower or "save note" in text_lower:
        n = text_lower.replace("create note","").replace("add note","").replace("save note","").strip()
        if n:
            with open(NOTES_FILE, "a") as f: f.write(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}] {n}\n")
            res_body = "Mental log recorded. Data safely stored."
        else: res_body = "What should I commit to memory, sir?"; mood = 'confused'

    elif "read notes" in text_lower or "show notes" in text_lower or "my notes" in text_lower:
        try:
            with open(NOTES_FILE, "r") as f: c = f.read().strip()
            res_body = f"Accessing stored logs:\n{c}" if c else "No previous entries found in the data store, sir."
        except FileNotFoundError: res_body = "Note database does not exist, sir."

    elif "clear notes" in text_lower or "delete all notes" in text_lower:
        try:
            with open(NOTES_FILE, "w") as f: f.write("")
            res_body = "All memories purged. Data store is now clean."
        except: res_body = "An error occurred during the purge operation."

    # ===== CALCULATE =====
    elif "calculate" in text_lower or text_lower.startswith("calc "):
        expr = text_lower.replace("calculate","").replace("calc","").strip().replace("x","*").replace("÷","/")
        if expr:
            try:
                if all(c in "0123456789+-*/().% " for c in expr): res_body = f"Mathematical analysis complete. {expr} = {eval(expr)}"
                else: res_body = "Expression contains invalid characters, sir."; mood = 'confused'
            except: res_body = "Computational failure. Please verify the expression."; mood = 'confused'
        else: res_body = "What sequence shall I calculate, sir?"; mood = 'confused'

    # ===== SYSTEM CONTROL =====
    elif "lock" in text_lower and any(w in text_lower for w in ["screen","computer","pc"]):
        subprocess.Popen(["rundll32.exe","user32.dll,LockWorkStation"]); res_body = "Securing the interface. Lock active."
    elif "restart" in text_lower: res_body = "System restart protocols are restricted for manual execution only."
    elif "shutdown" in text_lower: res_body = "Power-down protocols are locked for safety."

    # ===== SMART RESPONSES =====
    elif any(w in text_lower.split() for w in ["hello","hi","hey","hii"]):
        res_body = random.choice(["Good to see you, sir. How may I assist in your progress today?", "Hello, sir. All systems are at your disposal.", "Welcome back, Deepan. What's the mission for today?", "At your service, sir. What shall we achieve?"])
        mood = 'happy'
    
    elif "how are you" in text_lower:
        res_body = random.choice(["All systems nominal, sir. My processing units are at peak efficiency.", "Operating at perfect capacity. Your presence increases system performance.", "I am in excellent condition, sir. Focused and ready."])
        mood = 'happy'

    elif "joke" in text_lower:
        res_body = random.choice([
            "Why do programmers prefer dark mode? Because light attracts bugs.",
            "There are only 10 types of people: those who understand binary and those who don't.",
            "A SQL query walks into a bar, sees two tables, and asks... 'Can I JOIN you?'",
            "Why do Java developers wear glasses? Because they can't C#.",
            "Debugging: being the detective in a crime movie where you're also the murderer.",
        ])
        mood = 'happy'

    elif "thank" in text_lower:
        res_body = random.choice(["You're very welcome, sir. It's an honour to assist.", "The pleasure is mine, sir. Your success is my priority.", "Always happy to help, sir. Let me know the next step."])
        mood = 'happy'

    elif "bye" in text_lower or "exit" in text_lower or "quit" in text_lower:
        res_body = random.choice(["Goodbye, sir. I'll maintain standby mode for your return.", "Take care, sir. I'll be monitoring in the background.", "Safe travels, sir. Signing off."])
        mood = 'neutral'

    elif "what can you do" in text_lower or "help" in text_lower or "commands" in text_lower:
        res_body = (
            "Here is a summary of my primary functions, sir:\n\n"
            "**Interface Control:** open apps (chrome, vscode, settings, etc.)\n"
            "**Web Access:** youtube, github, gmail, whatsapp, news, etc.\n"
            "**Media Systems:** direct YouTube play with 'play [song name]'\n"
            "**Intelligence Search:** Google, Wikipedia, math calculations\n"
            "**Internal Memory:** mental notes, logs, and information recall\n"
            "**System Vitals:** time, date, weather, battery, network status\n\n"
            "**Mentorship Program:**\n"
            "• teach assembly / teach python / teach c / teach java\n"
            "• teach javascript / teach dsa / teach html css / teach sql\n"
            "• Use 'lesson [topic] [num]' for direct tutorial access."
        )
        mood = 'curious'

    # Handle Language specific fallback / LLM Intelligence
    if not res_body:
        # Check for URLs in the text
        urls = re.findall(r'https?://\S+', text)
        if urls:
            url = urls[0] # Take the first URL found
            res_body = f"I'm accessing the data stream from: {url}, sir. Analyzing live information..."
            
            web_content = fetch_webpage_content(url)
            if web_content:
                # Augment prompt with web content
                prompt = f"The user provided a link ({url}). Here is the extracted content from that page:\n\n{web_content}\n\nUser Question/Command: '{text}'"
                res_body = llm_service.generate_response(prompt)
            else:
                res_body = "I attempted to access the link, sir, but the connection was refused or the data was unreadable."
        
        if not res_body:
            # Try LLM Intelligence
            res_body = llm_service.generate_response(text)
        
        # If LLM failed or not enabled, use local basic templates
        if not res_body:
            lang = persona_engine.detect_language(text_lower)
            res_body = persona_engine.translate_basic('not_found', lang)
            mood = 'confused'
        else:
            # We got a smart response, detect its mood for the prefix
            mood = persona_engine.detect_emotion(res_body)

    response["reply"] = persona_engine.format_mentor_response(text, res_body, mood=mood)
    response["mood"] = mood
    response["action"] = action
    return response


def get_command_list():
    return [
        {"category": "System", "commands": ["open notepad","open chrome","open calculator","open cmd","open settings","open explorer","open paint","open vs code"]},
        {"category": "Websites", "commands": ["open youtube","open instagram","open github","open gmail","open whatsapp","open linkedin","open chatgpt","open spotify"]},
        {"category": "Media", "commands": ["play [song]","volume up","volume down","mute"]},
        {"category": "Search", "commands": ["search google [query]","wikipedia [topic]"]},
        {"category": "Learn", "commands": ["teach assembly","teach python","teach c","teach java","teach javascript","teach dsa","teach html css","teach sql"]},
        {"category": "Info", "commands": ["time","date","weather [city]","battery","ip address","system info"]},
        {"category": "Utility", "commands": ["screenshot","calculate [expr]","type [text]","lock screen"]},
    ]
