from bs4 import BeautifulSoup

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def clean_comment_from_garbage(comment_text):
    """
        removes text from <script> and <style> tags and return text only
    """
    soup = BeautifulSoup(comment_text, "html.parser") 
    for s in soup(['script', 'style']):
        s.decompose()
    return ' '.join(soup.stripped_strings)