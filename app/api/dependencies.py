from app.src.banking_agency.BankingAgencyRepository import BankingAgencyRepository
from app.src.banking_agency.BankingAgencyService import BankingAgencyService

class Dependencies:
    banking_agency_service = None
    @staticmethod
    def get_banking_agency_service() -> BankingAgencyService:
        if Dependencies.banking_agency_service is None:
            Dependencies.banking_agency_service = BankingAgencyService(BankingAgencyRepository("EBanxDemo"))
        return Dependencies.banking_agency_service
