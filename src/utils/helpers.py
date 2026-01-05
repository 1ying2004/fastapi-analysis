def safe_divide(a, b):
    return a / b if b != 0 else 0

def format_date(dt):
    return dt.strftime('%Y-%m-%d')

def truncate_string(s, length=50):
    return s[:length] + '...' if len(s) > length else s
