import re

def validate_name(name):
    """
    Validates a full name: letters, spaces, dots, hyphens only.
    Returns (True, "") if valid, else (False, error_message)
    """
    if not name or not name.strip():
        return False, "Name cannot be empty."

    name = name.strip()

    # Full string match
    pattern = r"[A-Za-z][A-Za-z\s\.\-]{1,48}"

    if not re.fullmatch(pattern, name):
        return False, "Please enter a valid name (letters only, no numbers or symbols)."

    # Ensure full name (at least two words)
    if len(name.split()) < 2:
        return False, "Please enter your full name (at least first and last name)."

    return True, ""

def validate_email(email):
    """
    Validates an email address.
    Returns True if valid, False otherwise.
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    '''<local-part>@<domain>.<TLD> (TLD:Top-level domain)ex:john.doe@example.com,user_123@my-domain.org,alice+test@gmail.co'''
    return re.match(pattern, email) is not None

def validate_indian_phone(phone):
    """
    Validates Indian phone numbers.
    Returns True if valid, False otherwise.
    """
    pattern = r"^(?:\+91[\-\s]?|0)?[6-9]\d{9}$"
    return re.match(pattern, phone) is not None

def validate_experience(exp):
    """
    Validates experience as a positive float number.
    Returns True if valid, False otherwise.
    """
    try:
        val = float(exp)
        return val >= 0
    except ValueError:
        return False

def validate_role_semantic(role):
    allowed_roles = [
        "Software Engineer", "Data Scientist", "DevOps Engineer",
        "Product Manager", "HR Manager", "QA Engineer", "Machine Learning Engineer",
        "GenAI Engineer","Data Scientist"
    ]
    role = role.strip().title()  # normalize
    if role in allowed_roles:
        return True, ""
    return False, f"Role '{role}' is not recognized. Please enter a valid role."

def validate_tech_stack(tech_stack):
    """
    Validates a tech stack input.
    - Must be non-empty
    - Each item should be a known technology
    """
    if not tech_stack.strip():
        return False, "Tech stack cannot be empty."

    # Split by comma
    items = [t.strip().title() for t in tech_stack.split(",") if t.strip()]
    if not items:
        return False, "Please enter at least one technology."

    # List of allowed technologies (extend as needed)
    allowed_techs = [
        "Python", "Java", "C++", "C#", "Javascript", "React", "Node.js",
        "Django", "Flask", "SQL", "MongoDB", "Redis", "Tensorflow",
        "PyTorch", "Keras", "Docker", "Kubernetes", "Machine Learning","Deep Learning","GenAi"
    ]

    invalid_items = [t for t in items if t not in allowed_techs]
    if invalid_items:
        return False, f"Unknown technologies detected: {', '.join(invalid_items)}."

    return True, ""

def goodbye_message():
    return "🙏 Thank you for your time.<br><br>✨ All the best for your future!"

