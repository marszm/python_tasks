import requests

# Aby opracować fragment kodu korzystający z interfejsu API REST udostępnionego przez myDSV w celu wyłączenia kont firmowych i użytkowników na podstawie podanej nazwy firmy, musimy wykonać następujące kroki:
# 1.Uzyskać identyfikator firmy: Najpierw musimy pobrać identyfikator firmy, korzystając z podanej nazwy firmy. ->  linia 20
# 2.Wyłącz dostęp API: Po uzyskaniu identyfikatora firmy możemy zaktualizować status API_ENABLED firmy na false, skutecznie wyłączając dostęp do API dla tej firmy.->  linia 28
# 3.Wyłącz konta użytkowników: Następnie musimy pobrać listę użytkowników powiązanych z firmą za pomocą identyfikatora firmy. Następnie możemy przeglądać listę użytkowników i aktualizować status Włączony każdego użytkownika na fałszywy, skutecznie wyłączając jego konta.

def get_company_id(company_name):
    url = "https://api.mydsv.com/companies"
    # Krok 1: Uwierzytelnij się i uzyskaj identyfikator firmy na podstawie nazwy firmy
    try:
        response = requests.get(url)
        companies = response.json()

        for company in companies:
            if company["Name"] == company_name:
                return company["ID"]

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


def disable_api(company_id):
    # Krok 2: Wyłącz API dla firmy
    url = f"https://api.mydsv.com/companies/{company_id}"
    payload = {
        "API_ENABLED": False
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            print("API access disabled successfully")
        else:
            print(f"Failed to disable API access: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


def disable_user_accounts(company_id):
    url = f"https://api.mydsv.com/users?company_id={company_id}"

    # Krok 3: Wyłącz wszystkie konta użytkowników w firmie

    try:
        response = requests.get(url)
        users = response.json()

        for user in users:
            user_id = user["ID"]
            disable_user(user_id)

        print("User accounts disabled successfully")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


def disable_user(user_id):
    url = f"https://api.mydsv.com/users/{user_id}"
    payload = {
        "Enabled": False
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            print(f"User account {user_id} disabled successfully")
        else:
            print(f"Failed to disable user account {user_id}: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


def main():
    # pamietaj i nazwie formy
    company_name = "Company Name"
    company_id = get_company_id(company_name)
    if company_id:
        disable_api(company_id)
        disable_user_accounts(company_id)


if __name__ == "__main__":
    main()
