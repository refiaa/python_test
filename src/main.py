from http_client.http_client import HttpClient
from scanners.sql_injection_scanner import SqlInjectionScanner
from scanners.xss_scanner import XssScanner
from crawler.crawler import WebCrawler
from reporter.vulnerability_reporter import VulnerabilityReporter
from attacker.attack_executor import AttackExecutor
from datetime import datetime

def main():
    base_url = "TARGET SITE DOMAIN HERE"
    wordlist_path = "./payloads/wordlist.txt"
    http_client = HttpClient(base_url)

    sql_scanner = SqlInjectionScanner(http_client)
    xss_scanner = XssScanner(http_client)
    crawler = WebCrawler(base_url, wordlist_path, max_depth=3)
    reporter = VulnerabilityReporter(log_file='vulnerabilities.log', report_file='vulnerability_report.txt')
    attacker = AttackExecutor(http_client)

    crawler.crawl()
    crawled_results = crawler.get_results()
    for url in crawled_results:
        print(f"Found URL: {url}")

    client_ip = reporter.get_client_ip()
    detection_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    for url in crawled_results:
        if base_url in url:
            relative_url = url.replace(base_url, "").lstrip("/")
            sql_result = sql_scanner.scan(relative_url, "username")
            sql_details = {
                "endpoint": sql_result.get("endpoint", "N/A"),
                "param": sql_result.get("param", "N/A"),
                "payload": sql_result.get("payload", "N/A"),
                "status_code": sql_result.get("status_code", "N/A"),
                "response": sql_result.get("response", "N/A"),
                "detection_time": detection_time,
                "client_ip": client_ip,
                "url": url
            }
            reporter.add_vulnerability(base_url, "SQL Injection", sql_result["vulnerable"], sql_details)

    for url in crawled_results:
        if base_url in url:
            relative_url = url.replace(base_url, "").lstrip("/")
            xss_result = xss_scanner.scan(relative_url, "query")
            xss_details = {
                "endpoint": xss_result.get("endpoint", "N/A"),
                "param": xss_result.get("param", "N/A"),
                "payload": xss_result.get("payload", "N/A"),
                "status_code": xss_result.get("status_code", "N/A"),
                "response": xss_result.get("response", "N/A"),
                "detection_time": detection_time,
                "client_ip": client_ip,
                "url": url
            }
            reporter.add_vulnerability(base_url, "XSS", xss_result["vulnerable"], xss_details)

    report = reporter.generate_report()

    with open("vulnerability_report.txt", "w", encoding="utf-8") as file:
        file.write(report)
        
    login_endpoint = crawler.get_login_page()
    if login_endpoint:
        attack_result = attacker.execute_login_attack(login_endpoint, "username", "password")
        attack_details = {
            "login_endpoint": login_endpoint,
            "username_param": "username",
            "password_param": "password",
            "result": attack_result,
            "detection_time": detection_time,
            "client_ip": client_ip,
            "url": login_endpoint
        }
        reporter.add_vulnerability(base_url, "Login Attack", "Admin access granted!" in attack_result, attack_details)
        print(attack_result)
    else:
        print("Login page not found.")

if __name__ == "__main__":
    main()
