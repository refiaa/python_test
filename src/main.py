from http_client.http_client import HttpClient
from scanners.sql_injection_scanner import SqlInjectionScanner
from scanners.xss_scanner import XssScanner
from crawler.crawler import WebCrawler
from reporter.vulnerability_reporter import VulnerabilityReporter
from attacker.attack_executor import AttackExecutor

def main():
    base_url = "TARGET SITE DOMAIN HERE"
    http_client = HttpClient(base_url)

    sql_scanner = SqlInjectionScanner(http_client)
    xss_scanner = XssScanner(http_client)
    crawler = WebCrawler(base_url, max_depth=3)
    reporter = VulnerabilityReporter(log_file='vulnerabilities.log')
    attacker = AttackExecutor(http_client)

    crawler.crawl()
    crawled_results = crawler.get_results()
    for url in crawled_results:
        print(f"Found URL: {url}")

    sql_result = None
    xss_result = None

    for url in crawled_results:
        if base_url in url:
            relative_url = url.replace(base_url, "").lstrip("/")
            sql_result = sql_scanner.scan(relative_url, "username")
            reporter.add_vulnerability(sql_result)

    for url in crawled_results:
        if base_url in url:
            relative_url = url.replace(base_url, "").lstrip("/")
            xss_result = xss_scanner.scan(relative_url, "query")
            reporter.add_vulnerability(xss_result)

    report = reporter.generate_report()
    print(report)

    if sql_result and sql_result.get("vulnerable"):
        attack_result = attacker.execute_attack(sql_result)
        print(attack_result)

if __name__ == "__main__":
    main()
