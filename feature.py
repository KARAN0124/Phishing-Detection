import re
import pandas as pd
from urllib.parse import urlparse
from tldextract import extract
import ipaddress

class FeatureExtraction:
    def __init__(self, url):
        self.url = url
        self.extracted = extract(url)  # Extract once to optimize performance
        self.parsed_url = urlparse(url)

    def has_ip_address(self):
        try:
            hostname = self.parsed_url.hostname  # Extract hostname only
            ipaddress.ip_address(hostname)
            return 1
        except (ValueError, TypeError):  # Handle invalid values
            return 0

    def count_dots(self):
        return self.parsed_url.netloc.count('.')

    def count_hyphens(self):
        return self.url.count('-')

    def url_length(self):
        return len(self.url)

    def has_at_symbol(self):
        return 1 if '@' in self.url else 0

    def count_slashes(self):
        return self.url.count('/')

    def count_question_marks(self):
        return self.url.count('?')

    def count_equals(self):
        return self.url.count('=')

    def count_ampersands(self):
        return self.url.count('&')

    def count_underscores(self):
        return self.url.count('_')

    def count_percent_signs(self):
        return self.url.count('%')

    def domain_dot_count(self):
        return self.extracted.domain.count('.')

    def domain_length(self):
        return len(self.extracted.domain)

    def is_https(self):
        return 1 if self.url.lower().startswith('https://') else 0

    def count_suspicious_words(self):
        suspicious_words = {'login', 'free', 'click', 'verify', 'update', 'secure', 'account', 'ebayisapi', 'paypal'}
        return sum(1 for word in suspicious_words if word in self.url.lower())

    def extract_features(self):
        return {
            'has_ip': self.has_ip_address(),
            'dot_count': self.count_dots(),
            'hyphen_count': self.count_hyphens(),
            'url_length': self.url_length(),
            'has_at_symbol': self.has_at_symbol(),
            'slash_count': self.count_slashes(),
            'question_mark_count': self.count_question_marks(),
            'equals_count': self.count_equals(),
            'ampersand_count': self.count_ampersands(),
            'underscore_count': self.count_underscores(),
            'percent_sign_count': self.count_percent_signs(),
            'domain_dot_count': self.domain_dot_count(),
            'domain_length': self.domain_length(),
            'is_https': self.is_https(),
            'suspicious_word_count': self.count_suspicious_words()
        }

# Function to process a list of URLs
def process_urls(url_list):
    features = [FeatureExtraction(url).extract_features() for url in url_list]
    return pd.DataFrame(features)

# Example usage
if __name__ == "__main__":
    url_list = [
        "http://example.com",
        "https://secure-login.net",
        "http://192.168.1.1/login",
        "https://free-offers.net",
        "http://example.com?verify=true",
    ]

    df = process_urls(url_list)
    print(df)
