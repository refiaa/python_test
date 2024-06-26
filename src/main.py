from http_client.http_client import HttpClient
from scanners.sql_injection_scanner import SqlInjectionScanner
from scanners.xss_scanner import XssScanner
from scanners.ssrf_scanner import SSRFScanner
from scanners.directory_traversal_scanner import DirectoryTraversalScanner
from crawler.crawler import WebCrawler
from reporter.vulnerability_reporter import VulnerabilityReporter
from reporter.ssrf_dts_reporter import SsrfDtsReporter
from attacker.attack_executor import AttackExecutor
from datetime import datetime

def main():
    base_url = "TARGET SITE DOMAIN HERE"
    wordlist_path = "./payloads/endpoints.txt"
    http_client = HttpClient(base_url)

    sql_scanner = SqlInjectionScanner(http_client)
    xss_scanner = XssScanner(http_client)
    ssrf_scanner = SSRFScanner(http_client)
    dts_scanner = DirectoryTraversalScanner(http_client)
    crawler = WebCrawler(base_url, wordlist_path, max_depth=3)
    reporter = VulnerabilityReporter(log_file='vulnerabilities.log', report_file='vulnerability_report.txt')
    ssrf_dts_reporter = SsrfDtsReporter(log_file='vulnerability_report_SSRF-dts.txt')
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
            
            # SQL Injection Scan
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

            # XSS Scan
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

            # SSRF Scan
            ssrf_result = ssrf_scanner.scan(relative_url, "url")
            ssrf_details = {
                "endpoint": ssrf_result.get("endpoint", "N/A"),
                "param": ssrf_result.get("param", "N/A"),
                "payload": ssrf_result.get("payload", "N/A"),
                "status_code": ssrf_result.get("status_code", "N/A"),
                "response": ssrf_result.get("response", "N/A"),
                "detection_time": detection_time,
                "client_ip": client_ip,
                "url": url
            }
            ssrf_dts_reporter.add_vulnerability(base_url, "SSRF", ssrf_result["vulnerable"], ssrf_details)

            # Directory Traversal Scan
            dts_result = dts_scanner.scan(relative_url, "file")
            dts_details = {
                "endpoint": dts_result.get("endpoint", "N/A"),
                "param": dts_result.get("param", "N/A"),
                "payload": dts_result.get("payload", "N/A"),
                "status_code": dts_result.get("status_code", "N/A"),
                "response": dts_result.get("response", "N/A"),
                "detection_time": detection_time,
                "client_ip": client_ip,
                "url": url
            }
            ssrf_dts_reporter.add_vulnerability(base_url, "Directory Traversal", dts_result["vulnerable"], dts_details)

    report = reporter.generate_report()
    ssrf_dts_report = ssrf_dts_reporter.generate_report()

    with open("vulnerability_report.txt", "w", encoding="utf-8") as file:
        file.write(report)
        
    with open("vulnerability_report_SSRF-dts.txt", "w", encoding="utf-8") as file:
        file.write(ssrf_dts_report)

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
