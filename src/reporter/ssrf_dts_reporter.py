import logging
import re

from typing import Dict

class SsrfDtsReporter:
    def __init__(self, log_file='vulnerability_report_SSRF-dts.txt'):
        self.vulnerabilities = []
        self.log_file = log_file
        logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

    def add_vulnerability(self, target_site: str, attack_type: str, success: bool, details: Dict):
        if success:
            vulnerability = {
                'target_site': target_site,
                'attack_type': attack_type,
                'success': success,
                'details': self._clean_html(details)
            }
            self.vulnerabilities.append(vulnerability)
            logging.info(f"Target site: {target_site}, Attack type: {attack_type}, Success: {success}, Details: {details}")
            self._append_to_log_file(vulnerability)

    def _clean_html(self, details: Dict) -> Dict:
        clean_details = {}
        html_pattern = re.compile('<.*?>')
        for key, value in details.items():
            clean_value = re.sub(html_pattern, '', value) if isinstance(value, str) else value
            clean_details[key] = clean_value
        return clean_details

    def _append_to_log_file(self, vulnerability: Dict):
        with open(self.log_file, 'a', encoding='utf-8') as file:
            file.write(f"Target site: {vulnerability['target_site']}\n")
            file.write(f"Attack type: {vulnerability['attack_type']}\n")
            file.write(f"Success: {vulnerability['success']}\n")
            for key, value in vulnerability['details'].items():
                file.write(f"{key}: {value}\n")
            file.write("\n")

    def generate_report(self):
        report = "\nSSRF and Directory Traversal Vulnerability Report\n\n"
        for vulnerability in self.vulnerabilities:
            report += f"Target site: {vulnerability['target_site']}\n"
            report += f"Attack type: {vulnerability['attack_type']}\n"
            report += f"Success: {vulnerability['success']}\n"
            for key, value in vulnerability['details'].items():
                report += f"{key}: {value}\n"
            report += "\n"
        return report