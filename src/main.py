from http_client.http_client import HttpClient
from scanners.sql_injection_scanner import SqlInjectionScanner
from scanners.xss_scanner import XssScanner
from brute_forcer.directory_brute_forcer import DirectoryBruteForcer
from reporter.vulnerability_reporter import VulnerabilityReporter
from attacker.attack_executor import AttackExecutor

def main():
    base_url = "here"
    http_client = HttpClient(base_url)

    sql_scanner = SqlInjectionScanner(http_client)
    xss_scanner = XssScanner(http_client)
    brute_forcer = DirectoryBruteForcer(http_client, "wordlist.txt")
    reporter = VulnerabilityReporter()
    attacker = AttackExecutor(http_client)

    brute_results = brute_forcer.brute_force()
    for result in brute_results:
        print(f"Found directory: {result['directory']}")

    sql_result = None
    xss_result = None

    for result in brute_results:
        if result["status"] == "found":
            sql_result = sql_scanner.scan(result["directory"], "username")
            reporter.add_vulnerability(sql_result)

    for result in brute_results:
        if result["status"] == "found":
            xss_result = xss_scanner.scan(result["directory"], "query")
            reporter.add_vulnerability(xss_result)

    report = reporter.generate_report()
    print(report)

    if sql_result and sql_result.get("vulnerable"):
        attack_result = attacker.execute_attack(sql_result)
        print(attack_result)

if __name__ == "__main__":
    main()
