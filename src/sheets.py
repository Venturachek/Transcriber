import logging
import gspread
from google.oauth2.service_account import Credentials
from src.config import settings

logging.basicConfig(
    level=logging.ERROR
)
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

HEADERS = [
    "Дата",
    "Початок розмови, представлення",
    "Чи дізнався менеджер про кузов авто",
    "Чи дізнався рік авто",
    "Чи дізнався менеджер пробіг",
    "Пропозиція комплексної діагностики",
    "Чи дізнався, які роботи виконувалися раніше",
    "Запис на сервіс",
    "Завершення розмови, прощання",
    "Які роботи з топ-100",
    "Чи дотримувався всіх інструкцій з топ-100",
    "Яких інструкцій не дотримувався",
    "Оцінка менеджера",
    "Коментар"
]

def sheet_connect():
    logging.info("Подключается")
    creds = Credentials.from_service_account_file(settings.GOOGLE_CREDENTIALS, scopes=SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(settings.SPREADSHEET_ID).get_worksheet_by_id(927837808)
    logging.info("Подключено")
    return sheet





def upload_result(sheet, text: str, analysis: dict):
    logging.info("Загрузка данных")
    try:
        row = [
        text,
        "",
        "",
        "",
        "",
        analysis.get("початок_розмови_представлення", 0),
        analysis.get("модель_авто", 0),
        analysis.get("рік_авто", 0),
        analysis.get("пробіг", 0),
        analysis.get("пропозиція_комплексної_діагностики", 0),
        analysis.get("раніше_виконані_роботи", 0),
        analysis.get("запис_на_сервіс", 0),
        analysis.get("завершення_розмови_прощання", 0),
        ", ".join(analysis.get("послуги_з_топ_100", [])),
        "+" if analysis.get("дотримання_всіх_інструкцій") else "-",
        "\n".join(analysis.get("пропущені_інструкції", [])),
        "",
        analysis.get("оцінка_менеджера", 0),
        "",
        analysis.get("коментар", ""),
    ]

        all_values = sheet.col_values(1)
        last_row = len([v for v in all_values if v]) + 1
        sheet.insert_row(row, last_row + 1)
    except Exception as e:
        logging.error(f"Error: {e}", exc_info=True)
        raise e

    last_row = len(sheet.get_all_values())
    score = analysis.get("оцінка_менеджера", 0)
    has_problems = score < 4
    if has_problems:
        sheet.format(f"R{last_row}", {"backgroundColor":{"red": 1.0, "green": 0.8, "blue": 0.8}})