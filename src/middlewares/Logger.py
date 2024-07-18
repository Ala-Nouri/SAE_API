import logging
import re
from src.models.Company import Company

log_level = logging.INFO
formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


class Logger:

    _loggers = {}  # Dictionary to store company loggers

    @staticmethod
    def create_company_log_handler(company_name):
        log_filename = f"company_{company_name}.log"
        file_handler = logging.FileHandler(log_filename)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        return file_handler

    @staticmethod
    def get_company_logger(company_id):
        company = Company.query.filter_by(company_id=company_id).first()
        if company.company_name not in Logger._loggers:
            logger = logging.getLogger(company.company_name)
            logger.setLevel(log_level)
            logger.addHandler(Logger.create_company_log_handler(company.company_name))
            logger.propagate = True
            Logger._loggers[company.company_name] = logger
        return Logger._loggers[company.company_name]
    
    @staticmethod
    def get_logs(company_id):
        def extract_log_data(log_line):   
            pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) INFO (.*)"
            match = re.match(pattern, log_line)
            if match:
                return {"date": match.group(1), "message": match.group(2).strip()}
            else:
                return None
            
        
        company = Company.query.filter_by(company_id=company_id).first()
        log_filename = f"company_{company.company_name}.log"
        logs = []
        try:
            with open(log_filename, "r") as log_file:
                log_lines = log_file.readlines()
            for log_line in log_lines:
                data = extract_log_data(log_line)
                if data:
                    logs.append(data)
            return logs
        except FileNotFoundError:
            return "Log file not found."
